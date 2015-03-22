NIKOLA=./bin/nikola

.PHONY: bootstrap build serve clean

build:
	./bin/python process-map.py europe/europe-map.svg files/europe-map.svg
	$(NIKOLA) build

serve:
	$(NIKOLA) serve

bootstrap:
	virtualenv --clear .
	./bin/pip install -r requirements.txt

clean:
	rm -rf cache output .doit.db
