# trusdx-audio

Script in this repository allows you to send and receive audio to/from your (tr)uSDX (https://dl2man.de/) transceiver.

It enables operating digital modes using nothing but a laptop, (tr)uSDX and, obviously, an antenna - with limited power (<0.5 W), but that should be plenty for weak signal modes.

It has been battle tested with FT8 and successfuly produced a signal on pskreporter (85 RX reports, including `W` and `VK`), as well as completed two QSOs.

![PSKreporter screenshot](img/ft8_reporter.jpg)
 
```
230416_181830    14.074 Tx FT8      0  0.0 1117 CQ SQ3SWF JO82                       
230416_181845    14.074 Rx FT8      0  1.2 1117 SQ3SWF F4ACR IN96
230416_181900    14.074 Tx FT8      0  0.0 1117 F4ACR SQ3SWF +00                     
230416_181915    14.074 Rx FT8     -5  1.0 1117 SQ3SWF F4ACR R-24
230416_181930    14.074 Tx FT8      0  0.0 1117 F4ACR SQ3SWF RR73                    
230416_181945    14.074 Rx FT8     -5  1.2 1117 SQ3SWF F4ACR 73

230416_182300    14.074 Tx FT8      0  0.0 1117 CQ SQ3SWF JO82                       
230416_182315    14.074 Rx FT8    -13  0.9  925 SQ3SWF MM0HVU -16
230416_182330    14.074 Tx FT8      0  0.0 1117 MM0HVU SQ3SWF R-13                   
230416_182345    14.074 Rx FT8    -13  1.0  926 SQ3SWF MM0HVU RR73
230416_182400    14.074 Tx FT8      0  0.0 1117 MM0HVU SQ3SWF 73                     
```

## Requirements

Your (tr)uSDX needs to run [alpha](https://dl2man.de/wp-content/uploads/2022/01/wp.php/alpha.html) firmware (otherwise it does not go properly from TX to RX).

You'll need a Linux PC (Raspberry PI should be fine, too) with PulseAudio, Python 3 and extra libraries: `pyserial` and `pyaudio`.

## Usage

* Create a new virtual audio device: `pactl load-module module-null-sink sink_name=TRUSDX sink_properties=device.description="TRUSDX"`
* Run the script in terminal: `trusdx-txrx.py`.
* Use `pavucontrol` to assign the newly created `TRUSDX` audio device to the application you'd like to use for transmitting and receiving (or do that from the application itself, if it includes audio settings - WSJT-X does).
* TX/RX switching is performed automatically by a simple VOX - when audio samples captured from the application contain no audio, the rig is set into receive mode.
* Important - make sure the transmitted signal looks good using a 2nd receiver. Well, I mean, reasonably good - not worse than "regular" signal produced by (tr)uSDX. Adjust the audio level in `pavucontrol`. Too high level of TX audio will create a total mess on RF output. Too low, the rig won't transmit anything or will transmit less than it is able to.

## Bugs, issues

Since the (tr)uSDX firmware is alpha, I have experienced a few hangs (where the rig did not go back from TX into receive) and occasional restarts. Not sure if they were related to the PC code or rather the firmware itself.

Keep in mind it's all experimental, no warranty or service included and your beloved QRP rig may go boom-boom - I suggest playing with USB-only power instead of full 12 V. It's enough power for digital modes anyway and much less violent on the finals.

73 de SQ3SWF
