#pragma once

#include "netlist.h"
#include "graph.h"

Graph recurcive_check(const NetList& scheme);

bool all_primitive_level(const NetList& scheme);

bool upper_hierarchy_check(const Graph& scheme);

bool lower_hierarchy_check(const Graph& expanded);

bool empty_pin_check(const Graph& expanded);

bool unconnected_circuit_check(const Graph& expanded);

bool incorrect_circuit_check(const Graph& expanded);

void write_check_result(std::string filename);