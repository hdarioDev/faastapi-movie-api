from fastapi import FastAPI

app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}
