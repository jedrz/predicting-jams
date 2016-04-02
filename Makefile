init:
	pip install -r requirements.txt

test:
	py.test test_predicting_jams.py
