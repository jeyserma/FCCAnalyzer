#ifndef FCCANALYZER_TWO_PHOTON_H
#define FCCANALYZER_TWO_PHOTON_H


namespace FCCAnalyses {




Vec_i get_hard_photons(Vec_mc mc, Vec_i ind) {
   Vec_i res;
    //cout << "dddddddddddd" << endl;
   
   for(size_t i = 0; i < mc.size(); ++i) {
        auto & p = mc[i];

        // select beam electrons
        if(std::abs(p.PDG) != 22) continue;

        int ms = p.parents_begin;
        int me = p.parents_end;
        for(size_t j = ms; j < me; j++) {
            int mother_pdgid = mc[ind[j]].PDG;
            if(std::abs(mother_pdgid) != 11) continue;
            res.push_back(i);
            break;
            //TLorentzVector tlv;
            //tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);

            
            //cout << "-------------- " << mother_pdgid << " " << tlv.E() << endl;
        }
        //int idx_ms = ind[ms];
        //int idx_me = ind[me-1];
        //int pdg_m1 = mc[idx_ms].PDG;
        //int pdg_m2 = mc[idx_me].PDG;
        
        
        
        
        /*
        if(std::abs(pdg_d1) == 24 or std::abs(pdg_d2) == 24) continue;
        if(p.PDG == 24) {
            res[0] = pdg_d1;
            res[1] = pdg_d2;
        }
        else {
            res[2] = pdg_d1;
            res[3] = pdg_d2;
        }
        */
   }
   //cout << "-------------- " << res[0] << " " << res[1] << " " << res[2] << " " << res[3] << endl;
   return res;
}

}


#endif