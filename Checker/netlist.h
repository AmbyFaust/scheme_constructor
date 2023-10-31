#pragma once

#include <iostream>
#include <vector>
#include <utility>

class Primitive
{
protected:
    std::vector<int> pins;

public:
    Primitive();
    ~Primitive();
};



class NetList : protected Primitive
{
protected:
    // inner connections
    std::pair<int, int> connections;

    // inner elements
    std::vector<void*> elements;

public:
    NetList();
    ~NetList();
};

