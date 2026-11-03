# MP2 – Data Processing REST API

## About the Project

For MP2, I built a REST API using Python and FastAPI that allows users to upload CSV files, validate their data, and clean datasets based on different settings.

The goal of this project was to practice building API endpoints and connecting them to a data-processing pipeline. I also worked with Pydantic models, error handling, logging, and automated testing.

## What My API Does

The API allows users to:

- Upload CSV files and store them with a dataset ID.
- Check whether a dataset contains required columns.
- Validate numeric columns.
- Remove duplicate rows.
- Handle missing values based on the selected settings.
- Configure outlier processing.
- Receive a report showing the results of data processing.

I also added middleware to track requests, record their response status codes, and measure how long they take.

## Running the Project

First, create and activate a Python virtual environment.

Then install the project dependencies:

`python -m pip install -r requirements.txt`

To start the API, run:

`python -m uvicorn main:app --reload`

Once the server is running, open:

`http://127.0.0.1:8000/docs`

This opens FastAPI's interactive documentation, where the endpoints can be tested.

## Main API Endpoints

**GET /health**

Checks whether the API is running.

**POST /upload**

Allows a user to upload a CSV file. The API reads the file, stores the dataset, and returns information such as the dataset ID, filename, number of rows, and column names.

**POST /datasets/{dataset_id}/process**

Processes an uploaded dataset using the settings provided in the request body. This includes validation and the selected cleaning operations.

## Testing

I used pytest and FastAPI's TestClient to test the API.

The tests I added check whether:

- The health endpoint responds correctly.
- A valid CSV file can be uploaded.
- An unsupported file type is rejected.
- A request for a dataset that does not exist returns a 404 error.

To run the tests:

`python -m pytest -q`

All four of these tests passed during my local testing.

## What I Learned

Through this project, I gained more experience working with FastAPI, Pydantic, pandas, and API endpoints. I also learned how middleware can be used to record information about requests without repeating the same code across different endpoints.

One of the most useful parts of this project was connecting the API to the data-processing functions and testing how the application responds to different inputs and errors.

## Tools Used

- Python
- FastAPI
- Pydantic
- pandas
- pytest
- Uvicorn