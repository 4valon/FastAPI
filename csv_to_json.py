from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
from typing import List
import io

app = FastAPI()
csv_data = {}

@app.post("/csv_to_json/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return JSONResponse(status_code=400, content={"message": "File not found or is not .csv file."})
    else:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')), delimiter=',')
        csv_data[file.filename] = df.to_dict(orient="records")
        json_data = [df.to_dict(orient="list")]
        if file.filename in csv_data:
            return JSONResponse(content=json_data)
        else:
            return JSONResponse(status_code=500, content={"message": "Unidentified error occured. Please try again, or choose different file."})