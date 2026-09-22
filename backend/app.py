"""
Головний веб-сервер та REST API для платформи ITCompass на FastAPI.
Підтримує автоматичну документацію Swagger за адресою: http://127.0.0.1:8000/docs
"""

import os
import json
import sqlite3
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, get_db_connection
from models import BookingCreate, BookingResponse, ProfessionItem, MentorItem, ReviewCreate, ReviewResponse

# Шлях до кореневої папки фронтенду D:\Web
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ініціалізація БД при старті сервера
    init_db()
    yield

app = FastAPI(
    title="ITCompass API",
    description="REST API для освітньої платформи ITCompass (довідник 16 професій, каталог менторів та букінг сесій).",
    version="1.0.0",
    lifespan=lifespan
)

# Налаштування CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------------
# 1. СТАТИЧНІ ФАЙЛИ ТА СТОРІНКИ ФРОНТЕНДУ
# ------------------------------------------------------------------------------
images_dir = os.path.join(BASE_DIR, "images")
css_dir = os.path.join(BASE_DIR, "css")
js_dir = os.path.join(BASE_DIR, "js")

if os.path.exists(images_dir):
    app.mount("/images", StaticFiles(directory=images_dir), name="images")
if os.path.exists(css_dir):
    app.mount("/css", StaticFiles(directory=css_dir), name="css")
if os.path.exists(js_dir):
    app.mount("/js", StaticFiles(directory=js_dir), name="js")

@app.get("/", summary="Головна сторінка сайту")
async def serve_index():
    index_path = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "ITCompass API працює. Відкрийте /docs для перегляду документації."}

@app.get("/professions.html", include_in_schema=False)
async def serve_professions():
    return FileResponse(os.path.join(BASE_DIR, "professions.html"))

@app.get("/profession-frontend.html", include_in_schema=False)
async def serve_profession_frontend():
    return FileResponse(os.path.join(BASE_DIR, "profession-frontend.html"))

@app.get("/mentors.html", include_in_schema=False)
async def serve_mentors_page():
    return FileResponse(os.path.join(BASE_DIR, "mentors.html"))

@app.get("/contacts.html", include_in_schema=False)
async def serve_contacts_page():
    return FileResponse(os.path.join(BASE_DIR, "contacts.html"))

# ------------------------------------------------------------------------------
# 2. REST API: СПЕЦІАЛЬНОСТІ ТА ДОКУМЕНТАЦІЯ (/api/professions)
# ------------------------------------------------------------------------------

@app.get("/api/professions", response_model=List[ProfessionItem], summary="Отримати список усіх 16 професій")
def get_professions(
    category: Optional[str] = Query(None, description="Фільтр за категорією: Software Engineering, QA, Data, Інфраструктура, Design, Management"),
    search: Optional[str] = Query(None, description="Пошук за ключовими словами або технологією")
):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM professions WHERE 1=1"
    params = []

    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR hard_skills LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard])

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(ProfessionItem(
            id=row["id"],
            slug=row["slug"],
            title=row["title"],
            category=row["category"],
            badge_class=row["badge_class"],
            description=row["description"],
            junior_duties=row["junior_duties"],
            middle_duties=row["middle_duties"],
            senior_duties=row["senior_duties"],
            hard_skills=json.loads(row["hard_skills"]),
            soft_skills=json.loads(row["soft_skills"]),
            docs=json.loads(row["docs_json"])
        ))
    return result

@app.get("/api/professions/{slug}", response_model=ProfessionItem, summary="Отримати деталі окремої професії")
def get_profession_by_slug(slug: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professions WHERE slug = ? OR id = ?", (slug, slug))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Спеціальність не знайдена")

    return ProfessionItem(
        id=row["id"],
        slug=row["slug"],
        title=row["title"],
        category=row["category"],
        badge_class=row["badge_class"],
        description=row["description"],
        junior_duties=row["junior_duties"],
        middle_duties=row["middle_duties"],
        senior_duties=row["senior_duties"],
        hard_skills=json.loads(row["hard_skills"]),
        soft_skills=json.loads(row["soft_skills"]),
        docs=json.loads(row["docs_json"])
    )

# ------------------------------------------------------------------------------
# 3. REST API: МЕНТОРИ (/api/mentors)
# ------------------------------------------------------------------------------

@app.get("/api/mentors", response_model=List[MentorItem], summary="Отримати список практикуючих менторів")
def get_mentors(tag: Optional[str] = Query(None, description="Фільтр за тегом технології (напр. React, Python)")):
    conn = get_db_connection()
    cursor = conn.cursor()

    if tag:
        cursor.execute("SELECT * FROM mentors WHERE tags LIKE ?", (f"%{tag}%",))
    else:
        cursor.execute("SELECT * FROM mentors")

    rows = cursor.fetchall()
    conn.close()

    result = []
    for row in rows:
        result.append(MentorItem(
            id=row["id"],
            slug=row["slug"],
            name=row["name"],
            title=row["title"],
            company=row["company"],
            experience_years=row["experience_years"],
            hourly_rate=row["hourly_rate"],
            tags=json.loads(row["tags"]),
            cases=row["cases"],
            initials=row["initials"],
            avatar_bg=row["avatar_bg"],
            avatar_color=row["avatar_color"]
        ))
    return result

