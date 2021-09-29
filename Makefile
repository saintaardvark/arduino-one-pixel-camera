ARDUINO_DIR  = /home/aardvark/arduino-1.8.12
BOARD_TAG     = uno
MONITOR_PORT  = /dev/ttyUSB0
USER_LIB_PATH := /home/aardvark/Arduino/libraries

# Libraries get listed here
# ARDUINO_LIBS = Rtc-master

ARDMK_DIR     = /home/aardvark/dev/arduino/Arduino-Makefile

# AVR_TOOLS_DIR = $(ARDUINO_DIR)/hardware/tools/avr
# AVRDUDE       = $(AVR_TOOLS_DIR)/bin/avrdude
# AVR_TOOLS_DIR = /usr

# AVRDUDE_CONF  = /etc/avrdude/avrdude.conf
# BOARDS_TXT    = /etc/arduino/boards.txt



include $(ARDMK_DIR)/Arduino.mk
