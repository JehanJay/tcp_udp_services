

cmake_minimum_required(VERSION 3.16.3)
project(MOBILE_COMMUNICATION)


include("cmake/DrivesMacros.cmake")

add_subdirectory(message_definitions)
add_subdirectory(proto_socket)