@app.get("/api/mentors/{mentor_id}", response_model=MentorItem, summary="Отримати профіль ментора за ID")
def get_mentor_by_id(mentor_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mentors WHERE id = ?", (mentor_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Ментор не знайдений")

    return MentorItem(
        id=row["id"],
        slug=row["slug"],
        name=row["name"],
        title=row["title"],
        company=row["company"],
        experience_years=row["experience_years"],
        hourly_rate=row["hourly_rate"],
        tags=json.loads(row["tags"]),
        cases=row["cases"],
        initials=row["initials"],
        avatar_bg=row["avatar_bg"],
        avatar_color=row["avatar_color"]
    )

# ------------------------------------------------------------------------------
# 4. REST API: ЗАЯВКИ ТА БРОНЮВАННЯ (/api/bookings)
# ------------------------------------------------------------------------------

@app.post("/api/bookings", response_model=BookingResponse, status_code=status.HTTP_201_CREATED, summary="Створити нову заявку на консультацію")
def create_booking(booking: BookingCreate):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO bookings (user_name, user_email, user_phone, profession, session_type, user_message, status)
        VALUES (?, ?, ?, ?, ?, ?, 'pending')
        """, (
            booking.userName,
            str(booking.userEmail),
            booking.userPhone,
            booking.professionSelect,
            booking.sessionType,
            booking.userMessage
        ))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()

        return BookingResponse(
            success=True,
            booking_id=booking_id,
            message="Дякуємо! Вашу заявку успішно зареєстровано в базі даних. Ментор зв'яжеться з вами найближчим часом.",
            data={
                "name": booking.userName,
                "email": str(booking.userEmail),
                "profession": booking.professionSelect,
                "session_type": booking.sessionType,
                "status": "pending"
            }
        )
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(status_code=500, detail=f"Помилка при збереженні заявки: {str(e)}")

@app.get("/api/bookings", summary="Переглянути всі заброньовані консультації (Адмін-панель)")
def list_bookings(status_filter: Optional[str] = Query(None, description="Фільтр: pending, confirmed, completed, cancelled")):
    conn = get_db_connection()
    cursor = conn.cursor()

    if status_filter:
        cursor.execute("SELECT * FROM bookings WHERE status = ? ORDER BY created_at DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

@app.patch("/api/bookings/{booking_id}/status", summary="Оновити статус заявки")
def update_booking_status(booking_id: int, new_status: str = Query(..., regex="^(pending|confirmed|completed|cancelled)$")):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()

    if rows_affected == 0:
        raise HTTPException(status_code=404, detail="Заявку не знайдено")

    return {"success": True, "booking_id": booking_id, "new_status": new_status}

# ------------------------------------------------------------------------------
# 5. REST API: ВІДГУКИ (/api/reviews)
# ------------------------------------------------------------------------------

@app.post("/api/reviews", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Додати відгук про ментора")
def add_review(review: ReviewCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO reviews (mentor_id, author_name, rating, comment)
    VALUES (?, ?, ?, ?)
    """, (review.mentor_id, review.author_name, review.rating, review.comment))
    conn.commit()
    review_id = cursor.lastrowid
    conn.close()

    return {"success": True, "review_id": review_id, "message": "Відгук успішно опубліковано!"}

@app.get("/api/reviews/{mentor_id}", response_model=List[ReviewResponse], summary="Отримати всі відгуки для ментора")
def get_mentor_reviews(mentor_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reviews WHERE mentor_id = ? ORDER BY created_at DESC", (mentor_id,))
    rows = cursor.fetchall()
    conn.close()

    return [
        ReviewResponse(
            id=row["id"],
            created_at=str(row["created_at"]),
            author_name=row["author_name"],
            rating=row["rating"],
            comment=row["comment"]
        ) for row in rows
    ]

# ------------------------------------------------------------------------------
# 6. СИСТЕМНИЙ СТАТУС (HEALTH CHECK)
# ------------------------------------------------------------------------------
@app.get("/api/health", summary="Перевірка працездатності сервера та БД")
def health_check():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM professions")
    professions_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM mentors")
    mentors_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM bookings")
    bookings_count = cursor.fetchone()[0]
    conn.close()

    return {
        "status": "healthy",
        "service": "ITCompass Backend",
        "framework": "FastAPI",
        "database": "SQLite (itcompass.db)",
        "stats": {
            "professions_registered": professions_count,
            "mentors_registered": mentors_count,
            "bookings_total": bookings_count
        }
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Запуск сервера ITCompass на http://127.0.0.1:8000")
    print("📖 Swagger інтерактивна документація: http://127.0.0.1:8000/docs")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
