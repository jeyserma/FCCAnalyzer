
import sys, os, glob, shutil, json, math, re, random
import ROOT
import functions

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.DisableImplicitMT()


def analyzer():
    ch = ROOT.TChain("events")
    for f in functions.findROOTFiles(dIn):
        ch.Add(f)
    #ch.Print()
    
    for iEv in range(0, ch.GetEntries()):
        ch.GetEntry(iEv)
        print(f"*************{iEv}")

        reco_particles = getattr(ch, "ReconstructedParticles")
        mc_particles = getattr(ch, "Particle")
        parents = getattr(ch, "Particle#0")
        daughters = getattr(ch, "Particle#1")
        tracks = getattr(ch, "EFlowTrack")
        
        
        ## example: get the Higgs daughters
        higgs_idx = -1
        for iP, mc_p in enumerate(mc_particles):
            if mc_p.PDG != 25:
                continue
            higgs_idx = iP
            break
            
        for k in range(mc_particles[higgs_idx].daughters_begin, mc_particles[higgs_idx].daughters_end):
            pass
            #print(k, mc_particles[daughters[k].index].PDG)
            
            
        ## number of particles, neutrals, charged, tracks, ...
        nParticles = len(reco_particles)
        nTracks = len(tracks)
        nNeutrals = 0
        nCharged = 0
        for p in reco_particles:
            if p.charge == 0:
                nNeutrals += 1
            else:
                nCharged += 1
        print(nTracks, nNeutrals, nCharged)
        
        
        
        

        ## reco particles
        
        
        quit()


if __name__ == "__main__":


    dIn = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm240/"
    
    analyzer()
    
    