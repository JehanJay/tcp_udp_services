#----------------------------------------------------------------
# Generated CMake target import file for configuration "Debug".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "protobuf::libprotobuf-lite" for configuration "Debug"
set_property(TARGET protobuf::libprotobuf-lite APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(protobuf::libprotobuf-lite PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libprotobuf-lited.so.3.11.2.0"
  IMPORTED_SONAME_DEBUG "libprotobuf-lited.so.3.11.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS protobuf::libprotobuf-lite )
list(APPEND _IMPORT_CHECK_FILES_FOR_protobuf::libprotobuf-lite "${_IMPORT_PREFIX}/lib/libprotobuf-lited.so.3.11.2.0" )

# Import target "protobuf::libprotobuf" for configuration "Debug"
set_property(TARGET protobuf::libprotobuf APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(protobuf::libprotobuf PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libprotobufd.so.3.11.2.0"
  IMPORTED_SONAME_DEBUG "libprotobufd.so.3.11.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS protobuf::libprotobuf )
list(APPEND _IMPORT_CHECK_FILES_FOR_protobuf::libprotobuf "${_IMPORT_PREFIX}/lib/libprotobufd.so.3.11.2.0" )

# Import target "protobuf::libprotoc" for configuration "Debug"
set_property(TARGET protobuf::libprotoc APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(protobuf::libprotoc PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/lib/libprotocd.so.3.11.2.0"
  IMPORTED_SONAME_DEBUG "libprotocd.so.3.11.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS protobuf::libprotoc )
list(APPEND _IMPORT_CHECK_FILES_FOR_protobuf::libprotoc "${_IMPORT_PREFIX}/lib/libprotocd.so.3.11.2.0" )

# Import target "protobuf::protoc" for configuration "Debug"
set_property(TARGET protobuf::protoc APPEND PROPERTY IMPORTED_CONFIGURATIONS DEBUG)
set_target_properties(protobuf::protoc PROPERTIES
  IMPORTED_LOCATION_DEBUG "${_IMPORT_PREFIX}/bin/protoc-3.11.2.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS protobuf::protoc )
list(APPEND _IMPORT_CHECK_FILES_FOR_protobuf::protoc "${_IMPORT_PREFIX}/bin/protoc-3.11.2.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
