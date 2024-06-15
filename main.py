from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {
                "id": 3,
                "title": "Inception",
                "overview": "A thief who steals corporate secrets through the use of dream-sharing technology...",
                "year": 2010,
                "rating": 8.8,
                "category": "Sci-Fi"
            }
        }

movies = [
    Movie(id=1, title="The Shawshank Redemption", overview="lorem ipsum dolor sit amet ... ", year=1994, rating=9.3, category="Drama"),
    Movie(id=2, title="The Godfather", overview="lorem ipsum dolor sit amet ... ", year=1972, rating=9.2, category="Crime"),
]


@app.get("/", tags=["Root"])
def read_root():
    return {"Hello": "World"}

@app.get('/movies', tags=['Movies'], response_model=List[Movie])
def get_movies():
    return movies

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int):
    for movie in movies:
        if movie.id == id:
            return movie
    return []

@app.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_year(year: int):
    return [item for item in movies if item.year == year]

@app.post('/movies', tags=['Movies'], response_model=Movie)
def create_movie(movie: Movie):
    movies.append(movie)
    return movie

@app.put('/movies/{id}', tags=['Movies'], response_model=Movie)
def update_movie(id: int, movie: Movie):
    for i, item in enumerate(movies):
        if item.id == id:
            movies[i] = movie
            return movie
    return {}

@app.delete('/movies/{id}', tags=['Movies'], response_model=Movie)
def delete_movie(id: int):
    for i, item in enumerate(movies):
        if item.id == id:
            movies.pop(i)
            return item
    return {}