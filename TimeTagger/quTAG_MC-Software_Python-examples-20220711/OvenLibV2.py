import matplotlib.pyplot as plt
import serial


class OvenController:
    def __init__(
        self,
        oven,
        port="COM7",
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1,
    ):
        self.oven = oven
        self.oven.port = port
        self.oven.baudrate = baudrate
        self.oven.parity = parity
        self.oven.stopbits = stopbits
        self.oven.bytesize = bytesize
        self.oven.timeout = timeout

        self.enable_oven()

    def enable_oven(self):
        self.oven.open()
        # define the right message string to enable heating the oven
        send_message = "\x01j00CB"
        self.oven.write(send_message.encode())
        self.oven.close()
        return

    def string_bit_converter(self, input_list):
        output_string = [""]
        j = 0
        for i in range(4, len(input_list)):
            if input_list[i] == ";":
                output_string.append("")
                j += 1
            elif input_list[i] != "\x01":
                output_string[j] += input_list[i]
        return output_string

    def check_temperature(self):
        self.oven.open()
        self.oven.flushOutput()
        send_message = "\x01j00CB"
        self.oven.write(send_message.encode())
        oven_output = self.oven.readline()
        oven_output_convert = list(oven_output)
        if oven_output_convert[0] == 1:
            oven_output_ascii = [chr(i) for i in oven_output_convert]
            self.oven.close()
            return float(self.string_bit_converter(oven_output_ascii)[1])
        else:
            self.oven.close()
            return self.check_temperature()

    def command_packet_constructor(self, T):
        start = "\x01"
        command = "i"
        data = "1;" + str(T) + ";100;0;100;1;0;"
        data_length = str(len(data))
        check_sum = hex(sum(list((start + command + data_length + data).encode())))[3:]
        command_packet = start + command + data_length + data + check_sum
        return command_packet

    def set_temperature(self, T):
        self.oven.open()
        send_message = self.command_packet_constructor(T)
        self.oven.write(send_message.encode())
        self.oven.close()

    def scan_plot_current_iteration(self, x, y):
        plt.close()
        plt.plot(x, y)
        plt.show()