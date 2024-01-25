
import functions
import helpers
import ROOT
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)


# define histograms
bins_p = (25000, 0, 250) # 10 MeV bins
bins_m_ll = (25000, 0, 250) # 10 MeV bins
bins_p_ll = (25000, 0, 250) # 10 MeV bins
bins_recoil = (200000, 0, 200) # 1 MeV bins 
bins_cosThetaMiss = (100000, -1, 1)

bins_p_beam = (100000, 75, 85) # 0.1 MeV bins

bins_theta = (320, -4, 4)
bins_phi = (80, -4, 4)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)
bins_dR = (1000, 0, 10)

bins_massweights = (5, 0, 5)

bins_reso = (10000, 0.95, 1.05)
bins_ecm_eff = (1000, 0.0, 1.0)
bins_cos = (100, -1, 1)
bins_acolinearity_deg = (1000, 0.0, 90.0)
bins_acolinearity_rad = (1000, 0.0, 1.0)

bins_theta_abs = (100, 0, 2)


bins_resolution = (10000, 0.95, 1.05)
bins_resolution_1 = (20000, 0, 2)

jet_energy = (1000, 0, 100) # 100 MeV bins
dijet_m = (2000, 0, 200) # 100 MeV bins
visMass = (2000, 0, 200) # 100 MeV bins
missEnergy  = (5000, 0, 500) # 100 MeV bins

dijet_m_final = (500, 50, 100) # 100 MeV bins
bins_ebalance = (1000, 0, 1)

