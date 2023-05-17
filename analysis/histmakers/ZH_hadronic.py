
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--jetAlgo", type=str, choices=["kt", "valencia", "genkt"], default="kt", help="Jet clustering algorithm")
args = parser.parse_args()

ROOT.EnableImplicitMT()
if args.nThreads: 
    ROOT.DisableImplicitMT()
    ROOT.EnableImplicitMT(int(args.nThreads))
print(ROOT.GetThreadPoolSize())

# define histogram bins
bins_count = (50, 0, 50)
jet_E = (250, 0, 250)
dijet_m = (200, 0, 200)
visEnergy = (200, 0, 200)
chi2 = (2000, 0, 200)

def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Define("RP_px",          "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py",          "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz",          "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",           "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("RP_m",           "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",           "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")

    #df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets_xyzm(RP_px, RP_py, RP_pz, RP_m)")
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
        
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    if args.jetAlgo == "kt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 4, 1, 0)(pseudo_jets)")
    elif args.jetAlgo == "valencia":
        df = df.Define("clustered_jets", "JetClustering::clustering_valencia(0.5, 1, 2, 0, 0, 1., 1.)(pseudo_jets)")
    elif args.jetAlgo == "genkt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
          

    
    
    
    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")
    
    df = df.Define("jets_tlv_corr", "FCCAnalyses::energyReconstructFourJet(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jet0_e_corr", "jets_tlv_corr[0].E()")
    df = df.Define("jet1_e_corr", "jets_tlv_corr[1].E()")
    df = df.Define("jet2_e_corr", "jets_tlv_corr[2].E()")
    df = df.Define("jet3_e_corr", "jets_tlv_corr[3].E()")
    df = df.Define("chi2", "jets_tlv_corr[4].E()")
    df = df.Define("jet_sum_e_corr", "jet0_e_corr+jet1_e_corr+jet2_e_corr+jet3_e_corr")
    
    
    df = df.Define("jets_tlv", "FCCAnalyses::jetsToTlv(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jet0_e", "jets_tlv[0].E()")
    df = df.Define("jet1_e", "jets_tlv[1].E()")
    df = df.Define("jet2_e", "jets_tlv[2].E()")
    df = df.Define("jet3_e", "jets_tlv[3].E()")
    df = df.Define("jet_sum_e", "jet0_e+jet1_e+jet2_e+jet3_e")
    
    results.append(df.Histo1D(("chi2", "", *chi2), "chi2"))
    results.append(df.Histo1D(("jet0_e_corr", "", *jet_E), "jet0_e_corr"))
    results.append(df.Histo1D(("jet1_e_corr", "", *jet_E), "jet1_e_corr"))
    results.append(df.Histo1D(("jet2_e_corr", "", *jet_E), "jet2_e_corr"))
    results.append(df.Histo1D(("jet3_e_corr", "", *jet_E), "jet3_e_corr"))
    results.append(df.Histo1D(("jet_sum_e_corr", "", *jet_E), "jet_sum_e_corr"))
    
    results.append(df.Histo1D(("jet0_e", "", *jet_E), "jet0_e"))
    results.append(df.Histo1D(("jet1_e", "", *jet_E), "jet1_e"))
    results.append(df.Histo1D(("jet2_e", "", *jet_E), "jet2_e"))
    results.append(df.Histo1D(("jet3_e", "", *jet_E), "jet3_e"))
    results.append(df.Histo1D(("jet_sum_e", "", *jet_E), "jet_sum_e"))
        
    df = df.Define("njets", "jets_e.size()")
    results.append(df.Histo1D(("njets", "", *bins_count), "njets"))
    df = df.Filter("njets >= 2")
        
    # reconstruct resonance (jets are pT ordered)
    df = df.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df = df.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df = df.Define("dijet", "jet1+jet2")
    df = df.Define("dijet_m", "dijet.M()")

    results.append(df.Histo1D(("jets_e", "", *jet_E), "jets_e"))
    results.append(df.Histo1D(("dijet_m", "", *dijet_m), "dijet_m"))
    
    
    df = df.Define("visibleEnergy", "FCCAnalyses::sumScalar(RP_e)") # energy of all PF/reconstructed candidates
    results.append(df.Histo1D(("visibleEnergy", "", *visEnergy), "visibleEnergy"))
    
    
    return results, weightsum
    
    


if __name__ == "__main__":
    
    wzp6_ee_bbH_Hbb_ecm240 = {"name": "wzp6_ee_bbH_Hbb_ecm240", "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_bbH_Hbb_ecm240/",  "xsec": 1}
    
    datasets = [wzp6_ee_bbH_Hbb_ecm240]

    result = functions.build_and_run(datasets, build_graph, "output_hadr.root", maxFiles=args.maxFiles)
    
