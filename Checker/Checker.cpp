#include <iostream>
#include "netlist.h"
//#include "parse_tools.h"
#include "graph.h"
#include "unfolding_graph.h"
#include "parse.h"


int main(int argc, char** argv){
	//const char* filename = "./correct1.json";
	const char* filename = argv[1];
	if (argc != 2) {
		std::cout << "Wrong amount of arguments passed: " << argc - 1 << " instead of 1";
		return 1;
	}
	std::cout << "Checking: " << filename << std::endl;
	const char* res_filename = "./check_result.txt";//argv[2];
	NetList main_scheme = parse_netlist(filename);
	std::cout << "Parse done" << std::endl;
	recurcive_check(main_scheme, res_filename);
	std::cout << "Check done. Result in " << res_filename << std::endl;
	return 0;
}
