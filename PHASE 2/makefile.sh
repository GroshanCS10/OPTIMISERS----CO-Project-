p3:
	python3 ./Phase\ I/start.py ${INP}.asm
	python3 ./Phase\ III/runscript_1.py ${INP}.mc
p2:
	python3 ./Phase\ I/start.py ${INP}.asm
	python3 ./Phase\ II/runscript.py ${INP}.mc