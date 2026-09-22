"""
Pydantic моделі валідації запитів та відповідей REST API ITCompass.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any

class ProfessionItem(BaseModel):
    id: int
    slug: str
    title: str
    category: str
    badge_class: str
    description: str
    junior_duties: str
    middle_duties: str
    senior_duties: str
    hard_skills: List[str]
    soft_skills: List[str]
    docs: List[Dict[str, str]]

class MentorItem(BaseModel):
    id: int
    slug: str
    name: str
    title: str
    company: str
    experience_years: int
    hourly_rate: int
    tags: List[str]
    cases: str
    initials: str
    avatar_bg: str
    avatar_color: str

class BookingCreate(BaseModel):
    userName: str = Field(..., min_length=2, max_length=100, description="Ім'я користувача")
    userEmail: EmailStr = Field(..., description="Електронна пошта")
    userPhone: Optional[str] = Field(None, max_length=30, description="Номер телефону")
    professionSelect: str = Field(..., description="Обрана спеціальність")
    sessionType: Optional[str] = Field("consultation", description="Формат сесії")
    userMessage: Optional[str] = Field(None, max_length=1000, description="Опис запиту")
    userConsent: bool = Field(True, description="Згода на обробку даних")

class BookingResponse(BaseModel):
    success: bool
    booking_id: int
    message: str
    data: Dict[str, Any]

class ReviewCreate(BaseModel):
    mentor_id: int
    author_name: str = Field(..., min_length=2, max_length=80)
    rating: int = Field(..., ge=1, le=5)
    comment: str = Field(..., min_length=5, max_length=1000)

class ReviewResponse(BaseModel):
    id: int
    created_at: str
    author_name: str
    rating: int
    comment: str
