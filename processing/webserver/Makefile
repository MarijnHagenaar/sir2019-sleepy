PY_FILES := $(wildcard *.py **/*.py)
SH_FILES := $(wildcard *.sh **/*.sh)
FLAKE8_FLAGS := --max-line-length=120 --ignore W606,E501 --inline-quotes="'"

all: isort lint

isort: $(PY_FILES)
	isort $(PY_FILES)

lint: $(PY_FILES) $(SH_FILES) sass
	flake8 $(FLAKE8_FLAGS) $(PY_FILES)
	pylint $(PY_FILES)
	shellcheck -f gcc $(SH_FILES)

sass: html/sass/*.scss
	python <<< "import sass; sass.compile(dirname=('html/sass', 'html/css'), output_style='compressed')"

clean:
	find . -name "*.pyc" -delete

.PHONY: all lint isort clean sass
