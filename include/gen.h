#ifndef FCCANALYZER_GEN_H
#define FCCANALYZER_GEN_H

#include "defines.h"

namespace FCCAnalyses {







Vec_tlv makeLorentzVectors_gen(Vec_rp in, ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {
	
	Vec_tlv result;
	for (auto & p: in) {
        
        int track_index = p.tracks_begin;
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        
		TLorentzVector tlv;
        if(mc_index >= 0 && mc_index < mc.size() ) {
            tlv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
            result.push_back(tlv);
        }
        else {
            cout << "MC track not found!" << endl;
        }	
	}
	return result;
}

Vec_mc get_gen_pdg(Vec_mc mc, int pdgId, bool abs=true, bool stable=true) {
   Vec_mc result;
   for(size_t i = 0; i < mc.size(); ++i) {
        auto & p = mc[i];
        if(!((abs and std::abs(p.PDG) == pdgId) or (not abs and p.PDG == pdgId))) continue;
        if(stable && p.generatorStatus != 1) continue;
        result.emplace_back(p);
        //if((abs and std::abs(p.PDG) == pdgId) or (not abs and p.PDG == pdgId)) result.emplace_back(p);
   }
   return result;
}



Vec_mc kkmc_get_beam_electrons(Vec_mc in, Vec_i ind) {
    // with BES enab led in KKMC, suebsequently Pythia stores the beam electrons with the nominal energy (no BES) according to the energy stored in the header
    // then it stores a daughter electron with BES (but mass zero)
    
    // to filter the beam electrons with BES, the parents of the parents of the daughter electron should be zero
    // assume only 1 parent
    
    // what happens if ISR is switched OFF?
    Vec_mc result;
    for(size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if(std::abs(p.PDG) != 11) continue;
        if(i==0 or i==1) continue; // neglect the initial Pythia beam electrons

        int parentIdx = in.at(i).parents_begin; // get parent of parent
        if(in.at(parentIdx).parents_begin == 0) {
            p.mass = 0.000511; // seems Pythia assigns zero mass to the electrons
            result.push_back(p); // 
        }
    }
    
    return result;

    /*
    bool ret = false;
    // in = the Particle collection
    // ind = the block with the indices for the parents, Particle#0.index

    // returns whether the particle i comes from the chain containing the Higgs

    if ( i < 0 || i >= in.size() ) return ret;

    int db = in.at(i).parents_begin;
    int de = in.at(i).parents_end;
  
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for idx=" << i << " with PDG=" << in.at(i).PDG << " having db=" << db << " and de=" << de << std::endl;
    

    if(db == de) return true; // top of tree

   
    for(int id = db; id < de; id++) { // loop over all parents

        int iparent = ind.at(id);
        //std::cout << " Analyze parent idx=" << iparent << " PDG=" << in.at(iparent).PDG << std::endl;
        
        //if(std::abs(in.at(iparent).PDG) == 11) ret = true; // if prompt
        if(iparent == 0) return true;
        else if(std::abs(in.at(iparent).PDG) == 25) ret = false; // non prompt, from Higgs decays
        else ret = whizard_zh_from_prompt(iparent, in, ind); // otherwise go up in the decay tree
    }
    
    return ret;
    */
}


}

#endif
