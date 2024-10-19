#ifndef FCCANALYZER_HWW_H
#define FCCANALYZER_HWW_H

namespace FCCAnalyses {


// for a given MC index, it returns whether or not one of these muons come (indirectly) from a Higgs decay
bool from_W_decay(int i, Vec_mc in, Vec_i ind) {

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

    if(db == de) return false; // top of tree

    for(int id = db; id < de; id++) { // loop over all parents

        int iparent = ind.at(id);
        if(std::abs(in.at(iparent).PDG) == 24) ret = true; // if W particle is found
        else if(std::abs(in.at(iparent).PDG) == 15) ret = false; // no muons from taus
        else ret = from_W_decay(iparent, in, ind); // otherwise go up in the decay tree
    }

    return ret;
}



// for a given lepton collection (legs), it returns whether or not one of these muons come (indirectly) from a Higgs decay
bool W_muonic_decays(Vec_mc mc, Vec_i parents, Vec_i daugther) {

    bool ret = true;
    // get Higgs
    int w_parent_idx = -1;
    //cout << "******************" << endl;
    for(size_t i = 0; i < mc.size(); ++i) {
        auto & p = mc[i];
        if(std::abs(p.PDG) != 24) continue;
        //cout << "select " << p.PDG << " PARENT" << mc.at(parents.at(p.parents_begin)).PDG  << endl;
        for(unsigned j = p.daughters_begin; j != p.daughters_end; ++j) {
            if(abs(mc.at(daugther.at(j)).PDG) != 13) {
                ret = false;
                break;
            }
            //cout << " DAUGHTER PDGID=" << mc.at(daugther.at(j)).PDG  << endl;
            //higgs_parent_idx = parents.at(j);
            break;
        }
    }

    return ret;
}



// for a given lepton collection (legs), it returns whether or not one of these muons come (indirectly) from a Higgs decay
Vec_rp from_W_decay(Vec_rp legs, Vec_i recind, Vec_i mcind, Vec_rp reco, Vec_mc mc, Vec_i parents, Vec_i daugther) {

    Vec_rp ret;
    for (size_t i = 0; i < legs.size(); ++i) {
        int track_index = legs[i].tracks_begin;
        int mc_index = ReconstructedParticle2MC::getTrack2MC_index(track_index, recind, mcind, reco);
        if(from_W_decay(mc_index, mc, parents)) {
            ret.push_back(legs[i]);
        }
    }
    return ret;
}


}

#endif