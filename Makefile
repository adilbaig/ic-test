test:
	python3 -m unittest discover

run:
	python3 index.py --customers=customers.json --radius=100

run_loud:
	python3 index.py --customers=customers.json --radius=100 --debug