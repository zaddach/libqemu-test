
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( arm_nop ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( arm_nop ${QEMU_LIB} ${LLVM_LIBRARIES} pthread tinfo dl)
ADD_DEPENDENCIES( arm_nop libqemu )

