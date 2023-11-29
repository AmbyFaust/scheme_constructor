#ifndef NETLIST_H
#define NETLIST_H


#include <QDebug>
#include <string>
#include <fstream>
#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <utility>

enum block_type {
    primitive = 0,
    netlist
};


class Object
{
public:
    std::string name;
    std::vector<std::string> pins;

    virtual block_type type() const = 0;
    std::vector<int> int_pins;                                              // описание пинов интами
};

class Primitive : Object
{
public:
    Primitive() {}
    Primitive(std::string n, std::vector<std::string> vec_pins);
    Primitive(std::vector<int> init_pins);
    ~Primitive() = default;

    void show();

    block_type type() const override { return primitive;  };

    const std::string& get_name() { return name; }
    std::vector<std::string>& get_pins() { return pins; }
};

class NetList : Object
{
protected:
    // for testing
    std::vector<int> pins_int;

    std::vector<std::string> edge_pins;                         // list of pins which are located on edge of block
    std::vector<std::vector<std::string>> pin_nets;             // list of pins_connections

    // inner elements
    std::vector<Object*> objects;

public:
    NetList() {}
    NetList(std::string n, std::vector <std::string> e_pins, std::vector<std::string> pins, std::vector<std::vector<std::string>> m_pin_nets);
    NetList(std::string n, std::vector<Object> objects, std::vector <std::string> e_pins, std::vector<std::string> pins, std::vector<std::vector<std::string>> m_pin_nets);
    NetList(std::vector<int> init_pins);
    ~NetList() = default;

    block_type type() const override { return netlist; };
    void add_connection(std::set<int> connection);

    void show();                                         // demonstration of class'es info

    const std::string& get_name() const { return name; }
    std::vector<std::string>& get_pins() { return pins; }
};

void test_objects();

#endif // !NETLIST_H
