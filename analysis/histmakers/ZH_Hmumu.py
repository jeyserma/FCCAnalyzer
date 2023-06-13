
import analysis, functions, helpers
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

functions.set_threads(args)


# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (3000, 0, 300) # 100 MeV bins
bins_p_ll = (200, 0, 200) # 1 GeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, -5, 5)
bins_eta = (600, -3, 3)
bins_phi = (500, -5, 5)
bins_aco = (200, 0, 4)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)
bins_dR = (1000, 0, 10)

bins_cat = (10, 0, 10)

bins_massweights = (5, 0, 5)

bins_resolution = (10000, 0.95, 1.05)

def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240", "wzp6_ee_eeH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    df = helpers.defineCutFlowVars(df) # make the cutX=X variables
    
    
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
    
    # cuts on leptons
    df = df.Define("leps", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")
    
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    df = df.Define("leps_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps, ReconstructedParticles)")
    df = df.Define("leps_sel_iso", "FCCAnalyses::sel_iso(0.25)(leps, leps_iso)") # 0.25
    

        
    # baseline selections and histograms
    results.append(df.Histo1D(("leps_all_p_cut0", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_theta_cut0", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi_cut0", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q_cut0", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no_cut0", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("leps_all_iso_cut0", "", *bins_iso), "leps_all_iso"))
    

    results.append(df.Histo1D(("leps_p_cut0", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("leps_theta_cut0", "", *bins_theta), "leps_theta"))
    results.append(df.Histo1D(("leps_phi_cut0", "", *bins_phi), "leps_phi"))
    results.append(df.Histo1D(("leps_q_cut0", "", *bins_charge), "leps_q"))
    results.append(df.Histo1D(("leps_no_cut0", "", *bins_count), "leps_no"))
    results.append(df.Histo1D(("leps_iso_cut0", "", *bins_iso), "leps_iso"))


    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1 && leps_sel_iso.size() > 0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))
    
    
    #########
    ### CUT 2 :at least 2 OS leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2 && abs(Sum(leps_q)) < leps_q.size()")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))
    
    #df = df.Filter("leps_no == 2")

    # build the H resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    df = df.Define("hbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(125, 91.2, 0.4, 240, false)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("hll", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[0]}") # the H
    df = df.Define("hll_leps", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[1],hbuilder_result[2]}") # the leptons
    df = df.Define("hll_m", "FCCAnalyses::ReconstructedParticle::get_mass(hll)[0]")
    df = df.Define("hll_p", "FCCAnalyses::ReconstructedParticle::get_p(hll)[0]")
    df = df.Define("hll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(hll)")
    df = df.Define("hll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(hll_recoil)[0]")
    df = df.Define("hll_category", "FCCAnalyses::polarAngleCategorization(0.8, 2.34)(hll_leps)")
    
    df = df.Define("hll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(hll_leps)")
    df = df.Define("hll_leps_dR", "FCCAnalyses::deltaR(hll_leps)")
    df = df.Define("hll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(hll_leps)")
     

    results.append(df.Histo1D(("hll_recoil_m_cut2", "", *bins_recoil), "hll_recoil_m"))
    
    
    #########
    ### CUT 3: Z recoil window
    #########
    df = df.Filter("hll_recoil_m < 120 && hll_recoil_m > 80")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    results.append(df.Histo1D(("hll_p_cut3", "", *bins_p_ll), "hll_p"))
    
    
    #########
    ### CUT 4: H momentum
    #########  
    df = df.Filter("hll_p > 30 && hll_p < 60") ## TODO
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))

    
    #########
    ### CUT 5: cosThetaMiss
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss"))

   
    df = df.Filter("cosTheta_miss < 1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))
   

    df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(leps)")
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(leps)")
    results.append(df.Histo1D(("acoplanarity_cut5", "", *bins_aco), "acoplanarity"))
    results.append(df.Histo1D(("acolinearity_cut5", "", *bins_aco), "acolinearity"))    
    
    
    #########
    ### CUT 6: recoil cut
    #########  
    
    df = df.Filter("hll_m > 0 && hll_m < 240")
    # final selection and histograms
    df = df.Filter("hll_recoil_m < 240 && hll_recoil_m > 0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    
        
    ########################
    # Final histograms
    ########################
    
    results.append(df.Histo1D(("hll_m", "", *bins_m_ll), "hll_m"))
    results.append(df.Histo1D(("hll_recoil_m", "", *bins_recoil), "hll_recoil_m"))
    results.append(df.Histo1D(("hll_p", "", *bins_p_ll), "hll_p"))


    

    
               
               

              

    
               
    return results, weightsum
    
    


if __name__ == "__main__":

    datasets = []

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_winter2023_IDEA_ecm240
    datasets_preproduction_IDEA = FCCee_winter2023_IDEA_ecm240.get_datasets(baseDir=baseDir) # list of all datasets

   

    bkgs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"]
    bkgs_rare = ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]
    signal = ["wzp6_ee_nunuH_Hmumu_ecm240", "wzp6_ee_eeH_Hmumu_ecm240", "wzp6_ee_tautauH_Hmumu_ecm240", "wzp6_ee_ccH_Hmumu_ecm240", "wzp6_ee_bbH_Hmumu_ecm240", "wzp6_ee_qqH_Hmumu_ecm240", "wzp6_ee_ssH_Hmumu_ecm240", "wzp6_ee_mumuH_Hmumu_ecm240"]
    
    
    	
    	
    select = signal
    select = signal + bkgs + bkgs_rare
    

    datasets += functions.filter_datasets(datasets_preproduction_IDEA, select)
    result = functions.build_and_run(datasets, build_graph, "tmp/output_ZH_Hmumu.root", maxFiles=args.maxFiles, norm=True, lumi=5000000)
    
