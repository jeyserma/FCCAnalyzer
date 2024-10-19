
import functions
import helpers
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
parser.add_argument("--flavor", type=str, help="Flavor (mumu or ee)", choices=["mumu", "ee"], default="mumu")
parser.add_argument("--ecm", type=int, help="Center-of-mass energy", choices=[240, 365], default=240)
parser.add_argument("--type", type=str, help="Run type (mass or xsec)", choices=["mass", "xsec"], default="mass")
parser.add_argument("--tag", type=str, help="Analysis tag", default="july24")
parser.add_argument('--gen', action='store_true', help="Do gen-level analysis")
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/higgs_mass_xsec/functions.h")
functions.add_include_file("analyses/higgs_mass_xsec/functions_gen.h")



# define histograms
bins_p_mu = (2000, 0, 200) # 100 MeV bins
bins_m_ll = (2000, 0, 200) # 100 MeV bins
bins_p_ll = (200, 0, 200) # 1 GeV bins
bins_recoil = (20000, 0, 200) # 10 MeV bins 
bins_recoil_fine = (20000, 120, 140) # 1 MeV bins 
bins_cosThetaMiss = (10000, 0, 1)

bins_theta = (500, 0, 5)
bins_phi = (500, -5, 5)
bins_aco = (400, -4, 4)

bins_count = (50, 0, 50)
bins_pdgid = (60, -30, 30)
bins_charge = (10, -5, 5)
bins_iso = (500, 0, 5)
bins_dR = (1000, 0, 10)

bins_cat = (10, 0, 10)
bins_resolution = (10000, -0.05, 0.05)

gen_ = "true" if args.gen else "false"

