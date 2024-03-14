#ifndef FCCANALYZER_BW_WEIGHTS_H
#define FCCANALYZER_BW_WEIGHTS_H

#include "defines.h"

namespace FCCAnalyses {




// Breit-Wigner mass weights
const double MZ_GEN_ = 91153.509740726733;
const double GAMMAZ_GEN_ = 2493.2018986110700;
//const double MW_GEN_ = 80351.812293789408;
//const double GAMMAW_GEN_ = 2090.4310808144846;
const double MW_GEN_ = 80379.0;
const double GAMMAW_GEN_ = 2085.0;



double computeBreitWignerWeight(double massVgen, double offset, int type) {

    double MV_GEN_ = 0;
    double GAMMAV_GEN_ = 0;
    if(type == 0) {
        MV_GEN_ = MZ_GEN_;
        GAMMAV_GEN_ = GAMMAZ_GEN_;
    }
    else {
        MV_GEN_ = MW_GEN_;
        GAMMAV_GEN_ = GAMMAW_GEN_;
    }

    double targetMass = MV_GEN_ + offset;
    //double gamma_cen = std::sqrt(MV_GEN_*MV_GEN_*(MV_GEN_*MV_GEN_+GAMMAV_GEN_*GAMMAV_GEN_));
    //double gamma = std::sqrt(targetMass*targetMass*(targetMass*targetMass+GAMMAV_GEN_*GAMMAV_GEN_));
    double s_hat = massVgen*massVgen*1000*1000;
    double offshell = s_hat - MV_GEN_*MV_GEN_;
    double offshellOffset = s_hat - targetMass*targetMass;
    double weight = (offshell*offshell + GAMMAV_GEN_*GAMMAV_GEN_*MV_GEN_*MV_GEN_) / (offshellOffset*offshellOffset + GAMMAV_GEN_*GAMMAV_GEN_*targetMass*targetMass);
    return weight;
}

double breitWignerWeights_WW(double massVgen1, double massVgen2, double offset, int type=1) {

    // Z -> type=0
    // W -> type=1
    double w1 = computeBreitWignerWeight(massVgen1, offset, type);
    double w2 = computeBreitWignerWeight(massVgen2, offset, type);
    return w1*w2;
}


}

#endif
