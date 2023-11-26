#include "unfolding_graph.h"

std::unordered_map<std::string, std::pair<size_t, size_t>> pins_to_Vertexes(const std::vector<std::string>& pins)
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
	std::unordered_map<std::string, std::pair<size_t, size_t>> vertexes;
	vertexes.reserve(pins.size());

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
				vertexes[pins[i]] = std::make_pair(i, index);
			}
			else 
			// ��� ��������� � ������ �����
			{ 
				vertexes[pins[i]] = std::make_pair(i, index);
				block_name = substring;
			}
		}
		else
		// �� ����� ������, ������ �������� � ������� �����
		{
			vertexes[pins[i]] = std::make_pair(i, index);
		}
		++index;
	}
	return vertexes;

}

void add_inner_components(const NetList& scheme, Graph& main_graph, 
	std::unordered_map<std::string, std::pair<size_t, size_t>>& vertexes)
/* ������� ���������� � Graph recurcive_check(const NetList& scheme);
* ���������� � ���� ���������� ��������� �������� 
*/
{
	for (Object* object : scheme.get_elements())
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
					main_graph.add_edge(vertexes.at(pin).first, common_vertex);
				}
			}
			else
			// �������� ����� ����� ��� ���� ���������
			{
				std::string pin1 = name + '.' + object->get_pins()[0];
				std::string pin2 = name + '.' + object->get_pins()[1];
				main_graph.add_edge(vertexes.at(pin1).first, vertexes.at(pin2).first);
			}
		}
		else if (object->type() == netlist) {
			NetList* subScheme = dynamic_cast<NetList*>(object);
			if (subScheme) {
				Graph add_graph = recurcive_check(*subScheme);
				// ��������� �������� ���� � ���� ������������ ����� �������� ���������� ��������
				unsigned int main_graph_back = main_graph.get_vertex_cnt(); // ������ ��� ������� ����� ������

				std::unordered_map<std::string, size_t> subVertexes; // ���� - ��� ���� ���������� ��������,
																	 // �������� - ���������� ����� ������� � add_graph
				subVertexes.reserve(subScheme->get_pins().size());
				for (size_t i = 0; i < subScheme->get_pins().size(); ++i) {
					subVertexes[subScheme->get_pins()[i]] = i;
					main_graph.add_vertex();
				}
				for (std::string pin : subScheme->get_outterPins())
				// ���������� ������� ����� ��������� ����� � �������� ������
				{
					std::string pin_in_main = name + '.' + pin;
					main_graph.add_edge(vertexes[pin_in_main].first, subVertexes[pin] + main_graph_back);
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

Graph recurcive_check(const NetList& scheme)
{
	std::unordered_map<std::string, std::pair<size_t, size_t>> vertexes;
	vertexes = pins_to_Vertexes(scheme.get_pins());

	Graph upper_graph(scheme.get_outterPins().size() + scheme.get_elements().size()); //���� ��� �������� �������� ������
	Graph main_graph(scheme.get_pins().size()); //����� ����

	for (const std::vector<std::string> connect : scheme.get_connections())
	// ���������� ������ ��������� �����, ���������� ������ ����� �������� ������ ��������
	{
		// ���������� ���������� �� ����� (������ �� ������, ������ � �������, ������ � ������).
		for (size_t i = 0; i < connect.size() - 1; ++i)
		{
			/*unsigned int v1_main = vertexes[connect[i]].first;
			unsigned int v1_upper = vertexes[connect[i]].second;
			unsigned int v2_main = vertexes[connect[i+1]].first;
			unsigned int v2_upper = vertexes[connect[i+1]].second;*/
			unsigned int v1_main = vertexes.at(connect[i]).first;
			unsigned int v1_upper = vertexes.at(connect[i]).second;
			unsigned int v2_main = vertexes.at(connect[i + 1]).first;
			unsigned int v2_upper = vertexes.at(connect[i + 1]).second;

			main_graph.add_edge(v1_main, v2_main);
			upper_graph.add_edge(v1_upper, v2_upper);
		}
		main_graph.add_edge(vertexes.at(connect[0]).first, vertexes.at(connect.back()).first);
		upper_graph.add_edge(vertexes.at(connect[0]).second, vertexes.at(connect.back()).second);
	}

	if (upper_hierarchy_check(upper_graph))
	{
		write_check_result("abc.txt", "upper_hierarchy_check error");
		return Graph(1);
	}

	add_inner_components(scheme, main_graph, vertexes);
	
	return main_graph;
}