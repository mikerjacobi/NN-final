#Makefile for Flatworld II V1.0 tpc 17 March 2009
CC = gcc
FILES = FWmain.o
#for Linux
IPATH= -I/usr/include/GL
LPATH= -L/usr/lib

OPSYS = $(shell uname)

COPTS = -O2 -lpython2.6
LDLIBS = -lGL -lGLU -lglut -lm

ifeq ($(OPSYS), Darwin)
	IPATH += -I/sw/include
	LPATH += -L/sw/lib
	LDLIBS = -framework GLUT -framework OpenGL -framework Cocoa
#COPTS += -flat_namespace -undefined suppress
endif


all: FWmain.o FWmainNG.o *.c
	$(CC) -g -Wall $(COPTS) $(FILES) $(IPATH) $(LPATH) $(LDLIBS) -o FWmain
	$(CC) -g -Wall $(COPTS) FWmainNG.o $(IPATH) $(LPATH) $(LDLIBS) -o FWmainNG
	$(CC) -c -Wall $(COPTS) $(IPATH) FWmain.c
	$(CC) -c -Wall $(COPTS) $(IPATH) FWmainNG.c

FWmain: $(FILES)
	 $(CC) -g -Wall $(COPTS) $(FILES) $(IPATH) $(LPATH) $(LDLIBS) -o FWmain

FWmain.o: *.c 
	$(CC) -c -Wall $(COPTS) $(IPATH) FWmain.c

FWmainNG: FWmainNG.o
	 $(CC) -g -Wall $(COPTS) FWmainNG.o $(IPATH) $(LPATH) $(LDLIBS) -o FWmainNG

FWmainNG.o: *.c 
	$(CC) -c -Wall $(COPTS) $(IPATH) FWmainNG.c

clean:
	-rm -f *.o FWmain FWmainNG