def build_graph(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []
    
    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")
    sigProcs = []
    
    
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
    df = df.Alias("Photon0", "Photon#0.index")
    df = df.Alias("Muon0", "Muon#0.index")

    # gen photons
    df = df.Define("gen_photons", "FCCAnalyses::get_gen_pdg(Particle, 22)")
    df = df.Define("gen_photons_p", "FCCAnalyses::MCParticle::get_p(gen_photons)")
    df = df.Define("gen_photons_theta", "FCCAnalyses::MCParticle::get_theta(gen_photons)")
    df = df.Define("gen_photons_phi", "FCCAnalyses::MCParticle::get_phi(gen_photons)")
    df = df.Define("gen_photons_no", "FCCAnalyses::MCParticle::get_n(gen_photons)")
    results.append(df.Histo1D(("gen_photons_p", "", *bins_p), "gen_photons_p"))
    results.append(df.Histo1D(("gen_photons_theta", "", *bins_theta), "gen_photons_theta"))
    results.append(df.Histo1D(("gen_photons_phi", "", *bins_phi), "gen_photons_phi"))
    results.append(df.Histo1D(("gen_photons_no", "", *bins_count), "gen_photons_no"))
    
    # reco photons
    df = df.Define("photons", "FCCAnalyses::ReconstructedParticle::get(Photon0, ReconstructedParticles)")
    df = df.Define("photons_p", "FCCAnalyses::ReconstructedParticle::get_p(photons)")
    df = df.Define("photons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(photons)")
    df = df.Define("photons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(photons)")
    df = df.Define("photons_no", "FCCAnalyses::ReconstructedParticle::get_n(photons)")
    results.append(df.Histo1D(("photons_p", "", *bins_p), "photons_p"))
    results.append(df.Histo1D(("photons_theta", "", *bins_theta), "photons_theta"))
    results.append(df.Histo1D(("photons_phi", "", *bins_phi), "photons_phi"))
    results.append(df.Histo1D(("photons_no", "", *bins_count), "photons_no"))
    
    
    # gen leptons
    df = df.Define("gen_leptons", "FCCAnalyses::get_gen_pdg(Particle, 13)")
    df = df.Define("gen_leptons_p", "FCCAnalyses::MCParticle::get_p(gen_leptons)")
    df = df.Define("gen_leptons_theta", "FCCAnalyses::MCParticle::get_theta(gen_leptons)")
    df = df.Define("gen_leptons_phi", "FCCAnalyses::MCParticle::get_phi(gen_leptons)")
    df = df.Define("gen_leptons_charge", "FCCAnalyses::MCParticle::get_charge(gen_leptons)")
    df = df.Define("gen_leptons_no", "FCCAnalyses::MCParticle::get_n(gen_leptons)")
    results.append(df.Histo1D(("gen_leptons_p", "", *bins_p), "gen_leptons_p"))
    results.append(df.Histo1D(("gen_leptons_theta", "", *bins_theta), "gen_leptons_theta"))
    results.append(df.Histo1D(("gen_leptons_phi", "", *bins_phi), "gen_leptons_phi"))
    results.append(df.Histo1D(("gen_leptons_charge", "", *bins_charge), "gen_leptons_charge"))
    results.append(df.Histo1D(("gen_leptons_no", "", *bins_count), "gen_leptons_no"))
    
    
    # reco leptons
    df = df.Define("leptons", "FCCAnalyses::ReconstructedParticle::get(Muon0, ReconstructedParticles)")
    df = df.Define("leptons_p", "FCCAnalyses::ReconstructedParticle::get_p(leptons)")
    df = df.Define("leptons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(leptons)")
    df = df.Define("leptons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(leptons)")
    df = df.Define("leptons_charge", "FCCAnalyses::ReconstructedParticle::get_charge(leptons)")
    df = df.Define("leptons_no", "FCCAnalyses::ReconstructedParticle::get_n(leptons)")
    results.append(df.Histo1D(("leptons_p", "", *bins_p), "leptons_p"))
    results.append(df.Histo1D(("leptons_theta", "", *bins_theta), "leptons_theta"))
    results.append(df.Histo1D(("leptons_phi", "", *bins_phi), "leptons_phi"))
    results.append(df.Histo1D(("leptons_charge", "", *bins_charge), "leptons_charge"))
    results.append(df.Histo1D(("leptons_no", "", *bins_count), "leptons_no"))
    
    
    # lepton resolution
    df = df.Define("lepton_reso_p", "FCCAnalyses::leptonResolution_p(leptons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("lepton_reso_theta", "FCCAnalyses::leptonResolution_theta(leptons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    df = df.Define("lepton_reso_phi", "FCCAnalyses::leptonResolution_phi(leptons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle)")
    results.append(df.Histo1D(("lepton_reso_p", "", *bins_reso), "lepton_reso_p"))
    results.append(df.Histo1D(("lepton_reso_theta", "", *bins_reso), "lepton_reso_theta"))
    results.append(df.Histo1D(("lepton_reso_phi", "", *bins_reso), "lepton_reso_phi"))
    
    # beam electrons
    df = df.Define("beam_electrons", "FCCAnalyses::kkmc_get_beam_electrons(Particle, Particle0)")
    df = df.Define("beam_electrons_p", "FCCAnalyses::MCParticle::get_p(beam_electrons)")
    df = df.Define("beam_electrons_theta", "FCCAnalyses::MCParticle::get_theta(beam_electrons)")
    df = df.Define("beam_electrons_phi", "FCCAnalyses::MCParticle::get_phi(beam_electrons)")
    df = df.Define("beam_electrons_charge", "FCCAnalyses::MCParticle::get_charge(beam_electrons)")
    df = df.Define("beam_electrons_no", "FCCAnalyses::MCParticle::get_n(beam_electrons)")
    df = df.Define("crossingAngle", "FCCAnalyses::crossingAngle(beam_electrons)")
    results.append(df.Histo1D(("beam_electrons_p", "", *bins_p_beam), "beam_electrons_p"))
    results.append(df.Histo1D(("beam_electrons_theta", "", *bins_theta), "beam_electrons_theta"))
    results.append(df.Histo1D(("beam_electrons_phi", "", *bins_phi), "beam_electrons_phi"))
    results.append(df.Histo1D(("beam_electrons_charge", "", *bins_charge), "beam_electrons_charge"))
    results.append(df.Histo1D(("beam_electrons_no", "", *bins_count), "beam_electrons_no"))
    results.append(df.Histo1D(("beam_electrons_crossingAngle", "", *bins_phi), "crossingAngle"))
    
    # reconstruct resonance
    df = df.Filter("leptons_no == 2")
    df = df.Define("leptons_tlv", "FCCAnalyses::makeLorentzVectors(leptons)")
    df = df.Define("m_ll", "(leptons_tlv[0]+leptons_tlv[1]).M()")
    df = df.Define("p_ll", "(leptons_tlv[0]+leptons_tlv[1]).P()")
    results.append(df.Histo1D(("m_ll", "", *bins_m_ll), "m_ll"))
    results.append(df.Histo1D(("p_ll", "", *bins_p_ll), "p_ll"))
  

    # muon angular analysis (effective ECM, AFB, acolinearity, ...)
    df = df.Define("theta_plus", "(leptons_charge[0] > 0) ? leptons_theta[0] : leptons_theta[1]")
    df = df.Define("theta_minus", "(leptons_charge[0] < 0) ? leptons_theta[0] : leptons_theta[1]")
    df = df.Define("cos_theta_plus", "cos(theta_plus)")
    df = df.Define("cos_theta_minus", "cos(theta_minus)")
    df = df.Define("acolinearity_rad", "FCCAnalyses::acolinearity(leptons)")
    df = df.Define("acolinearity_deg", "acolinearity_rad*180./acos(-1)")
    
    df = df.Define("cosThetac", "(sin(theta_plus-theta_minus))/(sin(theta_plus)+sin(theta_minus))")
    df = df.Define("ecm_eff", "(sin(theta_plus) + sin(theta_minus) - sin(theta_plus+theta_minus))/(sin(theta_plus) + sin(theta_minus) + sin(theta_plus+theta_minus))")
    
    results.append(df.Histo1D(("theta_plus", "", *bins_theta), "theta_plus"))
    results.append(df.Histo1D(("theta_minus", "", *bins_theta), "theta_minus"))
    results.append(df.Histo1D(("cos_theta_plus", "", *bins_cos), "cos_theta_plus"))
    results.append(df.Histo1D(("cos_theta_minus", "", *bins_cos), "cos_theta_minus"))
    results.append(df.Histo1D(("cosThetac", "", *bins_cos), "cosThetac"))
    results.append(df.Histo1D(("ecm_eff", "", *bins_ecm_eff), "ecm_eff"))
    results.append(df.Histo1D(("acolinearity_rad", "", *bins_acolinearity_rad), "acolinearity_rad"))
    results.append(df.Histo1D(("acolinearity_deg", "", *bins_acolinearity_deg), "acolinearity_deg"))
  
    return results, weightsum
    


if __name__ == "__main__":

    datadict = {"basePath": "/"} # allow to run locally
    #datadict['yfswwp8_ww_mumu_ecm160_born'] = {"xsec": 0.03792974, "path": "/work/submit/jaeyserm/fccee/FCCProducer/generator/yfsww3-1.18-export/demo/output_born.root"}
    #datadict['yfswwp8_ww_mumu_ecm160'] = {"xsec": 0.02692397, "path": "/work/submit/jaeyserm/fccee/FCCProducer/generator/yfsww3-1.18-export/demo/output.root"}
    
    datadict['output_160_nom'] = {"xsec": 0.02692397, "path": "/work/submit/jaeyserm/fccee/FCCProducer/generator/yfsww3-1.18-export/demo/output_160_nom.root"}
    datadict['output_158_nom'] = {"xsec": 0.02692397, "path": "/work/submit/jaeyserm/fccee/FCCProducer/generator/yfsww3-1.18-export/demo/output_158_nom.root"}
    datadict['output_158_alt'] = {"xsec": 0.02692397, "path": "/work/submit/jaeyserm/fccee/FCCProducer/generator/yfsww3-1.18-export/demo/output_158_alt.root"}

    datasets_to_run = ["yfswwp8_ww_mumu_ecm160_born", "yfswwp8_ww_mumu_ecm160"]
    functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_yfswwp8_validation.root", args)
