#ifndef ZH_UTILS_H
#define ZH_UTILS_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace FCCAnalyses {
    
    

  

float deltaR(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    
    if(in.size() != 2) return -1;
    
    ROOT::Math::PxPyPzEVector tlv1;
    tlv1.SetPxPyPzE(in.at(0).momentum.x, in.at(0).momentum.y, in.at(0).momentum.z, in.at(0).energy);

    ROOT::Math::PxPyPzEVector tlv2;
    tlv2.SetPxPyPzE(in.at(1).momentum.x, in.at(1).momentum.y, in.at(1).momentum.z, in.at(1).energy);
    
    return std::sqrt(std::pow(tlv1.Eta()-tlv2.Eta(), 2) + std::pow(tlv1.Phi()-tlv2.Phi(), 2));
   
}



ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> missingEnergy(float ecm, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> ret;
    edm4hep::ReconstructedParticleData res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
    
}

float visibleMass(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += p.momentum.x;
        py += p.momentum.y;
        pz += p.momentum.z;
        e += p.energy;
    }

    float ptot2 = std::pow(px, 2) + std::pow(py, 2) + std::pow(pz, 2);
    float de2 = std::pow(e, 2);
    if (de2 < ptot2) return -999.;
    float Mvis = std::sqrt(de2 - ptot2);
    return Mvis;
}
  
float missingMass(float ecm, ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += p.momentum.x;
        py += p.momentum.y;
        pz += p.momentum.z;
        e += p.energy;
    }
    if(ecm < e) return -99.;

    float ptot2 = std::pow(px, 2) + std::pow(py, 2) + std::pow(pz, 2);
    float de2 = std::pow(ecm - e, 2);
    if (de2 < ptot2) return -999.;
    float Mmiss = std::sqrt(de2 - ptot2);
    return Mmiss;
}
    
float sumScalar(ROOT::VecOps::RVec<float> in){
    
    float tot = std::accumulate(in.begin(), in.end(), 0);
    return tot;
}


// perturb the scale of the particles
struct polarAngleCategorization {
    polarAngleCategorization(float arg_thetaMin, float arg_thetaMax);
    float thetaMin = 0;
    float thetaMax = 5;
    int operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

polarAngleCategorization::polarAngleCategorization(float arg_thetaMin, float arg_thetaMax) : thetaMin(arg_thetaMin), thetaMax(arg_thetaMax) {};
int polarAngleCategorization::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    
    int nFwd = 0; // number of forward leptons
    for (size_t i = 0; i < in.size(); ++i) {
        
        auto & p = in[i];
        TLorentzVector lv;
        lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(lv.Theta() < thetaMin || lv.Theta() > thetaMax) nFwd += 1;
    }
    return nFwd;
}


    

ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  muon_quality_check(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
	
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;

    //at least one muon + and one muon - in each event
    int n_muon_plus = 0;
    int n_muon_minus = 0;
    int n = in.size();
    for(int i = 0; i < n; ++i) {
        if (in[i].charge == 1.0){
			++n_muon_plus;
        }
        else if (in[i].charge == -1.0){
            ++n_muon_minus;
        }
    }
    if(n_muon_plus >= 1 && n_muon_minus >= 1){
        result = in;
    }
    return result;
}


ROOT::VecOps::RVec<float> get_cosTheta_miss(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> met){
    
    ROOT::VecOps::RVec<float> result;
    float costheta = 0.;
    if(met.size() > 0) {
        
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));

    }
    result.push_back(costheta);
    return result;
}



ROOT::VecOps::RVec<float> leptonResolution_p(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons, ROOT::VecOps::RVec<int> recind,
                                ROOT::VecOps::RVec<int> mcind,
                                ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc){
    
    ROOT::VecOps::RVec<float> result;
    result.reserve(muons.size());
    
    for(int i = 0; i < muons.size(); ++i) {

        TLorentzVector reco_;
        reco_.SetXYZM(muons[i].momentum.x, muons[i].momentum.y, muons[i].momentum.z, muons[i].mass);
        int track_index = muons[i].tracks_begin;
        int mc_index = FCCAnalyses::ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        if(mc_index >= 0 && mc_index < (int)mc.size()) {
            TLorentzVector mc_;
            mc_.SetXYZM(mc.at(mc_index).momentum.x, mc.at(mc_index).momentum.y, mc.at(mc_index).momentum.z, mc.at(mc_index).mass);
            if(mc_.P() > 20) result.push_back(reco_.P()/mc_.P());
		}
    } 
    return result;
}



