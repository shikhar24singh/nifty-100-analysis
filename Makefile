load:
	python src/etl/loader.py

test:
	pytest

report:
	python report.py

dashboard:
	python dashboard.py

clean:
	rm -rf output/*