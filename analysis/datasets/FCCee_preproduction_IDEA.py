
import ROOT # switch to hex colors
import copy
import fnmatch

# http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/spring2021/Delphesevents_IDEA.php

def getDatasets(filt=None):

    datasets = []
    baseDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/pre_fall2022_training/IDEA/"

    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hbb_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hbb_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hcc_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hcc_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hdd_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hdd_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hgg_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hgg_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hss_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hss_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Htautau_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Htautau_ecm240" % baseDir,
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Huu_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Huu_ecm240" % baseDir,
        "xsec"      : 0.201868
    })


    # pre-fall (fixed muon isolation)
    datasets.append({
        "name"      : "wzp6_ee_mumuH_ecm240_prefall",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesEvents/pre_fall2022_training/IDEA/wzp6_ee_mumuH_ecm240",
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "wz3p6_ee_mumuH_ecm240_prefall",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesEvents/pre_fall2022/IDEA/wzp6_ee_mumuH_ecm240",
        "xsec"      : 0.201868
    })
    
    
    # winter v1 (fixed muon resolution)
    datasets.append({
        "name"      : "wz3p6_ee_mumuH_ecm240_winter",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v1/wz3p6_ee_mumuH_ecm240",
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "wzp6_ee_eeH_ecm240_winter",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v1/wzp6_ee_eeH_ecm240",
        "xsec"      : 0.201868
    })
    

    # winter v2 (electrons smeared with twice the resolution)
    datasets.append({
        "name"      : "wz3p6_ee_mumuH_ecm240_winter_v2",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v2/wz3p6_ee_mumuH_ecm240",
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "wzp6_ee_eeH_ecm240_winter_v2",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v2/wzp6_ee_eeH_ecm240",
        "xsec"      : 0.201868
    })
    
    datasets.append({
        "name"      : "wz2p6_ee_mumuH_ecm240_winter_v2",
        "datadir"   : "/eos/experiment/fcc/ee/generation/DelphesStandalone/Edm4Hep/pre_winter2023_tests_v2/wz2p6_ee_mumuH_ecm240/",
        "xsec"      : 0.201868
    })
    
    
    
    
    
    
    


    if filt == None: return datasets
    else: return [dataset for dataset in datasets if fnmatch.fnmatch(dataset['name'], filt)]
