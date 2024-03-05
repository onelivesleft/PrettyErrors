.PHONY: test clean build

clean:
	# clean all temp runs
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info

build: clean
	python setup.py sdist bdist_wheel

upload: build
	#twine upload --repository-url https://test.pypi.org/legacy/ dist/*
	twine upload dist/*
