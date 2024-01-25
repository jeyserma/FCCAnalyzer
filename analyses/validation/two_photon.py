
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
functions.add_include_file("analyses/validation/two_photon.h")


# define histograms

bins_m = (1000, 0, 100)
bins_p = (1000, 0, 100)


bins_theta = (5000, 0, 5)
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

bins_cos = (200, -1, 1)
bins_cos_abs = (10000, 0, 1)
bins_aco = (1000,0,1)
bins_cosThetaMiss = (10000, 0, 1)

bins_dR = (1000, 0, 10)


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


    # reco muons
    df = df.Alias("Muon0", "Muon#0.index")
    df = df.Define("muons_all", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(muons_all)")
    df = df.Define("muons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(muons_all)")
    df = df.Define("muons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons_all)")
    df = df.Define("muons_all_charge", "FCCAnalyses::ReconstructedParticle::get_charge(muons_all)")
    df = df.Define("muons_all_costheta", "FCCAnalyses::calculate_cos_theta(muons_all_theta, true)")

    results.append(df.Histo1D(("muons_all_no", "", *bins_count), "muons_all_no"))
    results.append(df.Histo1D(("muons_all_p", "", *bins_p), "muons_all_p"))
    results.append(df.Histo1D(("muons_all_theta", "", *bins_theta), "muons_all_theta"))
    results.append(df.Histo1D(("muons_all_charge", "", *bins_charge), "muons_all_charge"))
    results.append(df.Histo1D(("muons_all_costheta", "", *bins_cos_abs), "muons_all_costheta"))

    # gen muons
    df = df.Define("muons_gen", "FCCAnalyses::get_gen_pdg(Particle, 13, true)")
    df = df.Define("muons_gen_no", "FCCAnalyses::MCParticle::get_n(muons_gen)")
    df = df.Define("muons_gen_p", "FCCAnalyses::MCParticle::get_p(muons_gen)")
    df = df.Define("muons_gen_theta", "FCCAnalyses::MCParticle::get_theta(muons_gen)")
    df = df.Define("muons_gen_charge", "FCCAnalyses::MCParticle::get_charge(muons_gen)")
    df = df.Define("muons_gen_costheta", "FCCAnalyses::calculate_cos_theta(muons_gen_theta, true)")

    results.append(df.Histo1D(("muons_gen_no", "", *bins_count), "muons_gen_no"))
    results.append(df.Histo1D(("muons_gen_p", "", *bins_p), "muons_gen_p"))
    results.append(df.Histo1D(("muons_gen_theta", "", *bins_theta), "muons_gen_theta"))
    results.append(df.Histo1D(("muons_gen_charge", "", *bins_charge), "muons_gen_charge"))
    results.append(df.Histo1D(("muons_gen_costheta", "", *bins_cos_abs), "muons_gen_costheta"))

    # reco electrons
    df = df.Alias("Electron0", "Electron#0.index")
    df = df.Define("electrons_all", "FCCAnalyses::ReconstructedParticle::get(Electron0, ReconstructedParticles)")
    df = df.Define("electrons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(electrons_all)")
    df = df.Define("electrons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(electrons_all)")
    df = df.Define("electrons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(electrons_all)")
    df = df.Define("electrons_all_charge", "FCCAnalyses::ReconstructedParticle::get_charge(electrons_all)")
    df = df.Define("electrons_all_costheta", "FCCAnalyses::calculate_cos_theta(electrons_all_theta, true)")

    results.append(df.Histo1D(("electrons_all_no", "", *bins_count), "electrons_all_no"))
    results.append(df.Histo1D(("electrons_all_p", "", *bins_p), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_all_theta", "", *bins_theta), "electrons_all_theta"))
    results.append(df.Histo1D(("electrons_all_charge", "", *bins_charge), "electrons_all_charge"))
    results.append(df.Histo1D(("electrons_all_costheta", "", *bins_cos_abs), "electrons_all_costheta"))

    # gen electrons
    df = df.Define("electrons_gen", "FCCAnalyses::get_gen_pdg(Particle, 11, true)")
    df = df.Define("electrons_gen_no", "FCCAnalyses::MCParticle::get_n(electrons_gen)")
    df = df.Define("electrons_gen_p", "FCCAnalyses::MCParticle::get_p(electrons_gen)")
    df = df.Define("electrons_gen_theta", "FCCAnalyses::MCParticle::get_theta(electrons_gen)")
    df = df.Define("electrons_gen_charge", "FCCAnalyses::MCParticle::get_charge(electrons_gen)")
    df = df.Define("electrons_gen_costheta", "FCCAnalyses::calculate_cos_theta(electrons_gen_theta, true)")

    results.append(df.Histo1D(("electrons_gen_no", "", *bins_count), "electrons_gen_no"))
    results.append(df.Histo1D(("electrons_gen_p", "", *bins_p), "electrons_gen_p"))
    results.append(df.Histo1D(("electrons_gen_theta", "", *bins_theta), "electrons_gen_theta"))
    results.append(df.Histo1D(("electrons_gen_charge", "", *bins_charge), "electrons_gen_charge"))
    results.append(df.Histo1D(("electrons_gen_costheta", "", *bins_cos_abs), "electrons_gen_costheta"))

    # reco photons
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(photons_all)")
    df = df.Define("photons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(photons_all)")
    df = df.Define("photons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons_all)")
    df = df.Define("photons_all_costheta", "FCCAnalyses::calculate_cos_theta(photons_all_theta, true)")

    results.append(df.Histo1D(("photons_all_no", "", *bins_count), "photons_all_no"))
    results.append(df.Histo1D(("photons_all_p", "", *bins_p), "photons_all_p"))
    results.append(df.Histo1D(("photons_all_theta", "", *bins_theta), "photons_all_theta"))
    results.append(df.Histo1D(("photons_all_costheta", "", *bins_cos_abs), "photons_all_costheta"))

    # gen photons
    df = df.Define("photons_gen", "FCCAnalyses::get_gen_pdg(Particle, 22)")
    df = df.Define("photons_gen_no", "FCCAnalyses::MCParticle::get_n(photons_gen)")
    df = df.Define("photons_gen_p", "FCCAnalyses::MCParticle::get_p(photons_gen)")
    df = df.Define("photons_gen_theta", "FCCAnalyses::MCParticle::get_theta(photons_gen)")
    df = df.Define("photons_gen_costheta", "FCCAnalyses::calculate_cos_theta(photons_gen_theta, true)")

    results.append(df.Histo1D(("photons_gen_no", "", *bins_count), "photons_gen_no"))
    results.append(df.Histo1D(("photons_gen_p", "", *bins_p), "photons_gen_p"))
    results.append(df.Histo1D(("photons_gen_theta", "", *bins_theta), "photons_gen_theta"))
    results.append(df.Histo1D(("photons_gen_costheta", "", *bins_cos_abs), "photons_gen_costheta"))
    


    # Q2 -- sum of gen muons
    df = df.Define("muons_gen_tlv", "FCCAnalyses::makeLorentzVectors(muons_gen)")
    df = df.Define("dimuon", "muons_gen_tlv[0] + muons_gen_tlv[1]")
    df = df.Define("dimuon_m", "dimuon.M()")
    results.append(df.Histo1D(("dimuon_m", "", *bins_m), "dimuon_m"))


    df = df.Define("hard_photon_idx", "FCCAnalyses::get_hard_photons(Particle, Particle0)")
    results.append(df.Histo1D(("test", "", *bins_m), "hard_photon_idx"))
    
    df = df.Define("gamma1", "ROOT::Math::PxPyPzMVector(Particle[hard_photon_idx[0]].momentum.x, Particle[hard_photon_idx[0]].momentum.y, Particle[hard_photon_idx[0]].momentum.z, Particle[hard_photon_idx[0]].mass)")
    df = df.Define("gamma2", "ROOT::Math::PxPyPzMVector(Particle[hard_photon_idx[1]].momentum.x, Particle[hard_photon_idx[1]].momentum.y, Particle[hard_photon_idx[1]].momentum.z, Particle[hard_photon_idx[1]].mass)")
    df = df.Define("digamma", "gamma1+gamma2")
    df = df.Define("digamma_m", "digamma.M()")
    df = df.Define("digamma_m_scaled", "digamma_m/91.2")
    df = df.Define("gamma1_e", "gamma1.E()")
    df = df.Define("gamma1_theta", "gamma1.Theta()")
    df = df.Define("gamma2_e", "gamma2.E()")
    df = df.Define("gamma2_theta", "gamma2.Theta()")
    #df = df.Define("digamma_m", "cout << gamma1.E() << \" \"<<  gamma2.E() << endl; return 1;")
    results.append(df.Histo1D(("digamma_m", "", *bins_m), "digamma_m"))
    results.append(df.Histo1D(("digamma_m_scaled", "", *(1000, 0, 1)), "digamma_m_scaled"))

    results.append(df.Histo1D(("gamma1_e", "", *bins_p), "gamma1_e"))
    results.append(df.Histo1D(("gamma1_theta", "", *bins_theta), "gamma1_theta"))
    results.append(df.Histo1D(("gamma2_e", "", *bins_p), "gamma2_e"))
    results.append(df.Histo1D(("gamma2_theta", "", *bins_theta), "gamma2_theta"))
    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_to_run = ["wz3p6_ee_gaga_mumu_ecm91p2", "wz3p6_ee_gaga_mumu_ecm91p2_cfg1", "p8_ee_gaga_mumu_ecm91p2"]
    #datasets_to_run = ["wz3p6_ee_gaga_mumu_ecm91p2"]
    result = functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_two_photon.root", args, norm=False)
