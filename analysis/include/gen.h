#ifndef ZH_HIGGS_GEN_H
#define ZH_HIGGS_GEN_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace FCCAnalyses {
    
    
// returns the gen particles with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
float mll_gen_leps(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daughters) {

    //cout << "-----------" << endl;
    
    // get Higgs
    int higgs_parent_idx = -1;
    for(size_t i = 0; i < mc.size(); ++i) {
        if(higgs_parent_idx != -1) break;
        auto & p = mc[i];
        if(std::abs(p.PDG) != 25) continue;
        for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            
            higgs_parent_idx = parents.at(j);
            break;
        }
    }
    
    TLorentzVector d1;
    TLorentzVector d2;
    int i = 0;
    for(unsigned j = mc.at(higgs_parent_idx).daughters_begin; j != mc.at(higgs_parent_idx).daughters_end; ++j) {
        
        auto & p = mc.at(daughters.at(j));
        if(p.PDG == 25) continue;
        if(i == 0) d1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(i == 1) d2.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        i++;
    }
    
    //cout << d1.Theta() << "  " << d2.Theta() << " " << d1.DeltaR(d2) << endl;

    return (d1+d2).M();
} 
    
// returns the gen particles with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
float deltaR_gen_leps(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daughters) {

    //cout << "-----------" << endl;
    
    // get Higgs
    int higgs_parent_idx = -1;
    for(size_t i = 0; i < mc.size(); ++i) {
        if(higgs_parent_idx != -1) break;
        auto & p = mc[i];
        if(std::abs(p.PDG) != 25) continue;
        for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            
            higgs_parent_idx = parents.at(j);
            break;
        }
    }
    
    TLorentzVector d1;
    TLorentzVector d2;
    int i = 0;
    for(unsigned j = mc.at(higgs_parent_idx).daughters_begin; j != mc.at(higgs_parent_idx).daughters_end; ++j) {
        
        auto & p = mc.at(daughters.at(j));
        if(p.PDG == 25) continue;
        if(i == 0) d1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(i == 1) d2.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        i++;
    }
    
    //cout << d1.Theta() << "  " << d2.Theta() << " " << d1.DeltaR(d2) << endl;

    return d1.DeltaR(d2);
} 

    
// returns the gen particles with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
bool is_VBF(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daughters) {

    cout << "-----------" << endl;
    
    // get Higgs
    int higgs_parent_idx = -1;
    for(size_t i = 0; i < mc.size(); ++i) {
        if(higgs_parent_idx != -1) break;
        auto & p = mc[i];
        if(std::abs(p.PDG) != 25) continue;
        for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            
            cout << " PARENT PDGID=" << mc.at(parents.at(j)).PDG  << endl;
            higgs_parent_idx = parents.at(j);
            break;
        }
    }
    
    TLorentzVector d1;
    TLorentzVector d2;
    int i = 0;
    for(unsigned j = mc.at(higgs_parent_idx).daughters_begin; j != mc.at(higgs_parent_idx).daughters_end; ++j) {
        
        auto & p = mc.at(daughters.at(j));
        if(i == 0) d1.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(i == 1) d2.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        i++;
    }
    
    cout << d1.Theta() << "  " << d2.Theta() << " " << d1.DeltaR(d2) << endl;

    
    return false;
    for(size_t i = 0; i < mc.size(); ++i) {
        auto & p = mc[i];
        //if(std::abs(p.PDG) != 12) continue;
        //if(std::abs(mc.at(parents.at(i)).PDG) == 11) return true;
        cout << "PDGID=" << p.PDG << endl;
        
        for(unsigned j = p.daughters_begin; j != p.daughters_end; ++j) {
            cout << " DAUGHTER PDGID=" << mc.at(daughters.at(j)).PDG  << endl;
        }
        
        /*
        for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
            //cout << "  -> idx=" << " PDGID=" << mc.at(parents.at(j)).PDG  << endl;
            //if(std::abs(mc.at(parents.at(j)).PDG) == 11) {
             //   if(abs(p.PDG) == 12 or abs(mc.at(parents.at(j)).PDG) == 12) {
                cout << " PARENT PDGID=" << mc.at(parents.at(j)).PDG  << endl;
                //return true;
               // }
            //}
        }
        */
        
        //cout << "idx=" << i << " " << " status=" << mc.at(i).generatorStatus  << " parent=" << parents.at(i) << " PDGID=" << mc.at(parents.at(i)).PDG  << endl;
        /*
            for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
                if(std::abs(in.at(parents.at(j)).PDG) == 11) {
                    result.emplace_back(p);
                    break;
                }
            }
        */
    }
    return false;
} 

    
    
