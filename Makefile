build_release: sdist py3_bdist clean

sdist:
	python setup.py sdist

py3_bdist:
	python setup.py bdist_wheel

clean:
	-rm -rf build


.PHONY: build_release sdist py3_bdist clean
