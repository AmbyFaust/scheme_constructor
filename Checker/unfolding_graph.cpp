#include "unfolding_graph.h"
#include "check_tools.h"

std::unordered_map<std::string, std::pair<size_t, size_t>> pins_to_Vertices(const std::vector<std::string>& pins)
/* Функция вызывается в Graph recurcive_check(const NetList& scheme);
* Составление unordered_map из пинов
  ключом будет название пина, а элементом пара
  .first - номер вершины в основном графе
  .second - номер вершины в графе верхнего уровня иерархии,
	т.е пины принадлежащие одному вложенному блоку объединяются в одну вершину,
	пины внешнего нетлиста не обЪединяются
 
* предполагается, что пины соотвествующие одному вложенному блоку идут подряд
*/
{	
	std::unordered_map<std::string, std::pair<size_t, size_t>> vertices;
	vertices.reserve(pins.size());

	size_t index = 0;
	std::string block_name;

	for (size_t i = 0; i < pins.size(); ++i)
	{
		char symbol = '.'; // Искомый символ

		size_t found = pins[i].find(symbol); // Поиск символа

		if (found != std::string::npos)
		// нашли символ, значит работаем с внутренним пином
		{
			std::string substring = pins[i].substr(0, found); // выделение имени блока
			if (block_name == substring) 
			// очередной пин отностися к прошлому блоку
			{ 
				--index;
				vertices[pins[i]] = std::make_pair(i, index);
			}
			else 
			// пин относится к новому блоку
			{ 
				vertices[pins[i]] = std::make_pair(i, index);
				block_name = substring;
			}
		}
		else
		// не нашли символ, значит работаем с внешним пином
		{
			vertices[pins[i]] = std::make_pair(i, index);
		}
		++index;
	}
	return vertices;

}

void add_inner_components(const NetList& scheme, Graph& main_graph, 
	std::unordered_map<std::string, std::pair<size_t, size_t>>& vertices, const char* res_filename)
/* Функция вызывается в Graph recurcive_check(const NetList& scheme);
* Добавление в граф внутренних компонент нетлиста 
*/
{
	for (Object* object : scheme.get_objects())
	{
		std::string name = object->get_name();
		if (object->type() == primitive)
		{	
			if (object->get_pins().size() > 2)
			// добавляем фиктивную вершину и соедияем все пины примитива с ней
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
			// соединям между собой два пина примитива
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
				/// добавить проверку на Graph(1) прервать работу,выдать ошибку
				/*if (add_graph == Graph(1))
				{
					main_graph = Graph(1);
					return;
				}*/
				// соединяем основной граф и граф получившийся после проверки вложенного нетлиста
				unsigned int main_graph_back = main_graph.get_vertex_cnt(); // индекс для вставки новых вершин

				std::unordered_map<std::string, size_t> subVertexes; // ключ - имя пина вложенного нетлиста,
																	 // значение - порядковый номер вершины в add_graph
				subVertexes.reserve(subScheme->get_pins().size());
				for (size_t i = 0; i < subScheme->get_pins().size(); ++i) {
					subVertexes[subScheme->get_pins()[i]] = i;
					main_graph.add_vertex();
				}
				for (std::string pin : subScheme->get_edge_pins())
				// соединение внешних пинов вложенной схемы с основным графом
				{
					std::string pin_in_main = name + '.' + pin;
					main_graph.add_edge(vertices[pin_in_main].first, subVertexes[pin] + main_graph_back);
				}
				for (std::string pin : subScheme->get_pins())
				// добавление соединений из внутреннего графа в основной
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

	Graph upper_graph(scheme.get_edge_pins().size() + scheme.get_objects().size()); //граф для проверки верхнего уровня
	Graph main_graph(scheme.get_pins().size()); //общий граф

	for (const std::vector<std::string> connect : scheme.get_pin_nets())
	// соединение вершин основного графа, соединение вершин графа верхнего уровня иерархии
	{
		// соединение происходит по кругу (первый со вторым, второй с третьим, третий с первым).
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