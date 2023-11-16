#include "pch.h"
#include <iostream>


#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\check_tools.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\netlist.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\parse_tools.h"
#include "\Users\L-408-21\Desktop\MIPT\Cpract\Checker\Checker\graph.h"


TEST(TestCaseName, TestName) {
  EXPECT_EQ(1, 1);
  EXPECT_TRUE(true);
}

TEST(MyTestCase, MyTest) {
    // Ваши тестовые проверки здесь
    EXPECT_EQ(1, 1);
}

int main(int argc, char** argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
