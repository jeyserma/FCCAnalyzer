
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
    
    res = ROOT.TH1D("res", "", 10000, 0.5, 1.5)
    p_reco = ROOT.TH1D("p_reco", "", 200, 0, 20)
    p_reco_new = ROOT.TH1D("p_reco_new", "", 200, 0, 20)
    p_gen = ROOT.TH1D("p_gen", "", 200, 0, 20)
    m_inv_mc = ROOT.TH1D("m_inv_mc", "", 100, 0, 1)
    m_inv_rec = ROOT.TH1D("m_inv_rec", "", 100, 0, 1)
    
    for iEv in range(0, ch.GetEntries()):
        ch.GetEntry(iEv)
        
        
        reco_particles = getattr(ch, "ReconstructedParticles")
        mc_particles = getattr(ch, "Particle")
        parents = getattr(ch, "Particle#0")
        daughters = getattr(ch, "Particle#1")
        photons = getattr(ch, "Photon#0")
        
        recind = getattr(ch, "MCRecoAssociations#0")
        mcind = getattr(ch, "MCRecoAssociations#1")


        
        ## get the index of tau plus and tau minus
        taup_idx, taum_idx = -1, -1
        for iP, mc_p in enumerate(mc_particles):
            if mc_p.PDG == 15:
                taup_idx = iP
            if mc_p.PDG == -15:
                taum_idx = iP
            

        stable_particles = get_list_of_stable_particles_from_decay(taup_idx, mc_particles, daughters)
        if len(stable_particles) != 4:
            continue
            
        pdgs = []
        for sp in stable_particles:
            pdgs.append(mc_particles[sp].PDG)

       
        #if pdgs.count(22) != 2:
        #    continue
        if pdgs[3] != 22 or pdgs[2] != 22:
            continue
        
        ga1 = mc_particles[stable_particles[2]]
        ga2 = mc_particles[stable_particles[3]]
        
        lv1 = ROOT.Math.PxPyPzMVector(ga1.momentum.x, ga1.momentum.y, ga1.momentum.z, ga1.mass)
        lv2 = ROOT.Math.PxPyPzMVector(ga2.momentum.x, ga2.momentum.y, ga2.momentum.z, ga2.mass)
        s = lv1 + lv2
        
        if iEv%1000 == 0:
            print(f"*************{iEv}")
        #print(f"*************{iEv}")
        #print(f"*************{iEv}")
        reco_photons = []
        photons_idx = [p.index for p in photons]
        tlvs_mc, tlvs_rec = [], []
        for idx, r in enumerate(recind):
            
            i = r.index
            
            rec_index = r.index
            if i > len(mcind)-1:
                continue
            mc_index = mcind.at(i).index
            #print(idx, mc_particles.at(mc_index).PDG)
            
            if not rec_index in photons_idx:
                continue
            
            
            #m
            #if mc_index > len(mc_particles):
            #    continue
            #if mc_particles.at(mc_index).PDG != 22:
            #    continue
            tlv_reco = ROOT.Math.PxPyPzEVector(reco_particles.at(i).momentum.x,reco_particles.at(i).momentum.y,reco_particles.at(i).momentum.z,reco_particles.at(i).energy)
            #print(reco_particles.at(i).momentum.x,reco_particles.at(i).momentum.y,reco_particles.at(i).momentum.z,reco_particles.at(i).energy)
            tlv_mc = ROOT.Math.PxPyPzMVector(mc_particles.at(mc_index).momentum.x,mc_particles.at(mc_index).momentum.y,mc_particles.at(mc_index).momentum.z,mc_particles.at(mc_index).mass)
            #print(tlv.P(), tlv_reco.P())
            res.Fill(tlv_reco.P()/tlv_mc.P())
            p_reco.Fill(tlv_reco.P())
            p_gen.Fill(tlv_mc.P())
            #print(idx, tlv.P())
            tlvs_rec.append(tlv_reco)
            tlvs_mc.append(tlv_mc)
           

        # make resonance close to pi0 mass
        #for ik in range(0, len()):
        
        
        #print("ddddd",len(photons), len(ff))
        reco_photons = []
        for pIdx in photons:
            if pIdx.index > -1:
                p = reco_particles[pIdx.index]
                tlv = ROOT.Math.PxPyPzEVector(p.momentum.x, p.momentum.y, p.momentum.z, p.energy)
                #print(p.momentum.x, p.momentum.y, p.momentum.z, p.energy)
                reco_photons.append(p)
                p_reco_new.Fill(tlv.P())
        
        
        if len(tlvs_mc) != 2:
            continue
        if len(tlvs_rec) > 2:
            print(len(tlvs_rec))
        #quit()
        
        
        m_mc = (tlvs_mc[0] + tlvs_mc[1]).M()
        m_rec = (tlvs_rec[0] + tlvs_rec[1]).M()
        if m_mc < 0.12 or m_mc > 0.14:
            continue
        #print(m_mc, m_rec)
        
        m_inv_mc.Fill(m_mc)
        m_inv_rec.Fill(m_rec)
        
        #gar1 = ROOT.Math.PxPyPzEVector(reco_photons[0].momentum.x, reco_photons[0].momentum.y, reco_photons[0].momentum.z, reco_photons[0].energy)
        #gar2 = ROOT.Math.PxPyPzEVector(reco_photons[1].momentum.x, reco_photons[1].momentum.y, reco_photons[1].momentum.z, reco_photons[1].energy)
        #sr = gar1 + gar2
        #print(f"*************{iEv}")
        #print(s.M(), sr.M())
        #print()

    fOut = ROOT.TFile("res.root", "RECREATE")
    res.Write()
    p_reco.Write()
    p_gen.Write()
    p_reco_new.Write()
    m_inv_mc.Write()
    m_inv_rec.Write()
    fOut.Close()

def analyzer_zgamma(dIn):
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
        z_idx = -1, -1
        for iP, mc_p in enumerate(mc_particles):
            if mc_p.PDG != 23:
                continue

            db = mc_particles[iP].daughters_begin
            de = mc_particles[iP].daughters_end
            print(mc_p.PDG, db, de, mc_particles[daughters[db].index].PDG, mc_particles[daughters[de].index].PDG)
            


        
        
        
if __name__ == "__main__":


    ZH = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA/wzp6_ee_mumuH_ecm240/"
    tautau = "/eos/experiment/fcc/users/j/jaeyserm/sampleProduction/winter2023/wzp6_ee_tautau_ecm91p2/"
    zgamma = "/eos/experiment/fcc/ee/generation/DelphesEvents/winter2023/IDEA//wzp6_ee_qqH_HZa_ecm240/"
    analyzer_tau(tautau)
    #analyzer_zgamma(zgamma)
    