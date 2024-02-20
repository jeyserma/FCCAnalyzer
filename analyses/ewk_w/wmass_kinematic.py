
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


    # photons
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Define("photons_all", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_all_no", "FCCAnalyses::ReconstructedParticle::get_n(photons_all)")
    df = df.Define("photons_all_p", "FCCAnalyses::ReconstructedParticle::get_p(photons_all)")
    df = df.Define("photons_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons_all)")
    df = df.Define("photons_all_costheta", "FCCAnalyses::Vec_f ret; for(auto & theta: photons_all_theta) ret.push_back(std::abs(cos(theta))); return ret;")

    df = df.Define("w_decay_mode", "FCCAnalyses::yfsww_w_decay_mode(Particle, Particle1)")
    results.append(df.Histo1D(("muons_all_p", "", *(50, -25, 25)), "w_decay_mode"))
    
    df = df.Define("w_decay_idxs", "FCCAnalyses::yfsww_w_idxs(Particle, Particle1)")
    df = df.Define("w_plus", "Particle[w_decay_idxs[0]]")
    df = df.Define("w_minus", "Particle[w_decay_idxs[1]]")
    df = df.Define("w_plus_m", "w_plus.mass")
    df = df.Define("w_minus_m", "w_minus.mass")
    
    df = df.Define("weight_plus_10MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, 10)")
    df = df.Define("weight_minus_10MeV", "FCCAnalyses::breitWignerWeights_WW(w_plus_m, w_minus_m, -10)")
    
    results.append(df.Histo1D(("w_plus_m", "", *(200, 70, 90)), "w_plus_m"))
    results.append(df.Histo1D(("w_minus_m", "", *(200, 70, 90)), "w_minus_m"))
    results.append(df.Histo2D(("w_plus_minus_m", "", *(200, 70, 90, 200, 70, 90)), "w_plus_m", "w_minus_m"))
    
    results.append(df.Histo1D(("weight_plus_10MeV", "", *(200, 0, 2)), "weight_plus_10MeV"))
    results.append(df.Histo1D(("weight_minus_10MeV", "", *(200, 0, 2)), "weight_minus_10MeV"))
    
    results.append(df.Histo1D(("w_plus_m_plus_10MeV", "", *(200, 70, 90)), "w_plus_m", "weight_plus_10MeV"))
    results.append(df.Histo1D(("w_minus_m_plus_10MeV", "", *(200, 70, 90)), "w_minus_m", "weight_plus_10MeV"))

    results.append(df.Histo1D(("w_plus_m_minus_10MeV", "", *(200, 70, 90)), "w_plus_m", "weight_minus_10MeV"))
    results.append(df.Histo1D(("w_minus_m_minus_10MeV", "", *(200, 70, 90)), "w_minus_m", "weight_minus_10MeV"))

    # lepton kinematic histograms
    results.append(df.Histo1D(("muons_all_p", "", *bins_p), "muons_all_p"))
    results.append(df.Histo1D(("muons_all_theta", "", *bins_theta), "muons_all_theta"))
    results.append(df.Histo1D(("muons_all_q", "", *bins_charge), "muons_all_q"))
    results.append(df.Histo1D(("muons_all_no", "", *bins_count), "muons_all_no"))

    results.append(df.Histo1D(("electrons_all_p", "", *bins_p), "electrons_all_p"))
    results.append(df.Histo1D(("electrons_all_theta", "", *bins_theta), "electrons_all_theta"))
    results.append(df.Histo1D(("electrons_all_q", "", *bins_charge), "electrons_all_q"))
    results.append(df.Histo1D(("electrons_all_no", "", *bins_count), "electrons_all_no"))

    results.append(df.Histo1D(("photons_all_p", "", *bins_p), "photons_all_p"))
    results.append(df.Histo1D(("photons_all_theta", "", *bins_theta), "photons_all_theta"))
    results.append(df.Histo1D(("photons_all_no", "", *bins_count), "photons_all_no"))


    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets_to_run = ["yfsww_ee_ww_noBES_ecm157", "yfsww_ee_ww_noBES_ecm163", "yfsww_ee_ww_noBES_Born_ecm163"]
    functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_wmass_kinematic.root", args, norm=True, lumi=500000) # assume half of 10 ab-1 at 157/163 GeV
