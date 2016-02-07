PROJECT( libqemu-test )
CMAKE_MINIMUM_REQUIRED( VERSION 2.8 )

INCLUDE( ExternalProject )

SET( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_SOURCE_DIR}/cmake )


ExternalProject_Add(libqemu
#	GIT_REPOSITORY https://github.com/zaddach/libqemu.git
	GIT_REPOSITORY git@github.com:zaddach/libqemu
#	GIT_TAG 1c87ce8248bc7842952ef5f1cbd1a781f0ea0aca 
	GIT_TAG jonas/wip 
	SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/libqemu
	CONFIGURE_COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/configure --enable-lib --target-list=arm-lib --enable-debug --prefix=${CMAKE_CURRENT_BINARY_DIR}/libqemu --cxx=clang++
	BUILD_COMMAND ${MAKE}
	#BUILD_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu
	BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build
	INSTALL_DIR ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build
	INSTALL_COMMAND make install
)

FIND_PACKAGE( LLVM REQUIRED COMPONENTS jit bitreader bitwriter ipo linker engine irreader)
INCLUDE_DIRECTORIES(${LLVM_INCLUDE_DIRS})
ADD_DEFINITIONS(${LLVM_DEFINITIONS} -D__STDC_CONSTANT_MACROS -D__STDC_LIMIT_MACROS)
LINK_DIRECTORIES(${LLVM_LIBRARY_DIRS})

SET( QEMU_LIB ${CMAKE_CURRENT_BINARY_DIR}/libqemu.build/arm-lib/libqemu-arm.so )
INCLUDE_DIRECTORIES( ${CMAKE_CURRENT_SOURCE_DIR}/libqemu/include )
	

ADD_SUBDIRECTORY( arm_nop )
ADD_SUBDIRECTORY( thumb_nop )
