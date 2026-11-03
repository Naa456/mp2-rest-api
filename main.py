#to load virtual environment, do 
#  .\venv\Scripts\python.exe -m uvicorn main:app --reload
#if virtual already activated, just run python -m uvicorn main:app --reload
# this is the link/local address to access the API documentation: : http://127.0.0.1:8000/docs
#this is to run some test(automated test that checks whether other parts of our code behave correctly)
#to run tests, use: pytest : .\venv\Scripts\python.exe -m pytest -q
import io
import json
import logging
from pathlib import Path
import time
import uuid
from fastapi import Request

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from src import DatasetInfo, DatasetStorage, HealthResponse, setup_logging, ProcessConfig, ProcessingReport
from data_pipeline import (
    validate_dataframe,
    process_data,
    create_cleaning_report
)

setup_logging(verbose=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Processing API", version="1.0.0")
storage = DatasetStorage()

@app.middleware("http")
async def log_requests(request: Request, call_next):

    request_id = uuid.uuid4().hex[:8]
    start = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start

    logger.info(
        f"ID={request_id} "
        f"Status={response.status_code} "
        f"Duration={duration:.3f}s"
    )

    response.headers["X-Request-ID"] = request_id

    return response



@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the application status and version."""
    return {"status": "ok", "version": "1.0.0"}


@app.post("/upload", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    """Read and store a CSV upload."""
    extension = Path(file.filename or "").suffix.lower()

    if extension != ".csv":
        logger.warning("Unsupported file format: %s", extension)
        raise HTTPException(status_code=400, detail="Only CSV files are supported")

    contents = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as e:
        logger.warning("Invalid CSV upload: %s", e)
        raise HTTPException(status_code=400, detail="Unable to read the CSV file")

    dataset_id = storage.save(df, file.filename)
    logger.info(
        "Uploaded dataset: id=%s, filename=%s, rows=%s",
        dataset_id,
        file.filename,
        len(df),
    )
    return storage.get_metadata(dataset_id)


@app.post(
    "/datasets/{dataset_id}/process",
    response_model=ProcessingReport
)
def process_dataset(dataset_id: int, config: ProcessConfig):
    df = storage.get(dataset_id)

    if df is None:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    config_dict = config.model_dump()

    for column in config.validation.numeric_columns:
        if column not in df.columns:
            raise HTTPException(
                status_code=400,
                detail=f"Numeric column '{column}' not found"
            )

    try:
        validated_df = validate_dataframe(
            df,
            config.validation.required_columns,
            config.validation.numeric_columns
        )

        validation_rows_removed = len(df) - len(validated_df)
        before_processing = validated_df.copy()

        processed_df = process_data(
            validated_df,
            config_dict
        )

        cleaning_report = create_cleaning_report(
            before_processing,
            processed_df
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
    return {
        "id": dataset_id,
        "validation_rows_removed": validation_rows_removed,
        "cleaning_report": cleaning_report
    }