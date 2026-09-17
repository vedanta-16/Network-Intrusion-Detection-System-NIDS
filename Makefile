.PHONY: install data train test dashboard docker clean

install:
	pip install -r requirements.txt

data:
	python -m src.generate_sample_data --rows 10000 --attack-ratio 0.2

train:
	python -m src.train

test:
	pytest -v

dashboard:
	streamlit run dashboard/app.py

docker:
	docker compose up --build

clean:
	rm -rf logs/*.log logs/*.csv __pycache__ .pytest_cache
