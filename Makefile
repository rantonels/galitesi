NAME=galitesi
PRESNAME=slides
IMGFOLDER=images

.PHONY: $(NAME).pdf $(PRESNAME).pdf all clean

all: $(NAME).pdf $(PRESNAME).pdf

$(NAME).pdf: $(NAME).tex $(IMGFOLDER)/*
	latexmk -pvc -pdf -pdflatex="pdflatex -interactive=nonstopmode" $(NAME).tex

$(PRESNAME).pdf: $(PRESNAME).tex $(IMGFOLDER)/*
	latexmk -pvc -pdf -pdflatex="pdflatex -interactive=nonstopmode" $(PRESNAME).tex

cleanall:
	latexmk -C

clean:
	latexmk -c
