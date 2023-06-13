
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, choices=["ee", "mumu", "qq"], help="Flavor (ee, mumu, qq)", default="mumu")
parser.add_argument("--jetAlgo", type=str, choices=["kt", "valencia", "genkt"], default="genkt", help="Jet clustering algorithm")
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (20000, 0, 300) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (100, 0, 100)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_e = (1000, 0, 100)

bins_resolution = (10000, 0.95, 1.05)

bins_resolution_1 = (20000, 0, 2)

jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (2000, 0, 200) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins


    
    
def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Define("RP_px", "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles)")
    df = df.Define("RP_py", "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles)")
    df = df.Define("RP_pz", "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles)")
    df = df.Define("RP_e",  "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles)")
    df = df.Define("RP_m",  "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles)")
    df = df.Define("RP_q",  "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles)")
    df = df.Define("RP_no",  "FCCAnalyses::ReconstructedParticle::get_n(ReconstructedParticles)")
    
    # sum of reco particles energy
    df = df.Define("Evis",  "FCCAnalyses::visibleEnergy(ReconstructedParticles)")
    df = df.Define("Evis_norm", "Evis/91.2")
    
    results.append(df.Histo1D(("Evis", "", *bins_m_ll), "Evis"))
    results.append(df.Histo1D(("Evis_norm", "", *bins_resolution_1), "Evis_norm"))
    results.append(df.Histo1D(("RP_no", "", *bins_count), "RP_no"))
    results.append(df.Histo1D(("RP_q", "", *bins_charge), "RP_q"))
    results.append(df.Histo1D(("RP_e", "", *bins_e), "RP_e"))
    
    return results, weightsum
    
    df = df.Define("pseudo_jets", "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
    
    
    
 
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    if args.jetAlgo == "kt":
        df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 0, 10)(pseudo_jets)")
    elif args.jetAlgo == "valencia":
        df = df.Define("clustered_jets", "JetClustering::clustering_valencia(0.5, 1, 2, 0, 0, 1., 1.)(pseudo_jets)")
    elif args.jetAlgo == "genkt":
        df = df.Define("clustered_jets", "FCCAnalyses::JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
          


    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_phi", "FCCAnalyses::JetClusteringUtils::get_phi(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")
        
    df = df.Define("njets", "jets_e.size()")
    results.append(df.Histo1D(("njets", "", *bins_count), "njets"))
    df = df.Filter("njets >= 2")
        
    # reconstruct resonance (jets are pT ordered)
    df = df.Define("jet1", "ROOT::Math::PxPyPzEVector(jets_px[0], jets_py[0], jets_pz[0], jets_e[0])")
    df = df.Define("jet2", "ROOT::Math::PxPyPzEVector(jets_px[1], jets_py[1], jets_pz[1], jets_e[1])")
    df = df.Define("dijet", "jet1+jet2")
    df = df.Define("dijet_m", "dijet.M()")

    results.append(df.Histo1D(("jets_e", "", *jet_energy), "jets_e"))
    results.append(df.Histo1D(("dijet_m", "", *dijet_m), "dijet_m"))
    results.append(df.Histo1D(("dijet_m_final", "", *dijet_m_final), "dijet_m"))
   
    results.append(df.Histo1D(("jets_phi", "", *bins_phi), "jets_phi"))    

    
    df = df.Define("visibleMass", "FCCAnalyses::visibleMass(ReconstructedParticles)") # scalar
    df = df.Define("missingEnergy_vec", "FCCAnalyses::missingEnergy(91.1, ReconstructedParticles)") # returns a vector
    df = df.Define("missingEnergy", "FCCAnalyses::ReconstructedParticle::get_e(missingEnergy_vec)")
    
    results.append(df.Histo1D(("visibleMass", "", *visMass), "visibleMass"))    
    results.append(df.Histo1D(("missingEnergy", "", *missEnergy), "missingEnergy"))    
        
    
    return results, weightsum
    
    
    
    
    
   

if __name__ == "__main__":

    noma = {"name": "noma", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_tautau_ecm91p2/events_29142.root",  "xsec": 1}
    nomb = {"name": "nomb", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumu_ecm91p2/events_30796.root",  "xsec": 1}
        
    datasets = [noma, nomb]
    result = functions.build_and_run(datasets, build_graph_ll, "tmp/validation_kkmcee_mumu.root", maxFiles=args.maxFiles)