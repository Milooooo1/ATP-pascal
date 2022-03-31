#############################################################################
#
# Project Makefile
#
# (c) Wouter van Ooijen (www.voti.nl) 2016
#
# This file is in the public domain.
# 
#############################################################################

SERIAL_PORT ?= /dev/ttyUSB0

# source files in this project (main.cpp is automatically assumed)
SOURCES := out.asm

# header files in this project
HEADERS :=

# other places to look for files for this project
SEARCH  := 

out.asm:
	python3.10 main.py -f ~/ATP-pascal/example.pas -c

CLEAN += *.o out.asm

# set REATIVE to the next higher directory 
# and defer to the Makefile.due there
RELATIVE := $(RELATIVE).
include Makefile.due
