#include "check_tools.h"

bool upper_hierarchy_check(const Graph& scheme)
{
	if (scheme.is_cycled())
		return true;
	return false;
}

bool lower_hierarchy_check(const Graph& expanded)
{
	if (empty_pin_check(expanded) || unconnected_circuit_check(expanded))
		return true;
	return false;
}

bool unconnected_circuit_check(const Graph& expanded)
{
	if (expanded.get_components_cnt() > 1)
		return true;
	return false;
}

bool empty_pin_check(const Graph& expanded)
{
	return false;
}

void write_check_result(std::string filename, std::string res)
{
	std::ofstream out;
	out.open(filename);
	if (out.is_open())
		out << res << std::endl;
	out.close();
}
