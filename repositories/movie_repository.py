import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from models.movie import Movie as MovieModel
from schemas.movie_schema import Movie
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class MovieRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_all(self) -> List[MovieModel]:
        logger.info("Getting all movies.")
        return self._session.query(MovieModel).all()

    def get_by_id(self, movie_id: int) -> Optional[MovieModel]:
        logger.info("Getting movie by id.", extra=dict(movie_id=movie_id))
        return self._session.query(MovieModel).filter(MovieModel.id == movie_id).one_or_none()

    def get_by_year(self, year: int) -> List[MovieModel]:
        logger.info("Getting movies by year.", extra=dict(year=year))
        return self._session.query(MovieModel).filter(MovieModel.year == year).all()

    def create(self, movie_data: Movie) -> MovieModel:
        logger.info("Creating a new movie.")
        new_movie = MovieModel(**movie_data.dict())
        self._session.add(new_movie)
        self._session.commit()
        self._session.refresh(new_movie)
        return new_movie

    def update(self, movie_id: int, movie_data: Movie) -> MovieModel:
        logger.info("Updating movie.", extra=dict(movie_id=movie_id))
        movie = self.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        for key, value in movie_data.dict().items():
            setattr(movie, key, value)
        self._session.commit()
        self._session.refresh(movie)
        return movie

    def delete(self, movie_id: int) -> MovieModel:
        logger.info("Deleting movie.", extra=dict(movie_id=movie_id))
        movie = self.get_by_id(movie_id)
        if movie is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
        self._session.delete(movie)
        self._session.commit()
        return movie
