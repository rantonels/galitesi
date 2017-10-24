NAME=galitesi
IMGFOLDER=images

.PHONY: $(NAME).pdf all clean

all: $(NAME).pdf

$(NAME).pdf: $(NAME).tex $(IMGFOLDER)/*
	latexmk -pvc -pdf -pdflatex="pdflatex -interactive=nonstopmode"

cleanall:
	latexmk -C

clean:
	latexmk -c
