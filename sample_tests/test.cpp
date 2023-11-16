#include "pch.h"
#include <iostream>


#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\check_tools.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\netlist.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\parse_tools.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\graph.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\check_tools.cpp"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\netlist.cpp"
//#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\parse_tools.cpp"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\graph.cpp"

TEST(Example, ExampleTestName) {
  EXPECT_EQ(1, 1);
  EXPECT_TRUE(true);
}

TEST(GraphTest, CycledGraph) {
    // Ваши тестовые проверки здесь
    Graph g;
    for(int i = 0; i < 5; i++)
        g.add_vertex();
    g.add_edge(0, 1);
    g.add_edge(1, 2);
    g.add_edge(2, 0);
    EXPECT_TRUE(g.is_cycled());
}

TEST(GraphTest, TwoComponents) {
    // Ваши тестовые проверки здесь
    Graph g;
    g.add_vertex();
    g.add_vertex();
    g.add_vertex();
    g.add_edge(0, 1);
    EXPECT_EQ(g.get_components_cnt(), 2);
}


TEST(GraphTest, ThreeComponents) {
    // Ваши тестовые проверки здесь
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
