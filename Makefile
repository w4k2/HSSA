init:
	pip install -U -I -r requirements.txt

install: #test
	python setup.py install

getData:
	if [ ! -d "data" ]; then git clone https://github.com/w4k2/data.git; rm -rf data/.git; fi

publish: test
	python setup.py sdist upload

test: getData
	clear
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=hssa --nocapture

docs:
	cp README.md docs/index.md
	cp -r figures docs/
	pycco hssa/*.py

foo:
	./foo.py

.PHONY: publish test docs diagrams
