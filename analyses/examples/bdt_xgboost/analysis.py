
import functions
import helper_tmva
import ROOT
import argparse

parser = functions.make_def_argparser()
parser.add_argument('--maketree', action=argparse.BooleanOptionalAction)
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/higgs_mass_xsec/functions.h")
functions.add_include_file("analyses/higgs_mass_xsec/functions_gen.h")


# define histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (200, 0, 200) # 1 GeV bins
bins_recoil = (20000, 0, 200) # 10 MeV bins 
bins_recoil_fine = (20000, 120, 140) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, 0, 5)
bins_phi = (500, -5, 5)
bins_aco = (400, -4, 4)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)
bins_dR = (1000, 0, 10)

bins_cat = (10, 0, 10)


bins_resolution = (10000, 0.95, 1.05)
bins_mva_score = (100, 0, 1)

if not args.maketree:
    #tmva_helper = helper_tmva.TMVAHelperXGB("tmp/bdt_model_example.root", "bdt_model")
    tmva_helper = helper_tmva.TMVAHelperXML("TMVAClassification_BDTG.weights.xml")
    print(tmva_helper.variables)

def build_graph(df, dataset):

    print("build graph", dataset.name)
    hists, cols = [], []
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Alias("Lepton0", "Muon#0.index")
     
   
    # all leptons (bare)
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    df = df.Define("leps_all_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps_all, ReconstructedParticles)") 
    df = df.Define("leps_all_p_gen", "FCCAnalyses::gen_p_from_reco(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    
    # cuts on leptons
    df = df.Define("leps", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")
    
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    df = df.Define("leps_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps, ReconstructedParticles)")
    df = df.Define("leps_sel_iso", "FCCAnalyses::sel_iso(0.25)(leps, leps_iso)") # 0.25



    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1 && leps_sel_iso.size() > 0")
    
    #########
    ### CUT 2 :at least 2 OS leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2 && abs(Sum(leps_q)) < leps_q.size()")
    
    # build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    df = df.Define("zbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zll", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[0]}") # the Z
    df = df.Define("zll_leps", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[1],zbuilder_result[2]}") # the leptons
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]")
    df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)")
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]")
    
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)")
    df = df.Define("lep1_p", "zll_leps_p[0]")
    df = df.Define("lep2_p", "zll_leps_p[1]")
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)")
    df = df.Define("lep1_theta", "zll_leps_theta[0]")
    df = df.Define("lep2_theta", "zll_leps_theta[1]")
     
    
    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
    
    df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(leps)")
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(leps)")
   
    
    #########
    ### CUT 3: Z mass window
    #########  
    df = df.Filter("zll_m > 86 && zll_m < 96")
        
    
    #########
    ### CUT 4: Z momentum
    #########  
    df = df.Filter("zll_p > 20 && zll_p < 70")   
        
    #########
    ### CUT 5: recoil cut
    #########  
    df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    
    
   
    
    #########
    ### CUT 6: cosThetaMiss, for mass analysis
    #########  
    df = df.Filter("cosTheta_miss < 0.98")

 
    
    # columns for BDT
    cols.append("lep1_p")
    cols.append("lep2_p")
    cols.append("lep1_theta")
    cols.append("lep2_theta")
    cols.append("zll_p")
    cols.append("acoplanarity")
    cols.append("acolinearity")
    cols.append("zll_recoil_m")
    cols.append("cosTheta_miss")
    if args.maketree:
        return df, cols
    
    
    # histograms
    hists.append(df.Histo1D(("leps_p", "", *bins_p_mu), "leps_p"))
    hists.append(df.Histo1D(("zll_p", "", *bins_p_mu), "zll_p"))
    hists.append(df.Histo1D(("zll_m", "", *bins_m_ll), "zll_m"))
    hists.append(df.Histo1D(("zll_recoil", "", *bins_recoil), "zll_recoil_m"))    

    hists.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    hists.append(df.Histo1D(("acoplanarity", "", *bins_aco), "acoplanarity"))
    hists.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))
    
    
    
    df = df.Define("HCandPT__div_HCandMass", "lep1_theta")
    df = df.Define("photon_pt__div_HCandPT", "lep1_theta")
    df = df.Define("meson_pt__div_HCandPT", "lep1_theta")
    df = df.Define("photon_eta", "lep1_theta")
    df = df.Define("photon_mvaID", "lep1_theta")
    df = df.Define("DeepMETResolutionTune_pt", "lep1_theta")
    df = df.Define("meson_iso", "lep1_theta")
    df = df.Define("meson_sipPV", "lep1_theta")
    df = df.Define("meson_trk1_eta", "lep1_theta")
    df = df.Define("dPhiGammaMesonCand", "lep1_theta")
    df = df.Define("dEtaGammaMesonCand__div_HCandMass", "lep1_theta")
    df = df.Define("nGoodJets", "lep1_theta")

    
    df = tmva_helper.run_inference(df) # by default, makes a new column mva_score
    hists.append(df.Histo1D(("mva", "", *bins_mva_score), "mva_score"))
    
    return hists, weightsum
    
    
    
    
    
   

if __name__ == "__main__":

    wzp6_ee_mumuH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumuH_ecm240/",  "xsec": 0.0067643}
    p8_ee_WW_mumu_ecm240 = {"name": "p8_ee_WW_mumu_ecm240", "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents//winter2023/IDEA/p8_ee_WW_mumu_ecm240/",  "xsec": 0.25792}

    datasets = [p8_ee_WW_mumu_ecm240, wzp6_ee_mumuH_ecm240]
    datasets = [wzp6_ee_mumuH_ecm240]
    
    if args.maketree:
        for d in datasets: # run each process consecutively, no support yet for multiprocessing
            functions.build_and_run_snapshot([d], build_graph, "tmp/test_tree_{datasetName}.root", args)

    else:
        functions.build_and_run(datasets, build_graph, "tmp/test_bdt.root", args, norm=True, lumi=7200000)
    
