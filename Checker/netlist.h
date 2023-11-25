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
protected:
    std::string name;
    std::vector<std::string> pins;
public:
    Primitive() {}
    Primitive(std::string n, std::vector<std::string> vec_pins);
    Primitive(std::vector<int> init_pins);
    ~Primitive() = default;

    void show();

    block_type type() const override { return primitive;  };
};



class NetList : public Object
{
protected:
    // for testing
    std::vector<int> pins_int;

    std::string name;                                           // name of block
    std::vector<std::string> pins;                              // list of all pins
    std::vector<std::string> edge_pins;                         // list of pins which are located on edge of block
    std::map<std::string, std::vector<std::string>> pin_nets;   // list of pins_connections

    // inner elements
    std::vector<Object*> objects;
    // inner connections
    std::vector<std::set<int>> connections;

public:
    NetList() {}
    NetList(std::string n, std::vector <std::string> e_pins, std::vector<std::string> pins, std::map<std::string, std::vector<std::string>> m_pin_nets);
    NetList(std::string n, std::vector<Object> objects, std::vector <std::string> e_pins, std::vector<std::string> pins, std::map<std::string, std::vector<std::string>> m_pin_nets);
    NetList(std::vector<int> init_pins);
    ~NetList() = default;

    block_type type() const override { return netlist; };
    void add_connection(std::set<int> connection);

    void show();                                                 // demonstration of class'es info

    const std::vector<std::set<int>>& get_connections() const { return connections; }
};


void test_objects();

#endif // !NETLIST_H
