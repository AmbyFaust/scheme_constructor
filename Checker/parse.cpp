#include "parse.h"
#include "netlist.h"
#include "rapidjson/document.h"
#include "rapidjson/error/en.h"
#include "rapidjson/filereadstream.h"


NetList parse_netlist(const char* filename)
{
    std::string name("");

    // creating containers for pins and pin_nets
    std::vector<std::string> pins{};
    std::vector<std::string> edge_pins{};
    std::vector<std::vector<std::string>> pin_nets{};

    std::vector<NetList> blockList{};

    //getting Json
#pragma warning(suppress : 4996)
    FILE* fp = fopen(filename, "r");
    //std::cout << filename << " in parse" << std::endl;

    char js[65536];
    rapidjson::FileReadStream is(fp, js, sizeof(js));

    //std::cout << filename << " in parse 2" << std::endl;
    //qDebug() << js;

    rapidjson::Document document;

    if (!document.ParseStream(is).HasParseError())                                      // is file ok?
    {
        document.ParseStream(is);                                                       //parsing json
        fclose(fp);
    }
    else                                                                                // if not
    {                                                                                   // showing error
        //qDebug() << document.GetErrorOffset();                                          // & it's place
        //qDebug() << GetParseError_En(document.GetParseError());
        fclose(fp);
    }

    if (document["blck"]/*doc*/["type"] == "block")                                          // if block
    {

//INFO ABOUT NAME
        const rapidjson::Value& n = document["blck"]/*doc*/["name"];                         // reading name
        name = n.GetString();

// INFO ABOUT PINS
        const rapidjson::Value& pins_list = document["blck"]/*doc*/["pins"];                 // reading list of pins
        for (rapidjson::Value::ConstMemberIterator iter = pins_list.MemberBegin();
             iter != pins_list.MemberEnd(); ++iter)
        {
            const rapidjson::Value& pin_value = iter->value;
            std::string pin_name = pin_value["name"].GetString();
            if (pin_name.find('.'))                                                    // if pin is located on edge
                edge_pins.push_back(pin_name);
            pins.push_back(pin_name);
        }

// INFO ABOUT WIRES
        const rapidjson::Value& pinNets = document["blck"]/*doc*/["pin_nets"];
        for (rapidjson::Value::ConstMemberIterator iter = pinNets.MemberBegin();
             iter != pinNets.MemberEnd(); ++iter)
        {
            std::vector<std::string> pinsVector{};

            const rapidjson::Value& pin_net = iter->value;                              // reading wire name
//            std::string net_name = pin_net["name"].GetString();

            std::string pins = pin_net["pins"].GetString();                             // reading list of wire's pins
            size_t pos = 0;
            while((pos = pins.find(',')) != std::string::npos)
            {
                std::string pin = pins.substr(0, pos);
                pinsVector.push_back(pin);
                pins.erase(0, pos+1);
            }
            pinsVector.push_back(pins);
            pin_nets.push_back(pinsVector);
        }
    }
    NetList block(name, edge_pins, pins, pin_nets);

    return block;
}

Primitive parse_primitive(const char* filename)
{
    std::string name("");
    std::vector<std::string> pins{};

#pragma warning(suppress : 4996)
    FILE* fp = fopen(filename, "r");         // connecting json
    char js[65536];
    rapidjson::FileReadStream is(fp, js, sizeof(js));                           //stream file

    //qDebug() << js;

    rapidjson::Document document;                                               // connecting doc

    if (!document.ParseStream(is).HasParseError())                              // if everything is correct
    {                                                                           // parsing
        document.ParseStream(is);
        fclose(fp);
    }
    else                                                                        // or not
    {                                                                           // showing where is err
        //qDebug() << document.GetErrorOffset();                                  // what err it is
        //qDebug() << GetParseError_En(document.GetParseError());
        fclose(fp);
    }                                                                           // closing file

    if (document["primit"]["type"] == "primitive")                                    // checking if it's primitive
    {
        const rapidjson::Value& n = document["primit"]["name"];                 // getting name
        name = n.GetString();

        const rapidjson::Value& pins_list = document["primit"]["pins"];         // collecting pins
        for (rapidjson::Value::ConstMemberIterator iter = pins_list.MemberBegin();
             iter != pins_list.MemberEnd(); ++iter)
        {
            const rapidjson::Value& pin_value = iter->value;
            std::string pin_name = pin_value["name"].GetString();
            pins.push_back(pin_name);
        }
    }

    Primitive prim(name, pins);                                                 // creating object
    return prim;                                                                // returning object
}
