# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build

# Include any dependencies generated for this target.
include proto_socket/CMakeFiles/protoserver.dir/depend.make

# Include the progress variables for this target.
include proto_socket/CMakeFiles/protoserver.dir/progress.make

# Include the compile flags for this target's objects.
include proto_socket/CMakeFiles/protoserver.dir/flags.make

proto_socket/CMakeFiles/protoserver.dir/server.cpp.o: proto_socket/CMakeFiles/protoserver.dir/flags.make
proto_socket/CMakeFiles/protoserver.dir/server.cpp.o: ../proto_socket/server.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object proto_socket/CMakeFiles/protoserver.dir/server.cpp.o"
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket && /usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/protoserver.dir/server.cpp.o -c /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/proto_socket/server.cpp

proto_socket/CMakeFiles/protoserver.dir/server.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/protoserver.dir/server.cpp.i"
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/proto_socket/server.cpp > CMakeFiles/protoserver.dir/server.cpp.i

proto_socket/CMakeFiles/protoserver.dir/server.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/protoserver.dir/server.cpp.s"
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/proto_socket/server.cpp -o CMakeFiles/protoserver.dir/server.cpp.s

# Object files for target protoserver
protoserver_OBJECTS = \
"CMakeFiles/protoserver.dir/server.cpp.o"

# External object files for target protoserver
protoserver_EXTERNAL_OBJECTS =

proto_socket/protoserver: proto_socket/CMakeFiles/protoserver.dir/server.cpp.o
proto_socket/protoserver: proto_socket/CMakeFiles/protoserver.dir/build.make
proto_socket/protoserver: message_definitions/libProtoMessages.so
proto_socket/protoserver: ../protobuf_src/lib/libprotobuf.so
proto_socket/protoserver: proto_socket/CMakeFiles/protoserver.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable protoserver"
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/protoserver.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
proto_socket/CMakeFiles/protoserver.dir/build: proto_socket/protoserver

.PHONY : proto_socket/CMakeFiles/protoserver.dir/build

proto_socket/CMakeFiles/protoserver.dir/clean:
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket && $(CMAKE_COMMAND) -P CMakeFiles/protoserver.dir/cmake_clean.cmake
.PHONY : proto_socket/CMakeFiles/protoserver.dir/clean

proto_socket/CMakeFiles/protoserver.dir/depend:
	cd /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/proto_socket /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket /home/jehan/opa3l_ws/src/drives_tcp_udp_services/mobile_tcp_service/protobuf/build/proto_socket/CMakeFiles/protoserver.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : proto_socket/CMakeFiles/protoserver.dir/depend

