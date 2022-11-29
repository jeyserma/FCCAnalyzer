
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", default="mumu")
args = parser.parse_args()

ROOT.EnableImplicitMT()
if args.nThreads: 
    ROOT.DisableImplicitMT()
    ROOT.EnableImplicitMT(int(args.nThreads))
print(ROOT.GetThreadPoolSize())

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (20000, 0, 300) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

bins_resolution = (10000, 0.95, 1.05)

def build_graph_ll(df, dataset):

    print("build graph", dataset.name)
    results = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    if args.flavor == "mumu":
        df = df.Alias("Lepton0", "Muon#0.index")
    else:
        df = df.Alias("Lepton0", "Electron#0.index")
     
    
    
    # all leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    
    # cuts on leptons
    #df = df.Define("selected_muons", "FCCAnalyses::excluded_Higgs_decays(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)") # was 10
    df = df.Define("leps_sel_p", "FCCAnalyses::ReconstructedParticle::sel_p(20)(leps_all)")
    df = df.Alias("leps", "leps_sel_p") 
    
    df = df.Define("leps_p", "FCCAnalyses::ReconstructedParticle::get_p(leps)")
    df = df.Define("leps_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps)")
    df = df.Define("leps_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps)")
    df = df.Define("leps_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps)")
    df = df.Define("leps_no", "FCCAnalyses::ReconstructedParticle::get_n(leps)")
    
    # momentum resolution: reco/gen
    df = df.Define("leps_all_reso_p", "FCCAnalyses::leptonResolution_p(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("leps_reso_p", "FCCAnalyses::leptonResolution_p(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    

    # lepton kinematic histograms
    results.append(df.Histo1D(("leps_all_p_cut0", "", *bins_p_mu), "leps_all_p"))
    results.append(df.Histo1D(("leps_all_theta_cut0", "", *bins_theta), "leps_all_theta"))
    results.append(df.Histo1D(("leps_all_phi_cut0", "", *bins_phi), "leps_all_phi"))
    results.append(df.Histo1D(("leps_all_q_cut0", "", *bins_charge), "leps_all_q"))
    results.append(df.Histo1D(("leps_all_no_cut0", "", *bins_count), "leps_all_no"))
    results.append(df.Histo1D(("leps_all_reso_p_cut0", "", *bins_resolution), "leps_all_reso_p"))
    

    results.append(df.Histo1D(("leps_p_cut0", "", *bins_p_mu), "leps_p"))
    results.append(df.Histo1D(("leps_theta_cut0", "", *bins_theta), "leps_theta"))
    results.append(df.Histo1D(("leps_phi_cut0", "", *bins_phi), "leps_phi"))
    results.append(df.Histo1D(("leps_q_cut0", "", *bins_charge), "leps_q"))
    results.append(df.Histo1D(("leps_no_cut0", "", *bins_count), "leps_no"))
    results.append(df.Histo1D(("leps_reso_p_cut0", "", *bins_resolution), "leps_reso_p"))
    
   

    
    #########
    ### CUT 0: all events
    #########
    df = df.Define("cut0", "0")
    results.append(df.Histo1D(("cutFlow_cut0", "", *bins_count), "cut0"))
   

    #########
    ### CUT 1: at least a lepton with at least 1 isolated one
    #########
    df = df.Filter("leps_no >= 1").Define("cut1", "1")
    results.append(df.Histo1D(("cutFlow_cut1", "", *bins_count), "cut1"))
    
    
    #########
    ### CUT 2 :at least 2 leptons, and build the resonance
    #########
    df = df.Filter("leps_no >= 2").Define("cut2", "2")
    results.append(df.Histo1D(("cutFlow_cut2", "", *bins_count), "cut2"))
    

    # build the Z resonance from the reconstructed particles
    df = df.Define("zll", "FCCAnalyses::resonanceZBuilder2(91, false)(leps, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zll_m", "FCCAnalyses::ReconstructedParticle::get_mass(zll)")
    df = df.Define("zll_no", "FCCAnalyses::ReconstructedParticle::get_n(zll)")
    df = df.Define("zll_p", "FCCAnalyses::ReconstructedParticle::get_p(zll)")
    
    #########
    ### CUT 3 :at least 1 resonance (i.e. one opposite sign pair muon)
    #########
    df = df.Filter("zll_no >= 1").Define("cut3", "3")
    results.append(df.Histo1D(("cutFlow_cut3", "", *bins_count), "cut3"))


    #########
    ### CUT 4 :cut on Z mass
    #########
    df = df.Filter("zll_m[0] > 73 && zll_m[0] < 109").Define("cut4", "4")
    results.append(df.Histo1D(("cutFlow_cut4", "", *bins_count), "cut4"))
    
    
    ########################
    # Final histograms
    ########################
    results.append(df.Histo1D(("zll_m_cut4", "", *bins_m_ll), "zll_m"))
    results.append(df.Histo1D(("zll_p_cut4", "", *bins_p_ll), "zll_p"))
    results.append(df.Histo1D(("leps_p_cut4", "", *bins_p_mu), "leps_p"))
    
    return results, weightsum
    
    


if __name__ == "__main__":

    datasets = []
    import FCCee_spring2021_ecm91_IDEA
    baseDir_MIT = "/data/submit/cms/store/fccee"
    baseDir_CERN = "/data/shared/jaeyserm/fccee/" # /eos/experiment/fcc/ee/generation/DelphesEvents/
    
   
    
    if args.flavor == "mumu": 
        samples = ["p8_ee_Zmumu_ecm91", "p8_ee_Ztautau_ecm91"]
        datasets += FCCee_spring2021_ecm91_IDEA.getDatasets(select=samples, baseDir=baseDir_CERN)
        
        result = functions.build_and_run(datasets, build_graph_ll, "tmp/output_z_xsec_%s.root" % args.flavor, maxFiles=args.maxFiles, norm=True, lumi=150000000)

    if args.flavor == "ee":
    
        samples = ["p8_ee_Zee_ecm91", "p8_ee_Ztautau_ecm91"]
        datasets += FCCee_spring2021_ecm91_IDEA.getDatasets(select=samples, baseDir=baseDir_CERN)
        result = functions.build_and_run(datasets, build_graph_ll, "tmp/output_z_xsec_%s.root" % args.flavor, maxFiles=args.maxFiles, norm=True, lumi=150000000)
 
    if args.flavor == "qq":
        samples = ["p8_ee_Zuds_ecm91", "p8_ee_Zcc_ecm91", "p8_ee_Zbb_ecm91"]
        datasets += FCCee_spring2021_ecm91_IDEA.getDatasets(select=samples, baseDir=baseDir_CERN)
        # to be implemented

    
    
