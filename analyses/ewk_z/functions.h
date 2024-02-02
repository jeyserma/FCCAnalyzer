#ifndef FCCANALYZER_EWK_H
#define FCCANALYZER_EWK_H


namespace FCCAnalyses {

// Function that runs the fit for the thrust axis determination
struct thrustFit_mc {
    public:
        thrustFit_mc(const ROOT::VecOps::RVec<float> & arg_px,
        const ROOT::VecOps::RVec<float> & arg_py,
        const ROOT::VecOps::RVec<float> & arg_pz);
    float operator()(const double *par);

    private:
        ROOT::VecOps::RVec<float> _px; // vector of px
        ROOT::VecOps::RVec<float> _py; // vector of py
        ROOT::VecOps::RVec<float> _pz; // vector of pz
};

thrustFit_mc::thrustFit_mc(const ROOT::VecOps::RVec<float> & arg_px, const ROOT::VecOps::RVec<float> & arg_py, const ROOT::VecOps::RVec<float> & arg_pz) {
    _px=arg_px;
    _py=arg_py;
    _pz=arg_pz;
}

float thrustFit_mc::operator()(const double *pars){
    double num = 0.;
    double den = 0.;
    double mag = sqrt(pars[0]*pars[0] + pars[1]*pars[1] + pars[2]*pars[2]);

    for(unsigned int i =0; i<_px.size(); i++) {
        num += std::abs(_px[i]*(pars[0]/mag) + _py[i]*(pars[1]/mag) + _pz[i]*(pars[2]/mag));
        den += sqrt(_px[i]*_px[i] + _py[i]*_py[i] + _pz[i]*_pz[i]);
    }
    if(den>0.){
        double val = num / den;
        return -val;
    }
    return 0.;
};

// Finds the thrust axis based on a list of px, py, pz
// MC based, i.e. 
struct minimize_thrust_mc {
    minimize_thrust_mc(float ipx=1.0, float ipy=1.0, float ipz=1.0, std::string arg_minname="Minuit2", std::string arg_algoname="Migrad", int arg_maxcalls=10000, float arg_tolerance=0.001);
    ROOT::VecOps::RVec<float> operator()(const ROOT::VecOps::RVec<float> & px, const ROOT::VecOps::RVec<float> & py, const ROOT::VecOps::RVec<float> & pz);

    char const *_minname; // Minimizer to use, Minuit2 default
    char const *_algoname; // Optimisation algorithm, Migrad default
    int _maxcalls; // Maximum call to minimization function, default=100000
    float _tolerance; //Tolerance for minimization, default=0.001
    ROOT::Math::Minimizer *_min; //internal ROOT minimizer
    double _step[3]={0.001,0.001,0.001};
    double _variable[3];
};



minimize_thrust_mc::minimize_thrust_mc(float ipx=1.0, float ipy=1.0, float ipz=1.0, std::string arg_minname, std::string arg_algoname, int arg_maxcalls, float arg_tolerance) {
    _minname=arg_minname.c_str();
    _algoname=arg_algoname.c_str();
    _maxcalls=arg_maxcalls;
    _tolerance=arg_tolerance;

    _min = ROOT::Math::Factory::CreateMinimizer(_minname, _algoname);
    _min->SetMaxFunctionCalls(_maxcalls); // for Minuit/Minuit2
    _min->SetMaxIterations(10000);  // for GSL
    _min->SetTolerance(_tolerance);
    _min->SetPrintLevel(0);

    //std::cout << "INIT: f(" << ipx << "," << ipy << "," << ipz << "): " << std::endl;
    _variable[0] = ipx;
    _variable[1] = ipy;
    _variable[2] = ipz;
}

ROOT::VecOps::RVec<float> minimize_thrust_mc::operator()(const ROOT::VecOps::RVec<float> & px, const ROOT::VecOps::RVec<float> & py, const ROOT::VecOps::RVec<float> & pz) {
    _min->SetVariable(0,"x",_variable[0], _step[0]);
    _min->SetVariable(1,"y",_variable[1], _step[1]);
    _min->SetVariable(2,"z",_variable[2], _step[2]);
    // create functon wrapper for minmizer
    // a IMultiGenFunction type
    ROOT::Math::Functor f(thrustFit_mc(px,py,pz),3);
    _min->SetFunction(f);

    //min->SetValidError(true);
    //min->ProvidesError();
    _min->Minimize();
    //std::cout << "is valid error before hesse " << min->IsValidError() <<std::endl;
    //min->Hesse();
    //std::cout << "is valid error after hesse  " << min->IsValidError() <<std::endl;
    //std::cout << "Ncalls  " << _min->NCalls() << "  Niter " << _min->NIterations() <<std::endl;
    //_min->PrintResults();
    const double *xs = _min->X();
    const double *xs_err = _min->Errors();

    //std::cout << "Minimum: f(" << xs[0] << "," << xs[1] << "," << xs[2] << "): " << _min->MinValue()  << std::endl;

    ROOT::VecOps::RVec<float> result;
    result.push_back(-1.*_min->MinValue());
    result.push_back(xs[0]);
    result.push_back(xs_err[0]);
    result.push_back(xs[1]);
    result.push_back(xs_err[1]);
    result.push_back(xs[2]);
    result.push_back(xs_err[2]);

    return result;
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


}


#endif