// get the gen p from reco
std::vector<float> gen_p_from_reco(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs, ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

   std::vector<float> result;

   for (size_t i = 0; i < legs.size(); ++i) {
       
        int track_index = legs[i].tracks_begin;
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        
        TLorentzVector leg_lv;
        if(mc_index >= 0 && mc_index < mc.size() ) {
            leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index ).mass);
            result.push_back(leg_lv.P());
        }
        else {
            cout << "MC track not found!" << endl;
        }
   }
   return result;
}
    
ROOT::VecOps::RVec<edm4hep::MCParticleData> get_photons(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc) {

   ROOT::VecOps::RVec<edm4hep::MCParticleData> result;

   for(size_t i = 0; i < mc.size(); ++i) {
       
        auto & p = mc[i];
        if(p.PDG == 22) result.emplace_back(p);
   }
   return result;
}


    
// FSR
std::vector<int> FSR(ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daugther) {

   std::vector<int> result;

    cout << "*****************************" << endl;
   // i = index of a MC particle in the Particle block
   // in = the Particle collection
   // ind = the block with the indices for the daughters, Particle#1.index

   // returns a vector with the indices (in the Particle block) of the daughters of the particle i

   for (size_t i = 0; i < mc.size(); ++i) {
       
        if(mc.at(i).PDG != 22) continue;
       
        cout << "idx=" << i << " " << " status=" << mc.at(i).generatorStatus  << " parent=" << parents.at(i) << " PDGID=" << mc.at(parents.at(i)).PDG  << " daugher=" << daugther.at(i) << " PDGID=" << mc.at(daugther.at(i)).PDG << endl;
        
   }
   return result;
}
    
// for a given MC index, it returns whether or not one of these muons come (indirectly) from a Higgs decay
bool from_Higgsdecay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

    bool ret = false;
    std::vector<int> res;
    // i = index of a MC particle in the Particle block
    // in = the Particle collection
    // ind = the block with the indices for the parents, Particle#0.index

    // returns whether the particle i comes from the chain containing the Higgs

    if ( i < 0 || i >= in.size() ) return ret;

    int db = in.at(i).parents_begin;
    int de = in.at(i).parents_end;
  
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for idx=" << i << " with PDG=" << in.at(i).PDG << " having db=" << db << " and de=" << de << std::endl;
    

    if(db == de) return false; // top of tree
    
   
    for(int id = db; id < de; id++) { // loop over all parents

        int iparent = ind.at(id);
        //std::cout << " Analyze parent idx=" << iparent << " PDG=" << in.at(iparent).PDG << std::endl;
        
        if(std::abs(in.at(iparent).PDG) == 25) ret = true; // if Higgs is found
        else ret = from_Higgsdecay(iparent, in, ind); // otherwise go up in the decay tree
    }
    
    return ret;
}




// for a given muon collection (legs), it returns whether or not one of these muons come (indirectly) from a Higgs decay
bool from_Higgsdecay(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs, ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daugther) {
    
    bool ret = false;
    for (size_t i = 0; i < legs.size(); ++i) {
        
        int track_index = legs[i].tracks_begin;
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        if(from_Higgsdecay(mc_index, mc, parents)) {
            ret = true;
            break;
        }
    }
    
    return ret;
}


// for a given muon collection (legs), returns the muons which do not come (indirectly) from a Higgs decay
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> excluded_Higgs_decays(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs, ROOT::VecOps::RVec<int> recind, ROOT::VecOps::RVec<int> mcind, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents, ROOT::VecOps::RVec<int> daugther) {
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    //result.reserve(in.size());
    for (size_t i = 0; i < legs.size(); ++i) {
        auto & p = legs[i];
        int track_index = legs[i].tracks_begin;
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        if(not from_Higgsdecay(mc_index, mc, parents)) {
            result.emplace_back(p);
        }
    }
    return result;
}


    
    
    
 
// returns the gen particles with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
ROOT::VecOps::RVec<edm4hep::MCParticleData> select_prompt_leptons_gen(int m_pdg, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> parents) {

    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    for(size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if(std::abs(p.PDG) == m_pdg) {
            for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
                if(std::abs(in.at(parents.at(j)).PDG) == 11) {
                    result.emplace_back(p);
                    break;
                }
            }
        }
    }
    return result;
} 


// returns the gen particle indidex with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
ROOT::VecOps::RVec<int> select_prompt_leptons_idx(int m_pdg, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> parents) {

    ROOT::VecOps::RVec<int> result;
    for(size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if(std::abs(p.PDG) == m_pdg) {
            for(unsigned j = p.parents_begin; j != p.parents_end; ++j) {
                if(std::abs(in.at(parents.at(j)).PDG) == 11) {
                    result.emplace_back(i);
                    break;
                }
            }
        }
    }
    return result;
}
      
 

