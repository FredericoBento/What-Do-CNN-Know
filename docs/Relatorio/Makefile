ROOT_FILE 	= main
BACKUP_FILES 	= *~ *.bak
CLEAN_FILES 	= $(BACKUP_FILES) *.fls *.acn *.acr *.alg *.aux *.bcf *.bbl *.blg *.dvi *.fdb_latexmk *.glg *.glo *.gls *.idx *.ilg *.ind *.ist *.lof *.log *.lot *.lol *.maf *.mtc *.mtc0 *.nav *.nlo *.out *.pdfsync *.ps *.snm *.synctex.gz *.toc *.vrb *.xdy *.tdo *.run.xml *-blx.bib _minted-$(ROOT_FILE)
DIST_FILES 	= $(ROOT_FILE).pdf

.PHONY: clean distclean tex index frontispiece biber prepare simplethesis pdf

clean:
	echo $(CLEAN_FILES) | xargs $(RM) -r; \
	find . -name '*.aux' | xargs $(RM);

distclean: clean
	$(RM) $(DIST_FILES)

tex: 
	latexmk -silent -f -pdf -pdflatex="pdflatex -shell-escape -interaction=nonstopmode" -use-make $(ROOT_FILE).tex

index: 
	makeglossaries $(ROOT_FILE)
	

biber: 
	biber $(ROOT_FILE)

prepare: tex
	$(MAKE) index
	$(MAKE) biber
	
simplethesis: prepare
	$(MAKE) tex

pdf: prepare
	$(MAKE) tex
	