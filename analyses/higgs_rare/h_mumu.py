
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


# define histograms

bins_m = (250, 0, 250)
bins_p = (200, 0, 200)
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
bins_aco = (1000,-360,360)
bins_cosThetaMiss = (10000, 0, 1)



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


    #########
    ### CUT 0: all events
    #########
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    #########
    ### CUT 1: at least 2 muons
    #########
    df = df.Filter("muons_no >= 2")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    #########
    ### CUT 2 :at least one resonance from OS leptons
    #########

    # build the H resonance based on the available muons. Returns the best muon pair compatible with the H mass and recoil at 91 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system (H), index and 2 the leptons of the pair
    df = df.Define("hbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(125, 91.2, 0, 240, false)(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    
    df = df.Filter("hbuilder_result.size() > 0")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    df = df.Define("hmumu", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[0]}") # the H
    df = df.Define("hmumu_leps", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{hbuilder_result[1],hbuilder_result[2]}") # the muons
    df = df.Define("hmumu_m", "FCCAnalyses::ReconstructedParticle::get_mass(hmumu)[0]")
    df = df.Define("hmumu_p", "FCCAnalyses::ReconstructedParticle::get_p(hmumu)[0]")
    df = df.Define("hmumu_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(hmumu)")
    df = df.Define("hmumu_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(hmumu_recoil)[0]")



    #########
    ### CUT 3: recoil cut (Z mass)
    #########  
    results.append(df.Histo1D(("mumu_recoil_m_nOne", "", *bins_m), "hmumu_recoil_m"))
    df = df.Filter("hmumu_recoil_m > 80 && hmumu_recoil_m < 120") # 86, 114
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut3"))

    #####
    ### CUT 4: momentum
    #####
    results.append(df.Histo1D(("mumu_p_nOne", "", *bins_p), "hmumu_p"))
    df = df.Filter("hmumu_p > 20 && hmumu_p < 65")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut4"))


    ####
    ## CUT 5: cos theta(miss)
    ####
    df = df.Define("missingEnergy_rp", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("missingEnergy", "missingEnergy_rp[0].energy")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy_rp)")
    results.append(df.Histo1D(("cosThetaMiss_nOne", "", *bins_cosThetaMiss), "cosTheta_miss"))
    df = df.Filter("cosTheta_miss < 0.98")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut5"))


    ####
    ## CUT 6: missing energy
    ####
    results.append(df.Histo1D(("missingEnergy_nOne", "", *bins_m), "missingEnergy"))
    df = df.Filter("missingEnergy < 115 && (missingEnergy > 95 || missingEnergy < 30 )")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    #########
    ### CUT 7 :cut on Higgs mass
    #########
    results.append(df.Histo1D(("hmumu_m_nOne", "", *bins_m), "hmumu_m"))
    df = df.Filter("hmumu_m > 110 && hmumu_m < 130")
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut7"))


    results.append(df.Histo1D(("hmumu_m_nocat", "", *bins_m_zoom), "hmumu_m"))


    ##### CATEGORIZATION: based on #muons, # electrons, missing energy
    select_mumu = "muons_no == 4 && electrons_no == 0 && missingEnergy < 30"
    select_ee = "electrons_no == 2 && muons_no == 2 && missingEnergy < 30"
    select_nunu = "electrons_no == 0 && muons_no == 2 && missingEnergy > 95"
    select_qq = f"! ( ({select_mumu}) || ({select_ee}) || ({select_nunu}) )"


    #######
    # qq final state
    #######
    df_qq = df.Filter(select_qq)
    results.append(df_qq.Histo1D(("cutFlow", "", *bins_count), "cut8"))

    # define PF candidates collection by removing the muons
    df_qq = df_qq.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
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
    df_qq = df_qq.Define("dijet_m", "dijet.M()")

    results.append(df_qq.Histo1D(("zqq_jet1_p", "", *bins_p), "jet1_p"))
    results.append(df_qq.Histo1D(("zqq_jet2_p", "", *bins_p), "jet2_p"))
    results.append(df_qq.Histo1D(("zqq_m", "", *bins_m), "dijet_m"))
    results.append(df_qq.Histo1D(("zqq_hmumu_m", "", *bins_m_zoom), "hmumu_m"))


    #######
    # nunu final state
    #######
    df_nunu = df.Filter(select_nunu)
    results.append(df_nunu.Histo1D(("cutFlow", "", *bins_count), "cut9"))
    results.append(df_nunu.Histo1D(("znunu_hmumu_m", "", *bins_m_zoom), "hmumu_m"))

    #######
    # mumu final state
    #######
    df_mumu = df.Filter(select_mumu)
    results.append(df_mumu.Histo1D(("cutFlow", "", *bins_count), "cut10"))

    df_mumu = df_mumu.Define("muons_zmumu", "FCCAnalyses::ReconstructedParticle::remove(muons, hmumu_leps)")
    df_mumu = df_mumu.Define("muons_tlv", "FCCAnalyses::makeLorentzVectors(muons_zmumu)")
    df_mumu = df_mumu.Define("muon1_p", "muons_tlv[0].P()")
    df_mumu = df_mumu.Define("muon2_p", "muons_tlv[1].P()")
    df_mumu = df_mumu.Define("dimuon", "muons_tlv[0]+muons_tlv[1]")
    df_mumu = df_mumu.Define("dimuon_m", "dimuon.M()")

    results.append(df_mumu.Histo1D(("zmumu_muon1_p", "", *bins_p), "muon1_p"))
    results.append(df_mumu.Histo1D(("zmumu_muon2_p", "", *bins_p), "muon2_p"))
    results.append(df_mumu.Histo1D(("zmumu_m", "", *bins_m), "dimuon_m"))
    results.append(df_mumu.Histo1D(("zmumu_hmumu_m", "", *bins_m_zoom), "hmumu_m"))

    #######
    # ee final state
    #######
    df_ee = df.Filter(select_ee)
    results.append(df_ee.Histo1D(("cutFlow", "", *bins_count), "cut11"))

    df_ee = df_ee.Define("electrons_tlv", "FCCAnalyses::makeLorentzVectors(electrons)")
    df_ee = df_ee.Define("electron1_p", "electrons_tlv[0].P()")
    df_ee = df_ee.Define("electron2_p", "electrons_tlv[1].P()")
    df_ee = df_ee.Define("dielectron", "electrons_tlv[0]+electrons_tlv[1]")
    df_ee = df_ee.Define("dielectron_m", "dielectron.M()")

    results.append(df_ee.Histo1D(("zee_electron1_p", "", *bins_p), "electron1_p"))
    results.append(df_ee.Histo1D(("zee_electron2_p", "", *bins_p), "electron2_p"))
    results.append(df_ee.Histo1D(("zee_m", "", *bins_m), "dielectron_m"))
    results.append(df_ee.Histo1D(("zee_hmumu_m", "", *bins_m_zoom), "hmumu_m"))


    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_sig = ["wzp6_ee_nunuH_Hmumu_ecm240", "wzp6_ee_eeH_Hmumu_ecm240", "wzp6_ee_tautauH_Hmumu_ecm240", "wzp6_ee_ccH_Hmumu_ecm240", "wzp6_ee_bbH_Hmumu_ecm240", "wzp6_ee_qqH_Hmumu_ecm240", "wzp6_ee_ssH_Hmumu_ecm240", "wzp6_ee_mumuH_Hmumu_ecm240"]
    datasets_bkg = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240", "wzp6_ee_mumu_ecm240", "wzp6_ee_tautau_ecm240", "wzp6_egamma_eZ_Zmumu_ecm240", "wzp6_gammae_eZ_Zmumu_ecm240", "wzp6_gaga_mumu_60_ecm240", "wzp6_gaga_tautau_60_ecm240", "wzp6_ee_nuenueZ_ecm240"]

    datasets_to_run = datasets_sig + datasets_bkg
    #datasets_to_run = ["wzp6_ee_mumuH_Hmumu_ecm240"]
    result = functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_h_mumu.root", args, norm=True, lumi=7200000)