ROOT::VecOps::RVec<edm4hep::MCParticleData> gen_merge(ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> idx) {

    ROOT::VecOps::RVec<edm4hep::MCParticleData> result;
    result.reserve(idx.size());
    for (size_t i = 0; i < idx.size(); ++i) {
        auto & p = in[idx[i]];
        result.emplace_back(p);
    }
    return result;
} 
    

struct gen_sel_pdgIDInt {
    gen_sel_pdgIDInt(int arg_pdg, bool arg_chargeconjugate);
    int m_pdg = 13;
    bool m_chargeconjugate = true;
    ROOT::VecOps::RVec<int>  operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in);
};

gen_sel_pdgIDInt::gen_sel_pdgIDInt(int arg_pdg, bool arg_chargeconjugate) : m_pdg(arg_pdg), m_chargeconjugate( arg_chargeconjugate )  {};
ROOT::VecOps::RVec<int>  gen_sel_pdgIDInt::gen_sel_pdgIDInt::operator() (ROOT::VecOps::RVec<edm4hep::MCParticleData> in) {
    ROOT::VecOps::RVec<int> result;
    for(size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if(m_chargeconjugate) {
            if(std::abs( p.PDG) == std::abs(m_pdg)) result.push_back(i);
        }
        else {
            if(p.PDG == m_pdg) result.push_back(i);
        }
    }
    return result;
}





ROOT::VecOps::RVec<int> get_parentids(int mcind, ROOT::VecOps::RVec<edm4hep::MCParticleData> mc, ROOT::VecOps::RVec<int> parents){
  ROOT::VecOps::RVec<int> result;
  /*std::cout <<"================== Full Truth=================" <<std::endl;
  for (size_t i = 0; i < mc.size(); ++i) {
    std::cout << "i= " << i << "  PDGID "<< mc.at(i).PDG  <<  "  status  " << mc.at(i).generatorStatus << std::endl;
    for (unsigned j = mc.at(i).parents_begin; j != mc.at(i).parents_end; ++j)
      std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
  }*/

  //std::cout <<"================== NEW EVENT=================" <<std::endl;


    if (mcind<0){
      //result.push_back(-999);
      //continue;
    }
    //std::cout << "mc ind " << mcind.at(i) << "  PDGID "<< mc.at(mcind.at(i)).PDG  << "  status  " << mc.at(mcind.at(i)).generatorStatus << std::endl;
    for (unsigned j = mc.at(mcind).parents_begin; j != mc.at(mcind).parents_end; ++j) {
      //std::cout << "   ==index " << j <<" parents " << parents.at(j) << "  PDGID "<< mc.at(parents.at(j)).PDG << "  status  " << mc.at(parents.at(j)).generatorStatus << std::endl;
       result.push_back(parents.at(j));
    }
    //std::cout << mc.at(mcind.at(i)).parents_begin <<"---"<< mc.at(mcind.at(i)).parents_end<< std::endl;
    /*
    if (mc.at(mcind).parents_end - mc.at(mcind).parents_begin>1) {
      std::cout << "-999 "  << (mc.at(mcind).parents_end - mc.at(mcind).parents_begin)  << std::endl;
      result.push_back(-999);
    }
    else {
      //std::cout << "not -999 "<< parents.at(mc.at(mcind.at(i)).parents_begin) << std::endl;
      result.push_back(parents.at(mc.at(mcind).parents_begin));
    }
    */

  return result;
}

// return list of pdg from decay of a list of mother particle
std::vector<int> gen_decay_list(ROOT::VecOps::RVec<int> mcin, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

   std::vector<int> result;


   // i = index of a MC particle in the Particle block
   // in = the Particle collection
   // ind = the block with the indices for the daughters, Particle#1.index

   // returns a vector with the indices (in the Particle block) of the daughters of the particle i

   for (size_t i = 0; i < mcin.size(); ++i) {
        for (size_t j = 0; j < MCParticle::get_list_of_particles_from_decay(mcin[i],in,ind).size(); ++j) {
            if(in[MCParticle::get_list_of_particles_from_decay(mcin[i],in,ind)[j]].PDG != 25) {
                result.push_back(in[MCParticle::get_list_of_particles_from_decay(mcin[i], in, ind)[j]].PDG);
            }
        }
   }
   return result;
}










