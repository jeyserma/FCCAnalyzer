#ifndef HELPER_TMVA_H
#define HELPER_TMVA_H

#include <tbb/task_arena.h>

namespace FCCAnalyses {

class tmva_helper {
	public:
		tmva_helper(const std::string &filename, const std::string &name, const unsigned &nvars, const unsigned int nslots = 1) :
			model_(name, filename), nvars_(nvars) {

			const unsigned int nslots_actual = std::max(nslots, 1U);
					
			interpreters_.reserve(nslots_actual);
			for (unsigned int islot = 0; islot < nslots_actual; ++islot) {
				interpreters_.emplace_back(model_);
			}
		}

		double operator()(const Vec_f vars) {
			
			auto const tbb_slot = std::max(tbb::this_task_arena::current_thread_index(), 0);

			if (tbb_slot >= interpreters_.size()) {
				throw std::runtime_error("Not enough interpreters allocated for number of tbb threads");
			}

			auto &interpreter_data = interpreters_[tbb_slot];
			auto c = interpreter_data.Compute(vars);
			return c[0];
		}

    private:
		unsigned int nvars_;
        TMVA::Experimental::RBDT<> model_;
		std::vector<TMVA::Experimental::RBDT<>> interpreters_;

};

}

#endif

