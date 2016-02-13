
SET( SOURCE_FILES
	main.cpp
)

ADD_EXECUTABLE( ldhandler_accessed ${SOURCE_FILES} )
TARGET_LINK_LIBRARIES( ldhandler_accessed ${QEMU_LIB} ${LLVM_LIBRARIES} )
ADD_DEPENDENCIES( ldhandler_accessed libqemu )

