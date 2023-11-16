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

TEST(GraphTest, NComponents) {
    Graph g;
    int components = 100000; //1000000;
    for (int i = 1; i < components * 2; i += 2) {
        g.add_vertex();
        g.add_vertex();
        g.add_edge(i, i - 1);
    }
    EXPECT_EQ(g.get_components_cnt(), components);
}

TEST(CheckToolsTest, UpperHierrachyCycle) {
    Graph g;
    int vertexes = 100;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        g.add_edge(i, i - 1);
    }
    g.add_edge(vertexes - 1, 0);
    EXPECT_EQ(g.is_cycled(), true);
    EXPECT_EQ(upper_hierarchy_check(g), true);
}

TEST(CheckToolsTest, UpperHierrachyNotCycle) {
    Graph g;
    int vertexes = 100;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        if(i % 2)
            g.add_edge(i, i - 1);
    }
    g.add_edge(vertexes - 1, 0);
    EXPECT_EQ(g.is_cycled(), false);
    EXPECT_EQ(upper_hierarchy_check(g), false);
}

TEST(CheckToolsTest, LowerHierrachyConnectedCircuit) {
    Graph g;
    int vertexes = 100;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        g.add_edge(i, 0);
    }
    EXPECT_EQ(g.get_components_cnt() == 1, true);
    EXPECT_EQ(unconnected_circuit_check(g), false);
}


TEST(CheckToolsTest, LowerHierrachyCorrect) {
    Graph g;
    int vertexes = 100;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        if (i % 2)
            g.add_edge(i, i - 1);
    }
    g.add_edge(vertexes - 1, 0);
    EXPECT_EQ(g.is_cycled(), false);
    EXPECT_EQ(upper_hierarchy_check(g), false);
}


TEST(CheckToolsTest, LowerHierrachyUnconnectedCircuit) {
    Graph g;
    int vertexes = 100;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        if (i % 3)
            g.add_edge(i, i - 1);
    }
    EXPECT_EQ(g.get_components_cnt() > 1, true);
    EXPECT_EQ(unconnected_circuit_check(g), true);
}


TEST(CheckToolsTest, LowerHierrachyUnconnectedCircuitNoneEdges) {
    Graph g;
    int vertexes = 1000;
    g.add_vertex();
    for (int i = 1; i < vertexes; i++) {
        g.add_vertex();
        g.add_edge(i, i - 1);
    }
    g.add_edge(vertexes-1, 0);
    EXPECT_EQ(empty_pin_check(g), false);
    EXPECT_EQ(unconnected_circuit_check(g), false);
    EXPECT_EQ(lower_hierarchy_check(g), false);
}



int main(int argc, char** argv) {

    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
