# nanoHIL

nanoHIL is an Arduino Nano smoke bench. It checks that a device's pins move, and it reports what it sees to the host. That job is what a multi-thousand-dollar hardware-in-the-loop rig is often asked to do for a first checkout. Those rigs, including dSPACE, stay in place for the larger tests. nanoHIL is the inexpensive pass that runs first.

In nano4I4O the hardware under test is a second Nano, so the four checkout wires can be proven without a product. On a real bench the product attaches to the same nanoHIL pins. The second Nano is only the stand-in.

## Checkout wires for nano4I4O

| nanoHIL pin | HUT pin | Role in this project |
| --- | --- | --- |
| D2 | D2 | Digital checkout, level 0 or 1 |
| D3 | D3 | Digital checkout, level 0 or 1 |
| D4 | D4 | Digital checkout, level 0 or 1 |
| D5 | D5 | Digital checkout, level 0 or 1 |
| GND | GND | Shared ground |

D0 and D1 stay on the USB serial link to the host. They are not checkout wires. Reader frames use 115200 baud, 8 data bits, no parity, and 1 stop bit.

## Power and reset

| Pin | What a smoke bench can use it for |
| --- | --- |
| VIN | Unregulated supply into the onboard regulator, about 7 V to 12 V |
| 5V | Regulated 5 V rail. This is the logic level for the checkout pins |
| 3V3 | Board 3.3 V output from the onboard regulator. Not a checkout wire in nano4I4O |
| GND | Two ground pins. One of them is the shared ground to the device under test |
| RESET | Active-low reset. Also brought out on the ICSP header |
| AREF | Analog reference. Leave it open unless a test selects an external reference |

The USB connector powers the board and carries the serial report. Do not feed VIN and USB in a way that back-powers the regulator.

## Digital pins

| Pin | Also used as | PWM | Notes for a smoke bench |
| --- | --- | --- | --- |
| D0 | UART RX | no | Host serial receive. Keep it off the device harness |
| D1 | UART TX | no | Host serial transmit. Keep it off the device harness |
| D2 | external interrupt 0 | no | nano4I4O checkout wire |
| D3 | external interrupt 1 | yes | nano4I4O checkout wire. Also available as PWM on other benches |
| D4 |  | no | nano4I4O checkout wire |
| D5 |  | yes | nano4I4O checkout wire. Also available as PWM on other benches |
| D6 |  | yes | Free for a later smoke test |
| D7 |  | no | Free for a later smoke test |
| D8 |  | no | Free for a later smoke test |
| D9 |  | yes | Free for a later smoke test |
| D10 | SPI SS | yes | Free for a later smoke test. SPI chip select when SPI is in use |
| D11 | SPI MOSI | yes | Free for a later smoke test |
| D12 | SPI MISO | no | Free for a later smoke test |
| D13 | SPI SCK, onboard LED | no | Free for a later smoke test. Driving it also lights the LED |

## Analog pins

A0 through A7 are inputs to the 10-bit ADC. A0 through A5 can also be digital pins D14 through D19.

| Pin | Digital name | Other use | Notes for a smoke bench |
| --- | --- | --- | --- |
| A0 | D14 | ADC0 | Free analog or digital smoke channel |
| A1 | D15 | ADC1 | Free analog or digital smoke channel |
| A2 | D16 | ADC2 | Free analog or digital smoke channel |
| A3 | D17 | ADC3 | Free analog or digital smoke channel |
| A4 | D18 | ADC4, I2C SDA | Free. I2C data when a test needs the bus |
| A5 | D19 | ADC5, I2C SCL | Free. I2C clock when a test needs the bus |
| A6 | none | ADC6 | Analog input only on the ATmega328P Nano |
| A7 | none | ADC7 | Analog input only on the ATmega328P Nano |

## Buses already on the Nano

- UART on D0/D1, used here as the host report port.
- SPI on D10, D11, D12, and D13, plus the ICSP header (MOSI, MISO, SCK, reset, 5 V, ground).
- I2C on A4 and A5.

nano4I4O does not use SPI, I2C, PWM, or the ADC. Those pins stay available so a later smoke image can check them without a different board.
