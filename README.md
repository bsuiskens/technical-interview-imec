# technical-interview-imec
A 4 hour technical exam for software developer at the SSTS team of Imec.


Installation:

Python3 is required to run this application.

You need to add a .env file with the following lines

DATABASE_URL=sqlite:///./app.db
DATABASE_TEST_URL=sqlite:///./test.db
SEED_DATA_PATH=app/data/Company_A_database.xlsx

The required packages can be installed with the command:

pip install pandas openpyxl sqlalchemy fastapi uvicorn python-dotenv python-multipart pytest httpx

The application can be started with the command:

uvicorn app.main:app --reload

you can run the test suite with:

pytest

Troubleshooting:

if the pip or uvicorn command is giving an error, it's possible you need to use a virtual env within visual studio code:

python -m venv .venv 
.venv\Scripts\activate 