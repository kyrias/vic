VIC_FILES = __init__.py main.py encrypt.py decrypt.py \
            ik.py checkerboard.py transposition.py message_indicator.py \
            util.py rotation.py arithmetic.py

FILES = $(addprefix vic/, $(VIC_FILES)) setup.py README.rst

build_release: sdist py3_bdist py2_bdist clean

sdist:
	python setup.py sdist

py3_bdist:
	python setup.py bdist_wheel

py2_bdist: 3to2
	python2 3to2/setup.py bdist_wheel


3to2: $(addprefix 3to2/, $(FILES))
	3to2 --write --nobackups --no-diffs 3to2/
	sed -i 's|häyhänen|hayhanen|' 3to2/setup.py

3to2/%:
	install -D $(shell sed 's|3to2/||' <<<$@) $@

clean:
	-rm -rf 3to2
	-rm -rf build


.PHONY: build_release sdist py3_bdist py2_bdist 3to2 clean
