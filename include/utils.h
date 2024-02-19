#ifndef FCCANALYZER_UTILS_H
#define FCCANALYZER_UTILS_H

#include "defines.h"

namespace FCCAnalyses {

Vec_i getMaxAndSecondMaxIdx(Vec_f in) {
    int maxIndex = 0;
    int secondMaxIndex = -1; // Initialize to an invalid index

    for (int i = 1; i < in.size(); ++i) {
        if (in[i] > in[maxIndex]) {
            secondMaxIndex = maxIndex;
            maxIndex = i;
        } else if (secondMaxIndex == -1 || in[i] > in[secondMaxIndex]) {
            secondMaxIndex = i;
        }
    }
    Vec_i ret;
    ret.push_back(maxIndex);
    ret.push_back(secondMaxIndex);
    return ret;
}

Vec_i jetTruthFinder(std::vector<std::vector<int>> constituents, Vec_rp reco, Vec_mc mc, Vec_i mcind) {
    // jet truth=finder: match the gen-level partons (eventually with gluons) with the jet constituents
    // matching by mimimizing the sum of dr of the parton and all the jet constituents 

    Vec_tlv genQuarks; // Lorentz-vector of potential partons (gen-level)
    Vec_i genQuarks_pdgId; // corresponding PDG ID
    for(size_t i = 0; i < mc.size(); ++i) {
        int pdgid = abs(mc.at(i).PDG);
        if(pdgid > 6) continue; // only quarks 
        //if(pdgid > 6 and pdgid != 21) continue; // only quarks and gluons
        TLorentzVector tlv;
        tlv.SetXYZM(mc.at(i).momentum.x,mc.at(i).momentum.y,mc.at(i).momentum.z,mc.at(i).mass);
        genQuarks.push_back(tlv);
        genQuarks_pdgId.push_back(mc.at(i).PDG);
    }

    Vec_tlv recoParticles; // Lorentz-vector of all reconstructed particles
    for(size_t i = 0; i < reco.size(); ++i) {
        auto & p = reco[i];
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        recoParticles.push_back(tlv);
    }

    Vec_i usedIdx;
    Vec_i result;
    for(size_t iJet = 0; iJet < constituents.size(); ++iJet) {
        Vec_d dr;
        for(size_t iGen = 0; iGen < genQuarks.size(); ++iGen) {
            if(std::find(usedIdx.begin(), usedIdx.end(), iGen) != usedIdx.end()) {
                dr.push_back(1e99); // set infinite dr, skip
                continue;
            }
            dr.push_back(0);
            for(size_t i = 0; i < constituents[iJet].size(); ++i) {
                dr[iGen] += recoParticles[constituents[iJet][i]].DeltaR(genQuarks[iGen]);
            }
        }
        int maxDrIdx = std::min_element(dr.begin(),dr.end()) - dr.begin();
        usedIdx.push_back(maxDrIdx);
        result.push_back(genQuarks_pdgId[maxDrIdx]);

    }
    return result;
}

Vec_f calculate_cos_theta(Vec_f thetas, bool abs=true) {
    Vec_f ret; 
    for(auto & theta: thetas) {
        if(abs) ret.push_back(std::abs(cos(theta)));
        else ret.push_back(cos(theta));
    }
    return ret;
}

// make Lorentz vectors for a given RECO particle collection
Vec_tlv makeLorentzVectors(Vec_rp in) {
    Vec_tlv result;
    for(auto & p: in) {
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        result.push_back(tlv);
    }
    return result;
}


// make Lorentz vectors for a given MC particle collection
Vec_tlv makeLorentzVectors(Vec_mc in) {
    Vec_tlv result;
    for(auto & p: in) {
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        result.push_back(tlv);
    }
    return result;
}

// make Lorentzvectors from pseudojets
Vec_tlv makeLorentzVectors(Vec_f jets_px, Vec_f jets_py, Vec_f jets_pz, Vec_f jets_e) {
    Vec_tlv result;
    for(int i=0; i<jets_px.size(); i++) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(jets_px[i], jets_py[i], jets_pz[i], jets_e[i]);
        result.push_back(tlv);
    }
    return result;
}



