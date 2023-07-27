
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", choices=["mumu", "ee"], default="mumu")
args = parser.parse_args()

functions.set_threads(args)


def build_graph(df, dataset):

    print("build graph", dataset.name)
    cols = []    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    if args.flavor == "mumu":
        df = df.Alias("Lepton0", "Muon#0.index")
    else:
        df = df.Alias("Lepton0", "Electron#0.index")
     
   
    # all leptons (bare)
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    df = df.Define("leps_all_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps_all, ReconstructedParticles)") 
    df = df.Define("leps_all_p_gen", "FCCAnalyses::gen_p_from_reco(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    
    # cuts on leptons
    df = df.Define("leps", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")
    
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    df = df.Define("leps_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(leps, ReconstructedParticles)")
    df = df.Define("leps_sel_iso", "FCCAnalyses::sel_iso(0.25)(leps, leps_iso)") # 0.25



    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1 && leps_sel_iso.size() > 0")
    
    #########
    ### CUT 2 :at least 2 OS leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2 && abs(Sum(leps_q)) < leps_q.size()")
    
    # build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
    # technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    df = df.Define("zbuilder_result", "FCCAnalyses::resonanceBuilder_mass_recoil(91.2, 125, 0.4, 240, false)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zll", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[0]}") # the Z
    df = df.Define("zll_leps", "ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>{zbuilder_result[1],zbuilder_result[2]}") # the leptons
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)[0]")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)[0]")
    df = df.Define("zll_recoil", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zll)")
    df = df.Define("zll_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll_recoil)[0]")
    
    df = df.Define("zll_leps_p", "FCCAnalyses::ReconstructedParticle::get_p(zll_leps)")
    df = df.Define("zll_leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(zll_leps)")
     
    
    df = df.Define("missingEnergy", "FCCAnalyses::missingEnergy(240., ReconstructedParticles)")
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(missingEnergy)")
    #df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
    
    df = df.Define("acoplanarity", "FCCAnalyses::acoplanarity(leps)")
    df = df.Define("acolinearity", "FCCAnalyses::acolinearity(leps)")
   
    
    #########
    ### CUT 3: Z mass window
    #########  
    df = df.Filter("zll_m > 86 && zll_m < 96")
        
    
    #########
    ### CUT 4: Z momentum
    #########  
    df = df.Filter("zll_p > 20 && zll_p < 70")   
        
    #########
    ### CUT 5: recoil cut
    #########  
    df = df.Filter("zll_recoil_m < 140 && zll_recoil_m > 120")
    
    
   
    
    #########
    ### CUT 6: cosThetaMiss, for mass analysis
    #########  
    df = df.Filter("cosTheta_miss < 0.98")

 
    df = df.Define("lep1_p", "zll_leps_p[0]")
    df = df.Define("lep2_p", "zll_leps_p[1]")
    
    df = df.Define("lep1_theta", "zll_leps_theta[0]")
    df = df.Define("lep2_theta", "zll_leps_theta[1]")
    
    cols.append("lep1_p")
    cols.append("lep2_p")
    cols.append("lep1_theta")
    cols.append("lep2_theta")
    cols.append("zll_p")
    cols.append("acoplanarity")
    cols.append("acolinearity")
       
    cols.append("zll_recoil_m")
    cols.append("cosTheta_miss")
    
    
    return df, cols
    
    
    
    
    
   

if __name__ == "__main__":

    wzp6_ee_mumuH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumuH_ecm240/",  "xsec": 1}
    wzp6_ee_eeH_ecm240 = {"name": "wzp6_ee_mumuH_ecm240", "datadir": "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_eeH_ecm240/",  "xsec": 1}
    
    
    p8_ee_WW_ecm240 = {"name": "p8_ee_WW_ecm240", "datadir": "/eos/experiment/fcc/ee/generation/DelphesEvents//winter2023/IDEA/p8_ee_WW_ecm240/",  "xsec": 1}

    datasets = [p8_ee_WW_ecm240]
    
    functions.build_and_run_snapshot(datasets, build_graph, "tmp/test_tree_{datasetName}.root", maxFiles=args.maxFiles)

    
    
