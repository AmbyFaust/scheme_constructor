#pragma once

#include <vector>

class Graph {
	// another variant of graph storage may be used
	std::vector<std::vector<unsigned int>> adjacency_matrix;

	void add_edge(unsigned int v1, unsigned int v2, unsigned int cnt_edges = 1);
	void del_edge(unsigned int v1, unsigned int v2, unsigned int cnt_edges = 1);
	void add_vertex();
	void del_vertex(unsigned int v);
};