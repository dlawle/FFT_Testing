# Project Name
TARGET = ifft

# Sources
CPP_SOURCES = ifft.cpp\
patch_bay.cpp

# Library Locations
LIBDAISY_DIR = ../../libDaisy/
DAISYSP_DIR = ../../DaisySP/

# ASM Sources
ASM_SOURCES = \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_bitreversal2.s

# C sources, mostly CMSIS 
C_SOURCES = \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_rfft_fast_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_cfft_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_rfft_fast_init_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/BasicMathFunctions/arm_mult_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/ComplexMathFunctions/arm_cmplx_mag_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/StatisticsFunctions/arm_max_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/StatisticsFunctions/arm_mean_f32.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/CommonTables/arm_common_tables.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/CommonTables/arm_const_structs.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_bitreversal.c \
$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Source/TransformFunctions/arm_cfft_radix8_f32.c \

C_INCLUDES += \
-I$(LIBDAISY_DIR)/Drivers/CMSIS/DSP/Include

# Core location, and generic Makefile.
SYSTEM_FILES_DIR = $(LIBDAISY_DIR)/core
include $(SYSTEM_FILES_DIR)/Makefile