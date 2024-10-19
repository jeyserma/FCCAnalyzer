#ifndef FCCANALYZER_ZH_MASS_XSEC_H
#define FCCANALYZER_ZH_MASS_XSEC_H


namespace FCCAnalyses {


Vec_rp unBoostCrossingAngle(Vec_rp in, float angle) {
    Vec_rp result;
    float ta = std::tan(angle);
    for (size_t i=0; i < in.size(); ++i) {
        auto & p = in[i];
        edm4hep::ReconstructedParticleData newp = p;
        float e = p.energy;
        float px = p.momentum.x;
        float e_prime = e * sqrt(1 + ta*ta) + px * ta;
        float px_prime = px * sqrt(1 + ta*ta) + e * ta;
        newp.momentum.x = px_prime;
        newp.energy = e_prime;
        result.push_back(newp);
    }
    return result;
}

Vec_mc unBoostCrossingAngle(Vec_mc in, float angle) {
    Vec_mc result;
    float ta = std::tan(angle);
    for (size_t i=0; i < in.size(); ++i) {
        auto & p = in[i];
        TLorentzVector mc_;
        mc_.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        edm4hep::MCParticleData newp = p;
        float e = mc_.Energy();
        float px = p.momentum.x;
        float px_prime = px * sqrt(1 + ta*ta) + e * ta;
        newp.momentum.x = px_prime;
        result.push_back(newp);
    }
    return result;
}

// calculate the cosine(theta) of the missing energy vector
bool has_forward_photon(float cut, Vec_rp in) {
    
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        TLorentzVector lv;
        lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(lv.Theta() > (M_PI-cut) || lv.Theta() < cut) return true;
    }
    return false;
}




// calculate the number of foward leptons
struct polarAngleCategorization {
    polarAngleCategorization(float arg_thetaMin, float arg_thetaMax);
    float thetaMin = 0;
    float thetaMax = 5;
    int operator() (Vec_rp in);
};

polarAngleCategorization::polarAngleCategorization(float arg_thetaMin, float arg_thetaMax) : thetaMin(arg_thetaMin), thetaMax(arg_thetaMax) {};
int polarAngleCategorization::operator() (Vec_rp in) {
    
    int nFwd = 0; // number of forward leptons
    for (size_t i = 0; i < in.size(); ++i) {
        
        auto & p = in[i];
        TLorentzVector lv;
        lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(lv.Theta() < thetaMin || lv.Theta() > thetaMax) nFwd += 1;
    }
    return nFwd;
}


// calculate the cosine(theta) of the missing energy vector
float get_cosTheta_miss(Vec_rp met){
    
    float costheta = 0.;
    if(met.size() > 0) {
        
        TLorentzVector lv_met;
        lv_met.SetPxPyPzE(met[0].momentum.x, met[0].momentum.y, met[0].momentum.z, met[0].energy);
        costheta = fabs(std::cos(lv_met.Theta()));

    }
    return costheta;
}


// perturb the momentum scale with a given constant
struct lepton_momentum_scale {
    lepton_momentum_scale(float arg_scaleunc);
    float scaleunc = 1.;
    Vec_rp operator() (ROOT::VecOps::RVec<edm4hep::ReconstructedParticleData> in);
};

lepton_momentum_scale::lepton_momentum_scale(float arg_scaleunc) : scaleunc(arg_scaleunc) {};
Vec_rp lepton_momentum_scale::operator() (Vec_rp in) {
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        p.momentum.x = p.momentum.x*(1. + scaleunc);
        p.momentum.y = p.momentum.y*(1. + scaleunc);
        p.momentum.z = p.momentum.z*(1. + scaleunc);
        result.emplace_back(p);
    }
    return result;
}

Vec_rp correct_scale(Vec_rp in) {
    // correct scale as function of charge and theta
    Vec_rp result;
    result.reserve(in.size());
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        float scale = 1.;
        TLorentzVector tlv;
        tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(p.charge > 0) {
            scale = -3.10714E-05*std::abs(tlv.Theta()) + 9.99664E-01;
        }
        else {
            scale = 3.82143E-05*std::abs(tlv.Theta()) + 1.00016E+00;
        }
        p.momentum.x = p.momentum.x/scale;
        p.momentum.y = p.momentum.y/scale;
        p.momentum.z = p.momentum.z/scale;
        result.emplace_back(p);
    }
    return result;

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
    Vec_rp operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) ;
};

resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil(float arg_resonance_mass, float arg_recoil_mass, float arg_chi2_recoil_frac, float arg_ecm, bool arg_use_MC_Kinematics) {m_resonance_mass = arg_resonance_mass, m_recoil_mass = arg_recoil_mass, chi2_recoil_frac = arg_chi2_recoil_frac, ecm = arg_ecm, m_use_MC_Kinematics = arg_use_MC_Kinematics;}

Vec_rp resonanceBuilder_mass_recoil::resonanceBuilder_mass_recoil::operator()(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugthers) {

    Vec_rp result;
    result.reserve(3);
    std::vector<std::vector<int>> pairs; // for each permutation, add the indices of the muons
    int n = legs.size();
  
    if(n > 1) {
        ROOT::VecOps::RVec<bool> v(n);
        std::fill(v.end() - 2, v.end(), true); // helper variable for permutations
        do {
            std::vector<int> pair;
            rp reso;
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
  
        Vec_rp bestReso;
        
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
            float d = (1.0-chi2_recoil_frac)*mass + chi2_recoil_frac*rec;
            
            if(d < d_min) {
                d_min = d;
                idx_min = i;
            }

     
        }
        if(idx_min > -1) { 
            bestReso.push_back(result.at(idx_min));
            auto & l1 = legs[pairs[idx_min][0]];
            auto & l2 = legs[pairs[idx_min][1]];
            bestReso.emplace_back(l1);
            bestReso.emplace_back(l2);
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
    










// obsolete
Vec_rp muon_quality_check(Vec_rp in){
	
    Vec_rp result;

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
   
    
}


#endif