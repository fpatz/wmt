NIKOLA=./bin/nikola

.PHONY: bootstrap build serve

build:
	python europe/process-map.py europe/europe-map.svg files/europe-map.svg
	$(NIKOLA) build

serve:
	$(NIKOLA) serve

bootstrap:
	pip install -r requirements.txt
