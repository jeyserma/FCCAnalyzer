
import functions
import helpers
import ROOT
import argparse
import logging

import helper_jetclustering
import helper_flavourtagger

logger = logging.getLogger("fcclogger")

parser = functions.make_def_argparser()
args = parser.parse_args()
functions.set_threads(args)


# define histograms
bins_p = (200, 0, 200) # 100 MeV bins
bins_score = (100, 0, 1)
bins_count = (100, 0, 100)

# setup clustering and flavour tagging
njets = 4 # number of jets to be clustered
jetClusteringHelper = helper_jetclustering.ExclusiveJetClusteringHelper(njets, collection="ReconstructedParticles")
jetFlavourHelper = helper_flavourtagger.JetFlavourHelper(jetClusteringHelper.jets, jetClusteringHelper.constituents)
path = "data/flavourtagger/fccee_flavtagging_edm4hep_wc_v1"
jetFlavourHelper.load(f"{path}.json", f"{path}.onnx")

def build_graph(df, dataset):

    logging.info(f"build graph {dataset.name}")
    results, cols = [], []

    df = df.Define("weight", "1.0")
    weightsum = df.Sum("weight")

    # define collections
    df = df.Alias("Particle0", "Particle#0.index")
    df = df.Alias("Particle1", "Particle#1.index")
    df = df.Alias("MCRecoAssociations0", "MCRecoAssociations#0.index")
    df = df.Alias("MCRecoAssociations1", "MCRecoAssociations#1.index")

    # do clustering and tagging
    df = jetClusteringHelper.define(df)
    df = jetFlavourHelper.define_and_inference(df)
    df = df.Define("jet_tlv", "FCCAnalyses::makeLorentzVectors(jet_px, jet_py, jet_pz, jet_e)")
    results.append(df.Histo1D(("jet_p", "", *bins_p), "jet_p"))
    results.append(df.Histo1D(("jet_nconst", "", *(200, 0, 200)), "jet_nconst"))


    # the flavour tagger produces probabilities for each jet to be a G, Q(light), S, C or B jet
    df = df.Define("recojet_isG_jet0", "recojet_isG[0]")
    df = df.Define("recojet_isG_jet1", "recojet_isG[1]")
    df = df.Define("recojet_isG_jet2", "recojet_isG[2]")
    df = df.Define("recojet_isG_jet3", "recojet_isG[3]")

    df = df.Define("recojet_isQ_jet0", "recojet_isQ[0]")
    df = df.Define("recojet_isQ_jet1", "recojet_isQ[1]")
    df = df.Define("recojet_isQ_jet2", "recojet_isQ[2]")
    df = df.Define("recojet_isQ_jet3", "recojet_isQ[3]")

    df = df.Define("recojet_isS_jet0", "recojet_isS[0]")
    df = df.Define("recojet_isS_jet1", "recojet_isS[1]")
    df = df.Define("recojet_isS_jet2", "recojet_isS[2]")
    df = df.Define("recojet_isS_jet3", "recojet_isS[3]")

    df = df.Define("recojet_isC_jet0", "recojet_isC[0]")
    df = df.Define("recojet_isC_jet1", "recojet_isC[1]")
    df = df.Define("recojet_isC_jet2", "recojet_isC[2]")
    df = df.Define("recojet_isC_jet3", "recojet_isC[3]")

    df = df.Define("recojet_isB_jet0", "recojet_isB[0]")
    df = df.Define("recojet_isB_jet1", "recojet_isB[1]")
    df = df.Define("recojet_isB_jet2", "recojet_isB[2]")
    df = df.Define("recojet_isB_jet3", "recojet_isB[3]")


    results.append(df.Histo1D(("recojet_isC_jet0", "", *bins_score), "recojet_isC_jet0"))
    results.append(df.Histo1D(("recojet_isC_jet1", "", *bins_score), "recojet_isC_jet1"))
    results.append(df.Histo1D(("recojet_isC_jet2", "", *bins_score), "recojet_isC_jet2"))
    results.append(df.Histo1D(("recojet_isC_jet3", "", *bins_score), "recojet_isC_jet3"))

    results.append(df.Histo1D(("recojet_isB_jet0", "", *bins_score), "recojet_isB_jet0"))
    results.append(df.Histo1D(("recojet_isB_jet1", "", *bins_score), "recojet_isB_jet1"))
    results.append(df.Histo1D(("recojet_isB_jet2", "", *bins_score), "recojet_isB_jet2"))
    results.append(df.Histo1D(("recojet_isB_jet3", "", *bins_score), "recojet_isB_jet3"))
    
    # select 2 jets with highest B score (should form the Higgs for wzp6_ee_ccH_Hbb_ecm240)
    df = df.Define("bjet_idx", "FCCAnalyses::getMaxAndSecondMaxIdx(recojet_isB)")
    df = df.Define("dijet_higgs_m_reco", "(jet_tlv[bjet_idx[0]]+jet_tlv[bjet_idx[1]]).M()")
    results.append(df.Histo1D(("dijet_higgs_m_reco", "", *bins_p), "dijet_higgs_m_reco"))
    
    # select 2 jets with highest C score (should form the Z for wzp6_ee_ccH_Hbb_ecm240)
    df = df.Define("cjet_idx", "FCCAnalyses::getMaxAndSecondMaxIdx(recojet_isC)")
    df = df.Define("dijet_z_m_reco", "(jet_tlv[cjet_idx[0]]+jet_tlv[cjet_idx[1]]).M()")
    results.append(df.Histo1D(("dijet_z_m_reco", "", *bins_p), "dijet_z_m_reco"))


    # compare with jet-truth analysis
    df = df.Define("jets_mc", "FCCAnalyses::jetTruthFinder(_jetc, ReconstructedParticles, Particle, MCRecoAssociations1)")
    df = df.Define("njets", f"{njets}")
    df = df.Define("jets_higgs_mc", "FCCAnalyses::Vec_i res; for(int i=0;i<njets;i++) if(abs(jets_mc[i])==5) res.push_back(i); return res;") # assume H->bb
    df = df.Define("jets_z_mc", "FCCAnalyses::Vec_i res; for(int i=0;i<njets;i++) if(abs(jets_mc[i])!=5) res.push_back(i); return res;") # non bb jets
    df = df.Filter("jets_higgs_mc.size()==2")
    df = df.Filter("jets_z_mc.size()==2")
    df = df.Define("dijet_higgs_m_mc", "(jet_tlv[jets_higgs_mc[0]]+jet_tlv[jets_higgs_mc[1]]).M()")
    df = df.Define("dijet_z_m_mc", "(jet_tlv[jets_z_mc[0]]+jet_tlv[jets_z_mc[1]]).M()")

    results.append(df.Histo1D(("dijet_higgs_m_mc", "", *bins_p), "dijet_higgs_m_mc"))
    results.append(df.Histo1D(("dijet_z_m_mc", "", *bins_p), "dijet_z_m_mc"))


    return results, weightsum


if __name__ == "__main__":

    datadict = functions.get_datadicts() # get default datasets

    datasets = ["wzp6_ee_ccH_Hbb_ecm240"]


    datasets_to_run = datasets
    result = functions.build_and_run(datadict, datasets_to_run, build_graph, f"output_tagger.root", args, norm=True, lumi=7200000)
