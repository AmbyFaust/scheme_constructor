#include "netlist.h"






void NetList::add_connection(std::vector<std::string> pin_connection)
{
    if (pin_connection.size() < 2)
        return;
    connections.push_back(pin_connection); 
}
