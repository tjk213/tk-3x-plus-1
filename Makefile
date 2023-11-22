####################################################################################
##               ,:                                                         ,:    ##
##             ,' |                                                       ,' |    ##
##            /   :                                                      /   :    ##
##         --'   /       :::::::::::   :::::::::::   :::    :::       --'   /     ##
##         \/ />/           :+:            :+:       :+:   :+:        \/ />/      ##
##         / /_\           +:+            +:+       +:+  +:+          / /_\       ##
##      __/   /           +#+            +#+       +#++:++         __/   /        ##
##      )'-. /           +#+            +#+       +#+  +#+         )'-. /         ##
##      ./  :\          #+#        #+# #+#       #+#   #+#         ./  :\         ##
##       /.' '         ###         #####        ###    ###          /.' '         ##
##     '/'                                                        '/'             ##
##     +                                                          +               ##
##    '                                                          '                ##
####################################################################################
##            Copyright © 2023 Tyler J. Kenney. All rights reserved.              ##
####################################################################################
####################################################################################

TARGET = tk-3x+1

CXX = /usr/bin/clang++

CXXFILES = tk-3x+1.cpp
OBJFILES = $(patsubst %.cpp, %.o, $(CXXFILES))

all: $(TARGET)

CXXFLAGS = -Wall -Werror -std=gnu++17
CXXFLAGS += -I /opt/homebrew/opt/llvm/include
CXXFLAGS += -O3 -mcpu=apple-m1

LDFLAGS = -L /opt/homebrew/opt/llvm/lib
LIBS = -lLLVMCore -lLLVMSupport -lLLVMDemangle
LIBS += -lm -lz -lcurses

$(TARGET): $(OBJFILES)
	$(CXX) $(LDFLAGS) $(LIBS) -o $@ $^
