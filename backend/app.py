"""
Головний веб-сервер та REST API для платформи ITCompass на Flask.
Підтримує роздачу фронтенду, REST API, SQLite та інтерактивну панель адміністратора за адресою /admin.
"""

import os
import sys
import json
import sqlite3

# Налаштування кодування для Windows консолі
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, io.UnsupportedOperation):
        pass

from flask import Flask, request, jsonify, send_from_directory, render_template_string, abort
from flask_cors import CORS

from database import init_db, get_db_connection, generate_meet_code

# Шлях до кореня фронтенду D:\Web
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Дозволяємо запити з будь-якого джерела

# Ініціалізація бази даних при запуску
with app.app_context():
    init_db()

# ------------------------------------------------------------------------------
# 1. РОЗДАЧА ФРОНТЕНДУ ТА СТАТИЧНИХ ФАЙЛІВ
# ------------------------------------------------------------------------------

@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/professions.html')
def serve_professions():
    return send_from_directory(BASE_DIR, 'professions.html')

@app.route('/profession-frontend.html')
def serve_profession_frontend():
    return send_from_directory(BASE_DIR, 'profession-frontend.html')

@app.route('/mentors.html')
def serve_mentors():
    return send_from_directory(BASE_DIR, 'mentors.html')

@app.route('/contacts.html')
def serve_contacts():
    return send_from_directory(BASE_DIR, 'contacts.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'js'), filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'images'), filename)

# ------------------------------------------------------------------------------
# 2. REST API: СПЕЦІАЛЬНОСТІ (/api/professions)
# ------------------------------------------------------------------------------

@app.route('/api/professions', methods=['GET'])
def get_professions():
    category = request.args.get('category')
    search = request.args.get('search')

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM professions WHERE 1=1"
    params = []

    if category and category != 'all':
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
        result.append({
            "id": row["id"],
            "slug": row["slug"],
            "title": row["title"],
            "category": row["category"],
            "badge_class": row["badge_class"],
            "description": row["description"],
            "junior_duties": row["junior_duties"],
            "middle_duties": row["middle_duties"],
            "senior_duties": row["senior_duties"],
            "hard_skills": json.loads(row["hard_skills"]),
            "soft_skills": json.loads(row["soft_skills"]),
            "docs": json.loads(row["docs_json"])
        })

    return jsonify(result), 200

@app.route('/api/professions/<slug>', methods=['GET'])
def get_profession(slug):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM professions WHERE slug = ? OR id = ?", (slug, slug))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Спеціальність не знайдена"}), 404

    return jsonify({
        "id": row["id"],
        "slug": row["slug"],
        "title": row["title"],
        "category": row["category"],
        "badge_class": row["badge_class"],
        "description": row["description"],
        "junior_duties": row["junior_duties"],
        "middle_duties": row["middle_duties"],
        "senior_duties": row["senior_duties"],
        "hard_skills": json.loads(row["hard_skills"]),
        "soft_skills": json.loads(row["soft_skills"]),
        "docs": json.loads(row["docs_json"])
    }), 200

# ------------------------------------------------------------------------------
# 3. REST API: МЕНТОРИ (/api/mentors)
# ------------------------------------------------------------------------------

@app.route('/api/mentors', methods=['GET'])
def get_mentors():
    tag = request.args.get('tag')
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
        result.append({
            "id": row["id"],
            "slug": row["slug"],
            "name": row["name"],
            "title": row["title"],
            "company": row["company"],
            "experience_years": row["experience_years"],
            "hourly_rate": row["hourly_rate"],
            "tags": json.loads(row["tags"]),
            "cases": row["cases"],
            "initials": row["initials"],
            "avatar_bg": row["avatar_bg"],
            "avatar_color": row["avatar_color"]
        })

    return jsonify(result), 200

@app.route('/api/mentors/<int:mentor_id>', methods=['GET'])
def get_mentor(mentor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mentors WHERE id = ?", (mentor_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Ментор не знайдений"}), 404

    return jsonify({
        "id": row["id"],
        "slug": row["slug"],
        "name": row["name"],
        "title": row["title"],
        "company": row["company"],
        "experience_years": row["experience_years"],
        "hourly_rate": row["hourly_rate"],
        "tags": json.loads(row["tags"]),
        "cases": row["cases"],
        "initials": row["initials"],
        "avatar_bg": row["avatar_bg"],
        "avatar_color": row["avatar_color"]
    }), 200

