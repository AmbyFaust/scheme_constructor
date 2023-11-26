#ifndef NETLIST_H
#define NETLIST_H


#include <iostream>
#include <vector>
#include <string>
#include <utility>
#include <unordered_map>

enum block_type {
    primitive = 0,
    netlist
};


class Object {
public:
    std::string name;
    virtual const std::string & get_name() const { return name; };
    virtual block_type type() const = 0;
    std::vector<std::string> pins;
    virtual const std::vector<std::string>& get_pins() const { return pins; };
};


class Primitive : public Object
{
public:
    Primitive() {}
    Primitive(std::string name_, std::vector<std::string> init_pins) 
    { 
        name = name_;
        pins = init_pins;
    }
    ~Primitive() = default;

    block_type type() const override { return primitive;  };
};



class NetList : public Object
{
public:
    NetList() {}
    NetList(std::string name_, std::vector<std::string> init_pins, std::vector<std::string> outterPins_, // для тестов
            std::vector<Object*> elements_)
    {
        name = name_;
        pins = init_pins;
        outterPins = outterPins_;
        elements = elements_;

    }
    ~NetList() = default;

    void add_element(Object* object) { elements.push_back(object); } // для тестов
    void set_connections(const std::vector<std::vector<std::string>>& connections_)//тесты
    {
        connections = connections_;
    }

    block_type type() const override { return netlist; };
    void add_connection(std::vector<std::string> connection);

    const std::vector<std::vector<std::string>>& get_connections() const { return connections; }
    const std::vector<Object*>& get_elements() const { return elements;  } //Pavel
    const std::vector<std::string>& get_outterPins() const { return outterPins; }; //Pavel
private:
    // inner elements
    std::vector<Object*> elements;
    // inner connections
    std::vector<std::vector<std::string>> connections;//Pavel
    std::vector<std::string> outterPins; //Pavel
};


#endif // !NETLIST_H