// select the hadronic Z decays in ZH(Za), second Z)
bool hadronicDecays(Vec_mc mc_particles, Vec_i daughters) {

	size_t len = mc_particles.size();
    for(size_t i = 0; i < len; ++i) {
        if(mc_particles[i].PDG != 23) continue;

		int db = mc_particles[i].daughters_begin;
		int de = mc_particles[i].daughters_end;
		
		int pdgb = std::abs(mc_particles[daughters[db]].PDG);
		int pdge = std::abs(mc_particles[daughters[de]].PDG);
		
		int pdg_prodc = pdgb*pdge;
		if(pdg_prodc == 1 or pdg_prodc == 4 or pdg_prodc == 9 or pdg_prodc == 16 or pdg_prodc == 25) return true;
		else return false;
	}

	return false;
}
    
Vec_tlv jetsToTlv(Vec_f px, Vec_f py, Vec_f pz, Vec_f e) {

    Vec_tlv ret;
    for(int i=0; i<4; i++) {
        TLorentzVector tlv;
        tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        ret.push_back(tlv);
    }
    return ret;

}    
    
Vec_tlv energyReconstructFourJet(Vec_f px, Vec_f py, Vec_f pz, Vec_f e) {
    
    
    //cout << "***************" << endl;
    
    //cout << px.size() << endl;
    
    float p0 = std::sqrt(px[0]*px[0] + py[0]*py[0] + pz[0]*pz[0]);
    float p1 = std::sqrt(px[1]*px[1] + py[1]*py[1] + pz[1]*pz[1]);
    float p2 = std::sqrt(px[2]*px[2] + py[2]*py[2] + pz[2]*pz[2]);
    float p3 = std::sqrt(px[3]*px[3] + py[3]*py[3] + pz[3]*pz[3]);

    TMatrixD mtrx(4, 4);
    mtrx(0, 0) = 1;
    mtrx(0, 1) = 1;
    mtrx(0, 2) = 1;
    mtrx(0, 3) = 1;

    mtrx(1, 0) = px[0]/e[0];
    mtrx(1, 1) = px[1]/e[1];
    mtrx(1, 2) = px[2]/e[2];
    mtrx(1, 3) = px[3]/e[3];
    
    mtrx(2, 0) = py[0]/e[0];
    mtrx(2, 1) = py[1]/e[1];
    mtrx(2, 2) = py[2]/e[2];
    mtrx(2, 3) = py[3]/e[3];
    
    mtrx(3, 0) = pz[0]/e[0];
    mtrx(3, 1) = pz[1]/e[1];
    mtrx(3, 2) = pz[2]/e[2];
    mtrx(3, 3) = pz[3]/e[3];
    
    TMatrixD inv = mtrx.Invert();
    
    
    TVectorD vec(4);
    vec(0) = 240;
    vec(1) = 0;
    vec(2) = 0;
    vec(3) = 0;
    
    TVectorD res = inv*vec;
    
    bool isValid = true;
    
    if(res[0]<0 or res[1]<0 or res[2]<0 or res[3]<0 or res[0]>240 or res[1]>240 or res[2]>240 or res[3]>240) {
        isValid = false;
    }
    if(!isValid) {
        cout << "***************" << endl;
        cout << px[0] << " " << py[0] << " " << pz[0] << " " << p0 << " " << e[0] << " " << res[0] << endl;
        cout << px[1] << " " << py[1] << " " << pz[1] << " " << p1 << " " << e[1] << " " << res[1] << endl;
        cout << px[2] << " " << py[2] << " " << pz[2] << " " << p2 << " " << e[2] << " " << res[2] << endl;
        cout << px[3] << " " << py[3] << " " << pz[3] << " " << p3 << " " << e[3] << " " << res[3] << endl;
    }
    
    
    Vec_tlv ret;
    float chi2 = 0;
    for(int i=0; i<4; i++) {
        TLorentzVector tlv;
        if(isValid)
            tlv.SetPxPyPzE(px[i]*res[i]/e[i], py[i]*res[i]/e[i], pz[i]*res[i]/e[i], res[i]);
        else
            tlv.SetPxPyPzE(px[i], py[i], pz[i], e[i]);
        ret.push_back(tlv);
        
        if(res[i] > 0) {
            float uncert = 0.5*std::sqrt(e[i]) + 0.05*e[i];
            float delta = (e[i]-res[i])/uncert;
            chi2 += delta*delta;
        }
        else {
            chi2 += 1000.;
        }
    }
    
    // add chi2 as dummy to the list of Lorentz vectors
    TLorentzVector chi2_;
    chi2_.SetPxPyPzE(0, 0, 0, chi2);
    ret.push_back(chi2_);
    
    
    return ret;
}

  
// make Lorentz vectors for a given collections
TLorentzVector sum4Vectors(Vec_mc in) {
	
	TLorentzVector ret;
	for (auto & p: in) {
		TLorentzVector tlv;
		tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        ret += tlv;
	}
	return ret;
}
  


