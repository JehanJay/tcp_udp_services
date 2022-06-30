

cmake_minimum_required(VERSION 3.16.3)
project(MOBILE_COMMUNICATION)


include("cmake/DrivesMacros.cmake")

add_subdirectory(message_definitions)
add_subdirectory(proto_socket)

set(TARGET_FILE_DIR ${CMAKE_SOURCE_DIR}/build)

message(STATUS "CMAKE_SOURCE_DIR: ${CMAKE_SOURCE_DIR}")
message(STATUS "TARGET_FILE_DIR: ${TARGET_FILE_DIR}")

# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/libworhp.so  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/libTransWORHP.so  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/transworhp.xml  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/worhp.lic  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/worhp.xml  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)

# # add executables here.
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/spline0  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)
# file(COPY ${CMAKE_SOURCE_DIR}/transworhp/spline1  DESTINATION ${TARGET_FILE_DIR}/proto_socket/)

