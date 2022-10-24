
import analysis, functions
import ROOT
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--nThreads", type=int, help="number of threads", default=None)
parser.add_argument("--maxFiles", type=int, help="Max number of files (per dataset)", default=-1)
args = parser.parse_args()

ROOT.EnableImplicitMT()
if args.nThreads: 
    ROOT.DisableImplicitMT()
    ROOT.EnableImplicitMT(int(args.nThreads))
print(ROOT.GetThreadPoolSize())

# define histograms
bins_pt_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (300000, 0, 300) # 1 MeV bins
bins_pt_ll = (200000, 0, 200) # 1 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (100000, -1, 1)

bins_eta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

def build_graph(df, dataset):

    print("build graph", dataset.name)
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240", "p8_ee_ZH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Muon0", "Muon#0.index")
    
    # prompt gen muons
    # in Whizard, the mumuH process does not directly involve Z processes, hence they are not present in the gen particles
    # the muons either directly come from the hard scatter (electrons as mothers) or from Higgs decays
    df = df.Define("gen_prompt_muons", "FCCAnalyses::select_prompt_leptons(13, Particle, Particle0)")
    df = df.Define("gen_prompt_muons_pt", "FCCAnalyses::MCParticle::get_pt(gen_prompt_muons)")
    df = df.Define("gen_prompt_muons_eta", "FCCAnalyses::MCParticle::get_eta(gen_prompt_muons)")
    df = df.Define("gen_prompt_muons_phi", "FCCAnalyses::MCParticle::get_phi(gen_prompt_muons)")
    df = df.Define("gen_prompt_muons_charge", "FCCAnalyses::MCParticle::get_charge(gen_prompt_muons)")
    df = df.Define("gen_prompt_muons_no", "FCCAnalyses::MCParticle::get_n(gen_prompt_muons)")
    
    
    
    
    # select muons
    df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("muons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(muons)")
    df = df.Define("muons_eta", "FCCAnalyses::ReconstructedParticle::get_eta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_no", "FCCAnalyses::ReconstructedParticle::get_n(muons)")
    df = df.Define("selected_muons", "FCCAnalyses::ReconstructedParticle::sel_pt(2.)(muons)") # was 10
    df = df.Define("selected_muons_pt", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons)")
    df = df.Define("selected_muons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(selected_muons)")
    df = df.Define("selected_muons_no", "FCCAnalyses::ReconstructedParticle::get_n(selected_muons)")
        
    # event variables
    df = df.Define("cosTheta_miss", "FCCAnalyses::get_cosTheta_miss(MissingET)")
        
    # build the Z resonance and recoil  resonanceZBuilderHiggsPairs
    #df = df.Define("zed_leptonic", "FCCAnalyses::resonanceZBuilder2(91, false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic", "FCCAnalyses::resonanceZBuilderHiggsPairs(91, false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)")
    df = df.Define("zed_leptonic_m", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic)")
    df = df.Define("zed_leptonic_no", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic)")
    df = df.Define("zed_leptonic_pt", "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic)")
    df = df.Define("zed_leptonic_charge", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil)")
    
    # build the Z resonance and recoil using MC information from the selected muons
    df = df.Define("zed_leptonic_MC", "FCCAnalyses::resonanceZBuilder2(91, true)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_MC)")
    df = df.Define("zed_leptonic_recoil_MC",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_MC)")
    df = df.Define("zed_leptonic_recoil_m_MC", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_MC)")
        
    # gen analysis
    if dataset.name in sigProcs:
        df = df.Define("higgs_MC", "FCCAnalyses::gen_sel_pdgIDInt(25,false)(Particle)")
        df = df.Define("daughter_higgs", "FCCAnalyses::gen_decay_list(higgs_MC, Particle, Particle1)")
        df = df.Define("daughter_higgs_collapsed", "daughter_higgs.size()>1 ? ((abs(daughter_higgs[0])+abs(daughter_higgs[1]))*0.5) : -1000 ")
        
    # baseline selections and histograms
    results.append(df.Histo1D(("zed_leptonic_m_cut0", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut0", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt_cut0", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt_cut0", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss_cut0", "", *bins_cosThetaMiss), "cosTheta_miss"))
    
    results.append(df.Histo1D(("muons_pt", "", *bins_pt_mu), "muons_pt"))
    results.append(df.Histo1D(("muons_eta", "", *bins_eta), "muons_eta"))
    results.append(df.Histo1D(("muons_phi", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_charge", "", *bins_charge), "muons_charge"))
    results.append(df.Histo1D(("muons_no", "", *bins_count), "muons_no"))
    
    results.append(df.Histo1D(("gen_prompt_muons_pt", "", *bins_pt_mu), "gen_prompt_muons_pt"))
    results.append(df.Histo1D(("gen_prompt_muons_eta", "", *bins_eta), "gen_prompt_muons_eta"))
    results.append(df.Histo1D(("gen_prompt_muons_phi", "", *bins_phi), "gen_prompt_muons_phi"))
    results.append(df.Histo1D(("gen_prompt_muons_charge", "", *bins_charge), "gen_prompt_muons_charge"))
    results.append(df.Histo1D(("gen_prompt_muons_no", "", *bins_count), "gen_prompt_muons_no"))
    
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut0", "", *bins_count), "daughter_higgs_collapsed"))
        results.append(df.Histo1D(("zed_leptonic_no_cut0", "", *bins_count), "zed_leptonic_no"))
        results.append(df.Histo1D(("zed_leptonic_charge_cut0", "", *bins_charge), "zed_leptonic_charge"))
    
   
    df = df.Filter("muons_no >= 1")
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut01", "", *bins_count), "daughter_higgs_collapsed"))
        results.append(df.Histo1D(("zed_leptonic_no_cut01", "", *bins_count), "zed_leptonic_no"))
        results.append(df.Histo1D(("zed_leptonic_charge_cut01", "", *bins_charge), "zed_leptonic_charge"))
    df = df.Filter("muons_no >= 2")
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut02", "", *bins_count), "daughter_higgs_collapsed"))
        results.append(df.Histo1D(("zed_leptonic_no_cut02", "", *bins_count), "zed_leptonic_no"))
        results.append(df.Histo1D(("zed_leptonic_charge_cut02", "", *bins_charge), "zed_leptonic_charge"))
    df = df.Filter("selected_muons_no >= 2")
    if dataset.name in sigProcs:
        results.append(df.Histo1D(("higgs_decay_cut03", "", *bins_count), "daughter_higgs_collapsed"))
        results.append(df.Histo1D(("zed_leptonic_no_cut03", "", *bins_count), "zed_leptonic_no"))
        results.append(df.Histo1D(("zed_leptonic_charge_cut03", "", *bins_charge), "zed_leptonic_charge"))

    
    df = df.Filter("zed_leptonic_m.size() >= 0") # was ==1
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut1", "", *bins_count), "daughter_higgs_collapsed"))
    
    df = df.Filter("zed_leptonic_charge[0] == 0") # was ==1
    results.append(df.Histo1D(("zed_leptonic_m_cut1", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut1", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt_cut1", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt_cut1", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss_cut1", "", *bins_cosThetaMiss), "cosTheta_miss"))
    
    results.append(df.Histo1D(("zed_leptonic_charge_cut1", "", *bins_charge), "zed_leptonic_charge"))

    
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut11", "", *bins_count), "daughter_higgs_collapsed"))
    
    
    df = df.Filter("zed_leptonic_m[0] > 86 &&  zed_leptonic_m[0] < 96")
    #df = df.Filter("zed_leptonic_m[0] > 73 &&  zed_leptonic_m[0] < 120")
    results.append(df.Histo1D(("zed_leptonic_m_cut2", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut2", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt_cut2", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt_cut2", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss_cut2", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut2", "", *bins_count), "daughter_higgs_collapsed")) 
    
    df = df.Filter("zed_leptonic_pt[0] > 20 && zed_leptonic_pt[0] < 70")
    results.append(df.Histo1D(("zed_leptonic_m_cut3", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut3", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt_cut3", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt_cut3", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss_cut3", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut3", "", *bins_count), "daughter_higgs_collapsed")) 
    
    df = df.Filter("cosTheta_miss[0] < 0.98")
    results.append(df.Histo1D(("zed_leptonic_m_cut4", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_cut4", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt_cut4", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt_cut4", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss_cut4", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay_cut4", "", *bins_count), "daughter_higgs_collapsed")) 
    
    # final selection and histograms
    df = df.Filter("zed_leptonic_recoil_m[0] < 140 && zed_leptonic_recoil_m[0] > 120")
    results.append(df.Histo1D(("zed_leptonic_m", "", *bins_m_ll), "zed_leptonic_m"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m", "", *bins_recoil), "zed_leptonic_recoil_m"))
    results.append(df.Histo1D(("zed_leptonic_pt", "", *bins_pt_ll), "zed_leptonic_pt"))
    results.append(df.Histo1D(("selected_muons_pt", "", *bins_pt_mu), "selected_muons_pt"))
    results.append(df.Histo1D(("cosThetaMiss", "", *bins_cosThetaMiss), "cosTheta_miss"))
    if dataset.name in sigProcs: results.append(df.Histo1D(("higgs_decay", "", *bins_count), "daughter_higgs_collapsed")) 
    
    # MC based recoil
    results.append(df.Histo1D(("zed_leptonic_m_MC", "", *bins_m_ll), "zed_leptonic_m_MC"))
    results.append(df.Histo1D(("zed_leptonic_recoil_m_MC", "", *bins_recoil), "zed_leptonic_recoil_m_MC"))
    
    
    if dataset.name not in sigProcs:
        return results, weightsum
        
        
    
    
    
    #bins_count = (50, 0, 50)

    # systematics
        
    '''
    # muon momentum scale
    df = df.Define("muons_muscaleup", "momentum_scale(1e-5)(muons)")
    df = df.Define("muons_muscaledw", "momentum_scale(-1e-5)(muons)")
    df = df.Define("selected_muons_muscaleup", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_muscaleup)")
    df = df.Define("selected_muons_muscaledw", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_muscaledw)")
    df = df.Define("selected_muons_pt_muscaleup", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_muscaleup)")
    df = df.Define("selected_muons_pt_muscaledw", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_muscaledw)")
               
    df = df.Define("zed_leptonic_muscaleup", "resonanceZBuilder2(91, false)(selected_muons_muscaleup, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_muscaleup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_no_muscaleup", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_pt_muscaleup", "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_charge_muscaleup", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic_muscaleup)")
               
    df = df.Define("zed_leptonic_muscaledw", "resonanceZBuilder2(91, false)(selected_muons_muscaledw, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("zed_leptonic_m_muscaledw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_no_muscaledw", "FCCAnalyses::ReconstructedParticle::get_n(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_pt_muscaledw", "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_charge_muscaledw", "FCCAnalyses::ReconstructedParticle::get_charge(zed_leptonic_muscaledw)")
               
    df = df.Define("zed_leptonic_recoil_muscaleup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_muscaleup)")
    df = df.Define("zed_leptonic_recoil_muscaledw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_muscaledw)")
    df = df.Define("zed_leptonic_recoil_m_muscaleup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_muscaleup)")
    df = df.Define("zed_leptonic_recoil_m_muscaledw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_muscaledw)")
        
        
    # sqrt uncertainty
    df = df.Define("zed_leptonic_recoil_sqrtsup", "FCCAnalyses::ReconstructedParticle::recoilBuilder(240.002)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_sqrtsdw", "FCCAnalyses::ReconstructedParticle::recoilBuilder(239.998)(zed_leptonic)")
    df = df.Define("zed_leptonic_recoil_m_sqrtsup", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_sqrtsup)")
    df = df.Define("zed_leptonic_recoil_m_sqrtsdw", "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_sqrtsdw)")
               
               

    # .Define("zed_leptonic_recoil_mc",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(zed_leptonic_mc)")
    # .Define("zed_leptonic_recoil_m_mc","FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_recoil_mc)")
    #.Define("selected_muons_mc", "MC_to_reco(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, selected_muons, Particle)")
    #.Define("muon_resolution", "get_resolution(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, selected_muons, Particle)")
               
               
    #.Define("zed_leptonic_recoil_MC",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)( zed_leptonic_MC )")
    #.Define("zed_leptonic_recoil_MC_mass",   "FCCAnalyses::ReconstructedParticle::get_mass( zed_leptonic_recoil_MC )")
    #.Define("zed_leptonic",         "APCHiggsTools::resonanceZBuilder(91)(selected_muons)")   
    #
               
    #.Define("selected_muons_all", "FCCAnalyses::ReconstructedParticle::sel_pt(10.)(muons_all)")
    # create branch with muon transverse momentum
               
    #.Define("selected_muons_pt_mc", "FCCAnalyses::ReconstructedParticle::get_pt(selected_muons_mc)")
    # create branch with muon rapidity
               

    # create branch with muon total momentum
    #.Define("selected_muons_p",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons)")
    #.Define("selected_muons_p_mc",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_mc)")
    #.Define("selected_muons_p_muscaleup",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_muscaleup)")
    #.Define("selected_muons_p_muscaledw",     "FCCAnalyses::ReconstructedParticle::get_p(selected_muons_muscaledw)")
               
               
    #.Define("ISR_gamma_E", "ISR_gamma_E(selected_muons)")
    #.Define("ISR_costhetas", "ISR_costhetas(selected_muons)")
               
               
               
               
    #.Define("event_ht",     "FCCAnalyses::ReconstructedParticle::get_ht(muons, electrons, photons, jets, met)")
    # create branch with muon energy 
               
    # find zed candidates from  di-muon resonances  , returns the best candidate, closest to the Z
               
               
               
    #.Define("zed_leptonic_mc",           "FCCAnalyses::ReconstructedParticle::resonanceBuilder(91)(selected_muons_mc)")
               
    #.Define("zed_leptonic_pair",    "FCCAnalyses::ReconstructedParticle::resonancePairBuilder(91)(selected_muons)")
    #.Define("acoplanarity",      "FCCAnalyses::ReconstructedParticle::acoplanarity(zed_leptonic_pair)")
    #.Define("acolinearity",      "FCCAnalyses::ReconstructedParticle::acolinearity(zed_leptonic_pair)")
    # write branch with zed mass
               
               
    #.Define("zed_leptonic_m_mc",             "FCCAnalyses::ReconstructedParticle::get_mass(zed_leptonic_mc)")
    # write branch with zed transverse momenta
    #.Define("zed_leptonic_pt",      "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic)")
    #.Define("zed_leptonic_pt_mc",      "FCCAnalyses::ReconstructedParticle::get_pt(zed_leptonic_mc)")

    '''
 
    return results, weightsum
    
    


if __name__ == "__main__":

    # import spring2021 IDEA samples
    import FCCee_spring2021_IDEA
    #datasets = FCCee_spring2021_IDEA.getDatasets(filt="p8_ee_ZH_ecm240") # p8_ee_ZH_ecm240 
    datasets = FCCee_spring2021_IDEA.getDatasets(filt="wzp6_ee_mumuH_ecm240")
    #datasets += FCCee_spring2021_IDEA.getDatasets(filt="p8_ee_Zmumu_ecm91")
    

    result = functions.build_and_run(datasets, build_graph, "output.root", maxFiles=args.maxFiles)
    
