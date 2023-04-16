#!/usr/bin/env python3
# de SQ3SWF 2023

import pyaudio
import serial
import threading
import time

## change these (if you need to)
audio_tx_rate = 11525
audio_rx_rate = 7820
## 


buf = []    # buffer for received audio
urs = [0]   # underrun counter
tx_status = [False]

def receive_serial_audio(serport):
    while True:
        d = serport.read(500)
        buf.append(d)

def play_receive_audio(pastream):
    while True:
        if len(buf) < 2:
            print(f"UNDERRUN #{urs[0]} - refilling")
            urs[0] += 1
            while len(buf) < 10:
                time.sleep(0.01)
        pastream.write(buf[0])
        buf.remove(buf[0])


def transmit_audio_via_serial(pastream, serport):
    while True:
        samples = pastream.read(500)
        if min(samples) != 128 and max(samples) != 128: # if does not contain silence
            if not tx_status[0]:
                tx_status[0] = True
                print("TX ON")
                serport.write(b"UA1;TX0;")
            serport.write(samples)
            print(len(samples), min(samples), max(samples))
        elif tx_status[0]:  # if no signal is detected == silence
            time.sleep(0.1)
            serport.write(b";RX;")
            serport.write(b";RX;")
            serport.write(b";RX;")
            tx_status[0] = False
            print("TX OFF")




def main():
    in_stream = pyaudio.PyAudio().open(format = pyaudio.paUInt8, channels = 1, rate = audio_tx_rate, input = True)
    out_stream = pyaudio.PyAudio().open(format = pyaudio.paInt8, channels = 1, rate = audio_rx_rate, output = True)
    ser = serial.Serial("/dev/ttyUSB0", 115200)

    time.sleep(3) # wait for device to start after opening serial port
    ser.write(b"UA1;") # enable audio streaming

    threading.Thread(target=receive_serial_audio, args=(ser,)).start()
    threading.Thread(target=play_receive_audio, args=(out_stream,)).start()
    threading.Thread(target=transmit_audio_via_serial, args=(in_stream,ser)).start()

    # display some stats every 10 seconds
    ts = time.time()
    while 1:
        print(f"{int(time.time()-ts)} BUF: {len(buf)}")
        time.sleep(10)


if __name__ == '__main__':
    main()