
# http://fcc-physics-events.web.cern.ch/fcc-physics-events/FCCee/winter2023/Delphesevents_IDEA.php

def get_datasets(baseDir = ""):

    datasets = []

    ################## winter2023
    baseDir += "/winter2023/"

    ## muon signal samples
    datasets.append({"name": "p_wzp6_ee_mumuH_ecm240",                          "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_ecm240",                           "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-50MeV_ecm240",           "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-lower-50MeV_ecm240",            "xsec": 0.0067738})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-100MeV_ecm240",          "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-lower-100MeV_ecm240",           "xsec": 0.0067849})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-100MeV_ecm240",         "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-higher-100MeV_ecm240",          "xsec": 0.0067393})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-50MeV_ecm240",          "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-higher-50MeV_ecm240",           "xsec": 0.0067488})
    
    datasets.append({"name": "p_wzp6_ee_mumuH_noBES_ecm240",                    "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_noBES_ecm240",                     "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-50MeV_noBES_ecm240",     "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-lower-50MeV_noBES_ecm240",      "xsec": 0.0067738})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-100MeV_noBES_ecm240",    "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-lower-100MeV_noBES_ecm240",     "xsec": 0.0067849})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-100MeV_noBES_ecm240",   "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-higher-100MeV_noBES_ecm240",    "xsec": 0.0067393})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-50MeV_noBES_ecm240",    "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_mH-higher-50MeV_noBES_ecm240",     "xsec": 0.0067488})
    
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-lower-1pc_ecm240",            "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_BES-lower-1pc_ecm240",             "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-higher-1pc_ecm240",           "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_BES-higher-1pc_ecm240",            "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-lower-6pc_ecm240",            "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_BES-lower-6pc_ecm240",             "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-higher-6pc_ecm240",           "datadir": f"{baseDir}/IDEA/wzp6_ee_mumuH_BES-higher-6pc_ecm240",            "xsec": 0.0067643})

    # electron samples
    datasets.append({"name": "p_wzp6_ee_eeH_ecm240",                            "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_ecm240",                             "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-50MeV_ecm240",             "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-lower-50MeV_ecm240",              "xsec": 0.007169})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-100MeV_ecm240",            "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-lower-100MeV_ecm240",             "xsec": 0.007188})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-100MeV_ecm240",           "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-higher-100MeV_ecm240",            "xsec": 0.007137})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-50MeV_ecm240",            "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-higher-50MeV_ecm240",             "xsec": 0.007152})

    datasets.append({"name": "p_wzp6_ee_eeH_noBES_ecm240",                      "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_noBES_ecm240",                       "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-50MeV_noBES_ecm240",       "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-lower-50MeV_noBES_ecm240",        "xsec": 0.007169})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-100MeV_noBES_ecm240",      "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-lower-100MeV_noBES_ecm240",       "xsec": 0.007188})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-100MeV_noBES_ecm240",     "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-higher-100MeV_noBES_ecm240",      "xsec": 0.007137})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-50MeV_noBES_ecm240",      "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_mH-higher-50MeV_noBES_ecm240",       "xsec": 0.007152})

    datasets.append({"name": "p_wzp6_ee_eeH_BES-higher-6pc_ecm240",             "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_BES-higher-6pc_ecm240",              "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_BES-lower-6pc_ecm240",              "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_BES-lower-6pc_ecm240",               "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_BES-higher-1pc_ecm240",             "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_BES-higher-1pc_ecm240",              "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_BES-lower-1pc_ecm240",              "datadir": f"{baseDir}/IDEA/wzp6_ee_eeH_BES-lower-1pc_ecm240",               "xsec": 0.0071611})

    # 2021 ones
    #datasets.append({"name": "p_wzp6_ee_mumuH_ecm240_2021",                     "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/wzp6_ee_mumuH_ecm240/",     "xsec": 0.0067643})
    #datasets.append({"name": "p_wzp6_ee_mumuH_ecm240_2021_3T",                  "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA_3T/wzp6_ee_mumuH_ecm240/",  "xsec": 0.0067643})


    ################## 3T
    datasets.append({"name": "p_wzp6_ee_mumuH_ecm240_3T",                       "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_ecm240",                           "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-50MeV_ecm240_3T",        "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_mH-lower-50MeV_ecm240",            "xsec": 0.0067738})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-100MeV_ecm240_3T",       "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_mH-lower-100MeV_ecm240",           "xsec": 0.0067849})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-100MeV_ecm240_3T",      "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_mH-higher-100MeV_ecm240",          "xsec": 0.0067393})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-50MeV_ecm240_3T",       "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_mH-higher-50MeV_ecm240",           "xsec": 0.0067488})

    datasets.append({"name": "p_wzp6_ee_eeH_ecm240_3T",                         "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_eeH_ecm240",                             "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-50MeV_ecm240_3T",          "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_eeH_mH-lower-50MeV_ecm240",              "xsec": 0.007169})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-100MeV_ecm240_3T",         "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_eeH_mH-lower-100MeV_ecm240",             "xsec": 0.007188})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-100MeV_ecm240_3T",        "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_eeH_mH-higher-100MeV_ecm240",            "xsec": 0.007137})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-50MeV_ecm240_3T",         "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_eeH_mH-higher-50MeV_ecm240",             "xsec": 0.007152})

    datasets.append({"name": "p_wzp6_ee_mumuH_BES-lower-1pc_ecm240_3T",         "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_BES-lower-1pc_ecm240",             "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-higher-1pc_ecm240_3T",        "datadir": f"{baseDir}/IDEA_3T/wzp6_ee_mumuH_BES-higher-1pc_ecm240",            "xsec": 0.0067643})


    ################## CLD
    datasets.append({"name": "p_wzp6_ee_mumuH_ecm240_CLD",                      "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_ecm240",                           "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-50MeV_ecm240_CLD",       "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_mH-lower-50MeV_ecm240",            "xsec": 0.0067738})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-lower-100MeV_ecm240_CLD",      "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_mH-lower-100MeV_ecm240",           "xsec": 0.0067849})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-100MeV_ecm240_CLD",     "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_mH-higher-100MeV_ecm240",          "xsec": 0.0067393})
    datasets.append({"name": "p_wzp6_ee_mumuH_mH-higher-50MeV_ecm240_CLD",      "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_mH-higher-50MeV_ecm240",           "xsec": 0.0067488})

    datasets.append({"name": "p_wzp6_ee_mumuH_BES-lower-1pc_ecm240_CLD",        "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_BES-lower-1pc_ecm240",             "xsec": 0.0067643})
    datasets.append({"name": "p_wzp6_ee_mumuH_BES-higher-1pc_ecm240_CLD",       "datadir": f"{baseDir}/CLD/wzp6_ee_mumuH_BES-higher-1pc_ecm240",            "xsec": 0.0067643})


    datasets.append({"name": "p_wzp6_ee_eeH_ecm240_CLD",                        "datadir": f"{baseDir}/CLD/wzp6_ee_eeH_ecm240",                             "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-50MeV_ecm240_CLD",         "datadir": f"{baseDir}/CLD/wzp6_ee_eeH_mH-lower-50MeV_ecm240",              "xsec": 0.007169})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-100MeV_ecm240_CLD",        "datadir": f"{baseDir}/CLD/wzp6_ee_eeH_mH-lower-100MeV_ecm240",             "xsec": 0.007188})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-100MeV_ecm240_CLD",       "datadir": f"{baseDir}/CLD/wzp6_ee_eeH_mH-higher-100MeV_ecm240",            "xsec": 0.007137})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-50MeV_ecm240_CLD",        "datadir": f"{baseDir}/CLD/wzp6_ee_eeH_mH-higher-50MeV_ecm240",             "xsec": 0.007152})    


    ################## 2E

    datasets.append({"name": "p_wzp6_ee_eeH_ecm240_E2",                         "datadir": f"{baseDir}/IDEA_E2/wzp6_ee_eeH_ecm240",                             "xsec": 0.0071611})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-50MeV_ecm240_E2",          "datadir": f"{baseDir}/IDEA_E2/wzp6_ee_eeH_mH-lower-50MeV_ecm240",              "xsec": 0.007169})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-lower-100MeV_ecm240_E2",         "datadir": f"{baseDir}/IDEA_E2/wzp6_ee_eeH_mH-lower-100MeV_ecm240",             "xsec": 0.007188})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-100MeV_ecm240_E2",        "datadir": f"{baseDir}/IDEA_E2/wzp6_ee_eeH_mH-higher-100MeV_ecm240",            "xsec": 0.007137})
    datasets.append({"name": "p_wzp6_ee_eeH_mH-higher-50MeV_ecm240_E2",         "datadir": f"{baseDir}/IDEA_E2/wzp6_ee_eeH_mH-higher-50MeV_ecm240",             "xsec": 0.007152})    


    return datasets