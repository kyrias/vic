FILES = encrypt.py decrypt.py ik.py checkerboard.py transposition.py message_indicator.py util.py rotation.py

3to2: $(addprefix 3to2/, $(FILES))

3to2/%.py:
	-mkdir 3to2
	cp $(@F) 3to2/
	3to2 --write --nobackups --no-diffs $@

clean:
	-rm -rf 3to2

.PHONY: clean
