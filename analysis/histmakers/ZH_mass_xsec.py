
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
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
    sigProcs = ["wzp6_ee_mumuH_ecm240", "p8_ee_ZH_ecm240", "wzp6_ee_mumuH_ecm240_prefall", "wz3p6_ee_mumuH_ecm240_prefall", "wz3p6_ee_mumuH_ecm240_winter", "wz3p6_ee_mumuH_ecm240_winter_v2", "wzp6_ee_eeH_ecm240_winter", "wzp6_ee_eeH_ecm240_winter_v2", "wz2p6_ee_mumuH_ecm240_winter_v2"]
    sigProcs = ["wzp6_ee_mumuH_ecm240", "wzp6_ee_eeH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    if args.flavor == "mumu":
        df = df.Alias("Lepton0", "Muon#0.index")
        #df = df.Alias("Lepton0", "AllMuon#0.index")
    else:
        df = df.Alias("Lepton0", "Electron#0.index")
     
    
    # prompt gen muons
    # in Whizard, the mumuH process does not directly involve Z processes, hence they are not present in the gen particles
    # the muons either directly come from the hard scatter (electrons as mothers) or from Higgs decays
    ###df = df.Define("gen_prompt_muons_idx", "FCCAnalyses::select_prompt_leptons_idx(13, Particle, Particle0)")
    #df = df.Define("gen_prompt_muons", "FCCAnalyses::select_prompt_leptons_gen(13, Particle, Particle0)")
    #df = df.Define("gen_prompt_muons_p", "FCCAnalyses::MCParticle::get_p(gen_prompt_muons)")
    #df = df.Define("gen_prompt_muons_theta", "FCCAnalyses::MCParticle::get_theta(gen_prompt_muons)")
    #df = df.Define("gen_prompt_muons_phi", "FCCAnalyses::MCParticle::get_phi(gen_prompt_muons)")
    #df = df.Define("gen_prompt_muons_charge", "FCCAnalyses::MCParticle::get_charge(gen_prompt_muons)")
    #df = df.Define("gen_prompt_muons_no", "FCCAnalyses::MCParticle::get_n(gen_prompt_muons)")
    
    # photons
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
    df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
    
    df = df.Define("gen_photons", "FCCAnalyses::get_photons(Particle)")
    df = df.Define("gen_photons_p", "FCCAnalyses::MCParticle::get_p(gen_photons)")
    df = df.Define("gen_photons_theta", "FCCAnalyses::MCParticle::get_theta(gen_photons)")
    df = df.Define("gen_photons_phi", "FCCAnalyses::MCParticle::get_phi(gen_photons)")
    df = df.Define("gen_photons_no", "FCCAnalyses::MCParticle::get_n(gen_photons)")
    
    
    #df = df.Define("deltaR_gen_leps", "FCCAnalyses::deltaR_gen_leps(Particle, Particle0, Particle1)")
    #df = df.Define("mll_gen_leps", "FCCAnalyses::mll_gen_leps(Particle, Particle0, Particle1)")
    
    #df = df.Define("is_VBF", "FCCAnalyses::is_VBF(Particle, Particle0, Particle1)")
    #df = df.Filter("!is_VBF")

    
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
    #df = df.Define("selected_muons", "FCCAnalyses::excluded_Higgs_decays(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)") # was 10
    df = df.Define("leps_sel_p", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")
    df = df.Define("leps_sel_iso", "FCCAnalyses::sel_iso(99)(leps_sel_p, leps_all_iso)") # 0.25
    df = df.Alias("leps", "leps_sel_iso") 
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    df = df.Define("leps_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps, ReconstructedParticles)")
    
    # prompt leptons: filter the leptons from prompt production
    #df = df.Define("prompt_muons", "FCCAnalyses::select_prompt_leptons(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    #df = df.Define("prompt_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(prompt_muons)")
    #df = df.Define("prompt_muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(prompt_muons)")
    #df = df.Define("prompt_muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(prompt_muons)")
    #df = df.Define("prompt_muons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(prompt_muons)")
    #df = df.Define("prompt_muons_no", "FCCAnalyses::ReconstructedParticle::get_n(prompt_muons)")
    #df = df.Define("prompt_muons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(prompt_muons, ReconstructedParticles)")
   
    #df = df.Filter("prompt_muons.size() == 2")
    #df = df.Filter("selected_muons_no >= 2")
    
    
    #df = df.Define("muons_from_higgs", "FCCAnalyses::from_Higgsdecay(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    #df = df.Define("muons_from_prompt", "FCCAnalyses::from_prompt(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    #df = df.Filter("muons_from_higgs == false")
    #df = df.Filter("muons_from_prompt == true")
        

    # momentum resolution
    df = df.Define("leps_all_reso_p", "FCCAnalyses::leptonResolution_p(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("leps_reso_p", "FCCAnalyses::leptonResolution_p(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    
    # build the Z resonance and recoil using MC information from the selected muons
    #df = df.Define("zed_leptonic_MC", "FCCAnalyses::resonanceZBuilder2(91, true)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    #df = df.Define("zed_leptonic_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_MC)")
    #df = df.Define("zed_leptonic_recoil_MC",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_MC)")
    #df = df.Define("zed_leptonic_recoil_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_MC)")
        
    # gen analysis
    if dataset.name in sigProcs:
        df = df.Define("higgs_MC", "FCCAnalyses::gen_sel_pdgIDInt(25,false)(Particle)")
        df = df.Define("daughter_higgs", "FCCAnalyses::gen_decay_list(higgs_MC, Particle, Particle1)")
        df = df.Define("daughter_higgs_collapsed", "daughter_higgs.size()>1 ? ((abs(daughter_higgs[0])+abs(daughter_higgs[1]))*0.5) : -1000 ")
        
        
    # baseline selections and histograms
    results.append(df.Histo1D(("leps_all_p_cut0", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_p_gen_cut0", "", *bins_p_mu), "leps_all_p_gen"))
    results.append(df.Histo1D(("leps_all_theta_cut0", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi_cut0", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q_cut0", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no_cut0", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("leps_all_iso_cut0", "", *bins_iso), "leps_all_iso"))
    results.append(df.Histo1D(("leps_all_reso_p_cut0", "", *bins_resolution), "leps_all_reso_p"))
    

    results.append(df.Histo1D(("leps_p_cut0", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("leps_theta_cut0", "", *bins_theta), "leps_theta"))
    results.append(df.Histo1D(("leps_phi_cut0", "", *bins_phi), "leps_phi"))
    results.append(df.Histo1D(("leps_q_cut0", "", *bins_charge), "leps_q"))
    results.append(df.Histo1D(("leps_no_cut0", "", *bins_count), "leps_no"))
    results.append(df.Histo1D(("leps_iso_cut0", "", *bins_iso), "leps_iso"))
    results.append(df.Histo1D(("leps_reso_p_cut0", "", *bins_resolution), "leps_reso_p"))
    
    #results.append(df.Histo1D(("prompt_muons_p_cut0", "", *bins_p_mu), "prompt_muons_p"))
    #results.append(df.Histo1D(("prompt_muons_theta_cut0", "", *bins_theta), "prompt_muons_theta"))
    #results.append(df.Histo1D(("prompt_muons_phi_cut0", "", *bins_phi), "prompt_muons_phi"))
    #results.append(df.Histo1D(("prompt_muons_charge_cut0", "", *bins_charge), "prompt_muons_charge"))
    #results.append(df.Histo1D(("prompt_muons_no_cut0", "", *bins_count), "prompt_muons_no"))
    #results.append(df.Histo1D(("prompt_muons_iso_cut0", "", *bins_iso), "prompt_muons_iso"))
    #results.append(df.Histo1D(("prompt_muons_reso_cut0", "", *bins_resolution), "prompt_muons_reso"))
    
    #results.append(df.Histo1D(("gen_prompt_muons_p_cut0", "", *bins_p_mu), "gen_prompt_muons_p"))
    #results.append(df.Histo1D(("gen_prompt_muons_theta_cut0", "", *bins_theta), "gen_prompt_muons_theta"))
    #results.append(df.Histo1D(("gen_prompt_muons_phi_cut0", "", *bins_phi), "gen_prompt_muons_phi"))
    #results.append(df.Histo1D(("gen_prompt_muons_charge_cut0", "", *bins_charge), "gen_prompt_muons_charge"))
    #results.append(df.Histo1D(("gen_prompt_muons_no_cut0", "", *bins_count), "gen_prompt_muons_no"))
    
    results.append(df.Histo1D(("photons_p_cut0", "", *bins_p_mu), "photons_p"))
    results.append(df.Histo1D(("photons_theta_cut0", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi_cut0", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no_cut0", "", *bins_count), "photons_no"))
    
    results.append(df.Histo1D(("gen_photons_p", "", *bins_p_mu), "gen_photons_p"))
    results.append(df.Histo1D(("gen_photons_theta", "", *bins_theta), "gen_photons_theta"))
    results.append(df.Histo1D(("gen_photons_phi", "", *bins_phi), "gen_photons_phi"))
    results.append(df.Histo1D(("gen_photons_no", "", *bins_count), "gen_photons_no"))
    
    #results.append(df.Histo1D(("deltaR_gen_leps", "", *bins_dR), "deltaR_gen_leps"))
    #results.append(df.Histo1D(("mll_gen_leps", "", *bins_m_ll), "mll_gen_leps"))
    

    #df = df.Filter("daughter_higgs_collapsed == 23")
    
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut0", "", *bins_count), "daughter_higgs_collapsed"))
        
        df = df.Define("leps_all_from_higgs", "FCCAnalyses::from_Higgsdecay(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        results.append(df.Histo1D(("leps_all_from_higgs_cut0", "", *bins_count), "leps_all_from_higgs"))
        
        df = df.Define("leps_from_higgs", "FCCAnalyses::from_Higgsdecay(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        results.append(df.Histo1D(("leps_from_higgs_cut0", "", *bins_count), "leps_from_higgs"))
    
    
    
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow_cut0", "", *bins_count), "cut0"))

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1 && leps_sel_iso.size() > 0").Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow_cut1", "", *bins_count), "cut1"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut1", "", *bins_count), "daughter_higgs_collapsed"))
        
        results.append(df.Histo1D(("leps_all_from_higgs_cut1", "", *bins_count), "leps_all_from_higgs"))
        results.append(df.Histo1D(("leps_from_higgs_cut1", "", *bins_count), "leps_from_higgs"))
    
    
    #########
    ### CUT 2 :at least 2 OS leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2 && abs(Sum(leps_q)) < leps_q.size()").Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow_cut2", "", *bins_count), "cut2"))
    
    #df = df.Filter("leps_no == 2")

    # build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    df = df.Define("zbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zll", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[0]}") # the Z
    df = df.Define("zll_leps", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[1],zbuilder_result[2]}") # the leptons
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]")
    df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)")
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]")
    df = df.Define("zll_category", "FCCAnalyses::polarAngleCategorization(0.8, 2.34)(zll_leps)")
    
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)")
    df = df.Define("zll_leps_dR", "FCCAnalyses::deltaR(zll_leps)")
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)")
     
    df = df.Define("prompt_muons", "FCCAnalyses::whizard_zh_select_prompt_leptons(zll_leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("prompt_muons_no", "prompt_muons.size()")
    #df = df.Filter("prompt_muons.size() == 2") 

    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut2", "", *bins_count), "daughter_higgs_collapsed"))
        
        # for the selected muons, check whether they come from the Higgs (to optimize the pairing)
        df = df.Define("zll_leps_from_higgs", "FCCAnalyses::from_Higgsdecay(zll_leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
        results.append(df.Histo1D(("zll_leps_from_higgs_cut2", "", *bins_count), "zll_leps_from_higgs"))
        results.append(df.Histo1D(("prompt_muons_cut2", "", *bins_count), "prompt_muons_no"))
        #df = df.Filter("zll_leps_from_higgs == 0")
        #results.append(df.Histo1D(("zll_p_cut2", "", *bins_p_ll), "zll_p"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut1", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zll_m")) # 2D hists filling cannot be arrays
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut1", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zll_p"))
        #results.append(df.Histo1D(("zed_leptonic_m_cut2", "", *bins_m_ll), "zll_m"))
        #results.append(df.Histo1D(("zed_leptonic_recoil_m_cut2", "", *bins_recoil), "zll_recoil_m"))
        
        # branch it off
        df2 = df.Filter("zll_leps_from_higgs == 0")
        results.append(df2.Histo1D(("zll_m_correctPairs", "", *bins_m_ll), "zll_m"))
        results.append(df2.Histo1D(("zll_recoil_m_correctPairs", "", *bins_recoil), "zll_recoil_m"))
        results.append(df2.Histo1D(("zll_p_correctPairs", "", *bins_p_ll), "zll_p"))
        results.append(df2.Histo1D(("leps_p_correctPairs", "", *bins_p_mu), "zll_leps_p"))
        results.append(df2.Histo1D(("zll_leps_dR_correctPairs", "", *bins_dR), "zll_leps_dR"))
        results.append(df2.Histo1D(("zll_leps_theta_correctPairs", "", *bins_theta), "zll_leps_theta"))
        
        df3 = df.Filter("zll_leps_from_higgs > 0")
        results.append(df3.Histo1D(("zll_m_incorrectPairs", "", *bins_m_ll), "zll_m"))
        results.append(df3.Histo1D(("zll_recoil_m_incorrectPairs", "", *bins_recoil), "zll_recoil_m"))
        results.append(df3.Histo1D(("zll_p_incorrectPairs", "", *bins_p_ll), "zll_p"))
        results.append(df3.Histo1D(("leps_p_incorrectPairs", "", *bins_p_mu), "zll_leps_p"))
        results.append(df3.Histo1D(("zll_leps_dR_incorrectPairs", "", *bins_dR), "zll_leps_dR"))
        results.append(df3.Histo1D(("zll_leps_theta_incorrectPairs", "", *bins_theta), "zll_leps_theta"))
        
        results.append(df.Histo1D(("leps_all_from_higgs_cut2", "", *bins_count), "leps_all_from_higgs"))
        results.append(df.Histo1D(("leps_from_higgs_cut2", "", *bins_count), "leps_from_higgs"))
    
    #########
    ### CUT 3: Z mass window
    #########  
    df = df.Filter("zll_m > 86 && zll_m < 96").Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow_cut3", "", *bins_count), "cut3"))
    #df = df.Filter("zed_leptonic_m[0] > 73 &&  zed_leptonic_m[0] < 120")
    #results.append(df.Histo1D(("zll_m_cut3", "", *bins_m_ll), "zll_m"))
    #results.append(df.Histo1D(("zll_recoil_m_cut3", "", *bins_recoil), "zll_recoil_m"))
    #results.append(df.Histo1D(("zll_p_cut3", "", *bins_p_ll), "zll_p"))
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut3", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut3", "", *bins_count), "zll_leps_from_higgs"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut4", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut4", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        #results.append(df.Histo1D(("zed_leptonic_m_cut4", "", *bins_m_ll), "zed_leptonic_m"))
        #results.append(df.Histo1D(("zed_leptonic_recoil_m_cut4", "", *bins_recoil), "zed_leptonic_recoil_m"))
        
    
    #########
    ### CUT 4: Z momentum
    #########  
    df = df.Filter("zll_p > 20 && zll_p < 70").Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow_cut4", "", *bins_count), "cut4"))
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut4", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut4", "", *bins_count), "zll_leps_from_higgs"))
        #results.append(df.Histo1D(("zed_leptonic_p_cut5", "", *bins_p_ll), "zed_leptonic_p"))
        #results.append(df.Histo1D(("selected_muons_p_cut5", "", *bins_p_mu), "selected_muons_p"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut5", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut5", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        #results.append(df.Histo1D(("zed_leptonic_m_cut5", "", *bins_m_ll), "zed_leptonic_m"))
        #results.append(df.Histo1D(("zed_leptonic_recoil_m_cut5", "", *bins_recoil), "zed_leptonic_recoil_m"))
        
    
    #########
    ### CUT 5: cosThetaMiss, for mass analysis
    #########  
    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
    
    
    
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss"))
    
    df = df.Filter("cosTheta_miss < 5").Define("cut5", "5") # 0.98
    results.append(df.Histo1D(("cutFlow_cut5", "", *bins_count), "cut5"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut5", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut5", "", *bins_count), "zll_leps_from_higgs"))
        #results.append(df.Histo1D(("zed_leptonic_p_cut6", "", *bins_p_ll), "zed_leptonic_p"))
        #results.append(df.Histo1D(("selected_muons_p_cut6", "", *bins_p_mu), "selected_muons_p"))
        #results.append(df.Histo1D(("cosThetaMiss_cut6", "", *bins_cosThetaMiss), "cosTheta_miss"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut6", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        #results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut6", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        #results.append(df.Histo1D(("zed_leptonic_m_cut6", "", *bins_m_ll), "zed_leptonic_m"))
        #results.append(df.Histo1D(("zed_leptonic_recoil_m_cut6", "", *bins_recoil), "zed_leptonic_recoil_m"))
    
    # ISR photons
    results.append(df.Histo1D(("photons_p_cut5", "", *bins_p_mu), "photons_p"))
    results.append(df.Histo1D(("photons_theta_cut5", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi_cut5", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no_cut5", "", *bins_count), "photons_no"))        
    
    
    #df = df.Filter("muons_theta[0] < 2.14 && muons_theta[0] > 1.0 && muons_theta[1] < 2.14 && muons_theta[1] > 1.0")
    #df = df.Filter("muons_theta[0] < 2.0 && muons_theta[0] > 1.15")
    #df = df.Filter("mll_gen_leps < 93 && mll_gen_leps > 88")
    
    #########
    ### CUT 6: recoil cut
    #########  
    
    # final selection and histograms
    df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120").Define("cut6", "6")
    results.append(df.Histo1D(("cutFlow_cut6", "", *bins_count), "cut6"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut6", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut6", "", *bins_count), "zll_leps_from_higgs"))
    
    # ISR photons
    results.append(df.Histo1D(("photons_p_cut6", "", *bins_p_mu), "photons_p"))
    results.append(df.Histo1D(("photons_theta_cut6", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi_cut6", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no_cut6", "", *bins_count), "photons_no"))
    
    
    ########################
    # Final histograms
    ########################
    
    results.append(df.Histo2D(("zll_m", "", *(bins_m_ll + bins_cat)), "zll_m", "zll_category"))
    results.append(df.Histo2D(("zll_recoil_m", "", *(bins_recoil + bins_cat)), "zll_recoil_m", "zll_category"))
    results.append(df.Histo2D(("zll_p", "", *(bins_p_ll + bins_cat)), "zll_p", "zll_category"))
    results.append(df.Histo2D(("leps_p", "", *(bins_p_mu + bins_cat)), "leps_p", "zll_category"))
    results.append(df.Histo2D(("cosThetaMiss", "", *(bins_cosThetaMiss + bins_cat)), "cosTheta_miss", "zll_category"))
    
    
    # MC based recoil
    #results.append(df.Histo1D(("zed_leptonic_m_MC", "", *bins_m_ll), "zed_leptonic_m_MC"))
    #results.append(df.Histo1D(("zed_leptonic_recoil_m_MC", "", *bins_recoil), "zed_leptonic_recoil_m_MC"))
    
    
    
    

    
    #df = df.Define("massweights", "FCCAnalyses::breitWignerWeightsHiggs()")
    #df = df.Define("massweights_indices", "FCCAnalyses::indices_(5)")
    
    #results.append(df.Histo2D(("zed_leptonic_recoil_m_massweights", "", *(bins_recoil + bins_massweights)), "zed_leptonic_recoil_m_", "massweights_indices", "massweights"))
    
    if dataset.name not in sigProcs:
        return results, weightsum
        
        
    
    
    
    #bins_count = (50, 0, 50)

    # systematics
        
    '''
    # muon momentum scale
    df = df.Define("muons_muscaleup", "momentum_scale(1e-5)(muons)")
    df = df.Define("muons_muscaledw", "momentum_scale(-1e-5)(muons)")
    df = df.Define("selected_muons_muscaleup", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_muscaleup)")
    df = df.Define("selected_muons_muscaledw", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_muscaledw)")
    df = df.Define("selected_muons_pt_muscaleup", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_muscaleup)")
    df = df.Define("selected_muons_pt_muscaledw", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_muscaledw)")
               
    df = df.Define("zed_leptonic_muscaleup", "resonanceZBuilder2(91, false)(selected_muons_muscaleup, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_muscaleup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_no_muscaleup", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_pt_muscaleup", "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_charge_muscaleup", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic_muscaleup)")
               
    df = df.Define("zed_leptonic_muscaledw", "resonanceZBuilder2(91, false)(selected_muons_muscaledw, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_muscaledw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_no_muscaledw", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_pt_muscaledw", "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_charge_muscaledw", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic_muscaledw)")
               
    df = df.Define("zed_leptonic_recoil_muscaleup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_recoil_muscaledw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_recoil_m_muscaleup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_muscaleup)")
    df = df.Define("zed_leptonic_recoil_m_muscaledw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_muscaledw)")
        
        
    # sqrt uncertainty
    df = df.Define("zed_leptonic_recoil_sqrtsup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240.002)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_sqrtsdw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(239.998)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_m_sqrtsup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_sqrtsup)")
    df = df.Define("zed_leptonic_recoil_m_sqrtsdw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_sqrtsdw)")
               
               

    # .Define("zed_leptonic_recoil_mc",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_mc)")
    # .Define("zed_leptonic_recoil_m_mc","FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_mc)")
    #.Define("selected_muons_mc", "MC_to_reco(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, selected_muons, Particle)")
    #.Define("muon_resolution", "get_resolution(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, selected_muons, Particle)")
               
               
    #.Define("zed_leptonic_recoil_MC",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)( zed_leptonic_MC )")
    #.Define("zed_leptonic_recoil_MC_mass",   "FCCAnalyses::ReconstructedParticle::get_mass( zed_leptonic_recoil_MC )")
    #.Define("zed_leptonic",         "APCHiggsTools::resonanceZBuilder(91)(selected_muons)")   
    #
               
    #.Define("selected_muons_all", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_all)")
    # create branch with muon transverse momentum
               
    #.Define("selected_muons_pt_mc", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_mc)")
    # create branch with muon rapidity
               

    # create branch with muon total momentum
    #.Define("selected_muons_p",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons)")
    #.Define("selected_muons_p_mc",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_mc)")
    #.Define("selected_muons_p_muscaleup",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_muscaleup)")
    #.Define("selected_muons_p_muscaledw",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_muscaledw)")
               
               
    #.Define("ISR_gamma_E", "ISR_gamma_E(selected_muons)")
    #.Define("ISR_costhetas", "ISR_costhetas(selected_muons)")
               
               
               
               
    #.Define("event_ht",     "FCCAnalyses::ReconstructedParticle::get_ht(muons, electrons, photons, jets, met)")
    # create branch with muon energy 
               
    # find zed candidates from  di-muon resonances  , returns the best candidate, closest to the Z
               
               
               
    #.Define("zed_leptonic_mc",           "FCCAnalyses::ReconstructedParticle::resonanceBuilder(91)(selected_muons_mc)")
               
    #.Define("zed_leptonic_pair",    "FCCAnalyses::ReconstructedParticle::resonancePairBuilder(91)(selected_muons)")
    #.Define("acoplanarity",      "FCCAnalyses::ReconstructedParticle::acoplanarity(zed_leptonic_pair)")
    #.Define("acolinearity",      "FCCAnalyses::ReconstructedParticle::acolinearity(zed_leptonic_pair)")
    # write branch with zed mass
               
               
    #.Define("zed_leptonic_m_mc",             "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_mc)")
    # write branch with zed transverse momenta
    #.Define("zed_leptonic_pt",      "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic)")
    #.Define("zed_leptonic_pt_mc",      "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_mc)")

    '''
 
    return results, weightsum
    
    


if __name__ == "__main__":

    datasets = []

    # import spring2021 IDEA samples
    #import FCCee_spring2021_IDEA
    
    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_preproduction_IDEA
    datasets_preproduction_IDEA = FCCee_preproduction_IDEA.get_datasets(baseDir=baseDir) # list of all datasets

    
    if args.flavor == "mumu": 
        

        signal = ["wzp6_ee_mumuH_ecm240"]
        signal_mass = ["wzp6_ee_mumuH_mH-higher-100MeV_ecm240", "wzp6_ee_mumuH_mH-higher-50MeV_ecm240", "wzp6_ee_mumuH_mH-lower-100MeV_ecm240", "wzp6_ee_mumuH_mH-lower-50MeV_ecm240"]
        bkgs = ["p8_ee_WW_mumu_ecm240", "p8_ee_ZZ_Zll_ecm240", "wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240", "p8_ee_Zll_ecm240"] # p8_ee_WW_ecm240 p8_ee_ZZ_ecm240
        
        select = signal + signal_mass + bkgs
        select = ["wzp6_ee_mumuH_ecm240"]
        select = ["p8_ee_WW_mumu_ecm240", "p8_ee_WW_ecm240"]
    
    if args.flavor == "ee":
    
        signal = ["wzp6_ee_eeH_ecm240"]
        signal_mass = ["wzp6_ee_eeH_mH-higher-100MeV_ecm240", "wzp6_ee_eeH_mH-higher-50MeV_ecm240", "wzp6_ee_eeH_mH-lower-100MeV_ecm240", "wzp6_ee_eeH_mH-lower-50MeV_ecm240"]
        bkgs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_Zll_ecm240", "wzp6_ee_ee_Mee_30_150_ecm240", "wzp6_ee_tautau_ecm240", "p8_ee_Zll_ecm240"] #  p8_ee_ZZ_ecm240
        
        select = signal + signal_mass + bkgs
        select = ["wzp6_ee_eeH_ecm240"]
        
        
        

    datasets += functions.filter_datasets(datasets_preproduction_IDEA, select)
    result = functions.build_and_run(datasets, build_graph, "tmp/output_mass_xsec_%s.root" % args.flavor, maxFiles=args.maxFiles, norm=True, lumi=5000000)
    