struct resonanceZBuilderHiggsPairs {
    float m_resonance_mass;
    bool m_use_MC_Kinematics;
    resonanceZBuilderHiggsPairs(float arg_resonance_mass, bool arg_use_MC_Kinematics);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                                ROOT::VecOps::RVec<int> parents,
                                ROOT::VecOps::RVec<int> daugthers) ;
};

resonanceZBuilderHiggsPairs::resonanceZBuilderHiggsPairs(float arg_resonance_mass, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> resonanceZBuilderHiggsPairs::resonanceZBuilderHiggsPairs::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents,
                ROOT::VecOps::RVec<int> daugthers)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    int n = legs.size();
    std::vector<bool> hDecay;
    
    //cout << "*** BUILD RESO ***" << endl;
    //cout << "Number of leptons: " << n << endl;
  
    if (n >1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            edm4hep::ReconstructedParticleData reso;
            //set initial charge == 0
            reso.charge = 0;
            TLorentzVector reso_lv; 
            bool muonFromHiggsDecay = false;
            bool oneMuonFromHiggsDecay = false;
            for (int i = 0; i < n; ++i) {
                if (v[i]) {

                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    // Ideal detector resolution: use the kinematics of the MC particle instead
                    if ( m_use_MC_Kinematics) {

                         // ugly: particles_begin is not filled in RecoParticle.
                         // hence: either need to keep trace of the index of the legs into the RecoParticle collection,
                         // or (as done below) use the track index to map the leg to the MC particle :-(

                         int track_index = legs[i].tracks_begin ;   // index in the Track array
                         int mc_index = ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco );
                         if ( mc_index >= 0 && mc_index < mc.size() ) {
                         int pdgID = mc.at( mc_index).PDG;
                             leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index ).momentum.z, mc.at(mc_index ).mass );
                         }
                    }

                    else {   //use the kinematics of the reco'ed particle
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }
                    

                
                    
                    // find the Higgs MC particle
                    ROOT::VecOps::RVec<int> higgsParticle = gen_sel_pdgIDInt(25, false)(mc);
                    if(higgsParticle.size() > 0) {
                   
                    
                        //std::vector<int> tmp = gen_decay_list(higgsParticle, mc, daugthers);
                        //if(std::abs(tmp.at(0)) == 23) {
                        
                        int track_index = legs[i].tracks_begin ;   // index in the Track array    
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco); // MC index of the muon
                        
                        muonFromHiggsDecay = from_Higgsdecay(mc_index, mc, parents);
                        if(muonFromHiggsDecay) oneMuonFromHiggsDecay = true;
                        //if(muonFromHiggsDecay) std::cout << muonFromHiggsDecay << std::endl;
                        
                        //}
                    }
                    reso_lv += leg_lv;
                }
            }
      
      
            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            //if(oneMuonFromHiggsDecay == true) continue; // neglect wrong paired muons
            
            hDecay.push_back(oneMuonFromHiggsDecay);
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);

        } while (std::next_permutation(v.begin(), v.end()));
    }
  
    if (result.size() > 1) {
  
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> bestReso;
  
        // sort on mZ
        //auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
		//std::sort(result.begin(), result.end(), resonancesort);
        //ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
        //ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
        //ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
        //cout << " ->" << onlyBestReso.size() << " " << result.size() << endl;
        //return onlyBestReso;
        
        // sort on recoil
        
        //cout << "*** PAIR SELECTOR ***" << endl;
  
        
        int idx_min = -1;
        float d_min = 9e9;
        //cout << "-------------" << endl;
        for (int i = 0; i < result.size(); ++i) {
            
            //if(hDecay.at(i)) continue;
     
            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, 240);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        
            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - 91.2, 2); // mass
            float rec = std::pow(recoil_fcc.mass - 125.0, 2); // recoil
            float d = 0.5*mass + 0.5*rec;
            d = mass;
            
            //cout << " idx=" << i << "  mZ = "<< result.at(i).mass << " mRec = " << recoil_fcc.mass << " oneFromHiggs=" << hDecay.at(i) << endl;
            
            //cout << " one muon from higgs = " << hDecay.at(i) << " mZ = "<< result.at(i).mass << " mRec = " << recoil_fcc.mass << endl;
            
            // MC constrained
            /*
            if(hDecay.at(i) == 0) {
                idx_min = i;
                break;
            }
            */
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }
     
        }
     
        //cout << " nReso=" << result.size() << " mZ=" << result.at(idx_min).mass << endl;
        //if(hDecay.at(idx_min) == 1) cout << " nReso=" << result.size() << " mZ=" << result.at(idx_min).mass << endl;
     
        //cout << " -> selected idx=" << idx_min << " oneFromHiggs=" << hDecay.at(idx_min) << endl;
        if(idx_min > -1) bestReso.push_back(result.at(idx_min));
        return bestReso;
    }
    else {

       // if(result.size() > 0 and hDecay.at(0)) { // return empty if one muon comes from the Higgs decay
        //    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> bestReso;
       //     return bestReso;
        //}
        
        //if(result.size() > 0 and hDecay.at(0) == 1) cout << " nReso=" << result.size() << " mZ=" << result.at(0).mass << endl;
        return result;
    }
}    
    
    
    
    










