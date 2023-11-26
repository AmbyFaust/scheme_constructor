#ifndef UNFOLDING_GRAPH
#define UNFOLDING_GRAPH
#include "check_tools.h"

Graph recurcive_check(const NetList& scheme);

std::unordered_map<std::string, std::pair<size_t, size_t>> pins_to_Vertexes(const std::vector<std::string>& pins);

void add_inner_components(const NetList& scheme, Graph& main_graph, 
	std::unordered_map<std::string, std::pair<size_t, size_t>>& vertexes);

#endif // !UNFOLDING_GRAPH