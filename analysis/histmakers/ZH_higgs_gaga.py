
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

ROOT.EnableImplicitMT()
if args.nThreads: 
    ROOT.DisableImplicitMT()
    ROOT.EnableImplicitMT(int(args.nThreads))
print(ROOT.GetThreadPoolSize())

# define histograms
bins_p = (2000, 0, 200) # 100 MeV bins
bins_m_gaga = (3000, 0, 300) # 100 MeV bins
bins_p_gaga = (2000, 0, 200) # 100 MeV bins
bins_recoil = (2000, 0, 200) # 100 MeV bins 

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)





def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    
    
    # all photons
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
    df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")

    results.append(df.Histo1D(("photons_p", "", *bins_p), "photons_p"))
    results.append(df.Histo1D(("photons_theta", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no", "", *bins_count), "photons_no"))
    
    
    # select photons with momentum p > 30 GeV 
    # Higgs -> gamma gamma produces on average 125/2 = 62.5 GeV photons
    df = df.Define("selected_photons", "FCCAnalyses::ReconstructedParticle::sel_p(30)(photons)")
    df = df.Define("selected_photons_p", "FCCAnalyses::ReconstructedParticle::get_p(selected_photons)")
    df = df.Define("selected_photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(selected_photons)")
    df = df.Define("selected_photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(selected_photons)")
    df = df.Define("selected_photons_no", "FCCAnalyses::ReconstructedParticle::get_n(selected_photons)")
    
    results.append(df.Histo1D(("selected_photons_p", "", *bins_p), "selected_photons_p"))
    results.append(df.Histo1D(("selected_photons_theta", "", *bins_theta), "selected_photons_theta"))
    results.append(df.Histo1D(("selected_photons_phi", "", *bins_phi), "selected_photons_phi"))
    results.append(df.Histo1D(("selected_photons_no", "", *bins_count), "selected_photons_no"))
    
    
    # require at least 2 photons
    df = df.Filter("selected_photons_no >= 2")
    
    # make the resonance
    df = df.Define("resonance", "FCCAnalyses::resonanceHBuilder(125)(selected_photons)")
    df = df.Filter("resonance.size() > 0")
    
    df = df.Define("resonance_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance)")
    df = df.Define("resonance_p", "FCCAnalyses::ReconstructedParticle::get_p(resonance)")
    df = df.Define("resonance_recoil",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(resonance)")
    df = df.Define("recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance_recoil)")

    results.append(df.Histo1D(("resonance_m", "", *bins_m_gaga), "resonance_m"))
    results.append(df.Histo1D(("resonance_p", "", *bins_p_gaga), "resonance_p"))
    #results.append(df.Histo1D(("resonance_recoil", "", *bins_recoil), "resonance_recoil"))
     
    return results, weightsum
     
    
    
    
    
    # select muons
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("muons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(muons, ReconstructedParticles)") 
    
    #df = df.Define("selected_muons", "FCCAnalyses::excluded_Higgs_decays(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)") # was 10
    df = df.Define("selected_muons_", "FCCAnalyses::ReconstructedParticle::sel_p(20)(muons)")
    df = df.Define("selected_muons", "FCCAnalyses::sel_iso(99)(selected_muons_, muons_iso)") # 0.25
    
    
    
    # prompt muons
    df = df.Define("prompt_muons", "FCCAnalyses::select_prompt_leptons(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("prompt_muons_p", "FCCAnalyses::ReconstructedParticle::get_p(prompt_muons)")
    df = df.Define("prompt_muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(prompt_muons)")
    df = df.Define("prompt_muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(prompt_muons)")
    df = df.Define("prompt_muons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(prompt_muons)")
    df = df.Define("prompt_muons_no", "FCCAnalyses::ReconstructedParticle::get_n(prompt_muons)")
    df = df.Define("prompt_muons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(prompt_muons, ReconstructedParticles)")
   
    #df = df.Filter("selected_muons_no >= 2")
    
    
    #df = df.Define("muons_from_higgs", "FCCAnalyses::from_Higgsdecay(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    #df = df.Define("muons_from_prompt", "FCCAnalyses::from_prompt(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    #df = df.Filter("muons_from_higgs == false")
    #df = df.Filter("muons_from_prompt == true")
        

    # muon resolution
    df = df.Define("muons_reso", "FCCAnalyses::muonResolution(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("selected_muons_reso", "FCCAnalyses::muonResolution(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("prompt_muons_reso", "FCCAnalyses::muonResolution(prompt_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    
    # build the Z resonance and recoil using MC information from the selected muons
    df = df.Define("zed_leptonic_MC", "FCCAnalyses::resonanceZBuilder2(91, true)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_MC)")
    df = df.Define("zed_leptonic_recoil_MC",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_MC)")
    df = df.Define("zed_leptonic_recoil_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_MC)")
        
    # gen analysis
    if dataset.name in sigProcs:
        df = df.Define("higgs_MC", "FCCAnalyses::gen_sel_pdgIDInt(25,false)(Particle)")
        df = df.Define("daughter_higgs", "FCCAnalyses::gen_decay_list(higgs_MC, Particle, Particle1)")
        df = df.Define("daughter_higgs_collapsed", "daughter_higgs.size()>1 ? ((abs(daughter_higgs[0])+abs(daughter_higgs[1]))*0.5) : -1000 ")
        
        
    # baseline selections and histograms
    results.append(df.Histo1D(("muons_p_cut0", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta_cut0", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_cut0", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_charge_cut0", "", *bins_charge), "muons_charge"))
    results.append(df.Histo1D(("muons_no_cut0", "", *bins_count), "muons_no"))
    results.append(df.Histo1D(("muons_iso_cut0", "", *bins_iso), "muons_iso"))
    results.append(df.Histo1D(("muons_reso_cut0", "", *bins_resolution), "muons_reso"))
    

    results.append(df.Histo1D(("selected_muons_p_cut0", "", *bins_p_mu), "selected_muons_p"))
    results.append(df.Histo1D(("selected_muons_theta_cut0", "", *bins_theta), "selected_muons_theta"))
    results.append(df.Histo1D(("selected_muons_phi_cut0", "", *bins_phi), "selected_muons_phi"))
    results.append(df.Histo1D(("selected_muons_charge_cut0", "", *bins_charge), "selected_muons_charge"))
    results.append(df.Histo1D(("selected_muons_no_cut0", "", *bins_count), "selected_muons_no"))
    results.append(df.Histo1D(("selected_muons_iso_cut0", "", *bins_iso), "selected_muons_iso"))
    results.append(df.Histo1D(("selected_muons_reso_cut0", "", *bins_resolution), "selected_muons_reso"))
    
    results.append(df.Histo1D(("prompt_muons_p_cut0", "", *bins_p_mu), "prompt_muons_p"))
    results.append(df.Histo1D(("prompt_muons_theta_cut0", "", *bins_theta), "prompt_muons_theta"))
    results.append(df.Histo1D(("prompt_muons_phi_cut0", "", *bins_phi), "prompt_muons_phi"))
    results.append(df.Histo1D(("prompt_muons_charge_cut0", "", *bins_charge), "prompt_muons_charge"))
    results.append(df.Histo1D(("prompt_muons_no_cut0", "", *bins_count), "prompt_muons_no"))
    results.append(df.Histo1D(("prompt_muons_iso_cut0", "", *bins_iso), "prompt_muons_iso"))
    results.append(df.Histo1D(("prompt_muons_reso_cut0", "", *bins_resolution), "prompt_muons_reso"))
    
    results.append(df.Histo1D(("gen_prompt_muons_p_cut0", "", *bins_p_mu), "gen_prompt_muons_p"))
    results.append(df.Histo1D(("gen_prompt_muons_theta_cut0", "", *bins_theta), "gen_prompt_muons_theta"))
    results.append(df.Histo1D(("gen_prompt_muons_phi_cut0", "", *bins_phi), "gen_prompt_muons_phi"))
    results.append(df.Histo1D(("gen_prompt_muons_charge_cut0", "", *bins_charge), "gen_prompt_muons_charge"))
    results.append(df.Histo1D(("gen_prompt_muons_no_cut0", "", *bins_count), "gen_prompt_muons_no"))
    
    
    # forward/central resolution
    df = df.Define("muons_central", "FCCAnalyses::sel_eta_abs(0,0.8)(muons)")
    df = df.Define("muons_forward", "FCCAnalyses::sel_eta_abs(0.8,20)(muons)")
    df = df.Define("muons_central_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_central)")
    df = df.Define("muons_forward_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_forward)")
    df = df.Define("muons_central_reso", "FCCAnalyses::muonResolution(muons_central, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("muons_forward_reso", "FCCAnalyses::muonResolution(muons_forward, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    
    results.append(df.Histo1D(("muons_central_reso_cut0", "", *bins_resolution), "muons_central_reso"))
    results.append(df.Histo1D(("muons_forward_reso_cut0", "", *bins_resolution), "muons_forward_reso"))
    results.append(df.Histo1D(("muons_central_theta_cut0", "", *bins_theta), "muons_central_theta"))
    results.append(df.Histo1D(("muons_forward_theta_cut0", "", *bins_theta), "muons_forward_theta"))
    
    # p dependent resolution
    df = df.Define("muons_0_30", "FCCAnalyses::ReconstructedParticle::sel_p(0,30)(muons)")
    df = df.Define("muons_30_50", "FCCAnalyses::ReconstructedParticle::sel_p(30,50)(muons)")
    df = df.Define("muons_50_70", "FCCAnalyses::ReconstructedParticle::sel_p(50,70)(muons)")
    df = df.Define("muons_70_100", "FCCAnalyses::ReconstructedParticle::sel_p(70,100)(muons)")
    df = df.Define("muons_0_30_reso", "FCCAnalyses::muonResolution(muons_0_30, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("muons_30_50_reso", "FCCAnalyses::muonResolution(muons_30_50, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("muons_50_70_reso", "FCCAnalyses::muonResolution(muons_50_70, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("muons_70_100_reso", "FCCAnalyses::muonResolution(muons_70_100, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    results.append(df.Histo1D(("muons_0_30_reso_cut0", "", *bins_resolution), "muons_0_30_reso"))
    results.append(df.Histo1D(("muons_30_50_reso_cut0", "", *bins_resolution), "muons_30_50_reso"))
    results.append(df.Histo1D(("muons_50_70_reso_cut0", "", *bins_resolution), "muons_50_70_reso"))
    results.append(df.Histo1D(("muons_70_100_reso_cut0", "", *bins_resolution), "muons_70_100_reso"))
    
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut0", "", *bins_count), "daughter_higgs_collapsed"))
    
    # bare plots
    
   
    #########
    ### CUT 1
    #########
    df = df.Filter("selected_muons_no >= 1")
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut1", "", *bins_count), "daughter_higgs_collapsed"))
        
    #########
    ### CUT 2
    #########
    df = df.Filter("selected_muons_no >= 2")
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut2", "", *bins_count), "daughter_higgs_collapsed"))
        
    #########
    ### CUT 3
    #########    
    # build the Z resonance and recoil  resonanceZBuilderHiggsPairs
    #df = df.Define("zed_leptonic", "FCCAnalyses::resonanceZBuilder2(91, false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic", "FCCAnalyses::resonanceZBuilderHiggsPairs(91, false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zed_leptonic_m", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic)")
    df = df.Define("zed_leptonic_no", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic)")
    df = df.Define("zed_leptonic_p", "FCCAnalyses::ReconstructedParticle::get_p(zed_leptonic)")
    df = df.Define("zed_leptonic_charge", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil)")
    
    df = df.Define("zed_leptonic_m_", "zed_leptonic_m[0]")
    df = df.Define("zed_leptonic_p_", "zed_leptonic_p[0]")
    df = df.Define("zed_leptonic_recoil_m_", "zed_leptonic_recoil_m[0]")
    
    df = df.Filter("zed_leptonic_m.size() >= 0") # was ==1
    if dataset.name in sigProcs:
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut3", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut3", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        results.append(df.Histo1D(("zed_leptonic_m_cut3", "", *bins_m_ll), "zed_leptonic_m_"))
        results.append(df.Histo1D(("zed_leptonic_recoil_m_cut3", "", *bins_recoil), "zed_leptonic_recoil_m"))
        results.append(df.Histo1D(("higgs_decay_cut3", "", *bins_count), "daughter_higgs_collapsed"))
    
    
    #########
    ### CUT 4
    #########  
    df = df.Filter("zed_leptonic_no == 1")
    df = df.Filter("zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96")
    #df = df.Filter("zed_leptonic_m[0] > 73 &&  zed_leptonic_m[0] < 120")
    results.append(df.Histo1D(("zed_leptonic_m_cut4", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut4", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_p_cut4", "", *bins_p_ll), "zed_leptonic_p"))
    results.append(df.Histo1D(("selected_muons_p_cut4", "", *bins_p_mu), "selected_muons_p"))
    if dataset.name in sigProcs:
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut4", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut4", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        results.append(df.Histo1D(("zed_leptonic_m_cut4", "", *bins_m_ll), "zed_leptonic_m"))
        results.append(df.Histo1D(("zed_leptonic_recoil_m_cut4", "", *bins_recoil), "zed_leptonic_recoil_m"))
        results.append(df.Histo1D(("higgs_decay_cut4", "", *bins_count), "daughter_higgs_collapsed")) 
    
    #########
    ### CUT 5
    #########  
    df = df.Filter("zed_leptonic_p[0] > 20 && zed_leptonic_p[0] < 70")
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("zed_leptonic_p_cut5", "", *bins_p_ll), "zed_leptonic_p"))
        results.append(df.Histo1D(("selected_muons_p_cut5", "", *bins_p_mu), "selected_muons_p"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut5", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut5", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        results.append(df.Histo1D(("zed_leptonic_m_cut5", "", *bins_m_ll), "zed_leptonic_m"))
        results.append(df.Histo1D(("zed_leptonic_recoil_m_cut5", "", *bins_recoil), "zed_leptonic_recoil_m"))
        results.append(df.Histo1D(("higgs_decay_cut5", "", *bins_count), "daughter_higgs_collapsed")) 
    
    #########
    ### CUT 6
    #########  
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
    #df = df.Filter("cosTheta_miss[0] < 0.98")
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("zed_leptonic_p_cut6", "", *bins_p_ll), "zed_leptonic_p"))
        results.append(df.Histo1D(("selected_muons_p_cut6", "", *bins_p_mu), "selected_muons_p"))
        results.append(df.Histo1D(("cosThetaMiss_cut6", "", *bins_cosThetaMiss), "cosTheta_miss"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_m_cut6", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_m_"))
        results.append(df.Histo2D(("higgs_decay_zed_leptonic_p_cut6", "", *(bins_count + bins_m_ll)), "daughter_higgs_collapsed", "zed_leptonic_p_"))
        results.append(df.Histo1D(("zed_leptonic_m_cut6", "", *bins_m_ll), "zed_leptonic_m"))
        results.append(df.Histo1D(("zed_leptonic_recoil_m_cut6", "", *bins_recoil), "zed_leptonic_recoil_m"))
        results.append(df.Histo1D(("higgs_decay_cut6", "", *bins_count), "daughter_higgs_collapsed")) 
    
    
    # final selection and histograms
    df = df.Filter("zed_leptonic_recoil_m[0] < 140 && zed_leptonic_recoil_m[0] > 120")
    results.append(df.Histo1D(("zed_leptonic_m", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_p", "", *bins_p_ll), "zed_leptonic_p"))
    results.append(df.Histo1D(("selected_muons_p", "", *bins_p_mu), "selected_muons_p"))
    results.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay", "", *bins_count), "daughter_higgs_collapsed")) 
    
    # MC based recoil
    results.append(df.Histo1D(("zed_leptonic_m_MC", "", *bins_m_ll), "zed_leptonic_m_MC"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_MC", "", *bins_recoil), "zed_leptonic_recoil_m_MC"))
    
    
    df = df.Define("massweights", "FCCAnalyses::breitWignerWeightsHiggs()")
    df = df.Define("massweights_indices", "FCCAnalyses::indices_(5)")
    
    results.append(df.Histo2D(("zed_leptonic_recoil_m_massweights", "", *(bins_recoil + bins_massweights)), "zed_leptonic_recoil_m_", "massweights_indices", "massweights"))
    
    if dataset.name not in sigProcs:
        return results, weightsum
        
        
    
    

 
    return results, weightsum
    
    


if __name__ == "__main__":

    # import spring2021 IDEA samples
    import FCCee_spring2021_IDEA
    datasets = FCCee_spring2021_IDEA.getDatasets(filt="wzp6_ee_mumuH_ecm240")
 


    result = functions.build_and_run(datasets, build_graph, "tmp/output_higgs_gaga.root", maxFiles=args.maxFiles)
    
