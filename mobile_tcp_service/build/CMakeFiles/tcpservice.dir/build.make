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
CMAKE_SOURCE_DIR = /home/jehan/C++/tcpservice

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jehan/C++/tcpservice/build

# Include any dependencies generated for this target.
include CMakeFiles/tcpservice.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/tcpservice.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/tcpservice.dir/flags.make

CMakeFiles/tcpservice.dir/main.cpp.o: CMakeFiles/tcpservice.dir/flags.make
CMakeFiles/tcpservice.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/jehan/C++/tcpservice/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/tcpservice.dir/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/tcpservice.dir/main.cpp.o -c /home/jehan/C++/tcpservice/main.cpp

CMakeFiles/tcpservice.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/tcpservice.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/jehan/C++/tcpservice/main.cpp > CMakeFiles/tcpservice.dir/main.cpp.i

CMakeFiles/tcpservice.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/tcpservice.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/jehan/C++/tcpservice/main.cpp -o CMakeFiles/tcpservice.dir/main.cpp.s

# Object files for target tcpservice
tcpservice_OBJECTS = \
"CMakeFiles/tcpservice.dir/main.cpp.o"

# External object files for target tcpservice
tcpservice_EXTERNAL_OBJECTS =

tcpservice: CMakeFiles/tcpservice.dir/main.cpp.o
tcpservice: CMakeFiles/tcpservice.dir/build.make
tcpservice: CMakeFiles/tcpservice.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/jehan/C++/tcpservice/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable tcpservice"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/tcpservice.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/tcpservice.dir/build: tcpservice

.PHONY : CMakeFiles/tcpservice.dir/build

CMakeFiles/tcpservice.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/tcpservice.dir/cmake_clean.cmake
.PHONY : CMakeFiles/tcpservice.dir/clean

CMakeFiles/tcpservice.dir/depend:
	cd /home/jehan/C++/tcpservice/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jehan/C++/tcpservice /home/jehan/C++/tcpservice /home/jehan/C++/tcpservice/build /home/jehan/C++/tcpservice/build /home/jehan/C++/tcpservice/build/CMakeFiles/tcpservice.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/tcpservice.dir/depend

