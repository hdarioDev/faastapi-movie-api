from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field
from typing import List, Optional


app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(..., title="The title of the movie", min_length=1, max_length=100)
    overview: str = Field(..., title="The overview of the movie", min_length=1, max_length=500)
    year: int = Field(..., title="The year of the movie", ge=1900, le=2100)
    rating: float = Field(..., title="The rating of the movie", ge=0, le=10)
    category: str = Field(..., title="The category of the movie", min_length=1, max_length=50)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
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
def get_movies() -> List[Movie]:
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
    return movies

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1)) -> Movie:
    for movie in movies:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

@app.get('/movies/', tags=['Movies'], response_model=List[Movie])
def get_movies_by_year(year: int = Query( ge=1900, le=2100)) -> List[Movie]:
    filtered_movies = [item for item in movies if item.year == year]
    if not filtered_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found for the given year")
    return filtered_movies

@app.post('/movies', tags=['Movies'], response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(movie: Movie) -> Movie:
    movies.append(movie)
    return movie

@app.put('/movies/{id}', tags=['Movies'], response_model=Movie)
def update_movie(id: int, movie: Movie) -> Movie:
    for i, item in enumerate(movies):
        if item.id == id:
            movies[i] = movie
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

@app.delete('/movies/{id}', tags=['Movies'], response_model=Movie)
def delete_movie(id: int) -> Movie:
    for i, item in enumerate(movies):
        if item.id == id:
            movies.pop(i)
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

