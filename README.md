# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire. :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

## Setup
Install Miniconda to create a virtual Python environment: https://conda.io/en/latest/miniconda.html
Open Anaconda prompt and navigate to the directory of the local repo and enter:

    conda create --name streamlit-example python=3.11

### Installation required packages
Install the required packages with the following command:

    pip install -r requirements.txt

### Configuration
For configuration package python-dotenv is used. That means that a local .env file can override the corresponding environment variable. See .env.example as a starting point. Configure "APP_CONFIG_KEY" via "Application Settings" in the Azure App Service

### Azure App Service
The workfow 'master_rbrands-streamlit-example.yml' shows how to setup a CI/CD pipeline for Azure App Service (without container). See https://benalexkeen.com/deploying-streamlit-applications-with-azure-app-services/ for details. Create a Linux App Service with Python (latest version) as runtime. In configuration/General settings set the Startup Commmand:
    
    python -m streamlit run streamlit_app.py --server.port 8000 --server.address 0.0.0.0

## Running the application
Open Anaconda prompt and navigate to the directory of the local repo and enter:
    conda activate streamlit-example

Run the application with the following command:

    streamlit run streamlit_app.py

The application will open in a webrowser window at http://localhost:8501/