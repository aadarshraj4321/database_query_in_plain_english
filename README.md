# AI Powered Catalog Navigator
This project is an intelligent assistant that allows users to search a product catalog using natural language queries. It translates plain English questions into MongoDB database queries and displays the results through a simple web interface.
Features

**Natural Language Understanding**: Parses queries for categories, brands, prices, and ratings.
**MongoDB Integration**: Dynamically generates and executes queries against a MongoDB database.
**Web Interface**: A clean, user-friendly UI to enter queries and view results.
**REST API**: A Flask-based API for programmatic access and easy integration.

## Tech Stack
**Backend**: Python, Flask
**Database**: MongoDB (via MongoDB Atlas)

**NLU Library**: spaCy

**Frontend**: HTML, CSS, vanilla JavaScript

# How to Run Locally
### Prerequisites:
    Python 3.8+
    MongoDB database (local or a free Atlas cluster)
    Clone the Repository (or download the files):
    code
```bash
git clone <your-repo-url>
cd catalog-navigator
```
#### Create and Activate a Virtual Environment:

```bash
python3 -m venv venv
source venv/bin/activate
```
#### On Windows, use: venv\Scripts\activate
**Install Dependencies**:

```bash
pip install -r requirements.txt
```
#### Download the NLP Model:
```bash
python -m spacy download en_core_web_sm
```

#### Load the Sample Data:

```bash
Update the MONGO_URI in load_data.py with your database connection string.
Run the script to populate the database:

python load_data.py
Run the Application:
Make sure the MONGO_URI in app.py is also set to your connection string.
Start the Flask server:

python app.py
Access the Web Interface:
Open your web browser and navigate to http://127.0.0.1:8080 (or the port specified in the terminal).
How to Use
Simply open the web interface, type a query into the search box, and press "Search".
Example Queries:
show me all electronics
find products from Innovate AI Co.
show me products with a price under 300
find electronics with a rating above 4.5
Project Structure
```
```bash
/catalog-navigator
|
|-- app.py              
|-- load_data.py   
|-- requirements.txt    
|
|-- /modules
|   |-- __init__.py
|   |-- nlu.py         
|   |-- query_builder.py# MongoDB query generation logic
|
|-- /templates
    |-- index.html     


```