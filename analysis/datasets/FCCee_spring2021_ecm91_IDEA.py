
import ROOT # switch to hex colors
import copy
import fnmatch

# http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/spring2021/Delphesevents_IDEA.php

def getDatasets(filt=None, select=[], baseDir = ""):

    datasets = []
    baseDir = "%s/spring2021/IDEA/" % baseDir

    ## signal samples
    datasets.append({
        "name"      : "p8_ee_Zee_ecm91",
        "datadir"   : "%s/p8_ee_Zee_ecm91" % baseDir,
        "xsec"      : 1462.09
    })
    
    datasets.append({
        "name"      : "p8_ee_Zmumu_ecm91",
        "datadir"   : "%s/p8_ee_Zmumu_ecm91" % baseDir,
        "xsec"      : 1462.08
    })
    
    datasets.append({
        "name"      : "p8_ee_Ztautau_ecm91",
        "datadir"   : "%s/p8_ee_Ztautau_ecm91" % baseDir,
        "xsec"      : 1476.58
    })
    
    
    
    datasets.append({
        "name"      : "p8_ee_Zuds_ecm91",
        "datadir"   : "%s/p8_ee_Zuds_ecm91" % baseDir,
        "xsec"      : 18616.5
    })
    
    datasets.append({
        "name"      : "p8_ee_Zcc_ecm91",
        "datadir"   : "%s/p8_ee_Zcc_ecm91" % baseDir,
        "xsec"      : 5215.46
    })
    
    datasets.append({
        "name"      : "p8_ee_Zbb_ecm91",
        "datadir"   : "%s/p8_ee_Zbb_ecm91" % baseDir,
        "xsec"      : 6645.46
    })
    
    	
   
    if filt != None: return [dataset for dataset in datasets if fnmatch.fnmatch(dataset['name'], filt)]
    elif len(select) > 0: 
        ret = []
        for dataset in datasets:
            if dataset['name'] in select: ret.append(dataset)
        return ret
    else: return datasets