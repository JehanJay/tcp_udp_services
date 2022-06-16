macro(set_drives_cmake_install_prefix)

	if(NOT DRIVES_SKIP_ADTF_LAYER)
		set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install/")
		# if(${DRIVES_INSTALL_LOCALLY})
		# 	set(CMAKE_INSTALL_PREFIX "${CMAKE_BINARY_DIR}/install/")

		# else()
		# 	set(CMAKE_INSTALL_PREFIX "${ADTF_DIR}/addons/drives/${DRIVES_PLATFORM}")

		# endif()

	endif()

endmacro()

function(set_install_postfix_type_for_linux)

	string(TOLOWER "${CMAKE_BUILD_TYPE}" CMAKE_BUILD_TYPE_CMP)

	if("${CMAKE_BUILD_TYPE_CMP}" STREQUAL "release"
		OR "${CMAKE_BUILD_TYPE_CMP}" STREQUAL "relwithdebinfo"
	)

		set(INSTALL_POSTFIX_TYPE "" PARENT_SCOPE)
	else()

		set(INSTALL_POSTFIX_TYPE "debug" PARENT_SCOPE)
	endif()

endfunction()

function(drives_install target_name)

	if(NOT DRIVES_SKIP_ADTF_LAYER)
		set_drives_cmake_install_prefix()
		
		if(WIN32)
			set(INSTALL_POSTFIX "bin$<$<CONFIG:Debug>:/debug>") # depending on build type
		else()
			
			set_install_postfix_type_for_linux()
			set(INSTALL_POSTFIX "bin/${INSTALL_POSTFIX_TYPE}") # depending on build type
		endif()
		message(STATUS "CMAKE_INSTALL_PREFIX: ${CMAKE_INSTALL_PREFIX}")
		message(STATUS "INSTALL_POSTFIX: ${INSTALL_POSTFIX}")
		set(INSTALL_DIR "${CMAKE_INSTALL_PREFIX}${INSTALL_POSTFIX}") # depending on build type
		
		message(STATUS "Installing ${target_name} to ${INSTALL_DIR}")
		
		add_custom_command(
			TARGET ${target_name} POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E make_directory "${INSTALL_DIR}" # make sure directory exists
			COMMAND ${CMAKE_COMMAND} -E copy_if_different "$<TARGET_FILE:${target_name}>" "${INSTALL_DIR}"
		)
		
		get_target_property(target_type ${target_name} TYPE)
		if(WIN32)
			install(TARGETS ${target_name} RUNTIME DESTINATION "${INSTALL_POSTFIX}")
			
			if (NOT target_type STREQUAL STATIC_LIBRARY)
				install(FILES $<TARGET_PDB_FILE:${target_name}> DESTINATION "${INSTALL_POSTFIX}" OPTIONAL)
			endif()
		else()
			if (NOT target_type STREQUAL STATIC_LIBRARY AND NOT target_type STREQUAL EXECUTABLE)
				install(TARGETS ${target_name} LIBRARY DESTINATION "${INSTALL_POSTFIX}")
			endif()
		endif()
		
	endif()
endfunction()

function(drives_install_libraries target_name file_names file_names_debug)

	add_custom_target(
		${target_name}
	)

	if(NOT DRIVES_SKIP_ADTF_LAYER)
		set_drives_cmake_install_prefix()
		add_custom_command(
			TARGET ${target_name} PRE_BUILD
			COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_INSTALL_PREFIX}/bin" # make sure directory exists
			COMMAND ${CMAKE_COMMAND} -E make_directory "${CMAKE_INSTALL_PREFIX}/bin/debug" # make sure directory exists
			COMMAND ${CMAKE_COMMAND} -E copy_if_different "${file_names}" "${CMAKE_INSTALL_PREFIX}/bin"
			COMMAND ${CMAKE_COMMAND} -E copy_if_different "${file_names_debug}" "${CMAKE_INSTALL_PREFIX}/bin/debug"
			COMMAND_EXPAND_LISTS
		)
	
		set_property(TARGET ${target_name} PROPERTY FOLDER "drives_install_targets")

		install(FILES ${file_names} DESTINATION "${CMAKE_INSTALL_PREFIX}/bin")
		install(FILES ${file_names_debug} DESTINATION "${CMAKE_INSTALL_PREFIX}/bin/debug")

	endif()
endfunction()

function(drives_install_files_single target_name file_list install_dir)

	add_custom_target(
		${target_name}
	)

	if(NOT DRIVES_SKIP_ADTF_LAYER)
		add_custom_command(
			TARGET ${target_name} POST_BUILD
			COMMAND ${CMAKE_COMMAND} -E make_directory "${install_dir}"
			COMMAND ${CMAKE_COMMAND} -E copy_if_different "${file_list}" "${install_dir}"
			COMMAND_EXPAND_LISTS
		)
		
		set_property(TARGET ${target_name} PROPERTY FOLDER "drives_install_targets")
		message(STATUS "CALLED: drives_install_files_single")
		install(FILES ${file_list} DESTINATION "${install_dir}")

	endif()
endfunction()