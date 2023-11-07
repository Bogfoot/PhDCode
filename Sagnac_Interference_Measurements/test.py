import pyvisa as visa, pylab as pl


def main():
    _rm = visa.ResourceManager()
    dso = _rm.open_resource("USB0::0xF4EC::0xEE38::0123456789::INSTR")
    dso.write("chdr off")
    vdiv = dso.query("c1:vdiv?")
    ofst = dso.query("c1:ofst?")
    tdiv = dso.query("tdiv?")
    sara = dso.query("sara?")
    sara_unit = {"G": 1e9, "M": 1e6, "k": 1e3}
    for unit in sara_unit.keys():
        if sara.find(unit) != -1:
            sara = sara.split(unit)
            sara = float(sara[0]) * sara_unit[unit]
            break
    sara = float(sara)
    dso.timeout = 30000  # default value is 2000(2s)
    dso.chunk_size = 20 * 1024 * 1024  # default value is 20*1024(20k bytes)
    dso.write("c1:wf? dat2")
    recv = list(dso.read_raw())[15:]
    recv.pop()
    recv.pop()
    volt_value = []
    for data in recv:
        if data > 127:
            data = data - 255
        else:
            pass
        volt_value.append(data)
    time_value = []
    for idx in range(0, len(volt_value)):
        volt_value[idx] = volt_value[idx] / 25 * float(vdiv) - float(ofst)
        time_data = -(float(tdiv) * 14 / 2) + idx * (1 / sara)
        time_value.append(time_data)
    pl.figure(figsize=(7, 5))
    pl.plot(time_value, volt_value, markersize=2, label="Y-T")
    pl.legend()
    pl.grid()
    pl.show()


if __name__ == "__main__":
    main()
