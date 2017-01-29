init:
	pip install -r requirements.txt

install:
	python setup.py install

getData:
	if [ ! -d "data" ]; then git clone https://github.com/w4k2/data.git; rm -rf data/.git; fi

publish: test
	python setup.py sdist upload

test: getData
	clear
	nosetests --verbosity=2 --with-coverage -x --with-xunit -cover-erase --cover-package=hssa --nocapture

docs:
	pycco hssa/*.py

.PHONY: publish test docs
