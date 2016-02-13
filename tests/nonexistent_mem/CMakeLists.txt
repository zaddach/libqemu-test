
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( nonexistent_mem ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( nonexistent_mem ${QEMU_LIB} ${LLVM_LIBRARIES} )
ADD_DEPENDENCIES( nonexistent_mem libqemu )
ADD_DEPENDENCIES( check nonexistent_mem )

