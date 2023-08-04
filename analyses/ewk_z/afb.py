
import functions
import helpers
import ROOT
import argparse

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)

# define histograms
bins_p_mu = (20000, 0, 200) # 10 MeV bins
bins_m_ll = (10000, 0, 100) # 10 MeV bins
bins_p_ll = (20000, 0, 200) # 10 MeV bins

bins_theta = (500, -5, 5)
bins_phi = (500, -5, 5)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)

bins_cos = (100, -1, 1)

def build_graph(df, dataset):

    print("build graph", dataset.name)
    hists = []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Lepton0", "Muon#0.index")
    
    # gen muons
    df = df.Define("gen_muons", "FCCAnalyses::get_gen_pdg(Particle, 13)") # muon pdg index=13
    df = df.Define("gen_muons_p", "FCCAnalyses::MCParticle::get_p(gen_muons)")
    df = df.Define("gen_muons_theta", "FCCAnalyses::MCParticle::get_theta(gen_muons)")
    df = df.Define("gen_muons_phi", "FCCAnalyses::MCParticle::get_phi(gen_muons)")
    df = df.Define("gen_muons_no", "FCCAnalyses::MCParticle::get_n(gen_muons)")
    
    hists.append(df.Histo1D(("gen_muons_p", "", *bins_p_mu), "gen_muons_p"))
    hists.append(df.Histo1D(("gen_muons_theta", "", *bins_theta), "gen_muons_theta"))
    hists.append(df.Histo1D(("gen_muons_phi", "", *bins_phi), "gen_muons_phi"))
    hists.append(df.Histo1D(("gen_muons_no", "", *bins_count), "gen_muons_no"))
    
    hists.append(df.Histo1D(("evts_initial", "", *bins_count), "weight"))
    
    # get the leptons leptons
    df = df.Define("leps_all", "FCCAnalyses::ReconstructedParticle::get(Lepton0, ReconstructedParticles)")
    df = df.Define("leps_all_p", "FCCAnalyses::ReconstructedParticle::get_p(leps_all)")
    df = df.Define("leps_all_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leps_all)")
    df = df.Define("leps_all_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leps_all)")
    df = df.Define("leps_all_q", "FCCAnalyses::ReconstructedParticle::get_charge(leps_all)")
    df = df.Define("leps_all_no", "FCCAnalyses::ReconstructedParticle::get_n(leps_all)")
    
    # construct Lorentz vectors of the leptons
    df = df.Define("leps_tlv", "FCCAnalyses::makeLorentzVectors(leps_all)")
    df = df.Filter("leps_all_no == 2")
    
    df = df.Define("m_inv", "(leps_tlv[0]+leps_tlv[1]).M()")
    df = df.Filter("m_inv >= 50")
    
    df = df.Define("leps_gen_tlv", "FCCAnalyses::makeLorentzVectors_gen(leps_all, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("lep0_p", "leps_gen_tlv[0].P()")
    
    hists.append(df.Histo1D(("leps_all_gen_p", "", *bins_p_mu), "lep0_p"))
    
    df = df.Define("missingEnergy_vec", "FCCAnalyses::missingEnergy(91., ReconstructedParticles)")
    df = df.Define("missingEnergy", "missingEnergy_vec[0].energy")

    df = df.Define("visibleEnergy", "FCCAnalyses::visibleEnergy(ReconstructedParticles)")
  
    
    hists.append(df.Histo1D(("leps_all_p", "", *bins_p_mu), "leps_all_p"))
    hists.append(df.Histo1D(("leps_all_theta", "", *bins_theta), "leps_all_theta"))
    hists.append(df.Histo1D(("leps_all_phi", "", *bins_phi), "leps_all_phi"))
    hists.append(df.Histo1D(("leps_all_q", "", *bins_charge), "leps_all_q"))
    hists.append(df.Histo1D(("leps_all_no", "", *bins_count), "leps_all_no"))
    
    hists.append(df.Histo1D(("m_inv", "", *bins_m_ll), "m_inv"))
    hists.append(df.Histo1D(("missingEnergy", "", *bins_m_ll), "missingEnergy"))
    hists.append(df.Histo1D(("visibleEnergy", "", *bins_m_ll), "visibleEnergy"))
    
    df = df.Define("theta_plus", "(leps_all_q[0] > 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("theta_minus", "(leps_all_q[0] < 0) ? leps_all_theta[0] : leps_all_theta[1]")
    df = df.Define("cos_theta_plus", "cos(theta_plus)")
    df = df.Define("cos_theta_minus", "cos(theta_minus)")
    df = df.Define("cosThetac", "(sin(theta_plus-theta_minus))/(sin(theta_plus)+sin(theta_minus))")
    
    hists.append(df.Histo1D(("theta_plus", "", *bins_theta), "theta_plus"))
    hists.append(df.Histo1D(("theta_minus", "", *bins_theta), "theta_minus"))
    hists.append(df.Histo1D(("cos_theta_plus", "", *bins_cos), "cos_theta_plus"))
    hists.append(df.Histo1D(("cos_theta_minus", "", *bins_cos), "cos_theta_minus"))
    
    hists.append(df.Histo1D(("cosThetac", "", *bins_cos), "cosThetac"))
    
    hists.append(df.Histo1D(("evts_final", "", *bins_count), "weight"))
    return hists, weightsum

if __name__ == "__main__":

    baseDir = functions.get_basedir()
 
    wzp6_ee_mumu_ecm91p2 = {"name": f"wzp6_ee_mumu_ecm91p2", "datadir": f"/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_mumu_ecm91p2/", "xsec": 1}

    datasets = [wzp6_ee_mumu_ecm91p2]
    result = functions.build_and_run(datasets, build_graph, f"tmp/afb.root", args)
