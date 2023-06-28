
import sys, os, glob, shutil, json, math, re, random
import ROOT
import functions

ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)
ROOT.DisableImplicitMT()


def get_list_of_stable_particles_from_decay(idx, mc_particles, daughters):

    ret = []

    if idx < 0 or idx >= len(mc_particles):
        return ret

    db = mc_particles[idx].daughters_begin
    de = mc_particles[idx].daughters_end

    if db != de: # particle is unstable
        for id_ in range(db, de):
            idaughter = daughters[id_].index;
            rr = get_list_of_stable_particles_from_decay(idaughter, mc_particles, daughters)
            ret += rr
    else: # particle is stable
        ret.append(idx)
        return ret

    return ret
    
def get_list_of_particles_from_decay(idx, mc_particles, daughters):

    ret = []

    if idx < 0 or idx >= len(mc_particles):
        return ret

    db = mc_particles[idx].daughters_begin
    de = mc_particles[idx].daughters_end

    if db == de: # particle is stable
        return ret

    for idaughter in range(db, de):
        ret.append(daughters[idaughter].index)

    return ret
    

def analyzer_higgs(dIn):
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


def analyzer_tau(dIn):
    ch = ROOT.TChain("events")
    for f in functions.findROOTFiles(dIn):
        print(f"Add {f}")
        ch.Add(f)
        break
    #ch.Print()
    
    for iEv in range(0, ch.GetEntries()):
        ch.GetEntry(iEv)
        print(f"*************{iEv}")
        
        reco_particles = getattr(ch, "ReconstructedParticles")
        mc_particles = getattr(ch, "Particle")
        parents = getattr(ch, "Particle#0")
        daughters = getattr(ch, "Particle#1")

        print(len(reco_particles), len(mc_particles))
        
        ## get the index of tau plus and tau minus
        taup_idx, taum_idx = -1, -1
        for iP, mc_p in enumerate(mc_particles):
            if mc_p.PDG == 15:
                taup_idx = iP
            if mc_p.PDG == -15:
                taum_idx = iP
            

        stable_particles = get_list_of_stable_particles_from_decay(taup_idx, mc_particles, daughters)   
        for sp in stable_particles:
            print(sp, mc_particles[sp].PDG)
        
        
       
        
        #quit()

if __name__ == "__main__":


    ZH = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm240/"
    tautau = "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_tautau_ecm91p2/"
    
    analyzer_tau(tautau)
    
    