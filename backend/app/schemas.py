# backend/app/schemas.py

from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl

class SummaryResponse(BaseModel):
    summary: str
    key_points: list[str]
