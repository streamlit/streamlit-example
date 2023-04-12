create-env:
	conda env create -f local_dev/environment.yml

run-app:
	conda run -n driftmlpapp streamlit streamlit_app.py