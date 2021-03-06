find_path(F2C_INCLUDE_DIR NAMES f2c.h)
find_library(F2C_LIBRARY NAMES libf2c.a f2c)

set(F2C_INCLUDE_DIRS ${F2C_INCLUDE_DIR})
set(F2C_LIBRARIES ${F2C_LIBRARY})

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(F2C REQUIRED_VARS F2C_INCLUDE_DIR F2C_LIBRARY)
