
import functions
import helpers
import ROOT
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/ewk_z/functions.h")

# define histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (2000, 0, 200) # 100 MeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (100, 0, 100)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

dijet_m = (200, 0, 200) # 1 GeV bins



def build_graph(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # cluster all reconstructed particles
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",  "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("RP_m",  "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",  "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("RP_no",  "FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")


    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 4, 0, 10)(pseudo_jets)") # 4-jet clustering


    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)") # one-to-one mapping to reconstructedparticles
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")

    df = df.Define("jets_tlv", "FCCAnalyses::makeLorentzVectors(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jets_truth", "FCCAnalyses::jetTruthFinder(jetconstituents, ReconstructedParticles, Particle, MCRecoAssociations1)")
    df = df.Define("njets", "jets_e.size()")
    df = df.Define("jets_higgs", "FCCAnalyses::Vec_i res; for(int i=0;i<njets;i++) if(abs(jets_truth[i])==5) res.push_back(i); return res;") # assume H->bb
    df = df.Define("jets_z", "FCCAnalyses::Vec_i res; for(int i=0;i<njets;i++) if(abs(jets_truth[i])!=5) res.push_back(i); return res;")

    df = df.Filter("jets_higgs.size()==2")
    df = df.Filter("jets_z.size()==2")

    results.append(df.Histo1D(("njets", "", *bins_count), "njets"))
    results.append(df.Histo1D(("RP_no", "", *bins_count), "RP_no"))


    df = df.Define("dijet_higgs_m", "(jets_tlv[jets_higgs[0]]+jets_tlv[jets_higgs[1]]).M()")
    df = df.Define("dijet_z_m", "(jets_tlv[jets_z[0]]+jets_tlv[jets_z[1]]).M()")

    results.append(df.Histo1D(("dijet_higgs_m", "", *dijet_m), "dijet_higgs_m"))
    results.append(df.Histo1D(("dijet_z_m", "", *dijet_m), "dijet_z_m"))

    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets
    datasets_to_run = ["wzp6_ee_qqH_Hbb_ecm240"]
    result = functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_jetclustering.root", args, norm=True, lumi=150000000)
