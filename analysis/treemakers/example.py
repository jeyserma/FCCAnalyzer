
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

functions.set_threads(args)


def build_graph(df, dataset):

    print("build graph", dataset.name)
    cols = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Muon#0.index")

    
    
    # all leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    
    # cuts on leptons
    df = df.Define("leps_sel_p", "FCCAnalyses::ReconstructedParticle::sel_p(1)(leps_all)")
    df = df.Alias("leps", "leps_sel_p") 
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    

    

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1").Define("cut1", "1")
    
    
    #########
    ### CUT 2 :at least 2 leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2").Define("cut2", "2")
    

    # build the Z resonance from the reconstructed particles
    df = df.Define("zll", "FCCAnalyses::resonanceBuilder(91)(leps)")
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)")
    df = df.Define("zll_no", "FCCAnalyses::ReconstructedParticle::get_n(zll)")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)")
    
    #########
    ### CUT 3 :at least 1 resonance (i.e. one opposite sign pair muon)
    #########
    df = df.Filter("zll_no >= 1").Define("cut3", "3")


    #########
    ### CUT 4 :cut on Z mass
    #########
    df = df.Filter("(zll_m[0] > 73 && zll_m[0] < 109)").Define("cut4", "4")
    
    
    cols.append("leps_p")
    cols.append("leps_theta")
    cols.append("leps_phi")
    cols.append("leps_q")
    cols.append("leps_no")
       
    cols.append("zll_m")
    cols.append("zll_p")
    
    
    return df, cols
    
    

    
    
   

if __name__ == "__main__":

    wzp6_ee_mumuH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumuH_ecm240/",  "xsec": 1}
    wzp6_ee_eeH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_eeH_ecm240/",  "xsec": 1}
    datasets = [wzp6_ee_mumuH_ecm240, wzp6_ee_eeH_ecm240]
    
    functions.build_and_run_snapshot(datasets, build_graph, "tmp/test_tree_{datasetName}.root", maxFiles=args.maxFiles)

    
    
