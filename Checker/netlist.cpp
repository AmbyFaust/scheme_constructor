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

Primitive::Primitive(std::string n, std::vector<std::string> vec_pins)
{
    name = n;                                                               //name of primitive
    pins = vec_pins;                                                        //list of pins
}

Primitive::Primitive(std::vector<int> init_pins)
{
    int_pins = init_pins;
}                                                                           // default constructor

NetList::NetList(std::string n, std::vector<std::string> e_pins,
                 std::vector<std::string> vec_pins, std::map<std::string,   // classic constructor
                          std::vector<std::string>> m_pin_nets)
{
    name = n;                                                               // class name
    pins = vec_pins;                                                        // vector of inner pins
    edge_pins = e_pins;                                                     // vector of pins on edge of block
    pin_nets = m_pin_nets;                                                  // map of pin_connections
}

NetList::NetList(std::vector<int> init_pins)
{
    pins_int = init_pins;
}

void NetList::show()
{
    std::cout << "NAME: " << this->name << "\nPINS: ";
    for (const auto& pin : this->pins)
        std::cout << pin << ", ";
    std::cout << "\nEDGE_PINS: ";
    for (const auto& edge_pin : this->edge_pins)
        std::cout << edge_pin << ", ";
    std::cout << "\nWIRES:\n";
    for (const auto& [pin, nets] : this->pin_nets)
    {
        std::cout << pin << ": ";
        for (const auto& net : nets)
            std::cout << net << ", ";
        std::cout << '\n';
    }
}

void Primitive::show()
{
    std::cout << "NAME: " << this->name << "\nPINS: ";
    for (const auto& pin : this->pins)
        std::cout << pin << ' ';
    std::cout << "\n";
}

void NetList::add_connection(std::set<int> pin_connection)
{
    if (pin_connection.size() < 2)
        return;
    connections.push_back(pin_connection); 
}
