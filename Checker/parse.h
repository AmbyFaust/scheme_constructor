#ifndef PARSE_H
#define PARSE_H

#include "netlist.h"

NetList parse_netlist(const char* filename);

Primitive parse_primitive(const char* filename);

#endif //PARSE_H