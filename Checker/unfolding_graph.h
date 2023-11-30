#ifndef UNFOLDING_GRAPH
#define UNFOLDING_GRAPH
#include<unordered_map>
#include<string>
#include"graph.h"
#include"netlist.h"

Graph recurcive_check(const NetList& scheme);

std::unordered_map<std::string, std::pair<size_t, size_t>> pins_to_Vertices(const std::vector<std::string>& pins);

void add_inner_components(const NetList& scheme, Graph& main_graph, 
	std::unordered_map<std::string, std::pair<size_t, size_t>>& vertices);

#endif // !UNFOLDING_GRAPH