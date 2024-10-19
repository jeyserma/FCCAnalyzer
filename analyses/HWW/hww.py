
import functions
import helper_tmva
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
functions.add_include_file("analyses/HWW/functions.h")


# define histograms

bins_def = (250, 0, 250) # default 1 GeV binning
bins_p = (250, 0, 250)
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
bins_aco = (1000,0,1)
bins_cosThetaMiss = (10000, 0, 1)

bins_dR = (1000, 0, 10)
bins_merge = (1500, 0, 15000)



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
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("muons_tlv", "FCCAnalyses::makeLorentzVectors(muons)")


    # electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons)")
    df = df.Define("electrons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(electrons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")
    df = df.Define("electrons_tlv", "FCCAnalyses::makeLorentzVectors(electrons)")

    # missing energy (representing neutrinos)
    df = df.Define("missingEnergy_rp", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("missingEnergy_rp_tlv", "FCCAnalyses::makeLorentzVectors(missingEnergy_rp)")
    df = df.Define("missingEnergy", "missingEnergy_rp[0].energy")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy_rp)")
    results.append(df.Histo1D(("missingEnergy_noCut", "", *bins_def), "missingEnergy"))
    results.append(df.Histo1D(("cosThetaMiss_noCut", "", *bins_cosThetaMiss), "cosTheta_miss"))


    # lepton kinematic histograms
    results.append(df.Histo1D(("muons_p_noCut", "", *bins_def), "muons_p"))
    results.append(df.Histo1D(("muons_theta_noCut", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi_noCut", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_q_noCut", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no_noCut", "", *bins_count), "muons_no"))


    results.append(df.Histo1D(("electrons_p_noCut", "", *bins_def), "electrons_p"))
    results.append(df.Histo1D(("electrons_theta_noCut", "", *bins_theta), "electrons_theta"))
    results.append(df.Histo1D(("electrons_phi_noCut", "", *bins_phi), "electrons_phi"))
    results.append(df.Histo1D(("electrons_q_noCut", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no_noCut", "", *bins_count), "electrons_no"))


    # gen-level study: select only muonic W decays and check their kinematics
    doGEN = False
    if doGEN:
        if "wzp6_ee" in dataset.name:
            df = df.Filter("FCCAnalyses::W_muonic_decays(Particle, Particle0, Particle1)")

        filter_qq_mumu = "muons_no == 2 && electrons_no ==0 && (muons_q[0]+muons_q[1]) == 0" # 2 opposite sign muons
        df_qq_mumu = df.Filter(filter_qq_mumu)

        df_qq_mumu = df_qq_mumu.Define("leading_muon", "muons_p[0]")
        df_qq_mumu = df_qq_mumu.Define("subleading_muon", "muons_p[1]")
        
        results.append(df_qq_mumu.Histo1D(("qq_mumu_muons_p", "", *bins_def), "muons_p"))
        results.append(df_qq_mumu.Histo1D(("qq_mumu_leading_muon_p", "", *bins_def), "leading_muon"))
        results.append(df_qq_mumu.Histo1D(("qq_mumu_subleading_muon_p", "", *bins_def), "subleading_muon"))

        return results, weightsum

    if "wzp6_ee" in dataset.name:
        df = df.Filter("FCCAnalyses::W_muonic_decays(Particle, Particle0, Particle1)")


    ######################
    # Z(qq) W(munu)W(munu)
    ######################
    results.append(df.Histo1D(("cutFlow", "", *bins_count), "cut0"))

    filter_qq_mumu = "muons_no == 2 && electrons_no == 0 && (muons_q[0]+muons_q[1]) == 0" # 2 opposite sign muons
    df_qq_mumu = df.Filter(filter_qq_mumu)
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut1"))

    # cut on leading and subleading muon momentum
    df_qq_mumu = df_qq_mumu.Filter("muons_p[0] > 15 && muons_p[0] < 80 && muons_p[1] > 5 && muons_p[1] < 60")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut2"))

    # cut on missing energy
    results.append(df_qq_mumu.Histo1D(("qq_mumu_missingEnergy_pre", "", *bins_def), "missingEnergy"))
    df_qq_mumu = df_qq_mumu.Filter("missingEnergy < 110 && missingEnergy > 30")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut3"))
    
    # cut on cos theta of missing energy
    results.append(df_qq_mumu.Histo1D(("qq_mumu_cosThetaMiss_pre", "", *bins_cosThetaMiss), "cosTheta_miss"))
    df_qq_mumu = df_qq_mumu.Filter("cosTheta_miss < 0.99")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut4"))

    # cut on dimuon mass
    df_qq_mumu = df_qq_mumu.Define("dimuon", "muons_tlv[0] + muons_tlv[1]")
    df_qq_mumu = df_qq_mumu.Define("dimuon_m", "dimuon.M()")
    df_qq_mumu = df_qq_mumu.Define("dimuon_p", "dimuon.P()")
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dimuon_m_pre", "", *bins_def), "dimuon_m"))
    df_qq_mumu = df_qq_mumu.Filter("dimuon_m < 80")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut5"))

    # cut on dimuon momentum
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dimuon_p_pre", "", *bins_def), "dimuon_p"))
    df_qq_mumu = df_qq_mumu.Filter("dimuon_p < 90")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut6"))


    # do jet clustering on remaining particles

    # define PF candidates collection by removing the muons
    df_qq_mumu = df_qq_mumu.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_m", "FCCAnalyses::ReconstructedParticle::get_mass(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("RP_q", "FCCAnalyses::ReconstructedParticle::get_charge(rps_no_muons)")
    df_qq_mumu = df_qq_mumu.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    df_qq_mumu = df_qq_mumu.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
    df_qq_mumu = df_qq_mumu.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df_qq_mumu = df_qq_mumu.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")

    df_qq_mumu = df_qq_mumu.Filter("jetconstituents.size() == 2")
    df_qq_mumu = df_qq_mumu.Define("jetconstituents1", "jetconstituents[0].size()")
    df_qq_mumu = df_qq_mumu.Define("jetconstituents2", "jetconstituents[1].size()")

    # average: 
    df_qq_mumu = df_qq_mumu.Define("jetconstituents_avg", "(jetconstituents1+jetconstituents2)/2")
        
        
    results.append(df_qq_mumu.Histo1D(("jetconstituents1", "", *bins_def), "jetconstituents1"))
    results.append(df_qq_mumu.Histo1D(("jetconstituents2", "", *bins_def), "jetconstituents2"))
    results.append(df_qq_mumu.Histo1D(("jetconstituents_avg", "", *bins_def), "jetconstituents_avg"))
    
    # average: 
    #df_qq_mumu = df_qq_mumu.Define("jetconstituents_avg", "(jetconstituents[0]+jetconstituents[1])/2")

    df_qq_mumu = df_qq_mumu.Define("dmerge_01", "FCCAnalyses::JetClusteringUtils::get_exclusive_dmerge(clustered_jets, 0)")
    df_qq_mumu = df_qq_mumu.Define("dmerge_12", "FCCAnalyses::JetClusteringUtils::get_exclusive_dmerge(clustered_jets, 1)")
    df_qq_mumu = df_qq_mumu.Define("dmerge_23", "FCCAnalyses::JetClusteringUtils::get_exclusive_dmerge(clustered_jets, 2)")
    results.append(df_qq_mumu.Histo1D(("dmerge_01", "", *bins_merge), "dmerge_01"))
    results.append(df_qq_mumu.Histo1D(("dmerge_12", "", *bins_merge), "dmerge_12"))
    results.append(df_qq_mumu.Histo1D(("dmerge_23", "", *bins_merge), "dmerge_23"))

    df_qq_mumu = df_qq_mumu.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df_qq_mumu = df_qq_mumu.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df_qq_mumu = df_qq_mumu.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df_qq_mumu = df_qq_mumu.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df_qq_mumu = df_qq_mumu.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df_qq_mumu = df_qq_mumu.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df_qq_mumu = df_qq_mumu.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df_qq_mumu = df_qq_mumu.Define("jet1_p", "jet1.P()")
    df_qq_mumu = df_qq_mumu.Define("jet2_p", "jet2.P()")
    df_qq_mumu = df_qq_mumu.Define("dijet", "jet1+jet2")
    df_qq_mumu = df_qq_mumu.Define("dijet_tlv", "TLorentzVector ret; ret.SetPxPyPzE(dijet.Px(), dijet.Py(), dijet.Pz(), dijet.E()); return ret;")
    df_qq_mumu = df_qq_mumu.Define("dijet_m", "dijet.M()")
    df_qq_mumu = df_qq_mumu.Define("dijet_p", "dijet.P()")

    # compute recoil
    df_qq_mumu = df_qq_mumu.Define("recoil_p4", "TLorentzVector ret; ret.SetPxPyPzE(0, 0, 0, 240); ret = ret - dijet_tlv; return ret;")
    df_qq_mumu = df_qq_mumu.Define("recoil_p4_m", "recoil_p4.M()")


    # cut on jet momenta
    results.append(df_qq_mumu.Histo1D(("qq_mumu_jet1_p_pre", "", *bins_def), "jet1_p"))
    results.append(df_qq_mumu.Histo1D(("qq_mumu_jet2_p_pre", "", *bins_def), "jet2_p"))
    df_qq_mumu = df_qq_mumu.Filter("jet1_p < 80 && jet1_p > 30 && jet2_p < 60 && jet2_p > 10")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut7"))

    # cut on dijet mass
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dijet_m_pre", "", *bins_def), "dijet_m"))
    df_qq_mumu = df_qq_mumu.Filter("dijet_m < 130 && dijet_m > 60")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut8"))

    # cut on dijet momentum
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dijet_p_pre", "", *bins_def), "dijet_p"))
    df_qq_mumu = df_qq_mumu.Filter("dijet_p < 70 && dijet_p > 0")
    results.append(df_qq_mumu.Histo1D(("cutFlow", "", *bins_count), "cut9"))

    # cut on recoil
    results.append(df_qq_mumu.Histo1D(("qq_mumu_recoil_m_pre", "", *bins_def), "recoil_p4_m"))


    #### extra variables to cut on -- to be investigated
    # form Higgs candidate
    df_qq_mumu = df_qq_mumu.Define("higgs_cand", "missingEnergy_rp_tlv[0] + muons_tlv[0] + muons_tlv[1]")
    df_qq_mumu = df_qq_mumu.Define("higgs_cand_m", "higgs_cand.M()")
    df_qq_mumu = df_qq_mumu.Define("higgs_cand_p", "higgs_cand.P()")
    results.append(df_qq_mumu.Histo1D(("higgs_cand_m", "", *bins_def), "higgs_cand_m"))
    results.append(df_qq_mumu.Histo1D(("higgs_cand_p", "", *bins_def), "higgs_cand_p"))


    # angular cuts
    df_qq_mumu = df_qq_mumu.Define("dijet_dr", "std::hypot(jet1.Eta() - jet2.Eta(), jet1.Phi() - jet2.Phi())")
    df_qq_mumu = df_qq_mumu.Define("dimuon_dr", "std::hypot(muons_tlv[0].Eta() - muons_tlv[1].Eta(), muons_tlv[0].Phi() - muons_tlv[1].Phi())")
    df_qq_mumu = df_qq_mumu.Define("dimuon_dijet_dr", "std::hypot(dijet.Eta() - dimuon.Eta(), dijet.Phi() - dimuon.Phi())")

    results.append(df_qq_mumu.Histo1D(("qq_mumu_dijet_dr_pre", "", *bins_dR), "dijet_dr"))
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dimuon_dr_pre", "", *bins_dR), "dimuon_dr"))
    results.append(df_qq_mumu.Histo1D(("qq_mumu_dimuon_dijet_dr_pre", "", *bins_dR), "dimuon_dijet_dr"))


    return results, weightsum



if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_sig = ["wzp6_ee_mumuH_HWW_ecm240", "wzp6_ee_ssH_HWW_ecm240", "wzp6_ee_eeH_HWW_ecm240", "wzp6_ee_bbH_HWW_ecm240", "wzp6_ee_ccH_HWW_ecm240", "wzp6_ee_nunuH_HWW_ecm240", "wzp6_ee_qqH_HWW_ecm240", "wzp6_ee_tautauH_HWW_ecm240"]

    datasets_bkg = ["p8_ee_WW_ecm240", "p8_ee_ZZ_ecm240"]
    #datasets_bkg = []

    datasets_to_run = datasets_sig + datasets_bkg
    #datasets_to_run = ["wzp6_ee_nunuH_HWW_ecm240"]
    functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_HWW.root", args, norm=True, lumi=10800000)
