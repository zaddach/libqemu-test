PROJECT( libqemu-test )
CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

INCLUDE( ExternalProject )

SET( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake )

FIND_PACKAGE( LLVM REQUIRED COMPONENTS jit bitreader bitwriter ipo linker engine irreader)

INCLUDE_DIRECTORIES(${LLVM_INCLUDE_DIRS})
ADD_DEFINITIONS(${LLVM_DEFINITIONS} -D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
LINK_DIRECTORIES(${LLVM_LIBRARY_DIRS})

# Build qemulib

#First check if the submodule has already been checked out.
#If not, we can do that right here during the CMAKE generation.
IF (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure")
    EXECUTE_PROCESS (
	git submodule update --init libqemu
	WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}")
ENDIF (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure")

ExternalProject_Add(libqemu
	SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libqemu
	CONFIGURE_COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure --enable-lib --target-list=arm-lib --enable-debug --prefix=${CMAKE_CURRENT_BINARY_DIR}/libqemu --cxx=clang++
	BUILD_COMMAND ${MAKE}
	BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build
	INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build
	INSTALL_COMMAND make install
)

SET( QEMU_LIB ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build/arm-lib/libqemu-arm.so )
INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/include )
	

ADD_SUBDIRECTORY( arm_nop )
ADD_SUBDIRECTORY( thumb_nop )
