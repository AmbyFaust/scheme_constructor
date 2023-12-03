#include "unfolding_graph.h"
#include "check_tools.h"

std::unordered_map<std::string, std::pair<size_t, size_t>> pins_to_Vertices(const std::vector<std::string>& pins)
/* ������� ���������� � Graph recurcive_check(const NetList& scheme);
* ����������� unordered_map �� �����
  ������ ����� �������� ����, � ��������� ����
  .first - ����� ������� � �������� �����
  .second - ����� ������� � ����� �������� ������ ��������,
	�.� ���� ������������� ������ ���������� ����� ������������ � ���� �������,
	���� �������� �������� �� ������������
 
* ��������������, ��� ���� �������������� ������ ���������� ����� ���� ������
*/
{	
	std::unordered_map<std::string, std::pair<size_t, size_t>> vertices;
	vertices.reserve(pins.size());

	size_t index = 0;
	std::string block_name;

	for (size_t i = 0; i < pins.size(); ++i)
	{
		char symbol = '.'; // ������� ������

		size_t found = pins[i].find(symbol); // ����� �������

		if (found != std::string::npos)
		// ����� ������, ������ �������� � ���������� �����
		{
			std::string substring = pins[i].substr(0, found); // ��������� ����� �����
			if (block_name == substring) 
			// ��������� ��� ��������� � �������� �����
			{ 
				--index;
				vertices[pins[i]] = std::make_pair(i, index);
			}
			else 
			// ��� ��������� � ������ �����
			{ 
				vertices[pins[i]] = std::make_pair(i, index);
				block_name = substring;
			}
		}
		else
		// �� ����� ������, ������ �������� � ������� �����
		{
			vertices[pins[i]] = std::make_pair(i, index);
		}
		++index;
	}
	return vertices;

}

void add_inner_components(const NetList& scheme, Graph& main_graph, 
	std::unordered_map<std::string, std::pair<size_t, size_t>>& vertices, const char* res_filename)
/* ������� ���������� � Graph recurcive_check(const NetList& scheme);
* ���������� � ���� ���������� ��������� �������� 
*/
{
	for (Object* object : scheme.get_objects())
	{
		std::string name = object->get_name();
		if (object->type() == primitive)
		{	
			if (object->get_pins().size() > 2)
			// ��������� ��������� ������� � �������� ��� ���� ��������� � ���
			{
				main_graph.add_vertex();
				unsigned int common_vertex = main_graph.get_vertex_cnt() - 1;
				for (size_t i = 0; i < object->get_pins().size(); ++i)
				{
					std::string pin = name + '.' + object->get_pins()[i];
					main_graph.add_edge(vertices.at(pin).first, common_vertex);
				}
			}
			else
			// �������� ����� ����� ��� ���� ���������
			{
				std::string pin1 = name + '.' + object->get_pins()[0];
				std::string pin2 = name + '.' + object->get_pins()[1];
				main_graph.add_edge(vertices.at(pin1).first, vertices.at(pin2).first);
			}
		}
		else if (object->type() == netlist) {
			NetList* subScheme = dynamic_cast<NetList*>(object);
			if (subScheme) {
				Graph add_graph = recurcive_check(*subScheme, res_filename);
				/// �������� �������� �� Graph(1) �������� ������,������ ������
				/*if (add_graph == Graph(1))
				{
					main_graph = Graph(1);
					return;
				}*/
				// ��������� �������� ���� � ���� ������������ ����� �������� ���������� ��������
				unsigned int main_graph_back = main_graph.get_vertex_cnt(); // ������ ��� ������� ����� ������

				std::unordered_map<std::string, size_t> subVertexes; // ���� - ��� ���� ���������� ��������,
																	 // �������� - ���������� ����� ������� � add_graph
				subVertexes.reserve(subScheme->get_pins().size());
				for (size_t i = 0; i < subScheme->get_pins().size(); ++i) {
					subVertexes[subScheme->get_pins()[i]] = i;
					main_graph.add_vertex();
				}
				for (std::string pin : subScheme->get_edge_pins())
				// ���������� ������� ����� ��������� ����� � �������� ������
				{
					std::string pin_in_main = name + '.' + pin;
					main_graph.add_edge(vertices[pin_in_main].first, subVertexes[pin] + main_graph_back);
				}
				for (std::string pin : subScheme->get_pins())
				// ���������� ���������� �� ����������� ����� � ��������
				{
					for (unsigned int v2 : add_graph.get_edges(subVertexes[pin]))
						main_graph.add_edge(subVertexes[pin] + main_graph_back, v2 + main_graph_back);
				}
			}
		}
	}
}

Graph recurcive_check(const NetList& scheme, const char* res_filename)
{
	std::unordered_map<std::string, std::pair<size_t, size_t>> vertices;
	vertices = pins_to_Vertices(scheme.get_pins());

	Graph upper_graph(scheme.get_edge_pins().size() + scheme.get_objects().size()); //���� ��� �������� �������� ������
	Graph main_graph(scheme.get_pins().size()); //����� ����

	for (const std::vector<std::string> connect : scheme.get_pin_nets())
	// ���������� ������ ��������� �����, ���������� ������ ����� �������� ������ ��������
	{
		// ���������� ���������� �� ����� (������ �� ������, ������ � �������, ������ � ������).
		for (size_t i = 0; i < connect.size() - 1; ++i)
		{
			unsigned int v1_main = vertices.at(connect[i]).first;
			unsigned int v1_upper = vertices.at(connect[i]).second;
			unsigned int v2_main = vertices.at(connect[i + 1]).first;
			unsigned int v2_upper = vertices.at(connect[i + 1]).second;

			main_graph.add_edge(v1_main, v2_main);
			upper_graph.add_edge(v1_upper, v2_upper);
		}
		if (connect.size() > 2) {
			main_graph.add_edge(vertices.at(connect[0]).first, vertices.at(connect.back()).first);
			upper_graph.add_edge(vertices.at(connect[0]).second, vertices.at(connect.back()).second);
		}
	}

	if (upper_hierarchy_check(upper_graph))
	{
		write_check_result(res_filename, "CheckerLog: upper_hierarchy_check error.");
		std::cout << "CheckerLog: upper_hierarchy_check error." << std::endl;
		return Graph(1);
	}

	add_inner_components(scheme, main_graph, vertices, res_filename);
	write_check_result(res_filename, "CheckerLog: no errors found.");
	std::cout << "CheckerLog: no errors found." << std::endl;
	return main_graph;
}