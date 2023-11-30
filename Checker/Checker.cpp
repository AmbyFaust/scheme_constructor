#include <iostream>
#include "netlist.h"
#include "parse_tools.h"
#include "graph.h"
#include "unfolding_graph.h"
//#include "../googletest/include/gtest/gtest.h"
//#include "gtest/gtest.h"


/*TEST(MyTestCase, MyTest) {
	// Ваши тестовые проверки здесь
	EXPECT_EQ(1, 1);
}*/
void innerPrimitive()
{
	Primitive pr1("pr1", { "a1", "a2" });
	NetList base("base", { "n1", "pr1.a1", "pr1.a2", "n2" },
		{ "n1", "n2" }, { &pr1 });
	base.set_connections({ {"n1", "pr1.a1"},
				 {"n2", "pr1.a2"},
		});
	Graph graph = recurcive_check(base);

	Graph correct_graph(4);
	correct_graph.add_edge(0, 1);
	correct_graph.add_edge(1, 2);
	correct_graph.add_edge(2, 3);

	graph.show();
	correct_graph.show();
}

int main(int argc, char** argv){
	innerPrimitive();
	//test_graph();
	//test_objects();

	//::testing::InitGoogleTest(&argc, argv);
	//return RUN_ALL_TESTS();
}
