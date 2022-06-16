#include<iostream>
#include "hello.pb.h"

using namespace std;

int main()
{
    candy::Person p;
    p.set_name("Jehan");
    p.set_id(26);
    p.set_email("jehan@uni-bremen.de");

    cout << "\n Name is:" << p.name();
    cout << "\n ID is:" << p.id();
    cout << "\n Email is:" << p.email();
    return 0;
}

// protoc --cpp_out=. hello.proto
// g++ -std=c++17 test.cpp hello.pb.cc -o binarytestcpp `pkg-config --cflags --libs protobuf`