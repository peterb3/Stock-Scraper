Utilizes a web scraper to obtain pertinent Stock ticker data from Yahoo Finance, then, using the FastAPI framework, turns the scraper into a REST API that is deliverable to front end frameworks in JSON file format.

To start the server, run this command in terminal:
uvicorn main:app --reload

To get data from the app, route to the endpoint:
https://localhost:8000/v1/{symbol}/summary

Symbol represents a company stock ticker, such as AAPL for Apple inc.
