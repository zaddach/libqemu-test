
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( arm_invalid_opcode ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( arm_invalid_opcode ${QEMU_LIB} ${LLVM_LIBRARIES} )
ADD_DEPENDENCIES( arm_invalid_opcode libqemu )

