import sys
import matplotlib.pyplot as plot
import numpy as np
import visa
import time

def find_scope():
    # Get the USB device, e.g. 'USB0::0x1AB1::0x04CE::DS1ZA170300600'
    instruments = visa.get_instruments_list()
    usb = filter(lambda x: 'DS1' in x, instruments)
    if len(usb) != 1:
        print('No Scope found: ', instruments)
        #sys.exit(-1)
    else:
        print("Scope found at: "+usb[0])
        global scope
        scope = visa.instrument(usb[0], timeout=1, chunk_size=10240000) # bigger timeout for long mem


def capture(*args):
    freq = wave.ask_for_values("FREQ?")[0]
    voltage_high = wave.ask_for_values("VOLTage:HIGH?")[0]
    voltage_low = wave.ask_for_values("VOLTage:LOW?")[0]
    # Get the timescale
    timescale = scope.ask_for_values(":TIMebase:MAIN:SCALe?")[0]
    time.sleep(0.5)
    # And the timescale offset
    timeoffset = scope.ask_for_values(":TIMebase:MAIN:OFFSet?")[0]
    time.sleep(0.5)
    # Get the voltscale
    voltscale_ch1 = scope.ask_for_values(':CHAN1:SCAL?')[0]
    time.sleep(0.5)
    voltscale_ch2 = scope.ask_for_values(':CHAN2:SCAL?')[0]
    time.sleep(0.5)
    voltscale_ch3 = scope.ask_for_values(':CHAN3:SCAL?')[0]
    time.sleep(0.5)
    voltscale_ch4 = scope.ask_for_values(':CHAN4:SCAL?')[0]
    time.sleep(0.5)
    # And the voltage offset
    voltoffset = scope.ask_for_values(":CHAN1:OFFS?")[0]
    time.sleep(0.5)
    mdepth = int(scope.ask_for_values(":ACQuire:MDEPth?")[0])
    time.sleep(0.5)
    print(mdepth)
    ascii = 15625
    batches = mdepth/ascii

    scope.write(":WAVeform:FORMat ASCii")
    time.sleep(0.5)
    scope.write(":WAVeform:MODE RAW")
    time.sleep(0.5)

    scope.write(":WAV:SOUR CHAN1")
    time.sleep(0.5)
    rawdata_ch1 = scope.ask(":WAV:DATA?")[11:]
    time.sleep(0.5)
    '''
    scope.write(":WAV:SOUR CHAN2")
    time.sleep(0.5)
    rawdata_ch2 = scope.ask(":WAV:DATA?")[11:]
    time.sleep(0.5)
    '''
    data = []
    scope.write(":WAV:SOUR CHAN2")
    time.sleep(0.5)
    for batch in range(0,batches):
        scope.write(":WAV:STAR "+str((15625*batch)+1))
        time.sleep(1)
        scope.write(":WAV:STOP "+str(15625*(batch+1)))
        time.sleep(1)
        rawdata_ch2 = str(scope.ask(":WAV:DATA?")[11:])+str(',')
        time.sleep(5)
        data.append(rawdata_ch2.split(','))


    scope.write(":WAV:SOUR CHAN3")
    time.sleep(0.5)
    rawdata_ch3 = scope.ask(":WAV:DATA?")[11:]
    time.sleep(0.5)

    #data = np.frombuffer(rawdata_ch2, 'B')
    #data = rawdata_ch2.split(',')
    #print(data)
    timez = np.arange(len(data))

    plot.plot(timez, data)
    plot.title("Oscilloscope Channel 2")
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (' + tUnit + ')")
    plot.xlim(timez[0], timez[-1])
    plot.show()


find_scope()
