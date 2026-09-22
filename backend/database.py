"""
База даних SQLite для проєкту ITCompass.
Створює таблиці та заповнює початковими даними (16 спеціальностей, ментори).
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "itcompass.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Таблиця професій
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS professions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        badge_class TEXT NOT NULL,
        description TEXT NOT NULL,
        junior_duties TEXT NOT NULL,
        middle_duties TEXT NOT NULL,
        senior_duties TEXT NOT NULL,
        hard_skills TEXT NOT NULL,
        soft_skills TEXT NOT NULL,
        docs_json TEXT NOT NULL
    )
    """)

    # 2. Таблиця менторів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mentors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        slug TEXT NOT NULL,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        experience_years INTEGER NOT NULL,
        hourly_rate INTEGER NOT NULL,
        tags TEXT NOT NULL,
        cases TEXT NOT NULL,
        initials TEXT NOT NULL,
        avatar_bg TEXT NOT NULL,
        avatar_color TEXT NOT NULL
    )
    """)

    # 3. Таблиця заявок / бронювань консультацій
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_name TEXT NOT NULL,
        user_email TEXT NOT NULL,
        user_phone TEXT,
        profession TEXT NOT NULL,
        session_type TEXT NOT NULL,
        user_message TEXT,
        status TEXT DEFAULT 'pending'
    )
    """)

    # 4. Таблиця відгуків
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        mentor_id INTEGER,
        author_name TEXT NOT NULL,
        rating INTEGER NOT NULL,
        comment TEXT NOT NULL,
        FOREIGN KEY (mentor_id) REFERENCES mentors (id)
    )
    """)

    conn.commit()

    # Перевіряємо, чи є вже дані про спеціальності
    cursor.execute("SELECT COUNT(*) FROM professions")
    count = cursor.fetchone()[0]

    if count == 0:
        seed_professions(cursor)
        seed_mentors(cursor)
        conn.commit()
        print("✅ Базу даних успішно ініціалізовано та заповнено початковими даними!")
    else:
        print("ℹ️ База даних вже містить записи.")

    conn.close()

def seed_professions(cursor):
    professions_list = [
        (
            "frontend",
            "1. Frontend Developer (React/Vue)",
            "Software Engineering",
            "badge-dev",
            "Створення клієнтської частини сайтів та інтерактивних веб-додатків. Фахівець відповідає за швидкість завантаження, адаптивність та візуальну зручність інтерфейсу.",
            "Адаптивна верстка за макетами Figma (HTML5/CSS3), базова асинхронна логіка на JavaScript, робота з готовими REST API.",
            "Розробка SPA на React/Next.js/Vue, оптимізація продуктивності (Web Vitals), тестування компонентів (Jest/Playwright).",
            "Проєктування архітектури фронтенду, дизайн-систем, налаштування CI/CD пайплайнів, менторинг команди.",
            json.dumps(["HTML5 / CSS3 / Flexbox / Grid", "JavaScript (ES6+) & TypeScript", "React 19 / Vue.js / Next.js", "Tailwind CSS, Vite, Git"]),
            json.dumps(["Командна взаємодія (Scrum)", "Культура Code Review", "Увага до деталей (Pixel-Perfect)"]),
            json.dumps([
                {"name": "MDN Web Docs (Mozilla)", "url": "https://developer.mozilla.org/uk/docs/Web/HTML"},
                {"name": "React.dev — Офіційна документація", "url": "https://react.dev/"},
                {"name": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/"}
            ])
        ),
        (
            "backend",
            "2. Backend Developer (Node.js/Python/Java/Go)",
            "Software Engineering",
            "badge-dev",
            "Проєктування серверної архітектури, створення надійних REST/GraphQL/gRPC сервісів, робота з реляційними та NoSQL базами даних.",
            "Написання CRUD операцій, створення контролерів і маршрутів, написання простих SQL-запитів, документування API у Swagger.",
            "Проєктування схем баз даних, оптимізація складних SQL-запитів, робота з чергами повідомлень (RabbitMQ, Redis, Kafka).",
            "Мікросервісна архітектура, балансування навантаження, відмовостійкість систем, захист від DDoS та ін'єкцій.",
            json.dumps(["Node.js / Python (FastAPI/Django) / Go", "PostgreSQL, MySQL, Redis", "Docker, REST API, GraphQL", "Git, Linux базові команди"]),
            json.dumps(["Аналітичне мислення", "Вміння аргументувати архітектурні рішення", "Тайм-менеджмент"]),
            json.dumps([
                {"name": "Node.js Official Documentation", "url": "https://nodejs.org/docs/latest/api/"},
                {"name": "Python Docs", "url": "https://docs.python.org/3/"},
                {"name": "PostgreSQL Documentation", "url": "https://www.postgresql.org/docs/"}
            ])
        ),
        (
            "fullstack",
            "3. Fullstack Developer",
            "Software Engineering",
            "badge-dev",
            "Універсальний спеціаліст широкого профілю, який здатний самостійно створити готовий веб-сервіс від інтерфейсу користувача до сервера та бази даних.",
            "Розробка невеликих модулів фронтенду та підключення до власних ендпоінтів бекенду.",
            "Повний цикл розробки фічі (Full feature ownership): база даних + API + UI-компоненти.",
            "Вибір технологічного стеку для нових продуктів, оптимізація взаємодії клієнт-сервер.",
            json.dumps(["TypeScript на фронтенді та бекенді", "Next.js / NestJS / Express", "PostgreSQL / Prisma ORM", "Docker, Nginx"]),
            json.dumps(["Гнучкість мислення", "Самостійність у вирішенні комплексних задач"]),
            json.dumps([
                {"name": "Next.js Documentation", "url": "https://nextjs.org/docs"},
                {"name": "Prisma ORM Guide", "url": "https://www.prisma.io/docs"}
            ])
        ),
        (
            "mobile",
            "4. Mobile Developer (iOS / Android / Flutter)",
            "Software Engineering",
            "badge-dev",
            "Створення нативних та кросплатформних застосунків для смартфонів і планшетів на базі iOS та Android.",
            "Верстка мобільних екранів за дизайн-макетами, інтеграція з REST API, збереження локальних даних.",
            "Керування життєвим циклом екранів, робота з Push-сповіщеннями, офлайн-режим, анімації.",
            "Оптимізація пам'яті та енергоспоживання додатку, публікація в App Store та Google Play.",
            json.dumps(["Flutter & Dart / Swift (iOS) / Kotlin (Android)", "REST API, WebSocket", "SQLite / Room / CoreData"]),
            json.dumps(["Розуміння Human Interface Guidelines та Material Design", "Емпатія до користувача"]),
            json.dumps([
                {"name": "Flutter Official Docs", "url": "https://docs.flutter.dev/"},
                {"name": "Apple Developer Documentation", "url": "https://developer.apple.com/documentation/"}
            ])
        ),
        (
            "qa_manual",
            "5. Manual Testing Engineer",
            "Тестування ПЗ (QA)",
            "badge-qa",
            "Контроль якості програмного забезпечення, виявлення розбіжностей між очікуваною та фактичною поведінкою системи вручну.",
            "Проходження готових тест-кейсів, складання зрозумілих баг-репортів у Jira, димне тестування (Smoke testing).",
            "Складання тест-планів, матриці трасування вимог, тестування REST API через Postman, перевірка баз даних за допомогою SQL.",
            "Побудова QA-стратегії проєкту, управління релізами, аналіз ризиків якості.",
            json.dumps(["Теорія тестування (ISTQB)", "Postman, Swagger", "Базові SQL-запити (SELECT, JOIN)", "Jira, TestRail"]),
            json.dumps(["Уважність до дрібниць", "Критичне мислення", "Грамотна письмова фіксація багів"]),
            json.dumps([
                {"name": "ISTQB Glossary & Syllabus", "url": "https://www.istqb.org/"},
                {"name": "Postman Learning Center", "url": "https://learning.postman.com/"}
            ])
        ),
        (
            "qa_auto",
            "6. Test Automation Engineer (Python/Java/JS)",
            "Тестування ПЗ (QA)",
            "badge-qa",
            "Розробка автотестів для UI та API, побудова тестових фреймворків, які виконуються автоматично при кожному оновленні коду в CI/CD.",
            "Написання та підтримка автотестів за готовим шаблоном фреймворку, локалізація причин падіння тестів.",
            "Створення та розширення тест-фреймворків (Page Object Model), автоматизація API та E2E сценаріїв.",
            "Інтеграція автотестів у CI/CD пайплайни, оптимізація швидкості виконання, паралелізація тестів.",
            json.dumps(["Python / Java / TypeScript", "Playwright, Selenium WebDriver", "PyTest / JUnit", "Git, Docker, CI/CD"]),
            json.dumps(["Інженерний підхід", "Системне бачення архітектури тестування"]),
            json.dumps([
                {"name": "Playwright Documentation", "url": "https://playwright.dev/"},
                {"name": "Selenium Dev Guide", "url": "https://www.selenium.dev/documentation/"}
            ])
        ),
        (
            "data_analyst",
            "7. Data Analyst",
            "Data, AI and ML",
            "badge-data",
            "Збір, очищення та дослідження цифрових показників компанії, побудова інформативних дашбордів для прийняття бізнес-рішень.",
            "Вивантаження даних з баз через SQL, побудова базових звітів у Excel/Google Sheets, візуалізація метрик.",
            "Розробка інтерактивних дашбордів у Tableau/PowerBI, аналіз когорт і продуктових воронок, перевірка A/B тестів.",
            "Побудова системи продуктової та маркетингової аналітики, формування стратегічних бізнес-висновків.",
            json.dumps(["SQL (Window functions, CTE, агрегати)", "Tableau, PowerBI", "Python (Pandas, NumPy, Matplotlib)", "Математична статистика"]),
            json.dumps(["Вміння презентувати цифри нетехнічній аудиторії (Storytelling with data)"]),
            json.dumps([
                {"name": "PostgreSQL Tutorial for Data Analysis", "url": "https://www.postgresqltutorial.com/"},
                {"name": "Pandas Documentation", "url": "https://pandas.pydata.org/docs/"}
            ])
        ),
        (
            "data_scientist",
            "8. Data Scientist",
            "Data, AI and ML",
            "badge-data",
            "Створення прогнозних моделей машинного навчання, виявлення прихованих закономірностей у великих масивах інформації.",
            "Розвідувальний аналіз даних (EDA), підготовка ознак (Feature Engineering), навчання базових моделей класифікації/регресії.",
            "Тюнінг гіперпараметрів, оцінка якості моделей (ROC-AUC, F1-score), робота з градієнтним бустингом (XGBoost, LightGBM).",
            "Науково-дослідна діяльність (R&D), розробка кастомних алгоритмів, впровадження ML у бізнес-процеси.",
            json.dumps(["Python, Scikit-learn, XGBoost", "Лінійна алгебра, теорія ймовірностей", "Jupyter, Git, SQL"]),
            json.dumps(["Наукова допитливість", "Стійкість до експериментів із непередбачуваним результатом"]),
            json.dumps([
                {"name": "Scikit-learn Documentation", "url": "https://scikit-learn.org/stable/"},
                {"name": "Kaggle Learn Courses", "url": "https://www.kaggle.com/learn"}
            ])
        ),
        (
            "ml_ai",
            "9. Machine Learning / AI Engineer",
            "Data, AI and ML",
            "badge-data",
            "Навчання, оптимізація та інтеграція складних нейромереж (Computer Vision, NLP, LLM) у робочі продукти (Production ML / MLOps).",
            "Підготовка датасетів, донавчання (Fine-tuning) відкритих моделей нейромереж, написання API для інференсу.",
            "Оптимізація швидкодії моделей (Quantization, ONNX), розгортання в хмарі, моніторинг деградації даних.",
            "Архітектура генеративного ШІ (RAG-системи, агенти), керування розподіленим навчанням на GPU-кластерах.",
            json.dumps(["PyTorch, Transformers (Hugging Face)", "MLOps (MLflow, Docker, Triton)", "Python, CUDA basics, LangChain"]),
            json.dumps(["Швидка адаптація до нових досліджень у сфері ШІ"]),
            json.dumps([
                {"name": "PyTorch Documentation", "url": "https://pytorch.org/docs/stable/index.html"},
                {"name": "Hugging Face Guides", "url": "https://huggingface.co/docs"}
            ])
        ),
        (
            "data_engineer",
            "10. Data Engineer",
            "Data, AI and ML",
            "badge-data",
            "Проєктування та підтримка інфраструктури збору, трансформації та надійного зберігання терабайтів даних (ETL/ELT конвеєри, DWH).",
            "Підтримка існуючих конвеєрів перекачування даних, написання SQL скриптів трансформації.",
            "Розробка ETL пайплайнів у Apache Airflow, обробка потокових даних у Apache Kafka, оптимізація схем DWH.",
            "Проєктування озер даних (Data Lake) та хмарних сховищ (Snowflake, BigQuery, ClickHouse), надійність і безпека даних.",
            json.dumps(["SQL Advanced, Python", "Apache Spark, Airflow, Kafka", "ClickHouse / BigQuery / Snowflake", "Docker, Linux"]),
            json.dumps(["Системне інженерне мислення", "Дотримання культури цілісності даних"]),
            json.dumps([
                {"name": "Apache Spark Docs", "url": "https://spark.apache.org/docs/latest/"},
                {"name": "Apache Airflow Documentation", "url": "https://airflow.apache.org/docs/"}
            ])
        ),
        (
            "devops",
            "11. DevOps Engineer",
            "Інфраструктура та безпека",
            "badge-data",
            "Автоматизація процесів доставки коду, керування хмарною інфраструктурою як кодом (IaC), забезпечення безвідмовної роботи 24/7.",
            "Базове адміністрування Linux серверів, написання Dockerfile, налаштування простих пайплайнів GitLab CI / GitHub Actions.",
            "Налаштування оркестрації в Kubernetes (K8s), опис хмари через Terraform, моніторинг (Prometheus/Grafana).",
            "Архітектура Disaster Recovery, оптимізація хмарних витрат (FinOps), побудова корпоративних CI/CD стандартів.",
            json.dumps(["Linux (Ubuntu/Debian, Bash)", "Docker, Kubernetes (Helm)", "Terraform, Ansible", "AWS / GCP, GitLab CI, Prometheus"]),
            json.dumps(["Холоднокровність в аварійних ситуаціях (Incident management)", "Комунікабельність"]),
            json.dumps([
                {"name": "Kubernetes Documentation", "url": "https://kubernetes.io/docs/home/"},
                {"name": "Docker Official Docs", "url": "https://docs.docker.com/"},
                {"name": "Terraform Registry & Docs", "url": "https://developer.hashicorp.com/terraform/docs"}
            ])
        ),
        (
            "cloud_arch",
            "12. Cloud Architect",
            "Інфраструктура та безпека",
            "badge-data",
            "Проєктування глобальної архітектури хмарних рішень для enterprise-клієнтів із фокусом на масштабованість, безпеку та економічну ефективність.",
            "Розгортання типових хмарних компонентів за архітектурним шаблоном.",
            "Міграція локальних додатків у хмару (Lift & Shift, Cloud-native), налаштування VPC та міжсервісних зв'язків.",
            "Створення комплексних стратегій Multi-cloud, аудит відповідності регуляторним стандартам (GDPR, ISO 27001).",
            json.dumps(["AWS Certified Solutions Architect / GCP / Azure", "Microservices architecture", "Cloud Networking & Security", "FinOps"]),
            json.dumps(["Стратегічне планування", "Переговори з технічними лідерами та бізнес-стейкхолдерами"]),
            json.dumps([
                {"name": "AWS Well-Architected Framework", "url": "https://aws.amazon.com/architecture/well-architected/"},
                {"name": "Google Cloud Architecture Center", "url": "https://cloud.google.com/architecture"}
            ])
        ),
        (
            "cybersecurity",
            "13. Cybersecurity Specialist / InfoSec",
            "Інфраструктура та безпека",
            "badge-data",
            "Захист мережевих контурів, баз даних та додатків від несанкціонованого доступу, тестування на проникнення (Penetration Testing) та аудит коду.",
            "Моніторинг логів безпеки, перевірка відповідності базовим правилам кібергігієни, сканування на відомі вразливості.",
            "Проведення тестів на проникнення (PenTest), аудит додатків за стандартом OWASP Top 10, розслідування інцидентів.",
            "Побудова корпоративної політики Zero Trust, управління Security Operations Center (SOC).",
            json.dumps(["Мережеві протоколи (TCP/IP, DNS, TLS)", "OWASP Top 10, Burp Suite, Wireshark", "Linux Hardening, SIEM системи"]),
            json.dumps(["Етичність (White-hat mindset)", "Уважність до деталей безпеки"]),
            json.dumps([
                {"name": "OWASP Top 10 Web Security", "url": "https://owasp.org/www-project-top-ten/"},
                {"name": "National Cyber Security Center (NCSC)", "url": "https://www.ncsc.gov.uk/"}
            ])
        ),
        (
            "uiux",
            "14. UI/UX Designer",
            "Design",
            "badge-design",
            "Дослідження користувацького досвіду, проєктування клікабельних прототипів, вайрфреймів та побудова консистентних дизайн-систем у Figma.",
            "Підготовка графіки та іконок, створення екранів за готовою UI-кіт бібліотекою, передача макетів у верстку.",
            "Проведення глибинних інтерв'ю з користувачами, UX-аудит, складання CJM (Customer Journey Map), розробка складних компонентів у Figma.",
            "Керування продуктовою дизайн-системою, проведення дизайн-рев'ю, узгодження візуальної мови з бізнес-цілями компанії.",
            json.dumps(["Figma (Auto-layout, Components, Variables)", "Wireframing, Prototyping", "UX Research & Usability Testing", "Design Systems"]),
            json.dumps(["Емпатія", "Вміння аргументувати дизайнерські рішення мовою бізнес-метрик"]),
            json.dumps([
                {"name": "Nielsen Norman Group (UX Guidelines)", "url": "https://www.nngroup.com/articles/"},
                {"name": "Figma Help Center & Best Practices", "url": "https://help.figma.com/"}
            ])
        ),
        (
            "pm",
            "15. Project Manager (PM)",
            "Management, Analytics, and Product",
            "badge-mgmt",
            "Організація та координація команди розробників: планування спринтів, контроль дедлайнів і бюджету за методологіями Scrum та Kanban.",
            "Ведення задач у Jira/Trello, організація щоденних стендапів, фіксація домовленостей на зустрічах (Meeting notes).",
            "Планування спринтів, оцінка задач у Story Points, фасилітація ретроспектив, управління ризиками проєкту.",
            "Керування портфелем проєктів, фінансовий контроль бюджетів, оптимізація інженерних процесів компанії.",
            json.dumps(["Agile, Scrum, Kanban", "Jira, Confluence, ClickUp", "Управління ризиками (Risk Management)", "Roadmapping"]),
            json.dumps(["Лідерство", "Вирішення конфліктів", "Ефективна ділова комунікація"]),
            json.dumps([
                {"name": "Scrum Guide Official", "url": "https://scrumguides.org/"},
                {"name": "Atlassian Agile Coach", "url": "https://www.atlassian.com/agile"}
            ])
        ),
        (
            "ba",
            "16. Business Analyst (BA)",
            "Management, Analytics, and Product",
            "badge-mgmt",
            "Трансформація бізнес-ідей замовника у точні та детальні технічні вимоги (SRS), моделювання процесів (BPMN) та написання User Stories.",
            "Збір первинних вимог від замовника, опис простих User Stories з критеріями прийняття (Acceptance Criteria).",
            "Моделювання бізнес-процесів за нотацією BPMN 2.0, написання специфікацій вимог (Software Requirements Specification), прототипування інтерфейсів.",
            "Стратегічний бізнес-консалтинг, аналіз рентабельності фіч (ROI), керування змінами в масштабах великих систем.",
            json.dumps(["BPMN 2.0, UML діаграми", "User Stories & Use Cases", "SRS documentation", "Postman basics, SQL"]),
            json.dumps(["Структурованість мислення", "Уміння слухати та докопуватися до істинної проблеми клієнта"]),
            json.dumps([
                {"name": "IIBA BABOK Guide Overview", "url": "https://www.iiba.org/career-resources/a-guide-to-the-business-analysis-body-of-knowledge-babok-guide/"},
                {"name": "BPMN 2.0 Quick Reference", "url": "https://www.omg.org/spec/BPMN/2.0/"}
            ])
        )
    ]

    cursor.executemany("""
    INSERT INTO professions (
        slug, title, category, badge_class, description, junior_duties, middle_duties, senior_duties, hard_skills, soft_skills, docs_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, professions_list)

