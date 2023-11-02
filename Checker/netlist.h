#pragma once

#include <iostream>
#include <vector>
#include <set>
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
    std::vector<std::set<int>> connections;

    // inner elements
    std::vector<void*> elements;

public:
    NetList();
    ~NetList();
};
