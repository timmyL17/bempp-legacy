find_package(GreatCMakeCookOff NO_MODULE PATHS ${cookoff_path} REQUIRED)
initialize_cookoff()
include(PythonPackage)

find_python_package(os REQUIRED)
if(NOT os_FOUND)
    message(FATAL_ERROR "Could not find os package")
endif()
find_python_package(reallyshouldntexist QUIET)
if(reallyshouldntexist_FOUND)
    message(FATAL_ERROR "Should not find reallyshouldntexist package")
endif()
