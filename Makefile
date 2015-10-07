NIKOLA=./bin/nikola

.PHONY: bootstrap build serve clean production upload

build:
	./bin/python process-map.py europe/europe-map.svg files/europe-map.svg
	$(NIKOLA) build

production:
	./bin/python process-map.py europe/europe-map.svg files/europe-map.svg
	$(NIKOLA) build --conf=production.py

serve:
	$(NIKOLA) serve

bootstrap:
	virtualenv --clear .
	./bin/pip install -r requirements.txt

clean:
	rm -rf cache output .doit.db

upload: production
	lftp -f upload.ftp
