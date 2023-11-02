#include "netlist.h"

void test_objects()
{
    NetList a;
    NetList b({1, 2, 3});
    Primitive c;
    std::cout << a.type() << " " << b.type() << " " << c.type() << std::endl;
    std::vector<Object*> elem = { &a, &b, &c, &b, &c };
    for (auto el : elem)
        std::cout << el->type() << " ";
    std::cout << std::endl;

    for (auto el : elem[1]->get_pins()) {
        std::cout << el << " ";
    }std::cout << std::endl;

    a.add_connection({4, 7, 7, 8});
    a.add_connection({ 2,3 });
    b.add_connection({ 1,2,3,4,5 });
    for (int i = 0; i < elem.size(); i++) {
        std::cout << "block_" << i << std::endl;
        Object* ptr = elem[i];
        if (elem[i]->type() == netlist) {
            for (auto el : dynamic_cast<NetList*> (elem[i])->get_connections()) {
                std::cout << "connetion_row[i] -> ";
                for (auto pin : el)
                    std::cout << pin << " ";
                std::cout << std::endl;
            }std::cout << std::endl;
        }
        else {
            std::cout << "primitive" << std::endl << std::endl;
        }
    }
}




void NetList::add_connection(std::set<int> pin_connection)
{
    if (pin_connection.size() < 2)
        return;
    connections.push_back(pin_connection); 
}
