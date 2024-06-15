from fastapi import FastAPI

app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

movies = [
    {
        "id": 1,
        "title": "The Shawshank Redemption",
        "overview": "lorem ipsum dolor sit amet ... ",
        "year": 1994,
        "rating": 9.3,
        "category": "Drama"
    },
    {
        "id": 2,
        "title": "The Godfather",
        "overview": "lorem ipsum dolor sit amet ... ",
        "year": 1972,
        "rating": 9.2,
        "category": "Crime"
    },
]

@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}

@app.get('/movies', tags=['Movies'])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'])
def get_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            return movie
    return []

@app.get('/movies/', tags=['Movies'])
def get_movies_by_year(year: int):
    return [item for item in movies if item['year'] == year]
