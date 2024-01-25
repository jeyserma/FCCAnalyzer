
import functions
import helpers
import ROOT
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/higgs_mass_xsec/functions.h")
functions.add_include_file("analyses/higgs_mass_xsec/functions_gen.h")
functions.add_include_file("analyses/higgs_rare/functions.h")

# define histograms

bins_m = (250, 0, 250) # 100 MeV bins
bins_p = (200, 0, 200) # 100 MeV bins
bins_m_zoom = (200, 110, 130) # 100 MeV

bins_theta = (500, 0, 5)
bins_phi = (400, -4, 4)

bins_count = (100, 0, 100)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

bins_resolution = (10000, 0.95, 1.05)
bins_resolution_1 = (20000, 0, 2)

jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins

bins_cos = (100, -1, 1)
bins_cos_abs = (100, 0, 1)
bins_iso = (1000, 0, 10)
bins_aco = (1000,0,1)
bins_cosThetaMiss = (10000, 0, 1)

bins_m_fine = (500, 110, 130) # 100 MeV bins


def build_graph(df, dataset):

    logging.info(f"build graph {dataset.name}")
    results, cols = [], []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    df = helpers.defineCutFlowVars(df) # make the cutX=X variables
    
    # define collections
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # photons
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(photons_all)")
    df = df.Define("photons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons_all)")
    df = df.Define("photons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(photons_all)")

    df = df.Define("photons_all_costheta", "FCCAnalyses::Vec_f ret; for(auto & theta: photons_all_theta) ret.push_back(std::abs(cos(theta))); return ret;")
    
    results.append(df.Histo1D(("photons_all_p", "", *bins_p), "photons_all_p"))
    results.append(df.Histo1D(("photons_all_theta", "", *bins_theta), "photons_all_theta"))
    results.append(df.Histo1D(("photons_all_costheta", "", *bins_cos_abs), "photons_all_costheta"))


    df = df.Define("photons_sel_p", "FCCAnalyses::sel_range(40, 100, false)(photons_all, photons_all_p)")
    df = df.Define("photons_sel_p_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons_sel_p)")
    df = df.Define("photons_sel_p_costheta", "FCCAnalyses::Vec_f ret; for(auto & theta: photons_sel_p_theta) ret.push_back(std::abs(cos(theta))); return ret;")
    results.append(df.Histo1D(("photons_sel_p_theta", "", *bins_theta), "photons_all_theta"))
    results.append(df.Histo1D(("photons_sel_p_costheta", "", *bins_cos_abs), "photons_all_costheta"))
    
    df = df.Define("photons_sel_cost", "FCCAnalyses::sel_range(0, 0.9, false)(photons_sel_p, photons_sel_p_costheta)")
    df = df.Alias("photons", "photons_sel_cost")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_n", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
    df = df.Define("photons_costheta", "FCCAnalyses::Vec_f ret; for(auto & theta: photons_theta) ret.push_back(std::abs(cos(theta))); return ret;")

    df = df.Define("photon_leading_p", "photons_p[0]")
    df = df.Define("photon_leading_costheta", "photons_costheta[0]")

    # muons
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    df = df.Define("muons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_all)")
    df = df.Define("muons_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons_all)")
    df = df.Define("muons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
    df = df.Define("muons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")

    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")

    
    # electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    df = df.Define("electrons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons_all)")
    df = df.Define("electrons_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons_all)")
    df = df.Define("electrons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_all)")
    df = df.Define("electrons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_all)")

    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(electrons_all)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")


    # lepton kinematic histograms
    results.append(df.Histo1D(("muons_all_p_cut0", "", *bins_p), "muons_all_p"))
    results.append(df.Histo1D(("muons_all_theta_cut0", "", *bins_theta), "muons_all_theta"))
    results.append(df.Histo1D(("muons_all_phi_cut0", "", *bins_phi), "muons_all_phi"))
    results.append(df.Histo1D(("muons_all_q_cut0", "", *bins_charge), "muons_all_q"))
    results.append(df.Histo1D(("muons_all_no_cut0", "", *bins_count), "muons_all_no"))

    results.append(df.Histo1D(("electrons_all_p_cut0", "", *bins_p), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_all_theta_cut0", "", *bins_theta), "electrons_all_theta"))
    results.append(df.Histo1D(("electrons_all_phi_cut0", "", *bins_phi), "electrons_all_phi"))
    results.append(df.Histo1D(("electrons_all_q_cut0", "", *bins_charge), "electrons_all_q"))
    results.append(df.Histo1D(("electrons_all_no_cut0", "", *bins_count), "electrons_all_no"))

    results.append(df.Histo1D(("photons_p", "", *bins_p), "photons_p"))
    results.append(df.Histo1D(("photons_n", "", *bins_count), "photons_n"))
    results.append(df.Histo1D(("photon_leading_costheta", "", *bins_cosThetaMiss), "photon_leading_costheta"))
    results.append(df.Histo1D(("photon_leading_p", "", *bins_p), "photon_leading_p"))

    #########
    ### CUT 0: all events
    #########
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))


    #########
    ### CUT 1: at least 1 photon
    #########
    results.append(df.Histo1D(("photons_n_nOne", "", *bins_count), "photons_n"))
    df = df.Filter("photons_n >= 1")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))


    #########
    ### CUT 2: at least 2 photons
    #########
    df = df.Filter("photons_n >= 2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))


    #########
    ### CUT 3 :at least one resonance
    #########

    # build the H resonance based on the available muons. Returns the best muon pair compatible with the H mass and recoil at 91 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system (H), index and 2 the leptons of the pair
    df = df.Define("hbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(125, 91.2, 0.5, 240, false)(photons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    
    df = df.Filter("hbuilder_result.size() > 0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    
    df = df.Define("haa", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[0]}") # the H
    df = df.Define("haa_photons", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[1],hbuilder_result[2]}") # the photons
    df = df.Define("haa_m", "FCCAnalyses::ReconstructedParticle::get_mass(haa)[0]")
    df = df.Define("haa_p", "FCCAnalyses::ReconstructedParticle::get_p(haa)[0]")
    df = df.Define("haa_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(haa)")
    df = df.Define("haa_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(haa_recoil)[0]")


    #########
    ### CUT 4: recoil cut (Z mass)
    #########  
    results.append(df.Histo1D(("haa_recoil_m_nOne", "", *bins_m), "haa_recoil_m"))
    df = df.Filter("haa_recoil_m > 80 && haa_recoil_m < 120")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    #####
    ### CUT 5: momentum
    #####
    results.append(df.Histo1D(("haa_p_nOne", "", *bins_p), "haa_p"))
    df = df.Filter("haa_p > 20 && haa_p < 65")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    ####
    ## CUT 6: cos theta(miss)
    ####
    df = df.Define("missingEnergy_rp", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("missingEnergy", "missingEnergy_rp[0].energy")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy_rp)")
    #results.append(df.Histo1D(("cosThetaMiss_nOne", "", *bins_cosThetaMiss), "cosTheta_miss"))
    #df = df.Filter("cosTheta_miss < .95") # 0.98
    #results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    ####
    ## CUT 6: missing energy
    ####
    results.append(df.Histo1D(("missingEnergy_nOne", "", *bins_m), "missingEnergy"))
    df = df.Filter("missingEnergy < 115 && (missingEnergy > 95 || missingEnergy < 30 )")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    #########
    ### CUT 7 :cut on Higgs mass
    #########
    results.append(df.Histo1D(("haa_m_nOne", "", *bins_m), "haa_m"))
    df = df.Filter("haa_m > 110 && haa_m < 130")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut7"))



    df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(haa_photons)")
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(haa_photons)")
    results.append(df.Histo1D(("acoplanarity", "", *bins_aco), "acoplanarity"))
    results.append(df.Histo1D(("acolinearity", "", *bins_aco), "acolinearity"))
    results.append(df.Histo1D(("haa_m", "", *bins_m_zoom), "haa_m"))


    ##### CATEGORIZATION: based on #muons, # electrons, missing energy
    select_mumu = "muons_no == 2 && electrons_no == 0 && missingEnergy < 30"
    select_ee = "electrons_no == 2 && muons_no == 0 && missingEnergy < 30"
    select_nunu = "electrons_no == 0 && muons_no == 0 && missingEnergy > 95"
    select_qq = "electrons_no == 0 && muons_no == 0 && missingEnergy < 30"





    #######
    # qq final state
    #######
    df_qq = df.Filter(select_qq)
    results.append(df_qq.Histo1D(("cutFlow", "", *bins_count), "cut8"))
    
    results.append(df_qq.Histo1D(("zqq_photons_p", "", *bins_p), "photons_p"))
    results.append(df_qq.Histo1D(("zqq_photon_leading_costheta", "", *bins_cosThetaMiss), "photon_leading_costheta"))
    results.append(df_qq.Histo1D(("zqq_photons_costheta", "", *bins_cosThetaMiss), "photons_costheta"))
    results.append(df_qq.Histo1D(("zqq_photon_leading_p", "", *bins_p), "photon_leading_p"))

    # define PF candidates collection by removing the muons
    df_qq = df_qq.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, photons)")
    df_qq = df_qq.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons)")
    df_qq = df_qq.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons)")
    df_qq = df_qq.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons)")
    df_qq = df_qq.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons)")
    df_qq = df_qq.Define("RP_m", "FCCAnalyses::ReconstructedParticle::get_mass(rps_no_muons)")
    df_qq = df_qq.Define("RP_q", "FCCAnalyses::ReconstructedParticle::get_charge(rps_no_muons)")
    df_qq = df_qq.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    df_qq = df_qq.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
    df_qq = df_qq.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df_qq = df_qq.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df_qq = df_qq.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df_qq = df_qq.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df_qq = df_qq.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df_qq = df_qq.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df_qq = df_qq.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df_qq = df_qq.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df_qq = df_qq.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df_qq = df_qq.Define("jet1_p", "jet1.P()")
    df_qq = df_qq.Define("jet2_p", "jet2.P()")
    df_qq = df_qq.Define("dijet", "jet1+jet2")
    df_qq = df_qq.Define("dijet_tlv", "TLorentzVector ret; ret.SetPxPyPzE(dijet.Px(), dijet.Py(), dijet.Pz(), dijet.E()); return ret;")
    df_qq = df_qq.Define("dijet_m", "dijet.M()")
    df_qq = df_qq.Define("dijet_p", "dijet.P()")
    
    
    results.append(df_qq.Histo1D(("zqq_qq_p_nOne", "", *bins_p), "dijet_p"))
    df_qq = df_qq.Filter("dijet_p > 20 && dijet_p < 65")

    results.append(df_qq.Histo1D(("zqq_m_nOne", "", *bins_m), "dijet_m"))
    df_qq = df_qq.Filter("dijet_m < 105 && dijet_m > 80")

    results.append(df_qq.Histo1D(("zqq_m", "", *bins_m), "dijet_m"))
    results.append(df_qq.Histo1D(("zqq_haa_m", "", *bins_m_zoom), "haa_m"))
    results.append(df_qq.Histo1D(("zqq_aa_p", "", *bins_p), "haa_p"))
    results.append(df_qq.Histo1D(("zqq_qq_p", "", *bins_p), "dijet_p"))

    results.append(df_qq.Histo1D(("zqq_acoplanarity", "", *bins_aco), "acoplanarity"))
    results.append(df_qq.Histo1D(("zqq_acolinearity", "", *bins_aco), "acolinearity"))
    results.append(df_qq.Histo1D(("zqq_cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))

    #######
    # nunu final state
    #######
    df_nunu = df.Filter(select_nunu)
    results.append(df_nunu.Histo1D(("cutFlow", "", *bins_count), "cut9"))
    results.append(df_nunu.Histo1D(("znunu_haa_m", "", *bins_m_zoom), "haa_m"))


    #######
    # mumu final state
    #######
    df_mumu = df.Filter(select_mumu)
    results.append(df_mumu.Histo1D(("cutFlow", "", *bins_count), "cut10"))

    df_mumu = df_mumu.Define("muons_tlv", "FCCAnalyses::makeLorentzVectors(muons)")
    df_mumu = df_mumu.Define("dimuon", "muons_tlv[0]+muons_tlv[1]")
    df_mumu = df_mumu.Define("dimuon_m", "dimuon.M()")

    results.append(df_mumu.Histo1D(("zmumu_m_nOne", "", *bins_m), "dimuon_m"))
    df_mumu = df_mumu.Filter("dimuon_m > 80 && dimuon_m < 100")
    results.append(df_mumu.Histo1D(("zmumu_m", "", *bins_m), "dimuon_m"))
    results.append(df_mumu.Histo1D(("zmumu_haa_m", "", *bins_m_zoom), "haa_m"))

    #######
    # ee final state
    #######
    df_ee = df.Filter(select_ee)
    results.append(df_ee.Histo1D(("cutFlow", "", *bins_count), "cut11"))

    df_ee = df_ee.Define("electrons_tlv", "FCCAnalyses::makeLorentzVectors(electrons)")
    df_ee = df_ee.Define("dielectron", "electrons_tlv[0]+electrons_tlv[1]")
    df_ee = df_ee.Define("dielectron_m", "dielectron.M()")

    results.append(df_ee.Histo1D(("zee_m_nOne", "", *bins_m), "dielectron_m"))
    df_ee = df_ee.Filter("dielectron_m > 80 && dielectron_m < 100")
    results.append(df_ee.Histo1D(("zee_m", "", *bins_m), "dielectron_m"))
    results.append(df_ee.Histo1D(("zee_haa_m", "", *bins_m_zoom), "haa_m"))


    return results, weightsum



if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_sig = ["wzp6_ee_nunuH_Haa_ecm240", "wzp6_ee_eeH_Haa_ecm240", "wzp6_ee_tautauH_Haa_ecm240", "wzp6_ee_ccH_Haa_ecm240", "wzp6_ee_bbH_Haa_ecm240", "wzp6_ee_qqH_Haa_ecm240", "wzp6_ee_ssH_Haa_ecm240", "wzp6_ee_mumuH_Haa_ecm240"]
    datasets_bkg = ["wzp6_ee_gammagamma_ecm240", "kkmcee_ee_uu_ecm240", "kkmcee_ee_dd_ecm240", "kkmcee_ee_cc_ecm240", "kkmcee_ee_ss_ecm240", "kkmcee_ee_bb_ecm240"]


    datasets_to_run = datasets_sig + datasets_bkg
    result = functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_h_aa.root", args, norm=True, lumi=7200000)
