#ifndef NETLIST_H
#define NETLIST_H


//#include <QDebug>
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
    const std::string& get_name() const{ return name; }
    const std::vector<std::string>& get_pins() const { return pins; }

    virtual block_type type() const = 0;
    virtual ~Object() = default;
protected:
    std::string name;
    std::vector<std::string> pins;
};

class Primitive : public Object
{
public:
    Primitive() {}
    Primitive(std::string n, std::vector<std::string> vec_pins);
    ~Primitive() = default;

    void show();

    block_type type() const override { return primitive;  };
};

class NetList : public Object
{
protected:

    std::vector<std::string> edge_pins;                         // list of pins which are located on edge of block
    std::vector<std::vector<std::string>> pin_nets;             // list of pins_connections
    std::vector<Object*> objects;                               // inner elements

public:
    NetList() {}
    NetList(std::string n, std::vector <std::string> e_pins, std::vector<std::string> pins,
        std::vector<std::vector<std::string>> m_pin_nets);
    NetList(std::string n, std::vector<Object*> objects, std::vector <std::string> e_pins, std::vector<std::string> pins,
        std::vector<std::vector<std::string>> m_pin_nets);

    NetList(std::string name_, std::vector<std::string> pins_, std::vector <std::string> edge_pins_,
        std::vector<Object*> objects_); //for tests
    void set_connections(const std::vector<std::vector<std::string>> pin_nets_); // for tests

    ~NetList() = default;

    block_type type() const override { return netlist; };

    void show();                                         // demonstration of class'es info

    const std::vector<std::string>& get_edge_pins() const{ return edge_pins; }
    const std::vector<std::vector<std::string>>& get_pin_nets() const { return pin_nets; }
    const std::vector<Object*>& get_objects() const { return objects; }
};

void test_objects();

#endif // !NETLIST_H