// computes longitudinal and transversal energy balance of all particles
Vec_f energy_imbalance(Vec_rp in) {
    float e_tot = 0;
    float e_trans = 0;
    float e_long = 0;
    for(auto &p : in) {
        float mag = std::sqrt(p.momentum.x*p.momentum.x + p.momentum.y*p.momentum.y + p.momentum.z*p.momentum.z);
        float cost = p.momentum.z / mag;
        float sint =  std::sqrt(p.momentum.x*p.momentum.x + p.momentum.y*p.momentum.y) / mag;
        if(p.momentum.y < 0) sint *= -1.0;
        e_tot += p.energy;
        e_long += cost*p.energy;
        e_trans += sint*p.energy;
    }
    Vec_f result;
    result.push_back(e_tot);
    result.push_back(std::abs(e_trans));
    result.push_back(std::abs(e_long));
    return result;
}

    
// maps theta [pi/2, pi] to [0, pi/2]
Vec_f theta_abs(Vec_f in) {
    
    Vec_f result;
    result.reserve(in.size());
    
    for(int i = 0; i < in.size(); ++i) {
        
        if(in[i] > M_PI/2.0) result.push_back(M_PI/2.0-in[i]);
        else result.push_back(in[i]);
    }
    return result;
}

// deltaR between two reco particles, based on eta
float deltaR(Vec_rp in) {
    if(in.size() != 2) return -1;
    
    ROOT::Math::PxPyPzEVector tlv1;
    tlv1.SetPxPyPzE(in.at(0).momentum.x, in.at(0).momentum.y, in.at(0).momentum.z, in.at(0).energy);

    ROOT::Math::PxPyPzEVector tlv2;
    tlv2.SetPxPyPzE(in.at(1).momentum.x, in.at(1).momentum.y, in.at(1).momentum.z, in.at(1).energy);
    
    return std::sqrt(std::pow(tlv1.Eta()-tlv2.Eta(), 2) + std::pow(tlv1.Phi()-tlv2.Phi(), 2));
}

// crossing angle between particles in XZ plane
float crossingAngle(Vec_mc in) {
    if(in.size() != 2) return -999;
    
    float t1 = std::atan2(in[0].momentum.x, in[0].momentum.z);
    float t2 = std::atan2(in[1].momentum.x, in[1].momentum.z);
    return std::abs(t1-t2);
}

// acolinearity between two reco particles
float acolinearity(Vec_rp in) {
    if(in.size() < 2) return -999;

    TLorentzVector p1;
    p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

    TLorentzVector p2;
    p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

    TVector3 v1 = p1.Vect();
    TVector3 v2 = p2.Vect();
    return std::acos(v1.Dot(v2)/(v1.Mag()*v2.Mag())*(-1.));
}

// acoplanarity between two reco particles
float acoplanarity(Vec_rp in) {
    if(in.size() < 2) return -999;

    TLorentzVector p1;
    p1.SetXYZM(in[0].momentum.x, in[0].momentum.y, in[0].momentum.z, in[0].mass);

    TLorentzVector p2;
    p2.SetXYZM(in[1].momentum.x, in[1].momentum.y, in[1].momentum.z, in[1].mass);

    float acop = abs(p1.Phi() - p2.Phi());
    if(acop > M_PI) acop = 2 * M_PI - acop;
    acop = M_PI - acop;

    return acop;
}

// visible energy
float visibleEnergy(Vec_rp in, float p_cutoff = 0.0) {
    float e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        e += p.energy;
    }
    return e;
}

