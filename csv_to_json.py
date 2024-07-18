from fastapi import FastAPI, File, UploadFile
import csv

app = FastAPI()
error = "Wrong file extention."

@app.post("/csv_to_json/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return error
    else:
        contents = await file.read()
        decode = contents.decode('utf-8')
        csv_reader = csv.reader(decode.splitlines(), delimiter=',')
        keys = next(csv_reader)
        json_content = {key: [] for key in keys}

        for row in csv_reader:
            for key, value in zip(keys, row):
                json_content[key].append(value)
    
        return json_content