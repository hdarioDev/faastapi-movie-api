from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.security import HTTPBearer
from typing import List
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.movie_schema import Movie
from repositories.movie_repository import MovieRepository


movie_router = APIRouter()
http_bearer = HTTPBearer()

@movie_router.get('/movies', response_model=List[Movie], tags=['Movies'], dependencies=[Depends(http_bearer)], name="get_movies")
def get_movies(db: Session = Depends(get_db)) -> List[Movie]:
    movie_repository = MovieRepository(db)
    return movie_repository.get_all()

@movie_router.get('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)], name="get_movie")
def get_movie(id: int = Path(ge=1), db: Session = Depends(get_db)) -> Movie:
    movie_repository = MovieRepository(db)
    movie = movie_repository.get_by_id(id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    return movie

@movie_router.get('/movies/search', response_model=List[Movie], tags=['Movies'], dependencies=[Depends(http_bearer)], name="get_movies_by_year")
def get_movies_by_year(year: int = Query(ge=1900, le=2100), db: Session = Depends(get_db)) -> List[Movie]:
    movie_repository = MovieRepository(db)
    return movie_repository.get_by_year(year)

@movie_router.post('/movies', response_model=Movie, status_code=status.HTTP_201_CREATED, tags=['Movies'], dependencies=[Depends(http_bearer)], name="create_movie")
def create_movie(movie: Movie, db: Session = Depends(get_db)) -> Movie:
    movie_repository = MovieRepository(db)
    return movie_repository.create(movie)

@movie_router.put('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)], name="update_movie")
def update_movie(id: int, movie: Movie, db: Session = Depends(get_db)) -> Movie:
    movie_repository = MovieRepository(db)
    return movie_repository.update(id, movie)

@movie_router.delete('/movies/{id}', response_model=Movie, tags=['Movies'], dependencies=[Depends(http_bearer)], name="delete_movie")
def delete_movie(id: int, db: Session = Depends(get_db)) -> Movie:
    movie_repository = MovieRepository(db)
    return movie_repository.delete(id)
