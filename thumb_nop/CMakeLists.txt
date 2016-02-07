
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( thumb_nop ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( thumb_nop ${QEMU_LIB} ${LLVM_LIBRARIES} pthread tinfo dl)
ADD_DEPENDENCIES( thumb_nop libqemu )

