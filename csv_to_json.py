from fastapi import FastAPI, File, UploadFile
import csv

app = FastAPI()
error = "Wrong file extention."
error2 = "The file is empty or contains only headers."

@app.post("/csv_to_json")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        return error
    else:
        contents = await file.read()
        if not contents:
            return {}
        decode = contents.decode('utf-8')
        csv_reader = csv.reader(decode.splitlines(), delimiter=',')
        keys = next(csv_reader)
        json_content = {key: [] for key in keys}

        isRow = False
        Row = 0
        for row in csv_reader:
            isRow = True
            Row = Row + 1
            for key, value in zip(keys, row):
                json_content[key].append(value)
        if Row < 2:
            return {}
    
        return json_content