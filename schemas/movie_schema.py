from pydantic import BaseModel, Field
from typing import Optional

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
