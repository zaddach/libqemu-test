
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( thumb_nop ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( thumb_nop ${QEMU_LIB_ARM} ${LLVM_LIBRARIES} )
ADD_DEPENDENCIES( thumb_nop libqemu )
ADD_DEPENDENCIES( check thumb_nop )

