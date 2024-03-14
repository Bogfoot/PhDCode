CC=$(CROSS_COMPILE)gcc
RM=rm

OBJECTS= qutag_histogram.o

CFLAGS+= -Wall -O2 -g -fPIC $(INCLUDE)
LDFLAGS=-shared

CONTROLLER = qutag_histogram.so

all: $(CONTROLLER)

$(CONTROLLER): $(OBJECTS)
	$(CC) -o $(CONTROLLER) $(OBJECTS) $(CFLAGS) $(LDFLAGS)
	-$(RM) -f $(OBJECTS)

clean:
	-$(RM) -f $(OBJECTS)