struct resonanceBuilder {
    float m_resonance_mass;
    resonanceBuilder(float arg_resonance_mass);
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs);
};  

resonanceBuilder::resonanceBuilder(float arg_resonance_mass) { m_resonance_mass = arg_resonance_mass; }
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> resonanceBuilder::operator()(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> legs) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    int n = legs.size();
    if(n >1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true);
        do {
            edm4hep::ReconstructedParticleData reso;
            TLorentzVector reso_lv;
            for(int i = 0; i < n; ++i) {
                if(v[i]) {
                    reso.charge += legs[i].charge;
                    TLorentzVector leg_lv;
                    leg_lv.SetXYZM(legs[i].momentum.x, legs[i].momentum.y, legs[i].momentum.z, legs[i].mass);
                    reso_lv += leg_lv;
                }
            }
            if(reso.charge != 0) continue;
            reso.momentum.x = reso_lv.Px();
            reso.momentum.y = reso_lv.Py();
            reso.momentum.z = reso_lv.Pz();
            reso.mass = reso_lv.M();
            result.emplace_back(reso);
        } 
        while(std::next_permutation(v.begin(), v.end()));
    }
    if(result.size() > 1) {
        auto resonancesort = [&] (edm4hep::ReconstructedParticleData i ,edm4hep::ReconstructedParticleData j) { return (abs( m_resonance_mass -i.mass)<abs(m_resonance_mass-j.mass)); };
        std::sort(result.begin(), result.end(), resonancesort);
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator first = result.begin();
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>::const_iterator last = result.begin() + 1;
        ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> onlyBestReso(first, last);
        return onlyBestReso;
    } 
    else {
        return result;
    }
}





ROOT::VecOps::RVec<float> acolinearity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 ROOT::VecOps::RVec<float> result;
 if(in.size() != 2) return result;

 TLorentzVector p1;
 p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

 TLorentzVector p2;
 p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

 float acol = abs(p1.Theta() - p2.Theta());

 result.push_back(acol);
 return result;
}



ROOT::VecOps::RVec<float> acoplanarity(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in){
 ROOT::VecOps::RVec<float> result;
 if(in.size() != 2) return result;

 TLorentzVector p1;
 p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

 TLorentzVector p2;
 p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

 float acop = abs(p1.Phi() - p2.Phi());
 if(acop > M_PI) acop = 2 * M_PI - acop;
 acop = M_PI - acop;

 result.push_back(acop);
 return result;
}


// perturb the scale of the particles
struct momentum_scale {
    momentum_scale(float arg_scaleunc);
    float scaleunc = 1.;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

momentum_scale::momentum_scale(float arg_scaleunc) : scaleunc(arg_scaleunc) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  momentum_scale::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(in.size());

    for (size_t i = 0; i < in.size(); ++i) {
        
        auto & p = in[i];

        /*
        TLorentzVector lv;
        lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        lv *= (1. + scaleunc);

        p.momentum.x = lv.Px();
        p.momentum.y = lv.Py();
        p.momentum.z = lv.Pz();
        //p.energy = lv.E();
        */



        p.momentum.x = p.momentum.x*(1. + scaleunc);
        p.momentum.y = p.momentum.y*(1. + scaleunc);
        p.momentum.z = p.momentum.z*(1. + scaleunc);
        result.emplace_back(p);
    }
    
    return result;
}




/*                             
                                                       
    Tracks input: ROOT::VecOps::RVec<edm4hep::TrackState> tracks                                                   

    // make track Lorentzvectors
    for(size_t i = 0; i < tracks.size(); ++i) {
      
        double pT = 1e-3 * 0.3*2*TMath::Abs(1./tracks.at(i).omega);
        double theta = TMath::ATan(1./tracks.at(i).tanLambda); // tan(lambda) = cotan(theta)
        while(theta < 0) theta += TMath::Pi();
        double eta = - TMath::Log(TMath::Tan(theta/2.));
        double phi = tracks.at(i).phi;
        
        ROOT::Math::PtEtaPhiMVector tlv;
        tlv.SetPt(pT);
        tlv.SetEta(eta);
        tlv.SetPhi(phi);
        tlv.SetM(0);
        lv_track.push_back(tlv);

        //std::cout << "track " << i << " pT=" << pT << " theta=" << theta << " eta=" << eta << " phi=" << phi << std::endl;
      
    }

                                                       
  
*/




struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    ROOT::VecOps::RVec<double>  operator() ( ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop, 
									 ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rp) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };

ROOT::VecOps::RVec<double>  coneIsolation::coneIsolation::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> recop,
											       ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> rp) {
  
    ROOT::VecOps::RVec<double> result;
    result.reserve(recop.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rp.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rp.at(i).momentum.x, rp.at(i).momentum.y, rp.at(i).momentum.z, rp.at(i).energy);
        
        if(rp.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < recop.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(recop.at(i).momentum.x, recop.at(i).momentum.y, recop.at(i).momentum.z, recop.at(i).energy);
        lv_reco.push_back(tlv);
    }

    
    // compute the isolation (see https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154) 
    for (auto & lv_reco_ : lv_reco) {
    
        double sumNeutral = 0.0;
        double sumCharged = 0.0;
    
        // charged
        for (auto & lv_charged_ : lv_charged) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_charged_.Eta(), lv_charged_.Phi());
            if(dr > dr_min && dr < dr_max) sumCharged += lv_charged_.P();
        }
        
        // neutral
        for (auto & lv_neutral_ : lv_neutral) {
    
            double dr = coneIsolation::deltaR(lv_reco_.Eta(), lv_reco_.Phi(), lv_neutral_.Eta(), lv_neutral_.Phi());
            if(dr > dr_min && dr < dr_max) sumNeutral += lv_neutral_.P();
        }
        
        double sum = sumCharged + sumNeutral;
        double ratio= sum / lv_reco_.P();
        result.emplace_back(ratio);
    }
    return result;
}



struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<double> iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, ROOT::VecOps::RVec<double> iso) {
  ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
  result.reserve(in.size());
  for (size_t i = 0; i < in.size(); ++i) {
    auto & p = in[i];
    if (iso[i] < m_max_iso) {
      result.emplace_back(p);
    }
  }
  return result;
}


struct sel_eta {
    sel_eta(float arg_min_eta, float arg_max_eta = 1e10, bool arg_abs = true);
    float m_min_eta = 1.;
    float m_max_eta = 1e10;
    bool m_abs = true;
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};


sel_eta::sel_eta(float arg_min_eta, float arg_max_eta, bool arg_abs) : m_min_eta(arg_min_eta), m_max_eta(arg_max_eta), m_abs(arg_abs)  {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_eta::operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in) {
    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        float eta = (m_abs) ? abs(tlv.Eta()) : tlv.Eta();
        if(eta > m_min_eta && eta < m_max_eta) result.emplace_back(p);
    }
    return result;
}


// for a given MC index, it returns whether or not one of these muons come (indirectly) from a Higgs decay
bool from_prompt(int i, ROOT::VecOps::RVec<edm4hep::MCParticleData> in, ROOT::VecOps::RVec<int> ind) {

    bool ret = false;
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
    

    if(db == de) return true; // top of tree

   
    for(int id = db; id < de; id++) { // loop over all parents

        int iparent = ind.at(id);
        //std::cout << " Analyze parent idx=" << iparent << " PDG=" << in.at(iparent).PDG << std::endl;
        
        //if(std::abs(in.at(iparent).PDG) == 11) ret = true; // if prompt
        if(iparent == 0) return true;
        else if(std::abs(in.at(iparent).PDG) == 25) ret = false; // non prompt, from Higgs decays
        else ret = from_prompt(iparent, in, ind); // otherwise go up in the decay tree
    }
    
    return ret;
}


// returns the gen particles with given PDGID (absolute) that have the e+/e- as parent, i.e. from prompt
// in Whizard, the prompt leptons from the collision have two parents, the electron and positron
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> select_prompt_leptons(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in, 
                ROOT::VecOps::RVec<int> recind,
				ROOT::VecOps::RVec<int> mcind,
				ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> reco,
                ROOT::VecOps::RVec<edm4hep::MCParticleData> mc,
                ROOT::VecOps::RVec<int> parents, 
                ROOT::VecOps::RVec<int> daugther) {

    ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> result;
    for (size_t i = 0; i < in.size(); ++i) {
        int track_index = in[i].tracks_begin;
        int mc_index = FCCAnalyses::ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        if(from_prompt(mc_index, mc, parents)) {
            result.emplace_back(in[i]);
        }
    }
    return result;
} 
   



}



#endif
