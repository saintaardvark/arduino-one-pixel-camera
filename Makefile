DEV?=/dev/ttyUSB0
RSHELL=rshell --port $(DEV)
RSYNC_FLAGS?=
MODEM_SPEED=115200

log: venv
	$(VENV)/python ./logger.py

jl: venv
	$(VENV)/jupyter-lab

# --mirror: delete files on board that are not in source dir
install: kill_console
	$(RSHELL) rsync --mirror micropython/ /pyboard/

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
