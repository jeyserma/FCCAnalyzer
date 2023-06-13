
import analysis, functions
import ROOT
import argparse

#ROOT.TH1.SetDefaultSumw2(True)
#ROOT.TH2.SetDefaultSumw2(True)
#ROOT.TH3.SetDefaultSumw2(True)
#ROOT.THn.SetDefaultSumw2(True)


parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p = (10000, 0, 100) # 10 MeV bins
bins_m_ll = (20000, 0, 200) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (100000, -1, 1)

bins_p_beam = (100000, 40, 50) # 0.1 MeV bins

bins_theta = (320, -4, 4)
bins_phi = (80, -4, 4)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)
bins_dR = (1000, 0, 10)

bins_massweights = (5, 0, 5)

bins_reso = (10000, 0.95, 1.05)
bins_ecm_eff = (1000, 0.0, 1.0)
bins_cos = (100, -1, 1)
bins_acolinearity_deg = (1000, 0.0, 90.0)
bins_acolinearity_rad = (1000, 0.0, 1.0)

bins_theta_abs = (100, 0, 2)


bins_resolution = (10000, 0.95, 1.05)
bins_resolution_1 = (20000, 0, 2)

jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins
bins_ebalance = (1000, 0, 1)

bins_sum_score = (200, -5, 5)
bins_m_jj = (200, 0, 200)
bins_mrec_jj = (200, 0, 200)

bins_bdt = (10, 0, 1)
bins_mrec = (10, 80, 100)
bins_m = (10, 120, 130)

def build_graph(df, dataset): 
    
    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    df = df.Filter("muons_p < 20 && electrons_p < 20 && costhetainv < 0.85 && costhetainv > -0.85")
    
    results.append(df.Histo1D(("m_jj", "", *bins_m_jj), "M_jj"))
    results.append(df.Histo1D(("m_rec", "", *bins_mrec_jj), "Mrec_jj"))
    
    
    
    #df = df.Filter("M_jj > 100 && M_jj < 140")
    #df = df.Filter("Mrec_jj > 80 && Mrec_jj < 140")
    df = df.Filter("M_jj > 120 && M_jj < 130")
    df = df.Filter("Mrec_jj > 80 && Mrec_jj < 100")



    
    

    # jet2_scoreG per jet score
    # Hbb, Hcc, Hss, Hgg Htautau HWW_ZZ -> after BDT training
    
    
    #results.append(df.Histo1D(("score_B", "", *bins_sum_score), "B"))
    #results.append(df.Histo1D(("score_C", "", *bins_sum_score), "C"))
    #results.append(df.Histo1D(("score_S", "", *bins_sum_score), "S"))
    #results.append(df.Histo1D(("score_G", "", *bins_sum_score), "G"))
    #results.append(df.Histo1D(("score_Q", "", *bins_sum_score), "Q"))
    
    results.append(df.Histo1D(("Hbb", "", *bins_bdt), "Hbb"))
    results.append(df.Histo1D(("Hcc", "", *bins_bdt), "Hcc"))
    results.append(df.Histo1D(("Hss", "", *bins_bdt), "Hss"))
    results.append(df.Histo1D(("Hgg", "", *bins_bdt), "Hgg"))
    results.append(df.Histo1D(("Htautau", "", *bins_bdt), "Htautau"))
    results.append(df.Histo1D(("HWW_ZZ", "", *bins_bdt), "HWW_ZZ"))
    
    # 6 dim histogram (20^6=64000000 bins)
    results.append(df.HistoND(("multi_dim_bdt", "", 6, tuple([bins_bdt[0]]*6), tuple([bins_bdt[1]]*6), tuple([bins_bdt[2]]*6)), ("Hbb", "Hcc", "Hss", "Hgg", "Htautau", "HWW_ZZ")))

    # 8 dim histogram (20^6=64000000 bins)
    results.append(df.HistoND(("multi_dim_bdt", "", 8, tuple([bins_bdt[0]]*6+[bins_m[0], bins_mrec[0]]), tuple([bins_bdt[1]]*6+[bins_m[1], bins_mrec[1]]), tuple([bins_bdt[2]]*6+[bins_m[2], bins_mrec[2]])), ("Hbb", "Hcc", "Hss", "Hgg", "Htautau", "HWW_ZZ", "M_jj", "Mrec_jj")))
    
   
    
    
    return results, weightsum
  
    

if __name__ == "__main__":

    datasets = []
    baseDir = "/eos/experiment/fcc/ee/analyses/case-studies/higgs/flat_trees/zh_vvjj_v2/"

    Hbb = {"name": "Hbb", "datadir": f"{baseDir}/wzp6_ee_nunuH_Hbb_ecm240_score3",  "xsec": 0.0269}
    Hcc = {"name": "Hcc", "datadir": f"{baseDir}/wzp6_ee_nunuH_Hcc_ecm240_score3",  "xsec": 0.001335}
    Hss = {"name": "Hss", "datadir": f"{baseDir}/wzp6_ee_nunuH_Hss_ecm240_score3",  "xsec": 1.109e-05}
    Hgg = {"name": "Hgg", "datadir": f"{baseDir}/wzp6_ee_nunuH_Hgg_ecm240_score3",  "xsec": 0.003782}
    Htautau = {"name": "Htautau", "datadir": f"{baseDir}/wzp6_ee_nunuH_Htautau_ecm240_score3",  "xsec": 0.002897}
    HWW = {"name": "HWW", "datadir": f"{baseDir}/wzp6_ee_nunuH_HWW_ecm240_score3",  "xsec": 0.00994}
    HZZ = {"name": "HZZ", "datadir": f"{baseDir}/wzp6_ee_nunuH_HZZ_ecm240_score3",  "xsec": 0.00122}
    
    WW = {"name": "WW", "datadir": f"{baseDir}/p8_ee_WW_ecm240_score3",  "xsec": 16.4385}
    ZZ = {"name": "ZZ", "datadir": f"{baseDir}/p8_ee_ZZ_ecm240_score3",  "xsec": 1.35899}
    Zqq = {"name": "Zqq", "datadir": f"{baseDir}/p8_ee_Zqq_ecm240_score3",  "xsec": 52.6539}
    #qqH = {"name": "qqH", "datadir": f"{baseDir}/p8_ee_qqH_ecm240_score3",  "xsec": 0.13635}

    datasets = [Hbb, Hcc, Hss, Hgg, Htautau, HWW, HZZ, WW, ZZ, Zqq]
    #datasets = [ZZ, WW]
    result = functions.build_and_run(datasets, build_graph, "tmp/nunuH.root", maxFiles=args.maxFiles, norm=True, lumi=5000000)

