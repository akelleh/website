#### Connect over serial

After flashing the chip, get a REPL prompt over serial.

`picocom /dev/ttyUSB0 -b115200`


#### Set up WebREPL

From REPL serial prompt, run WebREPL setup.

`import webrepl_setup`


and follow the prompts.