# ------------------------------------------------------------------------------
# 4. REST API: ЗАЯВКИ ТА БРОНЮВАННЯ (/api/bookings)
# ------------------------------------------------------------------------------

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json() or {}

    name = data.get('userName', '').strip()
    email = data.get('userEmail', '').strip()
    phone = data.get('userPhone', '').strip()
    profession = data.get('professionSelect', '').strip()
    session_type = data.get('sessionType', 'consultation').strip()
    message = data.get('userMessage', '').strip()

    if not name or not email or not profession:
        return jsonify({"error": "Обов'язкові поля: userName, userEmail, professionSelect"}), 400

    meet_url = generate_meet_code()

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO bookings (user_name, user_email, user_phone, profession, session_type, user_message, meet_url, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """, (name, email, phone, profession, session_type, message, meet_url))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()

        return jsonify({
            "success": True,
            "booking_id": booking_id,
            "message": "Заявку успішно зареєстровано в базі даних SQLite!",
            "meet_url": meet_url,
            "data": {
                "name": name,
                "email": email,
                "profession": profession,
                "session_type": session_type,
                "status": "pending"
            }
        }), 201
    except Exception as e:
        conn.rollback()
        conn.close()
        return jsonify({"error": f"Помилка бази даних: {str(e)}"}), 500

@app.route('/api/bookings', methods=['GET'])
def list_bookings():
    status_filter = request.args.get('status')
    conn = get_db_connection()
    cursor = conn.cursor()

    if status_filter:
        cursor.execute("SELECT * FROM bookings WHERE status = ? ORDER BY created_at DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")

    rows = cursor.fetchall()
    conn.close()

    return jsonify([dict(row) for row in rows]), 200

@app.route('/api/bookings/<int:booking_id>/status', methods=['PATCH', 'POST'])
def update_booking_status(booking_id):
    data = request.get_json() or {}
    new_status = data.get('status') or request.args.get('status')

    if new_status not in ['pending', 'confirmed', 'completed', 'cancelled']:
        return jsonify({"error": "Невалідний статус"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = ? WHERE id = ?", (new_status, booking_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()

    if affected == 0:
        return jsonify({"error": "Заявку не знайдено"}), 404

    return jsonify({"success": True, "booking_id": booking_id, "new_status": new_status}), 200

# ------------------------------------------------------------------------------
# 5. ВЕБ-ПАНЕЛЬ АДМІНІСТРАТОРА (/admin)
# ------------------------------------------------------------------------------

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="uk">
<head>
  <meta charset="UTF-8">
  <title>ITCompass — Панель адміністратора (Flask)</title>
  <link rel="icon" type="image/svg+xml" href="/images/favicon.svg">
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/style.css">
  <style>
    body { background-color: #0F172A; color: #F1F5F9; font-family: 'Inter', sans-serif; }
    .admin-container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
    .admin-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155; padding-bottom: 20px; margin-bottom: 25px; }
    .stat-card { background: #1E293B; border: 1px solid #334155; border-radius: 12px; padding: 20px; text-align: center; }
    .stat-number { font-family: 'JetBrains Mono', monospace; font-size: 2.2rem; font-weight: 700; color: #3B82F6; }
    .admin-table { width: 100%; border-collapse: collapse; margin-top: 20px; background: #1E293B; border-radius: 12px; overflow: hidden; border: 1px solid #334155; }
    .admin-table th, .admin-table td { padding: 14px 16px; border-bottom: 1px solid #334155; text-align: left; font-size: 0.95rem; }
    .admin-table th { background: #0B1329; color: #94A3B8; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.05em; }
    .admin-table tr:hover { background: #273549; }
    .badge-status { padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; }
    .status-pending { background: #FEF3C7; color: #92400E; }
    .status-confirmed { background: #D1FAE5; color: #065F46; }
    .status-completed { background: #DBEAFE; color: #1E40AF; }
    .status-cancelled { background: #FEE2E2; color: #991B1B; }
    .btn-action { padding: 4px 8px; font-size: 0.8rem; border-radius: 6px; cursor: pointer; border: none; font-weight: 600; }
    .btn-confirm { background: #10B981; color: white; }
    .btn-cancel { background: #EF4444; color: white; }
  </style>
</head>
<body>
  <div class="admin-container">
    <div class="admin-header">
      <div>
        <h1 style="color: #FFFFFF; font-size: 1.8rem; margin-bottom: 4px;">🛠 ITCompass — Панель адміністратора</h1>
        <p style="color: #94A3B8; margin-bottom: 0;">Керування заявками на консультації (Flask + SQLite itcompass.db)</p>
      </div>
      <div>
        <a href="/" class="btn btn-primary" target="_blank">🌐 Відкрити сайт &nearr;</a>
      </div>
    </div>

    <!-- Статистичні картки -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px;">
      <div class="stat-card">
        <div class="stat-number">{{ stats.total_professions }}</div>
        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">IT-спеціальностей</div>
      </div>
      <div class="stat-card">
        <div class="stat-number" style="color: #10B981;">{{ stats.total_mentors }}</div>
        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Менторів у базі</div>
      </div>
      <div class="stat-card">
        <div class="stat-number" style="color: #F59E0B;">{{ stats.total_bookings }}</div>
        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Всього заявок</div>
      </div>
      <div class="stat-card">
        <div class="stat-number" style="color: #A855F7;">{{ stats.pending_bookings }}</div>
        <div style="color: #94A3B8; font-size: 0.85rem; margin-top: 4px;">Очікують відповіді</div>
      </div>
    </div>

    <h2 style="color: #FFFFFF; font-size: 1.3rem;">📋 Останні заявки від студентів та новачків</h2>

    <table class="admin-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Час</th>
          <th>Студент</th>
          <th>Контакти</th>
          <th>Спеціальність</th>
          <th>Формат</th>
          <th>Google Meet</th>
          <th>Статус</th>
          <th>Дії</th>
        </tr>
      </thead>
      <tbody>
        {% for b in bookings %}
        <tr>
          <td style="font-family: monospace; color: #94A3B8;">#{{ b.id }}</td>
          <td style="font-size: 0.85rem; color: #94A3B8;">{{ b.created_at[:16] }}</td>
          <td><strong>{{ b.user_name }}</strong></td>
          <td style="font-size: 0.85rem;">
            {{ b.user_email }}<br>
            <span style="color: #94A3B8;">{{ b.user_phone or '—' }}</span>
          </td>
          <td><span class="tag" style="background:#334155; color:#F8FAFC;">{{ b.profession }}</span></td>
          <td style="font-size: 0.85rem;">{{ b.session_type }}</td>
          <td>
            {% if b.meet_url %}
              <a href="{{ b.meet_url }}" target="_blank" style="color: #38BDF8; font-size: 0.85rem;">Приєднатися &nearr;</a>
            {% else %}
              —
            {% endif %}
          </td>
          <td>
            <span class="badge-status status-{{ b.status }}">
              {{ b.status }}
            </span>
          </td>
          <td>
            <button class="btn-action btn-confirm" onclick="updateStatus({{ b.id }}, 'confirmed')">&check;</button>
            <button class="btn-action btn-cancel" onclick="updateStatus({{ b.id }}, 'cancelled')">&times;</button>
          </td>
        </tr>
        {% else %}
        <tr>
          <td colspan="9" style="text-align: center; color: #94A3B8; padding: 40px;">
            Поки що немає зареєстрованих заявок. Спробуйте заповнити форму на сторінці <a href="/contacts.html" target="_blank" style="color: #38BDF8;">Контакти</a>!
          </td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <script>
    async function updateStatus(id, newStatus) {
      const res = await fetch('/api/bookings/' + id + '/status', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({status: newStatus})
      });
      if (res.ok) {
        window.location.reload();
      } else {
        alert('Помилка оновлення статусу');
      }
    }
  </script>
</body>
</html>
"""

@app.route('/admin')
def admin_panel():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM bookings ORDER BY created_at DESC")
    bookings = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM professions")
    total_professions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM mentors")
    total_mentors = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings")
    total_bookings = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM bookings WHERE status = 'pending'")
    pending_bookings = cursor.fetchone()[0]

    conn.close()

    stats = {
        "total_professions": total_professions,
        "total_mentors": total_mentors,
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings
    }

    return render_template_string(ADMIN_HTML, bookings=bookings, stats=stats)

# ------------------------------------------------------------------------------
# 6. СТАТУС СЕРВЕРА
# ------------------------------------------------------------------------------

@app.route('/api/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "ITCompass Backend",
        "framework": "Python Flask",
        "database": "SQLite (itcompass.db)",
        "admin_url": "/admin"
    }), 200

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 [Flask Backend] Сервер ITCompass запущено успішно!")
    print("🌐 Головний сайт:                 http://127.0.0.1:5000/")
    print("🛠 Панель адміністратора:         http://127.0.0.1:5000/admin")
    print("📡 API професій:                  http://127.0.0.1:5000/api/professions")
    print("=" * 60)
    app.run(host='127.0.0.1', port=5000, debug=True)
