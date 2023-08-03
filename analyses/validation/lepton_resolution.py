
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
args = parser.parse_args()

functions.set_threads(args)

# define histograms
bins_theta = (50, 0, 3.1415)
bins_p = (40, 0, 200) # 5 GeV bins
bins_resolution = (10000, 0.95, 1.05)




def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
        
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    if args.flavor == "mumu":
        df = df.Alias("Lep0", "Muon#0.index")
    else:
        df = df.Alias("Lep0", "Electron#0.index")
     
    
    
    # select muons
    df = df.Define("leptons", "FCCAnalyses::ReconstructedParticle::get(Lep0, ReconstructedParticles)")
    df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")
    df = df.Define("leptons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leptons)")
    df = df.Define("leptons_eta", "FCCAnalyses::ReconstructedParticle::get_eta(leptons)")
    df = df.Define("leptons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leptons)")
    df = df.Define("leptons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(leptons)")
    df = df.Define("leptons_no", "FCCAnalyses::ReconstructedParticle::get_n(leptons)")
    df = df.Define("leptons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leptons, ReconstructedParticles)") 
    
    

    # lepton resolution
    df = df.Define("leptons_reso", "FCCAnalyses::leptonResolution_p(leptons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    results.append(df.Histo3D(("lepton_reso", "", *(bins_p + bins_theta + bins_resolution)), "leptons_p", "leptons_theta", "leptons_reso"))

    

    return results, weightsum
    
    


if __name__ == "__main__":

    baseDir = functions.get_basedir() # get base directory of samples, depends on the cluster hostname (mit, cern, ...)
    import FCCee_winter2023_IDEA_ecm240
    datasets_preproduction_IDEA = FCCee_winter2023_IDEA_ecm240.get_datasets(baseDir=baseDir) # list of all datasets
    
    if args.flavor == "mumu": 
        select = ["wzp6_ee_mumuH_ecm240"]

    
    if args.flavor == "ee":
        select = ["wzp6_ee_eeH_ecm240"]

    datasets = functions.filter_datasets(datasets_preproduction_IDEA, select)
    result = functions.build_and_run(datasets, build_graph, "tmp/lepton_resolution_%s.root" % args.flavor, maxFiles=args.maxFiles, norm=True, lumi=5000000)
    
