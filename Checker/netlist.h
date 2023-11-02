#ifndef NETLIST_H
#define NETLIST_H


#include <iostream>
#include <vector>
#include <set>
#include <utility>

enum block_type {
    primitive = 0,
    netlist
};


class Object {
public:
    virtual block_type type() const = 0;
    std::vector<int> pins;
    virtual const std::vector<int>& get_pins() const { return pins; };
};


class Primitive : public Object
{
public:
    Primitive() {}
    Primitive(std::vector<int> init_pins) { pins = init_pins; }
    ~Primitive() = default;

    block_type type() const override { return primitive;  };
};



class NetList : public Object
{
public:
    NetList() {}
    NetList(std::vector<int> init_pins) { pins = init_pins; }
    ~NetList() = default;

    block_type type() const override { return netlist; };
    void add_connection(std::set<int> connection);

    const std::vector<std::set<int>>& get_connections() const { return connections; }
private:
    // inner elements
    std::vector<Object*> elements;
    // inner connections
    std::vector<std::set<int>> connections;
};


void test_objects();

#endif // !NETLIST_H