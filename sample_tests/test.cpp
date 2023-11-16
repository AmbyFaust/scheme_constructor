#include "pch.h"
#include <iostream>


#include "../Checker/check_tools.h"
#include "../Checker/netlist.h"
#include "../Checker/parse_tools.h"
#include "../Checker/graph.h"
#include "../Checker/check_tools.cpp"
#include "../Checker/netlist.cpp"
//#include "../Checker/parse_tools.cpp"
#include "../Checker/graph.cpp"


TEST(Example, ExampleTestName) {
  EXPECT_EQ(1, 1);
  EXPECT_TRUE(true);
}

TEST(GraphTest, CycledGraph) {
    // Âàøè òåñòîâûå ïðîâåðêè çäåñü
    Graph g;
    for(int i = 0; i < 5; i++)
        g.add_vertex();
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);
    EXPECT_TRUE(g.is_cycled());
}

TEST(GraphTest, TwoComponents) {
    Graph g;
    g.add_vertex();
    g.add_vertex();
    g.add_vertex();
    g.add_edge(0, 1);
    EXPECT_EQ(g.get_components_cnt(), 2);
}

TEST(GraphTest, ThreeComponents) {
    Graph g;
    g.add_vertex();
    g.add_vertex();
    g.add_vertex();
    EXPECT_EQ(g.get_components_cnt(), 3);
}


int main(int argc, char** argv) {

    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
