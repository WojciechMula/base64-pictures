main.pdf: main.tex encoding.tex decoding-lookup-example.tex decoding-merging.tex
	pdflatex main.tex

encoding.tex: encoding.tikz.py
	python $^ > /dev/shm/tmp
	mv /dev/shm/tmp $@

decoding-lookup-example.tex: decoding-lookup-example.tikz.py
	python $^ > /dev/shm/tmp
	mv /dev/shm/tmp $@

decoding-merging.tex: decoding-merging.tikz.py
	python $^ > /dev/shm/tmp
	mv /dev/shm/tmp $@

