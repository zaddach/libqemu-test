PROJECT( libqemu-test )
CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

INCLUDE( ExternalProject )

SET( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake )

FIND_PACKAGE( LLVM REQUIRED COMPONENTS jit bitreader bitwriter ipo linker engine irreader)

INCLUDE_DIRECTORIES(${LLVM_INCLUDE_DIRS})
ADD_DEFINITIONS(${LLVM_DEFINITIONS} -D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
LINK_DIRECTORIES(${LLVM_LIBRARY_DIRS})

SET (CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS} -std=c++11)

# Build qemulib
IF (${CMAKE_BUILD_TYPE} EQUAL "Debug")
	SET (QEMU_DEBUG --enable-debug)
ELSE (${CMAKE_BUILD_TYPE} EQUAL "Debug")
	SET (QEMU_DEBUG )
ENDIF (${CMAKE_BUILD_TYPE} EQUAL "Debug")

#First check if the submodule has already been checked out.
#If not, we can do that right here during the CMAKE generation.
IF (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure")
    EXECUTE_PROCESS (
	git submodule update --init libqemu
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
ENDIF (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure")

ExternalProject_Add(libqemu
	SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libqemu
	CONFIGURE_COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure --enable-lib --target-list=arm-lib,i386-lib,x86_64-lib --prefix=${CMAKE_CURRENT_BINARY_DIR}/libqemu --cxx=clang++ ${QEMU_DEBUG}
	BUILD_COMMAND $(MAKE)
	BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu
	INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu
	INSTALL_COMMAND make install
)

SET( QEMU_LIB_ARM ${CMAKE_CURRENT_BINARY_DIR}/libqemu/arm-lib/libqemu-arm.so )
SET( QEMU_LIB_I386 ${CMAKE_CURRENT_BINARY_DIR}/libqemu/i386-lib/libqemu-i386.so )
INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/include )

ADD_CUSTOM_COMMAND (
    OUTPUT features
    COMMAND ${CMAKE_COMMAND} -E create_symlink ${CMAKE_CURRENT_SOURCE_DIR}/features ${CMAKE_CURRENT_BINARY_DIR}/features) 

ADD_CUSTOM_TARGET (check
    COMMAND cucumber -q
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Run Aruba cucumber testsuite"
    DEPENDS features
)

ADD_SUBDIRECTORY( tests/arm_nop )
ADD_SUBDIRECTORY( tests/thumb_nop )
ADD_SUBDIRECTORY( tests/arm_invalid_opcode )
ADD_SUBDIRECTORY( tests/nonexistent_mem )
ADD_SUBDIRECTORY( tests/ldhandler_accessed )
ADD_SUBDIRECTORY( tests/i386_int3 )
