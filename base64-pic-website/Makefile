.PHONY: all clean

%.svg: %.pic *.macros
	dpic -v < "$<" > "$@"

%.png: %.svg
	inkscape -f "$<" --export-png="$@" --export-area-drawing --export-dpi 70 -b white
	optipng $@

PICS=$(wildcard *.pic)

all: $(PICS:.pic=.png)

clean:
	rm -f -v *.svg *.png
