#ifndef FCCANALYZER_JETCLUSTERING_H
#define FCCANALYZER_JETCLUSTERING_H

#include <tbb/task_arena.h>

#include "FastJet/JetClustering.h"
#include "FastJet/ExternalRecombiner.h"

#include "FCCAnalyses/JetClusteringUtils.h"

#include "fastjet/install/include/fastjet/JetDefinition.hh"
#include "fastjet/install/include/fastjet/PseudoJet.hh"
#include "fastjet/install/include/fastjet/Selector.hh"

namespace FCCAnalyses {
    
class clustering_ee_genkt_c {

    public:
        float _radius;   ///< jet cone radius
        int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
        float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
        int _sorted;         ///< pT ordering=0, E ordering=1
        int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
        float _exponent;     /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
        fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
        fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
        fastjet::ClusterSequence _cs;                ///<internal clustering sequence
        fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
        
        clustering_ee_genkt_c(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent) {
            _radius = arg_radius;
            _exclusive = arg_exclusive;
            _cut = arg_cut;
            _sorted = arg_sorted;
            _recombination = arg_recombination;
            _exponent = arg_exponent;

            // initialize jet algorithm
            fastjet::JetAlgorithm _jetAlgorithm = fastjet::JetAlgorithm::ee_genkt_algorithm;

            // initialize recombination scheme
            fastjet::RecombinationScheme _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

            //define the clustering sequence and jet definition
            //fastjet::ClusterSequence _cs;
            _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _exponent, _recombScheme);
            if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
              _def.set_recombiner(new ExternalRecombiner(_recombination));
        }
        
        JetClustering::FCCAnalysesJet cluster(const std::vector<fastjet::PseudoJet>& input) {


            //return empty struct
            if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
              return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

            fastjet::ClusterSequence _cs = fastjet::ClusterSequence(input, _def);

            //cluster jets
            std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
            //get dmerged elements
            std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
            std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

            //transform to FCCAnalysesJet
            return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);


        }
    
};

struct clustering_ee_genkt {
    public:
        clustering_ee_genkt(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent);
        JetClustering::FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& jets);

    private:
        float _radius;   ///< jet cone radius
        int _exclusive;  ///< flag for exclusive jet clustering. Possible choices are 0=inclusive clustering, 1=exclusive clustering that would be obtained when running the algorithm with the given dcut, 2=exclusive clustering when the event is clustered (in the exclusive sense) to exactly njets, 3=exclusive clustering when the event is clustered (in the exclusive sense) up to exactly njets, 4=exclusive jets obtained at the given ycut
        float _cut;  ///< pT cut for m_exclusive=0, dcut for m_exclusive=1, N jets for m_exlusive=2, N jets for m_exclusive=3, ycut for m_exclusive=4
        int _sorted;         ///< pT ordering=0, E ordering=1
        int _recombination;  ///< E_scheme=0, pt_scheme=1, pt2_scheme=2, Et_scheme=3, Et2_scheme=4, BIpt_scheme=5, BIpt2_scheme=6, E0_scheme=10, p_scheme=11
        float _exponent;     /// anti-kT algorithm=-1, cambridge algorithm=0, kT algorithm=1
        fastjet::JetAlgorithm _jetAlgorithm{fastjet::JetAlgorithm::undefined_jet_algorithm};  ///<internal jet algorithm
        fastjet::RecombinationScheme _recombScheme;  ///<internal recombination scheme
        fastjet::ClusterSequence _cs;                ///<internal clustering sequence
        fastjet::JetDefinition _def;                 ///<internal jetdefinition sequence
};


clustering_ee_genkt::clustering_ee_genkt(
      float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent) {
    _radius = arg_radius;
    _exclusive = arg_exclusive;
    _cut = arg_cut;
    _sorted = arg_sorted;
    _recombination = arg_recombination;
    _exponent = arg_exponent;

    // initialize jet algorithm
    fastjet::JetAlgorithm _jetAlgorithm = fastjet::JetAlgorithm::ee_genkt_algorithm;

    // initialize recombination scheme
    fastjet::RecombinationScheme _recombScheme = FCCAnalyses::JetClusteringUtils::recomb_scheme(_recombination);

    //define the clustering sequence and jet definition
    //fastjet::ClusterSequence _cs;
    _def = fastjet::JetDefinition(_jetAlgorithm, _radius, _exponent, _recombScheme);
    if (_recombScheme == fastjet::RecombinationScheme::external_scheme)
      _def.set_recombiner(new ExternalRecombiner(_recombination));
}
  


JetClustering::FCCAnalysesJet clustering_ee_genkt::operator()(const std::vector<fastjet::PseudoJet>& input) {
    //return empty struct
    if (FCCAnalyses::JetClusteringUtils::check(input.size(), _exclusive, _cut) == false)
      return FCCAnalyses::JetClusteringUtils::initialise_FCCAnalysesJet();

    fastjet::ClusterSequence _cs = fastjet::ClusterSequence(input, _def);

    //cluster jets
    std::vector<fastjet::PseudoJet> pjets = FCCAnalyses::JetClusteringUtils::build_jets(_cs, _exclusive, _cut, _sorted);
    //get dmerged elements
    std::vector<float> dmerge = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 0);
    std::vector<float> dmerge_max = FCCAnalyses::JetClusteringUtils::exclusive_dmerge(_cs, 1);

    //transform to FCCAnalysesJet
    return FCCAnalyses::JetClusteringUtils::build_FCCAnalysesJet(pjets, dmerge, dmerge_max);
  }
  

class clustering_helper {
    public:
        clustering_helper(float arg_radius, int arg_exclusive, float arg_cut, int arg_sorted, int arg_recombination, float arg_exponent, const unsigned int nslots = 1) {
            //clustering_ee_genkt tmp(arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent);
            clustering_ee_genkt_c ff = clustering_ee_genkt_c(arg_radius, arg_exclusive, arg_cut, arg_sorted, arg_recombination, arg_exponent);
            const unsigned int nslots_actual = std::max(nslots, 1U);

            interpreters_.reserve(nslots_actual);
            for (unsigned int islot = 0; islot < nslots_actual; ++islot) {
                interpreters_.emplace_back(ff);
            }
        }

        JetClustering::FCCAnalysesJet operator()(const std::vector<fastjet::PseudoJet>& input) {

            auto const tbb_slot = std::max(tbb::this_task_arena::current_thread_index(), 0);

            if (tbb_slot >= interpreters_.size()) {
                throw std::runtime_error("Not enough interpreters allocated for number of tbb threads");
            }

            auto &interpreter_data = interpreters_[tbb_slot];
            return interpreter_data.cluster(input);
        }

    private:
        unsigned int nvars_;
        std::vector<clustering_ee_genkt_c> interpreters_;

};


}


#endif