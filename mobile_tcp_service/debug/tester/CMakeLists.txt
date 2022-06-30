

cmake_minimum_required(VERSION 3.16.3)
project(TESTME)

set(CMAKE_CXX_STANDARD 20)

find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})
include_directories(${CMAKE_CURRENT_BINARY_DIR})

protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS hello.proto)

set(YOUR_DIRECTORY /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/tester)

add_executable (testtcp ${YOUR_DIRECTORY}/test.cpp ${PROTO_SRCS} ${PROTO_HDRS})

target_link_libraries(testtcp ${Protobuf_LIBRARIES})







