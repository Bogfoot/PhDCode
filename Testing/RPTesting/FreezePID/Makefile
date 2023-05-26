CC=$(CROSS_COMPILE)gcc
RM=rm

OBJECTSrpreadbuffer= rpreadbuffer.o calib.o main.o fpga.o pid.o generate.o lock.o fpga_pid.o fpga_awg.o fpga_lock.o worker.o

OBJECTSFreezePID= FreezePID.o rpreadandwrite.o calib.o fpga.o pid.o generate.o lock.o fpga_pid.o fpga_awg.o fpga_lock.o worker.o

OBJECTSrpreadandwrite= main.o rpreadandwrite.o calib.o fpga.o pid.o generate.o lock.o fpga_pid.o fpga_awg.o fpga_lock.o worker.o

OBJECTSrpreadandwriteSimple= rpreadandwrite_17_04_2023.o

CFLAGS+= -Wall -Werror -O2 -g -fPIC $(INCLUDE)
LDFLAGS=-shared

rpreadbuffer = rpreadbuffer.so
analogVoltage = FreezePID
rpreadandwrite = rpreadandwrite.so
rpreadandwriteSimple = rpreadandwriteSimple.so

#all: $(CONTROLLER)

rpreadbuffer: $(OBJECTSrpreadbuffer)
	$(CC) -o $(rpreadbuffer) $(OBJECTSrpreadbuffer) $(CFLAGS) $(LDFLAGS)
	-$(RM) -f $(OBJECTSrpreadbuffer)

cleanrpreadbuffer: -$(RM) -f $(OBJECTSrpreadbuffer)

analogVoltage: $(OBJECTSanalogVoltage)
	$(CC) -o $(analogVoltage) $(OBJECTSFreezePID) $(CFLAGS)
	-$(RM) -f $(OBJECTSFreezePID)

rpreadandwrite: $(OBJECTSrpreadandwrite)
	$(CC) -o $(rpreadandwrite) $(OBJECTSrpreadandwrite) $(CFLAGS) $(LDFLAGS)
	-$(RM) -f $(OBJECTSrpreadandwrite)
	
rpreadandwriteSimple: $(OBJECTSrpreadandwriteSimple)
	$(CC) -o $(rpreadandwriteSimple) $(OBJECTSrpreadandwriteSimple) $(CFLAGS) $(LDFLAGS)
	-$(RM) -f $(OBJECTSrpreadandwriteSimple)

cleanrpreadandwrite: -$(RM) -f $(OBJECTSrpreadandwrite)

cleananalogVoltage: -$(RM) -f $(OBJECTSanalogVoltage)

cleanrpreadandwriteSimple: -$(RM) -f $(OBJECTSrpreadandwriteSimple)