// build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
// technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
struct resonanceBuilder_mass_recoil {
    float m_resonance_mass;
    float m_recoil_mass;
    float chi2_recoil_frac;
    float ecm;
    bool m_use_MC_Kinematics;
    resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                                ROOT::VecOps::RVec<int> parents,
                                ROOT::VecOps::RVec<int> daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents,
                ROOT::VecOps::RVec<int> daugthers)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            edm4hep::ReconstructedParticleData reso;
            reso.charge = 0;
            TLorentzVector reso_lv; 
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    pair.push_back(i);
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;

                    if(m_use_MC_Kinematics) { // MC kinematics
                        int track_index = legs[i].tracks_begin;   // index in the Track array
                        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
                        if (mc_index >= 0 && mc_index < mc.size()) {
                            leg_lv.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
                        }
                    }
                    else { // reco kinematics
                         leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }

            if(reso.charge != 0) continue; // neglect non-zero charge pairs
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
            pairs.push_back(pair);

        } while(std::next_permutation(v.begin(), v.end()));
    }
    else {
        std::cout << "ERROR: resonanceBuilder_mass_recoil, at least two leptons required." << std::endl;
        exit(1);
    }
  
    if(result.size() > 1) {
  
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> bestReso;
        
        int idx_min = -1;
        float d_min = 9e9;
        for (int i = 0; i < result.size(); ++i) {
            
            // calculate recoil
            auto recoil_p4 = TLorentzVector(0, 0, 0, ecm);
            TLorentzVector tv1;
            tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
            recoil_p4 -= tv1;
      
            auto recoil_fcc = edm4hep::ReconstructedParticleData();
            recoil_fcc.momentum.x = recoil_p4.Px();
            recoil_fcc.momentum.y = recoil_p4.Py();
            recoil_fcc.momentum.z = recoil_p4.Pz();
            recoil_fcc.mass = recoil_p4.M();
            
            TLorentzVector tg;
            tg.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        
            float boost = tg.P();
            float mass = std::pow(result.at(i).mass - m_resonance_mass, 2); // mass
            float rec = std::pow(recoil_fcc.mass - m_recoil_mass, 2); // recoil
            float d = mass + chi2_recoil_frac*rec;
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }
     
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            result.emplace_back(l1);
            result.emplace_back(l2);
        }
        else {
            std::cout << "ERROR: resonanceBuilder_mass_recoil, no mininum found." << std::endl;
            exit(1);
        }
        return bestReso;
    }
    else {
        auto & l1 = legs[0];
        auto & l2 = legs[1];
        result.emplace_back(l1);
        result.emplace_back(l2);
        return result;
    }
}    
    


















    /*
std::vector<int> get_list_of_stable_particles_from_decay( int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

  std::vector<int> res;
  // i = index of a MC particle in the Particle block
  // in = the Particle collection
  // ind = the block with the indices for the daughters, Particle#1.index

  // returns a vector with the indices (in the Particle block) of the stable daughters of the particle i,
  // from the complete decay chain.

  if ( i < 0 || i >= in.size() ) return res;

  int db = in.at(i).daughters_begin ;
  int de = in.at(i).daughters_end; // always -1
  
  //std::cout << "Chain for " << in.at(i).PDG << std::endl;
  //std::cout << "Chain for " << in.at(i).PDG << std::endl;
  std::cout << "Chain for idx=" << i << " with PDG=" << in.at(i).PDG << " having nDaughters=" << (de-db) << std::endl;
    

  if ( db != de ) {// particle is unstable
    //int d1 = ind[db] ;
    //int d2 = ind[de-1];
    //for (int idaughter = d1; idaughter <= d2; idaughter++) {
    for (int id = db; id < de; id++) { // loop over all daughers
        //int idaughter = ind[ id ];
        int idaughter = ind.at(id);
        std::cout << " Analyze daugher " << in.at(idaughter).PDG <<  std::endl;
        std::vector<int> rr = get_list_of_stable_particles_from_decay( idaughter, in, ind) ;
        res.insert( res.end(), rr.begin(), rr.end() );
    }
  }
  else {    // particle is stable
     res.push_back( i ) ;
     return res ;
  }
  return res;
}

bool from_Higgsdecay(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

    bool ret = false;
    std::vector<int> res;
    // i = index of a MC particle in the Particle block
    // in = the Particle collection
    // ind = the block with the indices for the parents, Particle#0.index

    // returns whether the particle i comes from the chain containing the Higgs

    if ( i < 0 || i >= in.size() ) return ret;

    int db = in.at(i).parents_begin;
    int de = in.at(i).parents_end;
  
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for " << in.at(i).PDG << std::endl;
    //std::cout << "Chain for idx=" << i << " with PDG=" << in.at(i).PDG << " having db=" << db << " and de=" << de << std::endl;
    

    if(db == de) return false; // top of tree
    
   
    for(int id = db; id < de; id++) { // loop over all parents

        int iparent = ind.at(id);
        //std::cout << " Analyze parent idx=" << iparent << " PDG=" << in.at(iparent).PDG << std::endl;
        
        if(std::abs(in.at(iparent).PDG) == 25) ret = true; // if Higgs is found
        else ret = from_Higgsdecay(iparent, in, ind); // otherwise go up in the decay tree
    }
    
    return ret;

}






struct resonanceZBuilderHiggsPairs {
    float m_resonance_mass;
    bool m_use_MC_Kinematics;
    resonanceZBuilderHiggsPairs(float arg_resonance_mass, bool arg_use_MC_Kinematics);
    ROOT::VecOps::RVec<int> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                                ROOT::VecOps::RVec<int> parents,
                                ROOT::VecOps::RVec<int> daugthers) ;
};

resonanceZBuilderHiggsPairs::resonanceZBuilderHiggsPairs(float arg_resonance_mass, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

ROOT::VecOps::RVec<int> resonanceZBuilderHiggsPairs::resonanceZBuilderHiggsPairs::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents,
                ROOT::VecOps::RVec<int> daugthers)   {

  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  int n = legs.size();
  std::vector<bool> hDecay;
  
  if (n >1) {
    ROOT::VecOps::RVec<bool> v(n);
    std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
    do {
      edm4hep::ReconstructedParticleData reso;
      //set initial charge == 0
      reso.charge = 0;
      TLorentzVector reso_lv; 
      bool fromHiggsDecay = false;
      for (int i = 0; i < n; ++i) {
          if (v[i]) {
            //prevent +2 and -2 charged Z 
            if (reso.charge == legs[i].charge) continue;
            reso.charge += legs[i].charge;
            TLorentzVector leg_lv;

            // Ideal detector resolution: use the kinematics of the MC particle instead
            if ( m_use_MC_Kinematics) {

                 // ugly: particles_begin is not filled in RecoParticle.
                 // hence: either need to keep trace of the index of the legs into the RecoParticle collection,
                 // or (as done below) use the track index to map the leg to the MC particle :-(

                 int track_index = legs[i].tracks_begin ;   // index in the Track array
                 int mc_index = ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco );
                 if ( mc_index >= 0 && mc_index < mc.size() ) {
                 int pdgID = mc.at( mc_index).PDG;
                     leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index ).momentum.z, mc.at(mc_index ).mass );
                 }
            }

            else {   //use the kinematics of the reco'ed particle
                 leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
            }
        
            
            // get the Higgs MC particle
            ROOT::VecOps::RVec<int> higgsParticle = sel_pdgIDInt(25,false)(mc);
            if(higgsParticle.size() > 0) {
           
            
                std::vector<int> tmp = list_decays(higgsParticle, mc, daugthers);
                if(std::abs(tmp.at(0)) == 23) {
                
                int track_index = legs[i].tracks_begin ;   // index in the Track array    
                int mc_index = ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco ); // MC index of the muon
                
                fromHiggsDecay = from_Higgsdecay(mc_index, mc, parents);
                //if(fromHiggsDecay) std::cout << fromHiggsDecay << std::endl;
                
                }
            }
            reso_lv += leg_lv;
          }
      }
      
      
      hDecay.push_back(fromHiggsDecay);
      reso.momentum.x = reso_lv.Px();
      reso.momentum.y = reso_lv.Py();
      reso.momentum.z = reso_lv.Pz();
      reso.mass = reso_lv.M();
      result.emplace_back(reso);

    } while (std::next_permutation(v.begin(), v.end()));
  }
  
  
  if (result.size() > 1) {
  
     int idx_min = -1;
     float d_min = 9e9;
     for (int i = 0; i < result.size(); ++i) {
     
        // calculate recoil
        auto recoil_p4 = TLorentzVector(0, 0, 0, 240);
        TLorentzVector tv1;
        tv1.SetXYZM(result.at(i).momentum.x, result.at(i).momentum.y, result.at(i).momentum.z, result.at(i).mass);
        recoil_p4 -= tv1;
      
        auto recoil_fcc = edm4hep::ReconstructedParticleData();
        recoil_fcc.momentum.x = recoil_p4.Px();
        recoil_fcc.momentum.y = recoil_p4.Py();
        recoil_fcc.momentum.z = recoil_p4.Pz();
        recoil_fcc.mass = recoil_p4.M();
        
        float d = std::pow(result.at(i).mass - 91.2, 2); // + 5.*std::pow(recoil_fcc.mass - 125.0, 2);
        
        if(d < d_min) {
            d_min = d;
            idx_min = i;
        }
     
     }
     
     
     ROOT::VecOps::RVec<int> ret;
     ret.emplace_back(hDecay.at(idx_min));
     return ret;
     
     
   
  } else {
    
     //if(result.size() == 1 && hDecay.at(0)) std::cout << "from Higgs" << std::endl;
     ROOT::VecOps::RVec<int> ret;
     if(result.size() == 1) ret.emplace_back(hDecay.at(0));
     return ret;

  }
}





int compare(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> f1, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> f2) {

    if(f1.size() != f2.size()) {
        std::cout << "not equal size " << std::endl;
        return 2;
        }
    if(f1.size() > 0) {
    
        if((f1.at(0).mass - f2.at(0).mass) > 0.001) {
        
            std::cout << "no equal mass " << f1.at(0).mass << " " << f2.at(0).mass << std::endl;
            return 1;
        }
    
    }
    
    
    return 0;
}



ROOT::VecOps::RVec<int> from_higgs_decay(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents,
                ROOT::VecOps::RVec<int> daugthers)   {

    ROOT::VecOps::RVec<int> result;
    //ROOT::VecOps::RVec<float> muon_pt = ReconstructedParticle::get_pt(legs);
    int n = legs.size();
    //std::cout << "nMuons=" << n << std::endl;
    for(int i = 0; i < n; i++) { // loop over muon collection
    
        // get associated MC index of the RECO muon
        int track_index = legs[i].tracks_begin ;   // index in the Track array    
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco); // MC index of the muon
  
        bool ret = from_Higgsdecay(mc_index, mc, parents);
        result.emplace_back(ret);
        
        //std::cout << " fromHiggs=" << ret << " pT=" << muon_pt.at(i) << std::endl;
        
    }
    return result;
}

// returns the muon collection which comes from Higgs decays
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muon_from_higgs_decay(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs, ROOT::VecOps::RVec<int> from_higgs)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    int n = legs.size();
    for(int i = 0; i < n; i++) {
    
        if(from_higgs.at(i) == 1) result.emplace_back(legs.at(i));
    }
    //std::cout << "TOT=" << n << " fromHiggs=" << result.size() << std::endl;
    return result;
}

// returns the muon collection which comes  not from Higgs decays
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muon_not_from_higgs_decay(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs, ROOT::VecOps::RVec<int> from_higgs)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    int n = legs.size();
    for(int i = 0; i < n; i++) {
    
        if(from_higgs.at(i) == 0) result.emplace_back(legs.at(i));
    }
    //std::cout << "TOT=" << n << " fromHiggs=" << result.size() << std::endl;
    return result;
}


struct makePairs {
    int flag; // 0=all, 1=noHiggs, -1=!noHiggs
    bool m_use_MC_Kinematics;
    makePairs(int arg_flag, bool arg_use_MC_Kinematics);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
                                ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                                ROOT::VecOps::RVec<int> parents) ;
};

makePairs::makePairs(int arg_flag, bool arg_use_MC_Kinematics) {flag = arg_flag, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> makePairs::makePairs::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs,
				ROOT::VecOps::RVec<int> recind ,
				ROOT::VecOps::RVec<int> mcind ,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco ,
				ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    int n = legs.size();
    if (n >1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true);
        do {
            edm4hep::ReconstructedParticleData reso;
            //set initial charge == 0
            reso.charge = 0;
            TLorentzVector reso_lv; 
            bool fromHiggsDecay = false;
            for (int i = 0; i < n; ++i) {
                if (v[i]) {
                    
                    if (reso.charge == legs[i].charge) continue; // prevent +2 and -2 charged Z 
                   
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;
                    
                    // get the correspondig MC particle
                    int track_index = legs[i].tracks_begin ;   // index in the Track array
                    int mc_index = ReconstructedParticle2MC::getTrack2MC_index( track_index, recind, mcind, reco );
                    
                    if(std::abs(flag) == 1) {
                    
                        if ( mc_index >= 0 && mc_index < mc.size() ) {
                            bool fromHiggsDecay_ = from_Higgsdecay(mc_index, mc, parents);
                            if(!fromHiggsDecay) fromHiggsDecay = fromHiggsDecay_; // update fromHiggsDecay only if it's false
                        }
                        else {
                            std::cout << "MC INDEX NOT FOUND" << std::endl;
                        }
                    }
                    

                    // Ideal detector resolution: use the kinematics of the MC particle instead
                    if ( m_use_MC_Kinematics) {

                        // ugly: particles_begin is not filled in RecoParticle.
                        // hence: either need to keep trace of the index of the legs into the RecoParticle collection,
                        // or (as done below) use the track index to map the leg to the MC particle :-(

                        
                        if ( mc_index >= 0 && mc_index < mc.size() ) {
                            int pdgID = mc.at( mc_index).PDG;
                            leg_lv.SetXYZM(mc.at(mc_index ).momentum.x, mc.at(mc_index ).momentum.y, mc.at(mc_index ).momentum.z, mc.at(mc_index ).mass );
                        }
                    }
                    else {   //use the kinematics of the reco'ed particle
                        leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    }

                    reso_lv += leg_lv;
                }
            }
            
            if(reso.charge != 0) continue; // only zero charged pairs allowed
            if(flag == 1 && fromHiggsDecay) continue;
            if(flag == -1 && !fromHiggsDecay) continue;
            
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
        } while (std::next_permutation(v.begin(), v.end()));
    }
    
    //std::cout << result.size() << std::endl;
    return result;
    
    
  //if (result.size() > 1) {
   // auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
	//	std::sort(result.begin(), result.end(), resonancesort);
   // ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
   //ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
   // ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
   // return onlyBestReso;
  //} else {
  //  return result;
//  }
 
}


/*
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> selectPair(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> pairs)   {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    if(pairs.size() == 0) return result;
    
    if(pairs.size() == 1) {
    
        result.emplace_back(pairs.at(0));
        return result;
    }

    int idx_min = -1;
    float d_min = 9e9;
    //std::cout << "------------" << std::endl;
    for(int i = 0; i < pairs.size(); ++i) {
     
        // calculate recoil
        auto recoil_p4 = TLorentzVector(0, 0, 0, 240);
        TLorentzVector tv1;
        tv1.SetXYZM(pairs.at(i).momentum.x, pairs.at(i).momentum.y, pairs.at(i).momentum.z, pairs.at(i).mass);
        recoil_p4 -= tv1;
      
        
        //float d = std::pow(pairs.at(i).mass - 91.2, 2);
        //float d = std::pow(recoil_p4.M() - 125.0, 2);
        float d = std::pow(pairs.at(i).mass - 91.2, 2) / (2*2) + std::pow(recoil_p4.M() - 125.0, 2) / (0.8*0.8);
        
        //std::cout << " m=" << pairs.at(i).mass << " rec=" << recoil_p4.M() << " d=" << d << std::endl;
        if(d < d_min) {
            d_min = d;
            idx_min = i;
        }
    }
    
    //std::cout << idx_min << std::endl;

    //result.emplace_back(pairs.at(idx_min));
    result.emplace_back(pairs.at(0));
    return result;
}
*/


