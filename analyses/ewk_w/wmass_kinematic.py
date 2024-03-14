
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
functions.add_include_file("include/yfsww.h")
functions.add_include_file("include/breit_wigner_weights.h")

# define histograms

bins_m = (250, 0, 250)
bins_wmass = (120, 50, 110)
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
bins_aco = (1000,0,1)
bins_cosTheta = (10000, 0, 1)

bins_dR = (1000, 0, 10)


def build_graph(df, dataset):

    logging.info(f"build graph {dataset.name}")
    results, cols = [], []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Define("ECM", "163") # parse from sample name

    # define collections
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # muons
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    df = df.Define("muons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
    df = df.Define("muons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")

    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(muons_all)")
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")


    # electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    df = df.Define("electrons_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_all)")
    df = df.Define("electrons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_all)")

    df = df.Define("electrons", "FCCAnalyses::ReconstructedParticle::sel_p(25)(electrons_all)")
    df = df.Define("electrons_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons)")
    df = df.Define("electrons_q", "FCCAnalyses::ReconstructedParticle::get_charge(electrons)")
    df = df.Define("electrons_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons)")

    # photons
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(photons_all)")
    df = df.Define("photons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(photons_all)")
    df = df.Define("photons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons_all)")
    df = df.Define("photons_all_costheta", "FCCAnalyses::Vec_f ret; for(auto & theta: photons_all_theta) ret.push_back(std::abs(cos(theta))); return ret;")
    df = df.Define("photon_leading_p", "photons_all_p[0]")
    df = df.Define("photon_leading_costheta", "photons_all_costheta[0]")

    # missing energy
    df = df.Define("missingEnergy_rp", "FCCAnalyses::missingEnergy(ECM, ReconstructedParticles)")
    df = df.Define("missingEnergy_rp_tlv", "FCCAnalyses::makeLorentzVectors(missingEnergy_rp)")
    df = df.Define("missingEnergy", "missingEnergy_rp[0].energy")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy_rp)")
    




    # baseline plots
    results.append(df.Histo1D(("muons_all_p", "", *bins_p), "muons_all_p"))
    results.append(df.Histo1D(("muons_all_q", "", *bins_charge), "muons_all_q"))
    results.append(df.Histo1D(("muons_all_no", "", *bins_count), "muons_all_no"))

    results.append(df.Histo1D(("electrons_all_p", "", *bins_p), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_all_q", "", *bins_charge), "electrons_all_q"))
    results.append(df.Histo1D(("electrons_all_no", "", *bins_count), "electrons_all_no"))

    results.append(df.Histo1D(("muons_p", "", *bins_p), "muons_p"))
    results.append(df.Histo1D(("muons_q", "", *bins_charge), "muons_q"))
    results.append(df.Histo1D(("muons_no", "", *bins_count), "muons_no"))

    results.append(df.Histo1D(("electrons_p", "", *bins_p), "electrons_p"))
    results.append(df.Histo1D(("electrons_q", "", *bins_charge), "electrons_q"))
    results.append(df.Histo1D(("electrons_no", "", *bins_count), "electrons_no"))

    results.append(df.Histo1D(("photons_all_p", "", *bins_p), "photons_all_p"))
    results.append(df.Histo1D(("photons_all_costheta", "", *bins_cosTheta), "photons_all_costheta"))
    results.append(df.Histo1D(("photons_all_no", "", *bins_count), "photons_all_no"))
    results.append(df.Histo1D(("photon_leading_p", "", *bins_p), "photon_leading_p"))
    results.append(df.Histo1D(("photon_leading_costheta", "", *bins_cosTheta), "photon_leading_costheta"))

    results.append(df.Histo1D(("missingEnergy", "", *bins_m), "missingEnergy"))
    results.append(df.Histo1D(("cosTheta_miss", "", *bins_cosTheta), "cosTheta_miss"))

    # gen level
    df = df.Define("w_decay_mode", "FCCAnalyses::yfsww_w_decay_mode(Particle, Particle1)")
    results.append(df.Histo1D(("w_decay_mode", "", *(50, -25, 25)), "w_decay_mode"))

    df = df.Define("w_decay_idxs", "FCCAnalyses::yfsww_w_idxs(Particle, Particle1)")
    df = df.Define("w_plus", "Particle[w_decay_idxs[0]]")
    df = df.Define("w_minus", "Particle[w_decay_idxs[1]]")
    df = df.Define("w_plus_m", "w_plus.mass")
    df = df.Define("w_minus_m", "w_minus.mass")

    df = df.Define("weight_plus_50MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, 50)")
    df = df.Define("weight_minus_50MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, -50)")
    df = df.Define("weight_plus_10MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, 10)")
    df = df.Define("weight_minus_10MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, -10)")

    results.append(df.Histo1D(("w_plus_m", "", *(200, 70, 90)), "w_plus_m"))
    results.append(df.Histo1D(("w_minus_m", "", *(200, 70, 90)), "w_minus_m"))
    results.append(df.Histo2D(("w_plus_minus_m", "", *(200, 70, 90, 200, 70, 90)), "w_plus_m", "w_minus_m")) # 2D mass correlation plot

    results.append(df.Histo1D(("weight_plus_10MeV", "", *(20000, 0, 2)), "weight_plus_10MeV"))
    results.append(df.Histo1D(("weight_minus_10MeV", "", *(20000, 0, 2)), "weight_minus_10MeV"))

    results.append(df.Histo1D(("w_plus_m_plus_10MeV", "", *(200, 70, 90)), "w_plus_m", "weight_plus_10MeV"))
    results.append(df.Histo1D(("w_minus_m_plus_10MeV", "", *(200, 70, 90)), "w_minus_m", "weight_plus_10MeV"))

    results.append(df.Histo1D(("w_plus_m_minus_10MeV", "", *(200, 70, 90)), "w_plus_m", "weight_minus_10MeV"))
    results.append(df.Histo1D(("w_minus_m_minus_10MeV", "", *(200, 70, 90)), "w_minus_m", "weight_minus_10MeV"))

    results.append(df.Histo1D(("w_plus_m_plus_50MeV", "", *(200, 70, 90)), "w_plus_m", "weight_plus_50MeV"))
    results.append(df.Histo1D(("w_minus_m_plus_50MeV", "", *(200, 70, 90)), "w_minus_m", "weight_plus_50MeV"))

    results.append(df.Histo1D(("w_plus_m_minus_50MeV", "", *(200, 70, 90)), "w_plus_m", "weight_minus_50MeV"))
    results.append(df.Histo1D(("w_minus_m_minus_50MeV", "", *(200, 70, 90)), "w_minus_m", "weight_minus_50MeV"))

    # categorization

    ##############
    # munuqq
    ##############
    df_munuqq = df.Filter("muons_no == 1 && electrons_no == 0 && missingEnergy > 20")

    df_munuqq = df_munuqq.Define("rps_no_muons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, muons)")
    df_munuqq = df_munuqq.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_muons)")
    df_munuqq = df_munuqq.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_muons)")
    df_munuqq = df_munuqq.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_muons)")
    df_munuqq = df_munuqq.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_muons)")
    df_munuqq = df_munuqq.Define("RP_m", "FCCAnalyses::ReconstructedParticle::get_mass(rps_no_muons)")
    df_munuqq = df_munuqq.Define("RP_q", "FCCAnalyses::ReconstructedParticle::get_charge(rps_no_muons)")
    df_munuqq = df_munuqq.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    df_munuqq = df_munuqq.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
    df_munuqq = df_munuqq.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df_munuqq = df_munuqq.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df_munuqq = df_munuqq.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df_munuqq = df_munuqq.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df_munuqq = df_munuqq.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df_munuqq = df_munuqq.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df_munuqq = df_munuqq.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df_munuqq = df_munuqq.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df_munuqq = df_munuqq.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df_munuqq = df_munuqq.Define("jet1_p", "jet1.P()")
    df_munuqq = df_munuqq.Define("jet2_p", "jet2.P()")
    df_munuqq = df_munuqq.Define("dijet", "jet1+jet2")
    df_munuqq = df_munuqq.Define("dijet_tlv", "TLorentzVector ret; ret.SetPxPyPzE(dijet.Px(), dijet.Py(), dijet.Pz(), dijet.E()); return ret;")
    df_munuqq = df_munuqq.Define("dijet_m", "dijet.M()")
    df_munuqq = df_munuqq.Define("dijet_p", "dijet.P()")

    results.append(df_munuqq.Histo1D(("munuqq_dijet_m", "", *bins_wmass), "dijet_m"))
    results.append(df_munuqq.Histo1D(("munuqq_dijet_m_plus_50MeV", "", *bins_wmass), "dijet_m", "weight_plus_50MeV"))
    results.append(df_munuqq.Histo1D(("munuqq_dijet_m_minus_50MeV", "", *bins_wmass), "dijet_m", "weight_minus_50MeV"))


    ##############
    # enuqq
    ##############
    df_enuqq = df.Filter("muons_no == 0 && electrons_no == 1 && missingEnergy > 20")

    df_enuqq = df_enuqq.Define("rps_no_electrons", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, electrons)")
    df_enuqq = df_enuqq.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("RP_m", "FCCAnalyses::ReconstructedParticle::get_mass(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("RP_q", "FCCAnalyses::ReconstructedParticle::get_charge(rps_no_electrons)")
    df_enuqq = df_enuqq.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    df_enuqq = df_enuqq.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
    df_enuqq = df_enuqq.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df_enuqq = df_enuqq.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df_enuqq = df_enuqq.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df_enuqq = df_enuqq.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df_enuqq = df_enuqq.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df_enuqq = df_enuqq.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df_enuqq = df_enuqq.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df_enuqq = df_enuqq.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df_enuqq = df_enuqq.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df_enuqq = df_enuqq.Define("jet1_p", "jet1.P()")
    df_enuqq = df_enuqq.Define("jet2_p", "jet2.P()")
    df_enuqq = df_enuqq.Define("dijet", "jet1+jet2")
    df_enuqq = df_enuqq.Define("dijet_tlv", "TLorentzVector ret; ret.SetPxPyPzE(dijet.Px(), dijet.Py(), dijet.Pz(), dijet.E()); return ret;")
    df_enuqq = df_enuqq.Define("dijet_m", "dijet.M()")
    df_enuqq = df_enuqq.Define("dijet_p", "dijet.P()")

    results.append(df_enuqq.Histo1D(("enuqq_dijet_m", "", *bins_wmass), "dijet_m"))
    results.append(df_enuqq.Histo1D(("enuqq_dijet_m_plus_50MeV", "", *bins_wmass), "dijet_m", "weight_plus_50MeV"))
    results.append(df_enuqq.Histo1D(("enuqq_dijet_m_minus_50MeV", "", *bins_wmass), "dijet_m", "weight_minus_50MeV"))

    ##############
    # qqqq
    ##############
    df_qqqq = df.Filter("muons_no == 0 && electrons_no == 0 && missingEnergy < 20")

    df_qqqq = df_qqqq.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("RP_pz","FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("RP_e", "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("RP_m", "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("RP_q", "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df_qqqq = df_qqqq.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")

    df_qqqq = df_qqqq.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 4, 1, 0)(pseudo_jets)")
    df_qqqq = df_qqqq.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df_qqqq = df_qqqq.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df_qqqq = df_qqqq.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df_qqqq = df_qqqq.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df_qqqq = df_qqqq.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df_qqqq = df_qqqq.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df_qqqq = df_qqqq.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df_qqqq = df_qqqq.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df_qqqq = df_qqqq.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df_qqqq = df_qqqq.Define("jet3", "ROOT::Math::PxPyPzEVector(jets_px[2], jets_py[2], jets_pz[2], jets_e[2])")
    df_qqqq = df_qqqq.Define("jet4", "ROOT::Math::PxPyPzEVector(jets_px[3], jets_py[3], jets_pz[3], jets_e[3])")

    df_qqqq = df_qqqq.Define("comb1", "std::pow(((jet1+jet2).M()-80.3), 2) + std::pow(((jet3+jet4).M()-80.3), 2)")
    df_qqqq = df_qqqq.Define("comb2", "std::pow(((jet1+jet3).M()-80.3), 2) + std::pow(((jet2+jet4).M()-80.3), 2)")
    df_qqqq = df_qqqq.Define("comb3", "std::pow(((jet1+jet4).M()-80.3), 2) + std::pow(((jet2+jet3).M()-80.3), 2)")
    df_qqqq = df_qqqq.Define("combs", "std::vector<double>{comb1,comb2,comb3}")
    df_qqqq = df_qqqq.Define("min_idx", "return (int)(std::min_element(std::begin(combs), std::end(combs)) - combs.begin());")
    df_qqqq = df_qqqq.Define("w1", "return ((min_idx==0) ? (jet1+jet2) : ( (min_idx==1) ? (jet1+jet3) : (jet1+jet4)));")
    df_qqqq = df_qqqq.Define("w2", "return ((min_idx==0) ? (jet3+jet4) : ( (min_idx==1) ? (jet2+jet4) : (jet2+jet3)));")

    df_qqqq = df_qqqq.Define("w1_m", "w1.M()")
    df_qqqq = df_qqqq.Define("w2_m", "w2.M()")
    results.append(df_qqqq.Histo1D(("qqqq_w1_m", "", *bins_wmass), "w1_m"))
    results.append(df_qqqq.Histo1D(("qqqq_w2_m", "", *bins_wmass), "w2_m"))

    results.append(df_qqqq.Histo1D(("qqqq_w1_m_plus_50MeV", "", *bins_wmass), "w1_m", "weight_plus_50MeV"))
    results.append(df_qqqq.Histo1D(("qqqq_w1_m_minus_50MeV", "", *bins_wmass), "w1_m", "weight_minus_50MeV"))
    results.append(df_qqqq.Histo1D(("qqqq_w2_m_plus_50MeV", "", *bins_wmass), "w2_m", "weight_plus_50MeV"))
    results.append(df_qqqq.Histo1D(("qqqq_w2_m_minus_50MeV", "", *bins_wmass), "w2_m", "weight_minus_50MeV"))

    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_to_run = ["yfsww_ee_ww_noBES_ecm163", "yfsww_ee_ww_mw50MeVplus_noBES_ecm163", "yfsww_ee_ww_mw50MeVminus_noBES_ecm163", "p8_ee_Z_noBES_ecm163"]
    functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_wmass_kinematic.root", args, norm=True, lumi=500000) # assume half of 10 ab-1 at 157/163 GeV
