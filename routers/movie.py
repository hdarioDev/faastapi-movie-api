from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import HTTPBearer
from typing import List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from config.database import get_db
from models.movie import Movie as MovieModel


movie_router = APIRouter()
http_bearer = HTTPBearer()

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

@movie_router.get('/movies', response_model=List[Movie], tags=['Movies'], dependencies=[Depends(http_bearer)])
def get_movies(db: Session = Depends(get_db)) -> List[Movie]:
    movies = db.query(MovieModel).all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
    return movies

@movie_router.get('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)])
def get_movie(id: int = Path(ge=1), db: Session = Depends(get_db)) -> Movie:
    fmovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if fmovie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return fmovie

@movie_router.get('/movies/', response_model=List[Movie], tags=['Movies'], dependencies=[Depends(http_bearer)])
def get_movies_by_year(year: int = Query(ge=1900, le=2100), db: Session = Depends(get_db)) -> List[Movie]:
    movies = db.query(MovieModel).filter(MovieModel.year == year).all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found for the given year")
    return movies

@movie_router.post('/movies', response_model=Movie, status_code=status.HTTP_201_CREATED, tags=['Movies'], dependencies=[Depends(http_bearer)])
def create_movie(movie: Movie, db: Session = Depends(get_db)) -> Movie:
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return movie

@movie_router.put('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)])
def update_movie(id: int, movie: Movie, db: Session = Depends(get_db)) -> Movie:
    fmovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if fmovie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    for key, value in movie.dict().items():
        setattr(fmovie, key, value)
    db.commit()
    return movie

@movie_router.delete('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)])
def delete_movie(id: int, db: Session = Depends(get_db)) -> Movie:
    fmovie = db.query(MovieModel).filter(MovieModel.id == id).first()
    if fmovie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    db.delete(fmovie)
    db.commit()
    return fmovie
