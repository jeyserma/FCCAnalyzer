
import functions
import helpers
import argparse
import logging

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)

functions.add_include_file("analyses/higgs_mass_xsec/functions.h")
functions.add_include_file("analyses/higgs_mass_xsec/functions_gen.h")


bins_def = (500, 0, 500) # 100 MeV bins


def build_graph(df, dataset):

    logger.info(f"Build graph {dataset.name}")
    results = []
    
    ecm = 240 if '240' in dataset.name else 365

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")


    df = df.Define("visibleMass_reco", "FCCAnalyses::visibleMass(ReconstructedParticles)")
    df = df.Define("missingMass_reco", f"FCCAnalyses::missingMass({ecm}, ReconstructedParticles)")

    df = df.Define("visibleMass_gen", "FCCAnalyses::visibleMass(Particle)")
    df = df.Define("missingMass_gen", f"FCCAnalyses::missingMass({ecm}, Particle)") # it filters out the neutrinos


    results.append(df.Histo1D(("visibleMass_reco", "", *bins_def), "visibleMass_reco"))
    results.append(df.Histo1D(("missingMass_reco", "", *bins_def), "missingMass_reco"))

    results.append(df.Histo1D(("visibleMass_gen", "", *bins_def), "visibleMass_gen"))
    results.append(df.Histo1D(("missingMass_gen", "", *bins_def), "missingMass_gen"))

    df = df.Define("higgs_recoil_gen", f"FCCAnalyses::get_higgs_recoil({ecm}, Particle)")
    results.append(df.Histo1D(("higgs_recoil_gen", "", *bins_def), "higgs_recoil_gen"))

    df = df.Define("from_prompt", f"FCCAnalyses::neutrinos_from_prompt(Particle, Particle0)")

    df = df.Filter("from_prompt.size() == 4")
    df = df.Define("nu1", "ROOT::Math::PxPyPzMVector(from_prompt[0].momentum.x, from_prompt[0].momentum.y, from_prompt[0].momentum.z, from_prompt[0].mass)")
    df = df.Define("nu2", "ROOT::Math::PxPyPzMVector(from_prompt[1].momentum.x, from_prompt[1].momentum.y, from_prompt[1].momentum.z, from_prompt[1].mass)")
    df = df.Define("dinu", "nu1+nu2")
    df = df.Define("dinu_m", "dinu.M()")

    #df = df.Define("from_prompt_pdgid", "from_prompt[0].PDG")
    #df = df.Define("from_prompt_pdgid", "from_prompt.size()")
    results.append(df.Histo1D(("dinu_m", "", *bins_def), "dinu_m"))

    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts()
    datasets_to_run = ['wzp6_ee_nunuH_ecm240', 'wzp6_ee_nunuH_ecm365']

    datasets_to_run = ['wzp6_ee_nunuH_Haa_ecm365']
    
    datasets_to_run = ['wzp6_ee_nuenueH_Haa_ecm365', 'wzp6_ee_numunumuH_Haa_ecm365', 'wzp6_ee_nunuH_Haa_ecm365']
    lumi = 1080000 # 10.8 ab-1
    functions.build_and_run(datadict, datasets_to_run, build_graph, f"zh_vvh_study.root", args, norm=True, lumi=lumi)
