
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (20000, 0, 300) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)



def build_graph_ll(df, dataset):

    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Muon#0.index")

    
    
    # get the leptons leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    
    # construct Lorentz vectors of the leptons
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(leps_all)")
    
    results.append(df.Histo1D(("leps_all_p", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_theta", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no", "", *bins_count), "leps_all_no"))
    
    
    return results, weightsum
    
 
    
   

if __name__ == "__main__":

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_spring2021_ecm91_IDEA
    datasets_spring2021_ecm91 = FCCee_spring2021_ecm91_IDEA.get_datasets(baseDir=baseDir) # list of all datasets
    datasets = [] # list of datasets to be run over

    datasets += functions.filter_datasets(datasets_spring2021_ecm91, ["p8_ee_Zmumu_ecm91"])
    result = functions.build_and_run(datasets, build_graph_ll, "tmp/output_xsec_example.root", maxFiles=args.maxFiles)

    
