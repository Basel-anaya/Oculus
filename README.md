# Oculus travel Agent RAG System
A travel agent RAG System that uses Langchain and the Amadeus API within a Streamlit interface

## API Keys/.env file
Remember to create your .env file for your API keys as follows:

1. create a file `.env` in the same directory as `app.py`
2. This should contain all your API keys in the following format:
```
OPENAI_API_KEY=XXXXXXX
AMADEUS_CLIENT_ID=XXXXXXX
AMADEUS_CLIENT_SECRET=XXXXXXX
```
3. These automatically get loaded by dotenv in `app.py`


## Python Environment
Also contains the conda env dependency file: `requirements.txt`

To create the lightweight env using pipenv:

1. Copy my files to your directory or create a new branch
2. In VS Code (or terminal/shell/editor) cd to your new directory
2a. If not installed install pip and pipenv 
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
```
```
pip install pipenv
```
3. Create your new env: `pipenv install -r requirements.txt`
4. Activate env to run streamlit:  `pipenv shell`

Now with this env activated you should be able to run app.py as per the below.


## To Run streamlit.py App
To run use Terminal/Shell:

`streamlit run app.py`






