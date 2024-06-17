from fastapi import Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Optional
from config.database import engine, Base


from model import User
from utils import create_token, decode_token
from models.movie import Movie as MovieModel


app = FastAPI()
app.title = "My API"
app.description = "This is a fantastic API"
app.version = "1.0.0"

http_bearer = HTTPBearer()

Base.metadata.create_all(bind=engine)


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


@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token({"sub": user.email})
        return JSONResponse(status_code=200, content={"access_token": token, "token_type": "bearer"})
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email o contraseña incorrectos")

@app.get("/users/me", tags=["users"])
def read_users_me(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = credentials.credentials
    decoded_token = decode_token(token)
    if decoded_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"email": decoded_token["sub"]}

@app.get('/movies', tags=['Movies'], response_model=List[Movie], dependencies=[Depends(http_bearer)])
def get_movies() -> List[Movie]:
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found")
    return movies

@app.get('/movies/{id}', tags=['Movies'], response_model=Movie, dependencies=[Depends(http_bearer)])
def get_movie(id: int = Path(ge=1)) -> Movie:
    for movie in movies:
        if movie.id == id:
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

@app.get('/movies/', tags=['Movies'], response_model=List[Movie], dependencies=[Depends(http_bearer)])
def get_movies_by_year(year: int = Query( ge=1900, le=2100)) -> List[Movie]:
    filtered_movies = [item for item in movies if item.year == year]
    if not filtered_movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found for the given year")
    return filtered_movies

@app.post('/movies', tags=['Movies'], response_model=Movie, status_code=status.HTTP_201_CREATED, dependencies=[Depends(http_bearer)])
def create_movie(movie: Movie) -> Movie:
    movies.append(movie)
    return movie

@app.put('/movies/{id}', tags=['Movies'], response_model=Movie, dependencies=[Depends(http_bearer)])
def update_movie(id: int, movie: Movie) -> Movie:
    for i, item in enumerate(movies):
        if item.id == id:
            movies[i] = movie
            return movie
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

@app.delete('/movies/{id}', tags=['Movies'], response_model=Movie, dependencies=[Depends(http_bearer)])
def delete_movie(id: int) -> Movie:
    for i, item in enumerate(movies):
        if item.id == id:
            movies.pop(i)
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

