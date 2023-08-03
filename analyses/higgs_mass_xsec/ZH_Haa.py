
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
bins_p = (2000, 0, 200) # 100 MeV bins
bins_m_gaga = (3000, 0, 300) # 100 MeV bins
bins_p_gaga = (2000, 0, 200) # 100 MeV bins
bins_recoil = (2000, 0, 200) # 100 MeV bins 

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)



# define histogram bins
jet_E = (250, 0, 250)
dijet_m = (200, 0, 200)
visEnergy = (200, 0, 200)
chi2 = (2000, 0, 200)
bins_iso = (500, 0, 5)


def build_graph_aa(df, dataset):

    print("build graph", dataset.name)
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    
    
    # all photons
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
    df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")

    results.append(df.Histo1D(("photons_p", "", *bins_p), "photons_p"))
    results.append(df.Histo1D(("photons_theta", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no", "", *bins_count), "photons_no"))
    
    
    # select photons with momentum p > 30 GeV 
    # Higgs -> gamma gamma produces on average 125/2 = 62.5 GeV photons
    df = df.Define("selected_photons", "FCCAnalyses::ReconstructedParticle::sel_p(40)(photons)")
    df = df.Define("selected_photons_p", "FCCAnalyses::ReconstructedParticle::get_p(selected_photons)")
    df = df.Define("selected_photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(selected_photons)")
    df = df.Define("selected_photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(selected_photons)")
    df = df.Define("selected_photons_no", "FCCAnalyses::ReconstructedParticle::get_n(selected_photons)")
    
    results.append(df.Histo1D(("selected_photons_p", "", *bins_p), "selected_photons_p"))
    results.append(df.Histo1D(("selected_photons_theta", "", *bins_theta), "selected_photons_theta"))
    results.append(df.Histo1D(("selected_photons_phi", "", *bins_phi), "selected_photons_phi"))
    results.append(df.Histo1D(("selected_photons_no", "", *bins_count), "selected_photons_no"))
    
    
    # require at least 2 photons
    df = df.Filter("selected_photons_no == 2")
    
    # make the resonance
    df = df.Define("resonance", "FCCAnalyses::resonanceHBuilder(125)(selected_photons)")
    df = df.Filter("resonance.size() > 0")
    
    df = df.Define("resonance_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance)")
    df = df.Define("resonance_p", "FCCAnalyses::ReconstructedParticle::get_p(resonance)")
    df = df.Define("resonance_recoil",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(resonance)")
    df = df.Define("recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance_recoil)")

    results.append(df.Histo1D(("resonance_m", "", *bins_m_gaga), "resonance_m"))
    results.append(df.Histo1D(("resonance_p", "", *bins_p_gaga), "resonance_p"))
    results.append(df.Histo1D(("resonance_recoil", "", *bins_recoil), "recoil_m"))
     
    # remove photons from collection
    df = df.Define("ReconstructedParticles_trimmed", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, selected_photons)")
    df = df.Define("RP_px",          "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles_trimmed)")
    df = df.Define("RP_py",          "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles_trimmed)")
    df = df.Define("RP_pz",          "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles_trimmed)")
    df = df.Define("RP_e",           "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles_trimmed)")
    df = df.Define("RP_m",           "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles_trimmed)")
    df = df.Define("RP_q",           "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles_trimmed)")
    df = df.Define("pseudo_jets",    "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
        
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 2, 1, 0)(pseudo_jets)")
    #df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
    #df = df.Define("clustered_jets", "JetClustering::clustering_antikt(1.0, 0, 2, 0, 0)(pseudo_jets)") 
    
    
    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")
    
    df = df.Define("jets_tlv", "FCCAnalyses::jetsToTlv(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jet0_e", "jets_tlv[0].E()")
    df = df.Define("jet1_e", "jets_tlv[1].E()")
    df = df.Define("jet_sum_e", "jet0_e+jet1_e")
    
    
    results.append(df.Histo1D(("jet0_e", "", *jet_E), "jet0_e"))
    results.append(df.Histo1D(("jet1_e", "", *jet_E), "jet1_e"))
    results.append(df.Histo1D(("jet_sum_e", "", *jet_E), "jet_sum_e"))
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
    
    

def build_graph_za(df, dataset):

    print("build graph", dataset.name)
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240"]
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    
    
    # all photons
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
    df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")

    results.append(df.Histo1D(("photons_p", "", *bins_p), "photons_p"))
    results.append(df.Histo1D(("photons_theta", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no", "", *bins_count), "photons_no"))
    
    df = df.Define("photons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(photons, ReconstructedParticles)") 
    results.append(df.Histo1D(("photons_iso", "", *bins_iso), "photons_iso"))
    
    # select photons with momentum p > 30 GeV 
    # Higgs -> gamma gamma produces on average 125/2 = 62.5 GeV photons
    df = df.Define("preselected_photons", "FCCAnalyses::ReconstructedParticle::sel_p(15)(photons)")
    df = df.Define("preselected_photons_p", "FCCAnalyses::ReconstructedParticle::get_p(preselected_photons)")
    df = df.Define("preselected_photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(preselected_photons)")
    df = df.Define("preselected_photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(preselected_photons)")
    df = df.Define("preselected_photons_no", "FCCAnalyses::ReconstructedParticle::get_n(preselected_photons)")
    df = df.Define("preselected_photons_iso", "FCCAnalyses::coneIsolation(0.01, 0.5)(preselected_photons, ReconstructedParticles)") 

    
    results.append(df.Histo1D(("preselected_photons_p", "", *bins_p), "preselected_photons_p"))
    results.append(df.Histo1D(("preselected_photons_theta", "", *bins_theta), "preselected_photons_theta"))
    results.append(df.Histo1D(("preselected_photons_phi", "", *bins_phi), "preselected_photons_phi"))
    results.append(df.Histo1D(("preselected_photons_no", "", *bins_count), "preselected_photons_no"))
    results.append(df.Histo1D(("preselected_photons_iso", "", *bins_iso), "preselected_photons_iso"))
    
    
    df = df.Define("selected_photons", "FCCAnalyses::sel_iso(0.01)(preselected_photons, preselected_photons_iso)")
    df = df.Define("selected_photons_p", "FCCAnalyses::ReconstructedParticle::get_p(selected_photons)")
    df = df.Define("selected_photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(selected_photons)")
    df = df.Define("selected_photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(selected_photons)")
    df = df.Define("selected_photons_no", "FCCAnalyses::ReconstructedParticle::get_n(selected_photons)")
    
    results.append(df.Histo1D(("selected_photons_p", "", *bins_p), "selected_photons_p"))
    results.append(df.Histo1D(("selected_photons_theta", "", *bins_theta), "selected_photons_theta"))
    results.append(df.Histo1D(("selected_photons_phi", "", *bins_phi), "selected_photons_phi"))
    results.append(df.Histo1D(("selected_photons_no", "", *bins_count), "selected_photons_no"))
    
    
    # select hadronic Z decays
    df = df.Define("hadronicDecays", "FCCAnalyses::hadronicDecays(Particle, Particle1)")
    df = df.Filter("hadronicDecays")
    
    
    # require at least 2 photons
    df = df.Filter("selected_photons_no == 1")
    
    # make the resonance
    #df = df.Define("resonance", "FCCAnalyses::resonanceHBuilder(125)(selected_photons)")
    #df = df.Filter("resonance.size() > 0")
    
    #df = df.Define("resonance_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance)")
    #df = df.Define("resonance_p", "FCCAnalyses::ReconstructedParticle::get_p(resonance)")
    #df = df.Define("resonance_recoil",  "FCCAnalyses::ReconstructedParticle::recoilBuilder(240)(resonance)")
    #df = df.Define("recoil_m", "FCCAnalyses::ReconstructedParticle::get_mass(resonance_recoil)")

    #results.append(df.Histo1D(("resonance_m", "", *bins_m_gaga), "resonance_m"))
    #results.append(df.Histo1D(("resonance_p", "", *bins_p_gaga), "resonance_p"))
    #results.append(df.Histo1D(("resonance_recoil", "", *bins_recoil), "recoil_m"))
     
    # remove photons from collection
    df = df.Define("ReconstructedParticles_trimmed", "FCCAnalyses::ReconstructedParticle::remove(ReconstructedParticles, selected_photons)")
    df = df.Define("RP_px",          "FCCAnalyses::ReconstructedParticle::get_px(ReconstructedParticles_trimmed)")
    df = df.Define("RP_py",          "FCCAnalyses::ReconstructedParticle::get_py(ReconstructedParticles_trimmed)")
    df = df.Define("RP_pz",          "FCCAnalyses::ReconstructedParticle::get_pz(ReconstructedParticles_trimmed)")
    df = df.Define("RP_e",           "FCCAnalyses::ReconstructedParticle::get_e(ReconstructedParticles_trimmed)")
    df = df.Define("RP_m",           "FCCAnalyses::ReconstructedParticle::get_mass(ReconstructedParticles_trimmed)")
    df = df.Define("RP_q",           "FCCAnalyses::ReconstructedParticle::get_charge(ReconstructedParticles_trimmed)")
    df = df.Define("pseudo_jets",    "FCCAnalyses::JetClusteringUtils::set_pseudoJets(RP_px, RP_py, RP_pz, RP_e)")
        
    
    # more info: https://indico.cern.ch/event/1173562/contributions/4929025/attachments/2470068/4237859/2022-06-FCC-jets.pdf
    # https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/JetClustering.cc
    df = df.Define("clustered_jets", "JetClustering::clustering_ee_kt(2, 4, 1, 0)(pseudo_jets)")
    #df = df.Define("clustered_jets", "JetClustering::clustering_ee_genkt(1.5, 0, 0, 0, 0, -1)(pseudo_jets)")
    #df = df.Define("clustered_jets", "JetClustering::clustering_antikt(1.0, 0, 2, 0, 0)(pseudo_jets)") 
    
    
    df = df.Define("jets", "FCCAnalyses::JetClusteringUtils::get_pseudoJets(clustered_jets)")
    df = df.Define("jetconstituents", "FCCAnalyses::JetClusteringUtils::get_constituents(clustered_jets)")
    df = df.Define("jets_e", "FCCAnalyses::JetClusteringUtils::get_e(jets)")
    df = df.Define("jets_px", "FCCAnalyses::JetClusteringUtils::get_px(jets)")
    df = df.Define("jets_py", "FCCAnalyses::JetClusteringUtils::get_py(jets)")
    df = df.Define("jets_pz", "FCCAnalyses::JetClusteringUtils::get_pz(jets)")
    df = df.Define("jets_m", "FCCAnalyses::JetClusteringUtils::get_m(jets)")
    
    df = df.Define("jets_tlv", "FCCAnalyses::jetsToTlv(jets_px, jets_py, jets_pz, jets_e)")
    df = df.Define("jet0_e", "jets_tlv[0].E()")
    df = df.Define("jet1_e", "jets_tlv[1].E()")
    df = df.Define("jet2_e", "jets_tlv[2].E()")
    df = df.Define("jet3_e", "jets_tlv[3].E()")
    df = df.Define("jet_sum_e", "jet0_e+jet1_e+jet2_e+jet3_e")
    
    
    results.append(df.Histo1D(("jet0_e", "", *jet_E), "jet0_e"))
    results.append(df.Histo1D(("jet1_e", "", *jet_E), "jet1_e"))
    results.append(df.Histo1D(("jet2_e", "", *jet_E), "jet2_e"))
    results.append(df.Histo1D(("jet3_e", "", *jet_E), "jet3_e"))
    results.append(df.Histo1D(("jet_sum_e", "", *jet_E), "jet_sum_e"))
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


    baseDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
    wzp6_ee_nunuH_Haa_ecm240 = {"name": "wzp6_ee_nunuH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_nunuH_Haa_ecm240",  "xsec": 0.0001049}
    wzp6_ee_eeH_Haa_ecm240 = {"name": "wzp6_ee_eeH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_eeH_Haa_ecm240",  "xsec": 1.626e-05}
    wzp6_ee_bbH_Haa_ecm240 = {"name": "wzp6_ee_bbH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_bbH_Haa_ecm240",  "xsec": 6.803e-05}
    wzp6_ee_ssH_Haa_ecm240 = {"name": "wzp6_ee_ssH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_ssH_Haa_ecm240",  "xsec": 6.8e-05}
    wzp6_ee_tautauH_Haa_ecm240 = {"name": "wzp6_ee_tautauH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_tautauH_Haa_ecm240",  "xsec": 1.533e-05}
    wzp6_ee_qqH_Haa_ecm240 = {"name": "wzp6_ee_qqH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_qqH_Haa_ecm240",  "xsec": 0.0001211}
    wzp6_ee_ccH_Haa_ecm240 = {"name": "wzp6_ee_ccH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_ccH_Haa_ecm240",  "xsec": 5.298e-05}
    wzp6_ee_mumuH_Haa_ecm240 = {"name": "wzp6_ee_mumuH_Haa_ecm240", "datadir": f"{baseDir}/wzp6_ee_mumuH_Haa_ecm240",  "xsec": 1.535e-05}
    datasets = [wzp6_ee_nunuH_Haa_ecm240, wzp6_ee_eeH_Haa_ecm240, wzp6_ee_bbH_Haa_ecm240, wzp6_ee_ssH_Haa_ecm240, wzp6_ee_tautauH_Haa_ecm240, wzp6_ee_qqH_Haa_ecm240, wzp6_ee_ccH_Haa_ecm240, wzp6_ee_mumuH_Haa_ecm240]
    
    #result = functions.build_and_run(datasets, build_graph_aa, "tmp/output_higgs_gaga.root", maxFiles=args.maxFiles)
 
    baseDir = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/"
    wzp6_ee_nunuH_HZa_ecm240 = {"name": "wzp6_ee_nunuH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_nunuH_HZa_ecm240",  "xsec": 0.0001049}
    wzp6_ee_eeH_HZa_ecm240 = {"name": "wzp6_ee_eeH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_eeH_HZa_ecm240",  "xsec": 1.626e-05}
    wzp6_ee_bbH_HZa_ecm240 = {"name": "wzp6_ee_bbH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_bbH_HZa_ecm240",  "xsec": 6.803e-05}
    wzp6_ee_ssH_HZa_ecm240 = {"name": "wzp6_ee_ssH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_ssH_HZa_ecm240",  "xsec": 6.8e-05}
    wzp6_ee_tautauH_HZa_ecm240 = {"name": "wzp6_ee_tautauH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_tautauH_HZa_ecm240",  "xsec": 1.533e-05}
    wzp6_ee_qqH_HZa_ecm240 = {"name": "wzp6_ee_qqH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_qqH_HZa_ecm240",  "xsec": 0.0001211}
    wzp6_ee_ccH_HZa_ecm240 = {"name": "wzp6_ee_ccH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_ccH_HZa_ecm240",  "xsec": 5.298e-05}
    wzp6_ee_mumuH_HZa_ecm240 = {"name": "wzp6_ee_mumuH_HZa_ecm240", "datadir": f"{baseDir}/wzp6_ee_mumuH_HZa_ecm240",  "xsec": 1.535e-05}
    datasets = [wzp6_ee_nunuH_HZa_ecm240, wzp6_ee_eeH_HZa_ecm240, wzp6_ee_bbH_HZa_ecm240, wzp6_ee_ssH_HZa_ecm240, wzp6_ee_tautauH_HZa_ecm240, wzp6_ee_qqH_HZa_ecm240, wzp6_ee_ccH_HZa_ecm240, wzp6_ee_mumuH_HZa_ecm240]
 
    result = functions.build_and_run(datasets, build_graph_za, "tmp/output_higgs_za.root", maxFiles=args.maxFiles) 

    
    
