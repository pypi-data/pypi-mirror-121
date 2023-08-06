from typing import Optional, Union, List, Dict

import numpy as np
from cppyy.gbl.std import vector

import ROOT
import ROOT.RooStats as RS


def get_null_distribution(htr:ROOT.RooStats.HypoTestResult)->np.ndarray:
    return np.array(htr.GetNullDistribution().GetSamplingDistribution().data())

def get_alt_distribution(htr:ROOT.RooStats.HypoTestResult)->np.ndarray:
    return np.array(htr.GetAltDistribution().GetSamplingDistribution().data())

def get_merged_null_distribution(htr_list:List[ROOT.RooStats.HypoTestResult])->np.ndarray:
    return np.sort(np.array([get_null_distribution(htr) for htr in htr_list]).flatten())

def get_merged_alt_distribution(htr_list:List[ROOT.RooStats.HypoTestResult])->np.ndarray:
    return np.sort(np.array([get_alt_distribution(htr) for htr in htr_list]).flatten())

def process_hypotest_results(htr_list:List[RS.HypoTestResult],
                             remove_unconverged_toys:bool=True, 
                             use_2plr:bool=False,
                             do_invert:bool=True):
    if not isinstance(htr_list, list):
        htr_list = [htr_list]
    teststat_list = [htr.GetTestStatisticData() for htr in htr_list]
    if len(set(teststat_list)) > 1:
        raise RuntimeError("inconsistent test statistic values among hypotest results")
    teststat = teststat_list[0]
    if (teststat < 0.):
        print("WARNING: HypoTestResult has negative test statistic indicating a failed fit.")
    null_dist = get_merged_null_distribution(htr_list)
    alt_dist = get_merged_alt_distribution(htr_list)
    if remove_unconverged_toys:
        null_dist = null_dist[null_dist >= 0.]
        alt_dist  = alt_dist[alt_dist >= 0.]
    if use_2plr:
        null_dist *= 2
        alt_dist  *= 2
        teststat  *= 2
    null_dist_vec = vector['double'](null_dist)
    alt_dist_vec  = vector['double'](alt_dist)
    null_sampling_dist = RS.SamplingDistribution("null_dist", "", null_dist_vec)
    alt_sampling_dist  = RS.SamplingDistribution("alt_dist", "", alt_dist_vec)
    new_htr = htr_list[0].Clone()
    new_htr.SetNullDistribution(null_sampling_dist)
    new_htr.SetAltDistribution(alt_sampling_dist)
    new_htr.SetTestStatisticData(teststat)
    if do_invert:
        new_htr.SetBackgroundAsAlt()
    return new_htr

def merge_toy_results(results:List[Union[RS.HypoTestInverterResult,
                      RS.HypoTestResult]],
                      poi:Optional[ROOT.RooRealVar]=None,
                      remove_mu_with_failed_teststat:bool=True,
                      remove_unconverged_toys:bool=True, 
                      use_2plr:bool=False,
                      do_invert:bool=True,
                      silent:bool=False):
    hypotest_inverter_results = [r for r in results if r.ClassName() == 'RooStats::HypoTestInverterResult']
    hypotest_results          = [r for r in results if r.ClassName() == 'RooStats::HypoTestResult']

    if (not hypotest_inverter_results) and (not hypotest_results):
        raise ValueError("toy results must be either instance of "
                         "RooStats::HypoTestInverterResult or RooStats::HypoTestResult")
    if poi is None:
        if len(hypotest_inverter_results) > 0:
            base_result = hypotest_inverter_results[0]
            poi = base_result.GetParameters().first()
        else:
            base_result = hypotest_results[0]
            poi_name    = '_'.join(base_result.GetName().split('_')[:-1])
            poi         = ROOT.RooRealVar(poi_name, poi_name, 0)
            print("WARNING: POI information not given. New POI variable will be constructed "
                  " using name inferred from toy result (\"{}\"={}[{}, {}]).".format(
                      poi_name, poi.getVal(), poi.getRange()[0], poi.getRange()[1]))
    if not silent:
        print("INFO: Constructing HypoTestInverterResult with the following settings")
        print("                  CL: 0.95")
        print("             Use CLs: True")
        print("Interpolation Method: Linear")
    merged_result = RS.HypoTestInverterResult("merged_result", poi, 0.95)
    merged_result.SetConfidenceLevel(0.95)
    merged_result.UseCLs()
    merged_result.SetInterpolationOption(RS.HypoTestInverterResult.kLinear)
    temp_results = {}
    for result in hypotest_inverter_results:
        r_poi = result.GetParameters().first()
        if r_poi.GetName() != poi.GetName():
            raise RuntimeError("inconsistent POI used across toy results")
        for i in range(result.ArraySize()):
            htr = result.GetResult(i)
            mu = result.GetXValue(i)
            if mu not in temp_results:
                temp_results[mu] = []
            temp_results[mu].append(htr)
        
    for result in hypotest_results:
        try:
            mu = float(result.GetName().split('_')[-1])
        except:
            raise RuntimeError("failed to extract mu value from HypoTestResult name "
                               "(expect <poi_name>_<mu_value>)")
        if mu not in temp_results:
            temp_results[mu] = []
        temp_results[mu].append(result)

    for mu, htr_list in temp_results.items():
        teststat_list = [htr.GetTestStatisticData() for htr in htr_list]
        if any(teststat < 0 for teststat in teststat_list) and remove_mu_with_failed_teststat:
            print(f"WARNING: Removed results from mu = {mu} due to negative teststat value")
            continue
        new_htr = process_hypotest_results(htr_list,
                  remove_unconverged_toys=remove_unconverged_toys, 
                  use_2plr=use_2plr,
                  do_invert=do_invert)
        merged_result.Add(mu, new_htr)
    return merged_result