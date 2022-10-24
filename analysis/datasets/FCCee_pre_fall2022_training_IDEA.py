
import ROOT # switch to hex colors
import copy
import fnmatch

# http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/spring2021/Delphesevents_IDEA.php

def getDatasets(filt=None):

    datasets = []


    #####################################
    ### IDEA
    #####################################
    baseDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/pre_fall2022_training/IDEA/"

    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hbb_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hbb_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hcc_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hcc_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hdd_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hdd_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hgg_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hgg_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Hss_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Hss_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Htautau_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Htautau_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    
    datasets.append({
        "name"      : "p8_ee_ZH_Znunu_Huu_ecm240",
        "datadir"   : "%s/p8_ee_ZH_Znunu_Huu_ecm240" % baseDir,
        "xsec"      : 0.0067656
    })
    


    if filt == None: return datasets
    else: return [dataset for dataset in datasets if fnmatch.fnmatch(dataset['name'], filt)]
