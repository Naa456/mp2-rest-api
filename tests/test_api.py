
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


#2nd test for the upload endpoint

def test_upload_valid_csv():
    csv_data = b"student_id,score\n1,90\n2,80\n"

    response = client.post(
        "/upload",
        files={"file": ("sample.csv", csv_data, "text/csv")}
    )

    assert response.status_code == 200
    assert response.json()["rows"] == 2


def test_upload_invalid_file():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"hello", "text/plain")}
    )

    assert response.status_code == 400


def test_process_missing_dataset():
    response = client.post(
        "/datasets/999/process",
        json={
            "validation": {
                "required_columns": ["score"],
                "numeric_columns": ["score"]
            },
            "processing": {
                "remove_duplicates": True,
                "missing": {
                    "enabled": True,
                    "axis": "rows"
                },
                "outliers": {
                    "enabled": False,
                    "columns": []
                }
            }
        }
    )

    assert response.status_code == 404
