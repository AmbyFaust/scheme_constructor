#include "graph.h"

Graph::Graph(unsigned int vertex_cnt) 
	: vertex_cnt{vertex_cnt}
{
	for (int i = 0; i < vertex_cnt; i++) {
		adjacency_array.push_back(std::vector<unsigned int>());
	}
}

void Graph::add_edge(unsigned int v1, unsigned int v2)
{
	// assume that each edge is added only once
	// otherwise duplicates exist without set usage 
	if (v1 >= this->vertex_cnt || v2 >= this->vertex_cnt)
		return;
	this->adjacency_array[v1].push_back(v2);
	this->adjacency_array[v2].push_back(v1);
}

void Graph::del_edge(unsigned int v1, unsigned int v2)
{
	if (v1 >= this->vertex_cnt || v2 >= this->vertex_cnt)
		return;
	adjacency_array[v1].erase(
		std::remove(adjacency_array[v1].begin(), adjacency_array[v1].end(), v2), adjacency_array[v1].end());
	adjacency_array[v2].erase(
		std::remove(adjacency_array[v2].begin(), adjacency_array[v2].end(), v1), adjacency_array[v2].end());
}

void Graph::add_vertex()
{
	this->adjacency_array.push_back(std::vector<unsigned int>());
	this->vertex_cnt++;
}

void Graph::del_vertex(unsigned int v)
{
	if (v >= this->vertex_cnt)
		return;

	auto v_loc = adjacency_array.begin() + v;
	adjacency_array.erase(v_loc);

	for (int i = 0; i < adjacency_array.size(); i++) {
		adjacency_array[i].erase(
			std::remove(adjacency_array[i].begin(), adjacency_array[i].end(), v), adjacency_array[i].end());
	}
	this->vertex_cnt--;
}


unsigned int Graph::get_components_cnt() const
{
	if (vertex_cnt == 0)
		return 0;

	unsigned int cnt_res = 0;
	std::vector<unsigned int> visited(this->vertex_cnt, 0);
	int start_v = 0;
	bool stop = false;
	while (true) {
		std::cout << start_v << " <- start_v" << std::endl;
		for (auto el : visited) {
			std::cout << el << " ";
		}std::cout << std::endl;
		for (int i = start_v; i < visited.size(); i++) {
			if (visited[start_v] == 0) {
				break;
			}
			if (i == visited.size() - 1 && visited[i] > 0) {
				stop = true;
			}
			start_v++;
		}
		if (stop)
			break;
		dfs(start_v, start_v, visited);
		cnt_res++;
		for (auto el : visited) {
			std::cout << el << " ";
		}std::cout << std::endl;
		std::cout << cnt_res << std::endl;
	}
	return cnt_res;
}

bool Graph::is_cycled() const
{
	if (vertex_cnt == 0)
		return false;
	std::vector<unsigned int> visited(this->vertex_cnt, 0);
	int start_v = 0;
	bool stop = false;
	while (true) {
		for (int i = start_v; i < visited.size(); i++) {
			if (visited[start_v] == 0) {
				break;
			}
			if (i == visited.size() - 1 && visited[i] > 0) {
				stop = true;
			}
			start_v++;
		}
		if (stop)
			break;
		if (dfs(start_v, start_v, visited))
			return true;
	}
	return false;
}

void Graph::show()
{
	std::cout << "vertex_cnt: " << vertex_cnt << std::endl;
	for (int i = 0; i < this->vertex_cnt; i++) {
		for (int j = 0; j < this->vertex_cnt; j++) {
			if(std::find(adjacency_array[i].begin(), adjacency_array[i].end(), j) == std::end(adjacency_array[i])) {
				std::cout << "0 ";
			}
			else {
				std::cout << "1 ";
			}
		}
		std::cout << std::endl;
	}
}

bool Graph::dfs(unsigned int v, unsigned int p, std::vector<unsigned int>& visit_status) const
{
	visit_status[v] = 1;
	std::cout << "dfs_v: " << v << std::endl;
	for (int i = 0; i < this->adjacency_array[v].size(); i++) {
		int to = this->adjacency_array[v][i];
		if (to == p)
			continue;
		std::cout << "v: " << v << "to: " << to << std::endl;
		if (visit_status[to] == 0) {
			if (dfs(to, v, visit_status))
				return true;
		}
		else if (visit_status[to] == 1) {
			return true;
		}
	}
	visit_status[v] = 2;
	return false;
}

void test_graph()
{
	int v_num, num_actions;
	std::cin >> v_num >> num_actions;
	Graph a(v_num);
	int v1, v2;
	char act;
	for (int i = 0; i < num_actions; i++) {
		std::cin >> act;
		if (act == 'a') {
			std::cin >> v1 >> v2;
			a.add_edge(v1, v2);
		}
		else if (act == 'b') {
			std::cin >> v1 >> v2;
			a.del_edge(v1, v2);
		}
		else if (act == 'c') {
			a.add_vertex();
		}
		else if (act == 'd') {
			std::cin >> v1;
			a.del_vertex(v1);
		}
		else if (act == 'e') {
			std::cout << "cycle exist (bool): " << a.is_cycled() << std::endl;
		}
		else if (act == 'f') {
			std::cout << "components cnt = " << a.get_components_cnt() << std::endl;
		}
		a.show();
	}
}
