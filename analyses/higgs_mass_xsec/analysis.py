
import functions
import helpers
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", choices=["mumu", "ee"], default="mumu")
parser.add_argument("--type", type=str, help="Run type (mass or xsec)", choices=["mass", "xsec"], default="mass")
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



def build_graph(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []
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
    else:
        df = df.Alias("Lepton0", "Electron#0.index")

    df = helpers.defineCutFlowVars(df) # make the cutX=X variables

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
    df = df.Define("leps", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")

    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    df = df.Define("leps_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps, ReconstructedParticles)")
    df = df.Define("leps_sel_iso", "FCCAnalyses::sel_iso(0.25)(leps, leps_iso)") # 0.25

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
    
    
    
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1 && leps_sel_iso.size() > 0")
    results.append(df.Histo1D(("cutFlow_cut1", "", *bins_count), "cut1"))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut1", "", *bins_count), "daughter_higgs_collapsed"))
        results.append(df.Histo1D(("leps_all_from_higgs_cut1", "", *bins_count), "leps_all_from_higgs"))
        results.append(df.Histo1D(("leps_from_higgs_cut1", "", *bins_count), "leps_from_higgs"))

    #########
    ### CUT 2 :at least 2 OS leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2 && abs(Sum(leps_q)) < leps_q.size()")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

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

    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")

    df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(leps)")
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(leps)")
    
    results.append(df.Histo1D(("zll_m_cut2", "", *bins_m_ll), "zll_m"))

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
    df = df.Filter("zll_m > 86 && zll_m < 96")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    results.append(df.Histo1D(("zll_p_cut3", "", *bins_p_mu), "zll_p"))
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut3", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut3", "", *bins_count), "zll_leps_from_higgs"))

    #########
    ### CUT 4: Z momentum
    #########  
    df = df.Filter("zll_p > 20 && zll_p < 70")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))
    results.append(df.Histo1D(("zll_recoil_cut4", "", *bins_recoil), "zll_recoil_m"))
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut4", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut4", "", *bins_count), "zll_leps_from_higgs"))

    #########
    ### CUT 5: recoil cut
    #########  
    df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))
    results.append(df.Histo1D(("cosThetaMiss_cut5", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut5", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut5", "", *bins_count), "zll_leps_from_higgs"))

    #########
    ### CUT 6: cosThetaMiss, for mass analysis
    #########  
    if args.type == "mass":
        df = df.Filter("cosTheta_miss < 0.98")
    if dataset.name in sigProcs: 
        results.append(df.Histo1D(("higgs_decay_cut6", "", *bins_count), "daughter_higgs_collapsed")) 
        results.append(df.Histo1D(("zll_leps_from_higgs_cut6", "", *bins_count), "zll_leps_from_higgs"))
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))

    # final histograms
    results.append(df.Histo1D(("leps_p", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("zll_p", "", *bins_p_mu), "zll_p"))
    results.append(df.Histo1D(("zll_m", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_recoil", "", *bins_recoil), "zll_recoil_m"))

    results.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    results.append(df.Histo1D(("acoplanarity", "", *bins_aco), "acoplanarity"))
    results.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))
    
    results.append(df.Histo1D(("photons_p", "", *bins_p_mu), "photons_p"))
    results.append(df.Histo1D(("photons_theta", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no", "", *bins_count), "photons_no"))    


    ########################
    # Final histograms
    ########################
    results.append(df.Histo2D(("zll_recoil_m", "", *(bins_recoil_fine + bins_cat)), "zll_recoil_m", "zll_category"))
    results.append(df.Histo2D(("leps_reso_p", "", *(bins_resolution + bins_cat)), "leps_reso_p", "zll_category"))

    ########################
    # Systematics
    ########################

    # muon momentum scale
    df = df.Define("leps_scaleup", "FCCAnalyses::lepton_momentum_scale(1e-5)(leps)")
    df = df.Define("leps_scaledw", "FCCAnalyses::lepton_momentum_scale(-1e-5)(leps)")

    df = df.Define("zbuilder_result_scaleup", "FCCAnalyses::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(leps_scaleup, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zbuilder_result_scaledw", "FCCAnalyses::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(leps_scaledw, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zll_scaleup", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result_scaleup[0]}")
    df = df.Define("zll_scaledw", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result_scaledw[0]}")
    df = df.Define("zll_recoil_scaleup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll_scaleup)")
    df = df.Define("zll_recoil_scaledw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll_scaledw)")
    df = df.Define("zll_recoil_m_scaleup", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil_scaleup)[0]")
    df = df.Define("zll_recoil_m_scaledw", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil_scaledw)[0]")

    results.append(df.Histo2D(("zll_recoil_m_scaleup", "", *(bins_recoil_fine + bins_cat)), "zll_recoil_m_scaleup", "zll_category"))
    results.append(df.Histo2D(("zll_recoil_m_scaledw", "", *(bins_recoil_fine + bins_cat)), "zll_recoil_m_scaledw", "zll_category"))


    # sqrt uncertainty
    df = df.Define("zll_recoil_sqrtsup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240.002)(zll)")
    df = df.Define("zll_recoil_sqrtsdw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(239.998)(zll)")
    df = df.Define("zll_recoil_m_sqrtsup", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil_sqrtsup)[0]")
    df = df.Define("zll_recoil_m_sqrtsdw", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil_sqrtsdw)[0]")

    results.append(df.Histo2D(("zll_recoil_m_sqrtsup", "", *(bins_recoil_fine + bins_cat)), "zll_recoil_m_sqrtsup", "zll_category"))
    results.append(df.Histo2D(("zll_recoil_m_sqrtsdw", "", *(bins_recoil_fine + bins_cat)), "zll_recoil_m_sqrtsdw", "zll_category"))

    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets
    datasets_to_run = []

    if args.flavor == "mumu": 
        bkgs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240"]
        bkgs_rare = ["wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]

        signal_base = ["wzp6_ee_mumuH_ecm240", "wzp6_ee_mumuH_mH-lower-50MeV_ecm240", "wzp6_ee_mumuH_mH-lower-100MeV_ecm240", "wzp6_ee_mumuH_mH-higher-100MeV_ecm240", "wzp6_ee_mumuH_mH-higher-50MeV_ecm240", "wzp6_ee_mumuH_BES-higher-1pc_ecm240", "wzp6_ee_mumuH_BES-lower-6pc_ecm240", "wzp6_ee_mumuH_BES-higher-6pc_ecm240"]
        
        signal_noBES = ["wzp6_ee_mumuH_noBES_ecm240", "wzp6_ee_mumuH_mH-lower-50MeV_noBES_ecm240", "wzp6_ee_mumuH_mH-lower-100MeV_noBES_ecm240", "wzp6_ee_mumuH_mH-higher-100MeV_noBES_ecm240", "wzp6_ee_mumuH_mH-higher-50MeV_noBES_ecm240",  "wzp6_ee_mumuH_BES-lower-1pc_ecm240"] 
        
        signal_3T = ["wzp6_ee_mumuH_ecm240_3T", "wzp6_ee_mumuH_mH-lower-50MeV_ecm240_3T", "wzp6_ee_mumuH_mH-lower-100MeV_ecm240_3T", "wzp6_ee_mumuH_mH-higher-100MeV_ecm240_3T", "wzp6_ee_mumuH_mH-higher-50MeV_ecm240_3T", "wzp6_ee_mumuH_BES-lower-1pc_ecm240_3T", "wzp6_ee_mumuH_BES-higher-1pc_ecm240_3T"]
        
        signal_CLD = ["wzp6_ee_mumuH_ecm240_CLD", "wzp6_ee_mumuH_mH-lower-50MeV_ecm240_CLD", "wzp6_ee_mumuH_mH-lower-100MeV_ecm240_CLD", "wzp6_ee_mumuH_mH-higher-100MeV_ecm240_CLD", "wzp6_ee_mumuH_mH-higher-50MeV_ecm240_CLD",  "wzp6_ee_mumuH_BES-lower-1pc_ecm240_CLD", "wzp6_ee_mumuH_BES-higher-1pc_ecm240_CLD"]

        signal = signal_base + signal_noBES + signal_3T + signal_CLD
        datasets_to_run = signal + bkgs + bkgs_rare

    if args.flavor == "ee":
        bkgs = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_ee_Mee_30_150_ecm240", "wzp6_ee_tautau_ecm240"]
        bkgs_rare = ["wzp6_egamma_eZ_Zee_ecm240", "wzp6_gammae_eZ_Zee_ecm240", "wzp6_gaga_ee_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]

        signal_base = ["wzp6_ee_eeH_ecm240", "wzp6_ee_eeH_mH-lower-50MeV_ecm240", "wzp6_ee_eeH_mH-lower-100MeV_ecm240", "wzp6_ee_eeH_mH-higher-100MeV_ecm240", "wzp6_ee_eeH_mH-higher-50MeV_ecm240", "wzp6_ee_eeH_BES-lower-1pc_ecm240", "wzp6_ee_eeH_BES-higher-1pc_ecm240", "wzp6_ee_eeH_BES-lower-6pc_ecm240", "wzp6_ee_eeH_BES-higher-6pc_ecm240"]
        
        signal_noBES = ["wzp6_ee_eeH_noBES_ecm240", "wzp6_ee_eeH_mH-lower-50MeV_noBES_ecm240", "wzp6_ee_eeH_mH-lower-100MeV_noBES_ecm240", "wzp6_ee_eeH_mH-higher-100MeV_noBES_ecm240", "wzp6_ee_eeH_mH-higher-50MeV_noBES_ecm240"]
        
        signal_3T = ["wzp6_ee_eeH_ecm240_3T", "wzp6_ee_eeH_mH-lower-50MeV_ecm240_3T", "wzp6_ee_eeH_mH-lower-100MeV_ecm240_3T", "wzp6_ee_eeH_mH-higher-100MeV_ecm240_3T", "wzp6_ee_eeH_mH-higher-50MeV_ecm240_3T", "wz3p6_ee_eeH_BES-lower-1pc_ecm240_3T", "wz3p6_ee_eeH_BES-higher-1pc_ecm240_3T"]
        
        
        signal_E2 = ["wzp6_ee_eeH_ecm240_E2", "wzp6_ee_eeH_mH-lower-50MeV_ecm240_E2", "wzp6_ee_eeH_mH-lower-100MeV_ecm240_E2", "wzp6_ee_eeH_mH-higher-100MeV_ecm240_E2", "wzp6_ee_eeH_mH-higher-50MeV_ecm240_E2", "wz3p6_ee_eeH_BES-lower-1pc_ecm240_E2", "wz3p6_ee_eeH_BES-higher-1pc_ecm240_E2"]
        
        signal_CLD = ["wzp6_ee_eeH_ecm240_CLD", "wzp6_ee_eeH_mH-lower-50MeV_ecm240_CLD", "wzp6_ee_eeH_mH-lower-100MeV_ecm240_CLD", "wzp6_ee_eeH_mH-higher-100MeV_ecm240_CLD", "wzp6_ee_eeH_mH-higher-50MeV_ecm240_CLD", "wz3p6_ee_eeH_BES-lower-1pc_ecm240_CLD", "wz3p6_ee_eeH_BES-higher-1pc_ecm240_CLD"]

        signal = signal_base + signal_noBES + signal_3T + signal_CLD + signal_E2
        datasets_to_run = signal + bkgs + bkgs_rare

    functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_ZH_{args.type}_{args.flavor}.root", args, norm=True, lumi=7200000)
