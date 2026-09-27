SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

VHDL_SOURCES += $(shell pwd)/../rtl_vhdl/complex_mixer.vhd

TOPLEVEL = complex_mixer
MODULE = test_sdr_pipeline

include $(shell cocotb-config --makefiles)/Makefile.sim
