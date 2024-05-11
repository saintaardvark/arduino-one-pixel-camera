DEV?=/dev/ttyUSB0
RSHELL=rshell --port $(DEV)
RSYNC_FLAGS?=
MODEM_SPEED=115200

log:
	$(VENV)/python ./logger.py

jl:
	$(VENV)/jupyter-lab

install:
	$(RSHELL) rsync micropython/ /pyboard/

.PHONY: repl
repl:
	$(RSHELL) repl

.PHONY: rshell
rshell:
	$(RSHELL)

console: terminal
terminal:
	~/bin/espconsole.sh

.PHONY: kill_console
kill_console:
	@-pkill -9 screen

.PHONY: reset
reset:
	$(RSHELL) repl pyboard "~ import machine ~ machine.reset()~"

include Makefile.venv
