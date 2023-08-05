from typing import Optional, Union, List
import os
import math
import json

from quickstats.components import AbstractObject, ExtendedModel
from quickstats.components.numerics import str_encode_value

import ROOT

class ToyLimitCalculator(AbstractObject):
    
    def __init__(self, filename:str, data_name:str,
                 n_toys:int, seed:int=1234,
                 poi_name:Optional[str]=None, 
                 mu_null:float=1., mu_alt:float=0., 
                 mu_min:float=0., mu_max:float=10.,
                 minimizer:str="Minuit2", strategy:int=1,
                 eps:float=0.05, print_level:int=-1,
                 do_coarse_scan:bool=False,
                 fix_param:str='', profile_param:str='',
                 snapshot_name:Optional[Union[List[str], str]]=None,                 
                 verbosity:Optional[Union[int, str]]=None):
        super().__init__(verbosity=verbosity)
        
        self.model_base = ExtendedModel(filename,
                                        data_name=data_name,
                                        snapshot_name=snapshot_name,
                                        verbosity="WARNING")
        if fix_param:
            self.model_base.fix_parameters(fix_param)
        if profile_param:
            self.model_base.profile_parameters(profile_param)
        
        self.poi = self.model_base.get_poi(poi_name)
        
        self.model_SB = self.model_base.model_config
        self.poi.setVal(mu_null)
        self.poi.setRange(mu_min, mu_max)
        self.model_SB.SetSnapshot(self.poi)
        
        self.model_B = self.model_base.model_config.Clone("B_only")
        self.poi.setVal(mu_alt)
        self.poi.setRange(mu_min, mu_max)
        self.model_B.SetSnapshot(self.poi)        
        
        self.random_generator = ROOT.RooRandom.randomGenerator()
        self.random_generator.SetSeed(seed)
        
        pdf_SB = self.model_SB.GetPdf()
        globs_SB = self.model_SB.GetGlobalObservables()
        
        self.plr = ROOT.RooStats.ProfileLikelihoodTestStat(pdf_SB)
        self.plr.SetGlobalObservables(globs_SB)
        self.plr.SetOneSided(True)
        self.plr.SetReuseNLL(True)
        self.plr.SetPrintLevel(print_level)
        self.plr.SetMinimizer(minimizer)
        self.plr.SetStrategy(strategy)
        
        self.toy_mc = ROOT.RooStats.ToyMCSampler(self.plr, n_toys)
        self.freq_calculator = ROOT.RooStats.FrequentistCalculator(self.model_base.data, 
                                                                   self.model_B, 
                                                                   self.model_SB, 
                                                                   self.toy_mc)
        self.do_coarse_scan = do_coarse_scan
        self.eps            = eps
        
        self.coarse_result    = None
        self.fine_result      = None
        self.one_point_result = {}
        
    @staticmethod
    def scan_result_to_dict(scan_result):
        result = {}
        result["limits"] = {
            "obs": scan_result.UpperLimit(),
            0: scan_result.GetExpectedUpperLimit(0),
            1: scan_result.GetExpectedUpperLimit(1),
            2: scan_result.GetExpectedUpperLimit(2),
            -1: scan_result.GetExpectedUpperLimit(-1),
            -2: scan_result.GetExpectedUpperLimit(-1),
        }
        result["data"] = {
            "mu": [],
            "CLb": [],
            "CLs": [],
            "CLsplusb": [],
            "CLsplusbError": []
        }
        
        for i in range(scan_result.ArraySize()):
            result["data"]["mu"].append(scan_result.GetXValue(i))
            result["data"]["CLb"].append(scan_result.CLb(i))
            result["data"]["CLs"].append(scan_result.CLs(i))
            result["data"]["CLsplusb"].append(scan_result.CLsplusb(i))
            result["data"]["CLsplusbError"].append(scan_result.CLsplusbError(i))
        return result

    def display_limits(self, scan_result):
        limits = ToyLimitCalculator.scan_result_to_dict(scan_result)['limits']
        self.stdout.info("Limit Bands")
        self.stdout.info(f"+2 sigma :", limits[2])
        self.stdout.info(f"+1 sigma :", limits[1])
        self.stdout.info(f"-1 sigma :", limits[-1])
        self.stdout.info(f"-2 sigma :", limits[-2])
        self.stdout.info(f"  Median :", limits[0])
        self.stdout.info(f"Observed :", limits["obs"])
        self.stdout.info(f"-2 sigma:", limits[-2])
        
    def run_coarse_scan(self, scan_min:float, scan_max:float):
        
        scale      = 10**(1/3)
        steps      = (math.log(scan_max / scan_min) / math.log(scale)) + 1
        steps_ceil = math.ceil(steps)
        start, end = scan_min, scan_max
        
        self.stdout.info("INFO: Starting coarse search")
        self.stdout.info(f"INFO: Evaluating {steps_ceil} logarithmic points from {start} to {end}")
        
        inverter = ROOT.RooStats.HypoTestInverter(self.freq_calculator)
        inverter.SetVerbose()
        # 95% CLs limits
        inverter.SetConfidenceLevel(0.95) 
        inverter.UseCLs(True)
        
        self.stdout.info("INFO: Checking for problematic CLs values...")
        
        snapshot_0 = self.freq_calculator.GetNullModel().GetSnapshot()

        for i in range(steps_ceil):
            start = math.exp(math.log(scan_min) + i * math.log(scan_max / scan_min) / (steps - 1))
            self.poi.setVal(start)
            self.freq_calculator.GetNullModel().SetSnapshot(self.poi)
            result = self.freq_calculator.GetHypoTest()
            cls = result.CLs()
            if (math.isfinite(cls) and cls >= 0.):
                break
        if start >= end :
            raise RuntimeError("No acceptable points found in coarse scan")
        for i in range(steps_ceil):
            end = math.exp(math.log(scan_min) + (steps - 1 - i) * math.log(scan_max / scan_min) / (steps - 1))
            self.poi.setVal(end)
            self.freq_calculator.GetNullModel().SetSnapshot(self.poi)
            result = self.freq_calculator.GetHypoTest()
            cls = result.CLs()
            if (math.isfinite(cls) and cls >= 0.):
                break
        if start >= end :
            raise RuntimeError("No acceptable points found in coarse scan")
        steps      = math.log(end / start) / math.log(scale) + 1
        steps_ceil = math.ceil(steps)
        self.freq_calculator.GetNullModel().SetSnapshot(snapshot_0)
        self.stdout.info(f"INFO: Recalculated scan running {steps_ceil} logarithmic points from {start} to {end}")
        
        self.stdout.info("INFO: Running fixed scan")
        inverter.RunFixedScan(steps, start, end, True)
        result = inverter.GetInterval()
        result.SetInterpolationOption(ROOT.RooStats.HypoTestInverterResult.kLinear)
        
        self.coarse_result = result
        
        return result        

    def run_scans(self, scan_min:float, scan_max:float):
        
        start, end = scan_min, scan_max
        
        if self.do_coarse_scan:
            coarse_result = self.run_coarse_scan(scan_min, scan_max)
            start = coarse_result.minus_2 / 10**(1/3)
            end   = coarse_result.plus_2 / 10**(1/3)
            if (not math.isfinite(start)) or (not math.isfinite(end)):
                raise RuntimeError("Got non-finite bound from coarse limits")
            if (start < self.poi.getRange()[0]):
                raise RuntimeError("Got lower bound beyond POI minimum range")
            self.stdout.info(f"INFO: Bounds for fine search: [{start}, {end}]")
            self.display_limits(coarse_result)
        
        self.stdout.info("INFO: Starting fine search")

        scale      = 1. + self.eps
        steps      = (math.log(end / start) / math.log(scale)) + 1
        steps_ceil = math.ceil(steps)
        
        self.stdout.info(f"INFO: Evaluating {steps_ceil} logarithmic points from {start} to {end}")
        inverter = ROOT.RooStats.HypoTestInverter(self.freq_calculator)
        inverter.SetVerbose()
        # 95% CLs limits
        inverter.SetConfidenceLevel(0.95) 
        inverter.UseCLs(True)
        
        self.stdout.info("INFO: Running fixed scan")
        inverter.RunFixedScan(steps, start, end, True)
        result = inverter.GetInterval()
        result.SetInterpolationOption(ROOT.RooStats.HypoTestInverterResult.kLinear)
        
        self.display_limits(result)
        
        self.fine_result = result
        
        return result
    
    def run_one_point(self, poi_val:float):
        
        poi_val_0 = self.poi.getVal()
        
        self.stdout.info(f"INFO: Running HypoTest on mu value {poi_val}.")
    
        self.poi.setVal(poi_val)
        self.freq_calculator.GetNullModel().SetSnapshot(self.poi)
        result = self.freq_calculator.GetHypoTest()
        result.SetBackgroundAsAlt()
        
        self.poi.setVal(poi_val_0)
        
        self.one_point_result[poi_val] = result
        
        return result

    
    def save(self, filename:str="toy_limit_result.json"):
        
        if (self.fine_result is None) and (self.coarse_result is None) and (self.one_point_result is None):
            self.stdout.warning("WARNING: No result to save")

        base_dir = os.path.dirname(filename)
        base_name = os.path.basename(filename)
        extension = os.path.splitext(filename)[1]
            
        if self.coarse_result is not None:
            result = self.scan_result_to_dict(self.coarse_result)
            filename_coarse = os.path.join(base_dir, f"{base_name}_coarse{extension}")
            with open(filename_coarse) as f:
                json.dump(result, f, indent=2)
            self.stdout.info(f"INFO: Saved coarse toy limit result as `{filename}`.")
            
        if self.fine_result is not None:
            result = self.scan_result_to_dict(self.fine_result)
            with open(filename) as f:
                json.dump(result, f, indent=2)
            self.stdout.info(f"INFO: Saved toy limit result as `{filename}`.")

        if self.one_point_result is not None:
            for mu_val in self.one_point_result:
                mu_str = str_encode_value(mu_val)
                result = self.scan_result_to_dict(self.one_point_result[mu_val])
                filename_one_point = os.path.join(base_dir, f"{base_name}_{mu_str}{extension}")
                with open(filename_one_point) as f:
                    json.dump(result, f, indent=2)
                self.stdout.info(f"INFO: Saved toy limit result for mu = {mu_val} as `{filename}`.")