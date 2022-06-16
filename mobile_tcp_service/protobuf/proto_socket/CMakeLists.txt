

project(TCPCLIENT)

set(CMAKE_CXX_STANDARD 20)

# find_package(Protobuf REQUIRED)
# include_directories(${Protobuf_INCLUDE_DIRS})



include_directories(${CMAKE_CURRENT_BINARY_DIR})

# protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS hello.proto)

set(YOUR_DIRECTORY /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/proto_socket)

add_executable (protoclient ${YOUR_DIRECTORY}/client.cpp ${PROTO_SRCS} ${PROTO_HDRS})
add_executable (protoserver ${YOUR_DIRECTORY}/server.cpp ${PROTO_SRCS} ${PROTO_HDRS})

# target_link_libraries(protoclient ${Protobuf_LIBRARIES})
# target_link_libraries(protoserver ${Protobuf_LIBRARIES})

target_link_libraries(protoclient
PUBLIC
    ProtoMessages
)

target_link_libraries(protoserver
PUBLIC
    ProtoMessages
)








