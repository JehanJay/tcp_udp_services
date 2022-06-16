
###
# Setup Protobuf
###

project(messageDefinitions)

set(FOLDER_NAME mobile_message_definitions)
set(DRIVES_PROTOBUF_PATH "$ENV{PROTOBUF_PATH}" CACHE PATH "Path to Protobuf installation")
message(STATUS "DRIVES_PROTOBUF_PATH: ${DRIVES_PROTOBUF_PATH}")

list(APPEND CMAKE_PREFIX_PATH ${DRIVES_PROTOBUF_PATH})
message(STATUS "CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
#Only executed when building in catkin workspace

if(CATKIN_DEVEL_PREFIX)
	find_package(Protobuf 3)
	set(Protobuf_PROTOC_EXECUTABLE "${Protobuf_INCLUDE_DIR}/../tools/protobuf/protoc.exe" CACHE PATH "Protoc exe" FORCE)

else()
	set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/;${CMAKE_MODULE_PATH}")
	find_package(Protobuf 3)
endif()

if(${Protobuf_FOUND} AND "${_PROTOBUF_PROTOC_EXECUTABLE_VERSION}" VERSION_EQUAL "${Protobuf_VERSION}")
	message(STATUS "Protobuf found: Version ${Protobuf_VERSION}")
	set(PROTO_LIB_NAME ProtoMessages)
	set(PROTO_MESSAGES_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/mobile_message_definitions/include)
	message(STATUS "PROTO_MESSAGES_INCLUDE_DIR: ${PROTO_MESSAGES_INCLUDE_DIR}")
	add_subdirectory(mobile_message_definitions)
else()
	message(STATUS "Protobuf NOT found")
	message(WARNING "Skipping Protobuf dependent scopes.")
endif()

###
# Run proto compilation
###
if(DEFINED PROTO_LIB_NAME)
	message(STATUS "proto_files: ${proto_files}")
	message(STATUS "PROTO_LIB_NAME: ${PROTO_LIB_NAME}")
	protobuf_generate_cpp(
		PROTO_SRCS 
		PROTO_HDRS
		${proto_files}
	)
	
	add_custom_target(generate_protobuf_cpp ALL DEPENDS ${PROTO_SRCS} ${PROTO_HDRS})
	message(STATUS "FOLDER_NAME: ${FOLDER_NAME}")
	set_property(TARGET generate_protobuf_cpp PROPERTY FOLDER ${FOLDER_NAME})

	set(PROTOBUF_GENERATE_PREFIX "${CMAKE_BINARY_DIR}/")

	message(STATUS "PROTOBUF_GENERATE_PREFIX: ${PROTOBUF_GENERATE_PREFIX}")
	# set_drives_cmake_install_prefix()
	# message(STATUS "CMAKE_INSTALL_PREFIX_MD: ${CMAKE_INSTALL_PREFIX}")
	
	drives_install_files_single(protobuf_install_target_cpp_srcs "${PROTO_SRCS}" "${PROTOBUF_GENERATE_PREFIX}")
	drives_install_files_single(protobuf_install_target_cpp_hdrs "${PROTO_HDRS}" "${PROTOBUF_GENERATE_PREFIX}")
	add_dependencies(protobuf_install_target_cpp_srcs generate_protobuf_cpp)
	add_dependencies(protobuf_install_target_cpp_hdrs generate_protobuf_cpp)

	message(STATUS "PROTO_SRCS: ${PROTO_SRCS}")
	message(STATUS "PROTO_HDRS: ${PROTO_HDRS}")

	if (MSVC)
		add_library(${PROTO_LIB_NAME} STATIC
			${PROTO_SRCS}
			${PROTO_HDRS}
		)
	else()
		add_library(${PROTO_LIB_NAME} SHARED
			${PROTO_SRCS}
			${PROTO_HDRS}
		)
	endif()

	add_dependencies(${PROTO_LIB_NAME} protobuf_install_target_cpp_srcs protobuf_install_target_cpp_hdrs)

	set_property(TARGET ${PROTO_LIB_NAME} PROPERTY FOLDER ${FOLDER_NAME})

	if(CMAKE_COMPILER_IS_GNUCC)
		set_property(TARGET ${PROTO_LIB_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON) # for ubuntu: build with fpic!
	endif()

	#protobuf_generate puts the genrated .cc and .h in the build directory. Thus we need that directory as include
	target_include_directories(${PROTO_LIB_NAME}
		PUBLIC 
			${Protobuf_INCLUDE_DIRS}			
			${CMAKE_CURRENT_BINARY_DIR}
			${PROTO_MESSAGES_INCLUDE_DIR}
	)

	#target_link_libraries(${PROTO_LIB_NAME} PUBLIC ${Protobuf_LIBRARIES} ${Protobuf_LITE_LIBRARIES} ${Protobuf_PROTOC_LIBRARIES})
	target_link_libraries(${PROTO_LIB_NAME}
		PUBLIC
			${PROTOBUF_LIBRARIES}
	)

	# build without any compile options..
	# this especially removes compiler warnings for this target (protobuf throws lots of them..)
	set_target_properties(${PROTO_LIB_NAME} PROPERTIES COMPILE_OPTIONS "")

	# install shared libs in linux
	if(WIN32)
	else()

		set(protolib_path )

		list(APPEND PROTOBUF_LIBS "${Protobuf_LIBRARY_RELEASE}.${Protobuf_VERSION}.0")
		list(APPEND PROTOBUF_LIBS_DEB "${Protobuf_LIBRARY_DEBUG}.${Protobuf_VERSION}.0") 

		if (EXISTS ${PROTOBUF_LIBS} AND EXISTS ${PROTOBUF_LIBS_DEB})

			drives_install_libraries(protolib "${PROTOBUF_LIBS}" "${PROTOBUF_LIBS_DEB}")

			add_dependencies(${PROTO_LIB_NAME} protolib)

			drives_install(${PROTO_LIB_NAME})

		else()
			message(WARNING "PROTOBUF_LIBS or PROTOBUF_LIBS_DEB not found")
		endif()

	endif()
endif()