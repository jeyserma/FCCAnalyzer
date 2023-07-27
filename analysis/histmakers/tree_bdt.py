
import analysis, functions, helpers
import helper_tmva
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", choices=["mumu", "ee"], default="mumu")
args = parser.parse_args()

functions.set_threads(args)

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


variables = ['lep1_p', 'lep2_p', 'lep1_theta', 'lep2_theta', 'zll_p', 'acoplanarity', 'acolinearity', 'zll_recoil_m', 'cosTheta_miss']
tmva_helper = helper_tmva.TMVAHelper("tmp/bdt_model_example.root", "bdt_model", variables)


def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    if args.flavor == "mumu":
        df = df.Alias("Lepton0", "Muon#0.index")
    else:
        df = df.Alias("Lepton0", "Electron#0.index")
     
    df = helpers.defineCutFlowVars(df) # make the cutX=X variables
    
 
    
   
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
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)")
     
    
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

 
    results.append(df.Histo1D(("leps_p", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("zll_p", "", *bins_p_mu), "zll_p"))
    results.append(df.Histo1D(("zll_m", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_recoil", "", *bins_recoil), "zll_recoil_m"))    

    results.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    results.append(df.Histo1D(("acoplanarity", "", *bins_aco), "acoplanarity"))
    results.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))
    
    
    
    df = df.Define("lep1_p", "zll_leps_p[0]")
    df = df.Define("lep2_p", "zll_leps_p[1]")
    
    df = df.Define("lep1_theta", "zll_leps_theta[0]")
    df = df.Define("lep2_theta", "zll_leps_theta[1]")

    df = tmva_helper.run_inference(df) # by default, makes a new column mva_score
    results.append(df.Histo1D(("mva", "", *bins_mva_score), "mva_score"))
    
    #df = df.Define("MVA_score_1", ROOT.RDF.PassAsVec[9, float](tmva_helper), ['lep1_p', 'lep2_p', 'lep1_theta', 'lep2_theta', 'zll_p', 'acoplanarity', 'acolinearity', 'zll_recoil_m', 'cosTheta_miss'])
    #results.append(df.Histo1D(("mva", "", *bins_mva_score), "MVA_score"))
    #results.append(df.Histo1D(("mva1", "", *bins_mva_score), "MVA_score_1"))
    
    return results, weightsum
    
    
    
    
    
   

if __name__ == "__main__":

    wzp6_ee_mumuH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumuH_ecm240/",  "xsec": 1}
    wzp6_ee_eeH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_eeH_ecm240/",  "xsec": 1}
    p8_ee_WW_ecm240 = {"name": "p8_ee_WW_ecm240", "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents//winter2023/IDEA/p8_ee_WW_ecm240/",  "xsec": 1}

    datasets = [wzp6_ee_mumuH_ecm240, p8_ee_WW_ecm240]
    datasets = [wzp6_ee_mumuH_ecm240, p8_ee_WW_ecm240]
    
    result = functions.build_and_run(datasets, build_graph, "tmp/test_bdt.root", maxFiles=args.maxFiles, norm=True, lumi=7200000)
    
    
