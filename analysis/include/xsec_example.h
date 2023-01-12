#ifndef XSEC_EXAMPLE_H
#define XSEC_EXAMPLE_H

#include <cmath>
#include <vector>

#include "TLorentzVector.h"
#include "ROOT/RVec.hxx"
#include "edm4hep/ReconstructedParticleData.h"
#include "edm4hep/MCParticleData.h"
#include "edm4hep/ParticleIDData.h"

#include "ReconstructedParticle2MC.h"

namespace FCCAnalyses {
  


Vec_tlv makeLorentzVectors(Vec_rp in) {
	
	Vec_tlv result;
	for (auto & p: in) {
		TLorentzVector tlv;
		tlv.SetXYZM(p.momentum.x, p.momentum.y, p.momentum.z, p.mass);
		result.push_back(tlv);
	}
	return result;
}



    
}

#endif