def seed_mentors(cursor):
    mentors_list = [
        (
            "kovalenko",
            "Олександр Коваленко",
            "Senior Frontend Engineer",
            "MacPaw",
            6,
            850,
            json.dumps(["React", "TypeScript", "Next.js", "Web Vitals"]),
            "Допоміг 18 джуніорам отримати перший офер у 2024–2025 роках.",
            "ОК",
            "#DBEAFE",
            "#1E40AF"
        ),
        (
            "tkachenko",
            "Дмитро Ткаченко",
            "Tech Lead Python/Go",
            "Genesis",
            10,
            1200,
            json.dumps(["Python / FastAPI", "Go (Golang)", "PostgreSQL", "Kafka"]),
            "Аудит бекенд-архітектури pet-проєктів, mock-інтерв'ю з алгоритмів.",
            "ДТ",
            "#EDE9FE",
            "#5B21B6"
        ),
        (
            "melnyk",
            "Ірина Мельник",
            "Lead QA Automation",
            "Grammarly",
            8,
            950,
            json.dumps(["Python", "Playwright", "CI/CD Testing", "API Automation"]),
            "Супровід світчерів у перекваліфікації з Manual на Automation QA.",
            "ІМ",
            "#FEF3C7",
            "#92400E"
        ),
        (
            "kravchenko",
            "Василь Кравченко",
            "Senior DevOps / SRE",
            "Ciklum",
            7,
            1100,
            json.dumps(["Linux", "Docker & K8s", "Terraform", "AWS Cloud"]),
            "Налаштування тестового стенду для портфоліо майбутніх DevOps.",
            "ВК",
            "#D1FAE5",
            "#065F46"
        ),
        (
            "sydorenko",
            "Марина Сидоренко",
            "Senior Product Designer",
            "Ajax Systems",
            5,
            900,
            json.dumps(["Figma", "Design Systems", "UX Research", "Prototyping"]),
            "Детальний розбір 50+ дизайн-портфоліо з конкретними правками.",
            "МС",
            "#FCE7F3",
            "#9D174D"
        ),
        (
            "boyko",
            "Андрій Бойко",
            "Lead Project Manager / Agile Coach",
            "EPAM Systems",
            9,
            850,
            json.dumps(["Scrum / Kanban", "Jira Admin", "People Management", "Risk Analysis"]),
            "Підготовка до співбесід на посади PM / Scrum Master без досвіду.",
            "АБ",
            "#E2E8F0",
            "#1E293B"
        )
    ]

    cursor.executemany("""
    INSERT INTO mentors (
        slug, name, title, company, experience_years, hourly_rate, tags, cases, initials, avatar_bg, avatar_color
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, mentors_list)

if __name__ == "__main__":
    init_db()