// returns missing energy vector, based on reco particles
Vec_rp missingEnergy(float ecm, Vec_rp in, float p_cutoff = 0.0) {
    float px = 0, py = 0, pz = 0, e = 0;
    for(auto &p : in) {
        if (std::sqrt(p.momentum.x * p.momentum.x + p.momentum.y*p.momentum.y) < p_cutoff) continue;
        px += -p.momentum.x;
        py += -p.momentum.y;
        pz += -p.momentum.z;
        e += p.energy;
    }
    
    Vec_rp ret;
    rp res;
    res.momentum.x = px;
    res.momentum.y = py;
    res.momentum.z = pz;
    res.energy = ecm-e;
    ret.emplace_back(res);
    return ret;
    
}

// calculate the visisble mass of the event
float visibleMass(Vec_rp in, float p_cutoff = 0.0) {
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
  
// calculate the missing mass, given a ECM value
float missingMass(float ecm, Vec_rp in, float p_cutoff = 0.0) {
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
            result.push_back(reco_.P()/mc_.P());
            //if(mc_.P() > 20) result.push_back(reco_.P()/mc_.P());
		}
    } 
    return result;
}


ROOT::VecOps::RVec<float> leptonResolution_theta(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons, ROOT::VecOps::RVec<int> recind,
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
            result.push_back(reco_.Theta()/mc_.Theta());
		}
    } 
    return result;
}


ROOT::VecOps::RVec<float> leptonResolution_phi(ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> muons, ROOT::VecOps::RVec<int> recind,
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
            result.push_back(reco_.Phi()/mc_.Phi());
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














// compute the cone isolation for reco particles
struct coneIsolation {

    coneIsolation(float arg_dr_min, float arg_dr_max);
    double deltaR(double eta1, double phi1, double eta2, double phi2) { return TMath::Sqrt(TMath::Power(eta1-eta2, 2) + (TMath::Power(phi1-phi2, 2))); };

    float dr_min = 0;
    float dr_max = 0.4;
    Vec_f operator() (Vec_rp in, Vec_rp rps) ;
};

coneIsolation::coneIsolation(float arg_dr_min, float arg_dr_max) : dr_min(arg_dr_min), dr_max( arg_dr_max ) { };
Vec_f coneIsolation::coneIsolation::operator() (Vec_rp in, Vec_rp rps) {
  
    Vec_f result;
    result.reserve(in.size());

    std::vector<ROOT::Math::PxPyPzEVector> lv_reco;
    std::vector<ROOT::Math::PxPyPzEVector> lv_charged;
    std::vector<ROOT::Math::PxPyPzEVector> lv_neutral;

    for(size_t i = 0; i < rps.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(rps.at(i).momentum.x, rps.at(i).momentum.y, rps.at(i).momentum.z, rps.at(i).energy);
        
        if(rps.at(i).charge == 0) lv_neutral.push_back(tlv);
        else lv_charged.push_back(tlv);
    }
    
    for(size_t i = 0; i < in.size(); ++i) {

        ROOT::Math::PxPyPzEVector tlv;
        tlv.SetPxPyPzE(in.at(i).momentum.x, in.at(i).momentum.y, in.at(i).momentum.z, in.at(i).energy);
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


// filter reconstructed particles (in) based a property (prop) within a defined range (m_min, m_max)
struct sel_range {
    sel_range(float arg_min, float arg_max, bool arg_abs = false);
    float m_min = 0.;
    float m_max = 1.;
    bool m_abs = false;
    Vec_rp operator() (Vec_rp in, Vec_f prop);
};

sel_range::sel_range(float arg_min, float arg_max, bool arg_abs) : m_min(arg_min), m_max(arg_max), m_abs(arg_abs) {};
Vec_rp sel_range::operator() (Vec_rp in, Vec_f prop) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        float val = (m_abs) ? abs(prop[i]) : prop[i];
        if(val > m_min && val < m_max) result.emplace_back(p);
    }
    return result;
}









// obsolete
struct sel_iso {
    sel_iso(float arg_max_iso);
    float m_max_iso = .25;
    Vec_rp operator() (Vec_rp in, Vec_f iso);
  };

sel_iso::sel_iso(float arg_max_iso) : m_max_iso(arg_max_iso) {};
ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData>  sel_iso::operator() (Vec_rp in, Vec_f iso) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        if (iso[i] < m_max_iso) {
            result.emplace_back(p);
        }
    }
    return result;
}


// obsolete
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




}



#endif