double computeBreitWignerWeightHiggs(double offset) {
    
    double MH_GEN_ = 125.0*1000.;
    double GAMMAH_GEN_ = 0;


    double targetMass = MH_GEN_ + offset;
    double s_hat = MH_GEN_*MH_GEN_;
    double offshell = s_hat - MH_GEN_*MH_GEN_;
    double offshellOffset = s_hat - targetMass*targetMass;
    double weight = (offshell*offshell + GAMMAH_GEN_*GAMMAH_GEN_*MH_GEN_*MH_GEN_) / (offshellOffset*offshellOffset + GAMMAH_GEN_*GAMMAH_GEN_*targetMass*targetMass);
    return weight;
}

ROOT::VecOps::RVec<double> breitWignerWeightsHiggs() {
    

    ROOT::VecOps::RVec<double> res(5, 1);
    
    res[0] = computeBreitWignerWeightHiggs(-100);
    res[1] = computeBreitWignerWeightHiggs(-50);
    res[2] = computeBreitWignerWeightHiggs(0);
    res[3] = computeBreitWignerWeightHiggs(50);
    res[4] = computeBreitWignerWeightHiggs(100);
    return res;


}

ROOT::VecOps::RVec<int> indices_(const int& size, const int& start = 0) {
    ROOT::VecOps::RVec<int> res(size, 0);
    std::iota(std::begin(res), std::end(res), start);
    return res;
}

}

#endif