def build_graph(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []
    sigProcs = ["wzp6_ee_mumuH_ecm240", "wzp6_ee_eeH_ecm240", "wzp6_ee_mumuH_ecm365", "wzp6_ee_eeH_ecm365"]
    df = df.Define("ecm", f"{args.ecm}")

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")



    if 'fullsim' in dataset.name:
        df = df.Define("muons", f"FCCAnalyses::sel_type(13, PandoraPFOs)")
        #df = df.Alias("muons", "PandoraPFOs")
        df = df.Alias("Particle", "MCParticles")
        df = df.Alias("Particle0", "_MCParticles_parents.index")
        df = df.Alias("Particle1", "_MCParticles_daughters.index")
        #df = df.Alias("MCRecoAssociations0", "_RecoMCTruthLink_rec.index")
        #df = df.Alias("MCRecoAssociations1", "_RecoMCTruthLink_sim.index")
    else:
        df = df.Alias("Particle0", "Particle#0.index")
        df = df.Alias("Particle1", "Particle#1.index")
        #df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
        #df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")
        df = df.Alias("Muon", "Muon#0.index")

        df = df.Define("muons", "FCCAnalyses::ReconstructedParticle::get(Muon, ReconstructedParticles)")

    # get gen particle - assume only 1 particle in the event (first two are the vertex)
    df = df.Define("mc_particles_tlv", "FCCAnalyses::makeLorentzVectors(Particle)")
    df = df.Define("muon_gen", "mc_particles_tlv[2]")
    df = df.Define("muon_gen_p", "muon_gen.P()")
    df = df.Define("muon_gen_theta", "muon_gen.Theta()")
    df = df.Define("muon_gen_phi", "muon_gen.Phi()")

    #df = df.Filter("muon_gen_p > 1")

    #df = df.Define("muons_gen", f"FCCAnalyses::sel_type(13, Particle)")

    #df = df.Define("RP_MC_index", "FCCAnalyses::ReconstructedParticle2MC::getRP2MC_index(MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles)")
    #df = df.Define("muons_reso_p", "FCCAnalyses::leptonResolution_p(muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, RP_MC_index)")
    

    # all leptons (bare)
    df = df.Define("muons_p", "FCCAnalyses::ReconstructedParticle::get_p(muons)")
    df = df.Define("muons_theta", "FCCAnalyses::ReconstructedParticle::get_theta(muons)")
    df = df.Define("muons_phi", "FCCAnalyses::ReconstructedParticle::get_phi(muons)")
    df = df.Define("muons_q", "FCCAnalyses::ReconstructedParticle::get_charge(muons)")
    df = df.Define("muons_plus", "muons_q > 0")
    df = df.Define("muons_minus", "muons_q < 0")

    df = df.Define("muons_reso_p", "(muons_p - muon_gen_p) / muon_gen_p")
    df = df.Define("muons_reso_theta", "(muons_theta - muon_gen_theta) / muon_gen_theta")
    df = df.Define("muons_reso_phi", "(muons_phi - muon_gen_phi) / muon_gen_phi")
    df = df.Define("muons_plus_reso_p", "(muons_p[muons_plus] - muon_gen_p) / muon_gen_p")
    df = df.Define("muons_minus_reso_p", "(muons_p[muons_minus] - muon_gen_p) / muon_gen_p")

    results.append(df.Histo1D(("muons_p", "", *bins_p_mu), "muons_p"))
    results.append(df.Histo1D(("muons_theta", "", *bins_theta), "muons_theta"))
    results.append(df.Histo1D(("muons_phi", "", *bins_phi), "muons_phi"))
    results.append(df.Histo1D(("muons_reso_p", "", *bins_resolution), "muons_reso_p"))
    results.append(df.Histo1D(("muons_reso_theta", "", *bins_resolution), "muons_reso_theta"))
    results.append(df.Histo1D(("muons_reso_phi", "", *bins_resolution), "muons_reso_phi"))
    results.append(df.Histo1D(("muons_plus_reso_p", "", *bins_resolution), "muons_plus_reso_p"))
    results.append(df.Histo1D(("muons_minus_reso_p", "", *bins_resolution), "muons_minus_reso_p"))

    return results, weightsum


if __name__ == "__main__":

    datadict = {}
    datadict['basePath'] = '/ceph/submit/data/group/cms/store/fccee/particlegun/'
    #datadict['delphes_gun'] = {'xsec': 1, 'path': 'gun_test_delphes.root'}
    #datadict['fullsim_gun'] = {'xsec': 1, 'path': 'gun_test_fullsim.root'}


    guns = ["mu_theta_10-90_p_100", "mu_theta_10-90_p_75", "mu_theta_10-90_p_50", "mu_theta_10-90_p_40", "mu_theta_10-90_p_30", "mu_theta_10-90_p_20", "mu_theta_10-90_p_10", "mu_theta_10-90_p_5", "mu_theta_10-90_p_4", "mu_theta_10-90_p_3", "mu_theta_10-90_p_2", "mu_theta_90_p_20-80", "mu_theta_90_p_20-80_new", "mu_theta_85_p_20-80", "mu_theta_84_p_20-80", "mu_theta_83_p_20-80", "mu_theta_82_p_20-80", "mu_theta_81_p_20-80", "mu_theta_80_p_20-80", "mu_theta_75_p_20-80", "mu_theta_70_p_20-80", "mu_theta_60_p_20-80", "mu_theta_50_p_20-80", "mu_theta_40_p_20-80", "mu_theta_30_p_20-80", "mu_theta_20_p_20-80", "mu_theta_10_p_20-80"]

    guns = ["mu_theta_10-90_p_100", "mu_theta_10-90_p_75", "mu_theta_10-90_p_50", "mu_theta_10-90_p_40", "mu_theta_10-90_p_30", "mu_theta_10-90_p_20", "mu_theta_10-90_p_10", "mu_theta_10-90_p_5", "mu_theta_10-90_p_4", "mu_theta_10-90_p_3", "mu_theta_10-90_p_2", "mu_theta_90_p_20-80", "mu_theta_85_p_20-80", "mu_theta_80_p_20-80", "mu_theta_75_p_20-80", "mu_theta_70_p_20-80", "mu_theta_60_p_20-80", "mu_theta_50_p_20-80", "mu_theta_40_p_20-80", "mu_theta_30_p_20-80", "mu_theta_20_p_20-80", "mu_theta_10_p_20-80"]

    datasets_to_run = []
    for gun in guns:
        datadict[f'{gun}_delphes'] = {'xsec': 1, 'path': f'{gun}_delphes.root'}
        datadict[f'{gun}_delphes_SiTracking'] = {'xsec': 1, 'path': f'{gun}_delphes_SiTracking.root'}
        datadict[f'{gun}_fullsim'] = {'xsec': 1, 'path': f'{gun}_fullsim.root'}

        datasets_to_run.append(f'{gun}_delphes')
        datasets_to_run.append(f'{gun}_delphes_SiTracking')
        datasets_to_run.append(f'{gun}_fullsim')


    functions.build_and_run(datadict, datasets_to_run, build_graph, f"particlegun.root", args)


