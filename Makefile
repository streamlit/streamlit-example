create-env:
	conda env create -f local_dev/environment.yml

run-app:
	python -m streamlit run streamlit_app.py