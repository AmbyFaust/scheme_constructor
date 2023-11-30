#include "netlist.h"


Primitive::Primitive(std::string n, std::vector<std::string> vec_pins)
{
    name = n;                                                               //name of primitive
    pins = vec_pins;                                                        //list of pins
}
                                                                     

NetList::NetList(std::string n, std::vector<std::string> e_pins,            // classic constructor
                 std::vector<std::string> vec_pins, std::vector<std::vector<std::string>> m_pin_nets)
{
    name = n;                                                               // class name
    pins = vec_pins;                                                        // vector of inner pins
    edge_pins = e_pins;                                                     // vector of pins on edge of block
    pin_nets = m_pin_nets;                                                  // map of pin_connections
}

NetList::NetList(std::string name_, std::vector<std::string> pins_, std::vector <std::string> edge_pins_,
    std::vector<Object*> objects_) // for tests
{
    name = name_;
    pins = pins_;
    edge_pins = edge_pins_;
    objects = objects_;
}

void NetList::set_connections(const std::vector<std::vector<std::string>> pin_nets_) // for tests
{
    pin_nets = pin_nets_;
}



void NetList::show()
{
    std::cout << "NAME: " << this->name << "\nPINS: ";
    for (const auto& pin : this->pins)
        std::cout << pin << ", ";
    std::cout << "\nEDGE_PINS: ";
    for (const auto& edge_pin : this->edge_pins)
        std::cout << edge_pin << ", ";
    std::cout << "\nPIN_NETS:\n";
    for (const auto& pin_connect: this->pin_nets)
    {
        for (const auto& pin: pin_connect)
            std::cout << pin << ' ';
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
