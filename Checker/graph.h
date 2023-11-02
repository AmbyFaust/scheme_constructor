#ifndef GRAPH_H
#define GRAPH_H

#include <vector>
#include <algorithm>
#include <array>
#include <iostream>

class Graph {
public:
	Graph() : vertex_cnt{ 0 } {}
	Graph(unsigned int vertex_cnt);
	void add_edge(unsigned int v1, unsigned int v2);
	void del_edge(unsigned int v1, unsigned int v2);
	void add_vertex();
	void del_vertex(unsigned int v);

	unsigned int get_components_cnt() const;
	bool is_cycled() const;

	void show();

private:
	unsigned int vertex_cnt;
	
	// adjacency array - O(E) capacity
	std::vector<std::vector<unsigned int>> adjacency_array;
	// std::vector<std::set<unsigned int>> adjacency_array;

	bool dfs(unsigned int v, unsigned int p, std::vector<unsigned int>& visited) const;
};

void test_graph();

#endif //GRAPH_H