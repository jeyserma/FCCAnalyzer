#ifndef FCCANALYZER_ZH_RARE_H
#define FCCANALYZER_ZH_RARE_H


namespace FCCAnalyses {
    
// calculate the cosine(theta) of the missing energy vector
bool sel_costheta(float cut, Vec_rp in) {
    
    for (size_t i = 0; i < in.size(); ++i) {
        auto & p = in[i];
        TLorentzVector lv;
        lv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
        if(lv.Theta() > (M_PI-cut) || lv.Theta() < cut) return true;
    }
    return false;
}
    

}


#endif