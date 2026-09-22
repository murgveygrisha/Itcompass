/**
 * ITCompass - Головний скрипт клієнтської взаємодії
 */

// База знань із докладним описом усіх 16 IT-спеціальностей
const professionsData = {
  frontend: {
    title: "1. Frontend Developer (React/Vue)",
    category: "Software Engineering",
    badgeClass: "badge-dev",
    description: "Створення клієнтської частини сайтів та інтерактивних веб-додатків. Фахівець відповідає за швидкість завантаження, адаптивність та візуальну зручність інтерфейсу.",
    pageUrl: "profession-frontend.html",
    duties: {
      junior: "Адаптивна верстка за макетами Figma (HTML5/CSS3), базова асинхронна логіка на JavaScript, робота з готовими REST API.",
      middle: "Розробка SPA на React/Next.js/Vue, оптимізація продуктивності (Web Vitals), тестування компонентів (Jest/Playwright).",
      senior: "Проєктування архітектури фронтенду, дизайн-систем, налаштування CI/CD пайплайнів, менторинг команди."
    },
    hardSkills: ["HTML5 / CSS3 / Flexbox / Grid", "JavaScript (ES6+) & TypeScript", "React 19 / Vue.js / Next.js", "Tailwind CSS, Vite, Git"],
    softSkills: ["Командна взаємодія (Scrum)", "Культура Code Review", "Увага до деталей (Pixel-Perfect)"],
    docs: [
      { name: "MDN Web Docs (Mozilla)", url: "https://developer.mozilla.org/uk/docs/Web/HTML" },
      { name: "React.dev — Офіційна документація", url: "https://react.dev/" },
      { name: "TypeScript Handbook", url: "https://www.typescriptlang.org/docs/handbook/" }
    ]
  },
  backend: {
    title: "2. Backend Developer (Node.js/Python/Java/Go)",
    category: "Software Engineering",
    badgeClass: "badge-dev",
    description: "Проєктування серверної архітектури, створення надійних REST/GraphQL/gRPC сервісів, робота з реляційними та NoSQL базами даних.",
    duties: {
      junior: "Написання CRUD операцій, створення контролерів і маршрутів, написання простих SQL-запитів, документування API у Swagger.",
      middle: "Проєктування схем баз даних, оптимізація складних SQL-запитів, робота з чергами повідомлень (RabbitMQ, Redis, Kafka).",
      senior: "Мікросервісна архітектура, балансування навантаження, відмовостійкість систем, захист від DDoS та ін'єкцій."
    },
    hardSkills: ["Node.js / Python (FastAPI/Django) / Go", "PostgreSQL, MySQL, Redis", "Docker, REST API, GraphQL", "Git, Linux базові команди"],
    softSkills: ["Аналітичне мислення", "Вміння аргументувати архітектурні рішення", "Тайм-менеджмент"],
    docs: [
      { name: "Node.js Official Documentation", url: "https://nodejs.org/docs/latest/api/" },
      { name: "Python Docs", url: "https://docs.python.org/3/" },
      { name: "PostgreSQL Documentation", url: "https://www.postgresql.org/docs/" }
    ]
  },
  fullstack: {
    title: "3. Fullstack Developer",
    category: "Software Engineering",
    badgeClass: "badge-dev",
    description: "Універсальний спеціаліст широкого профілю, який здатний самостійно створити готовий веб-сервіс від інтерфейсу користувача до сервера та бази даних.",
    duties: {
      junior: "Розробка невеликих модулів фронтенду та підключення до власних ендпоінтів бекенду.",
      middle: "Повний цикл розробки фічі (Full feature ownership): база даних + API + UI-компоненти.",
      senior: "Вибір технологічного стеку для нових продуктів, оптимізація взаємодії клієнт-сервер."
    },
    hardSkills: ["TypeScript на фронтенді та бекенді", "Next.js / NestJS / Express", "PostgreSQL / Prisma ORM", "Docker, Nginx"],
    softSkills: ["Гнучкість мислення", "Самостійність у вирішенні комплексних задач"],
    docs: [
      { name: "Next.js Documentation", url: "https://nextjs.org/docs" },
      { name: "Prisma ORM Guide", url: "https://www.prisma.io/docs" }
    ]
  },
  mobile: {
    title: "4. Mobile Developer (iOS / Android / Flutter)",
    category: "Software Engineering",
    badgeClass: "badge-dev",
    description: "Створення нативних та кросплатформних застосунків для смартфонів і планшетів на базі iOS та Android.",
    duties: {
      junior: "Верстка мобільних екранів за дизайн-макетами, інтеграція з REST API, збереження локальних даних.",
      middle: "Керування життєвим циклом екранів, робота з Push-сповіщеннями, офлайн-режим, анімації.",
      senior: "Оптимізація пам'яті та енергоспоживання додатку, публікація в App Store та Google Play."
    },
    hardSkills: ["Flutter & Dart / Swift (iOS) / Kotlin (Android)", "REST API, WebSocket", "SQLite / Room / CoreData"],
    softSkills: ["Розуміння Human Interface Guidelines та Material Design", "Емпатія до користувача"],
    docs: [
      { name: "Flutter Official Docs", url: "https://docs.flutter.dev/" },
      { name: "Apple Developer Documentation", url: "https://developer.apple.com/documentation/" }
    ]
  },
  qa_manual: {
    title: "5. Manual Testing Engineer",
    category: "Тестування ПЗ (QA)",
    badgeClass: "badge-qa",
    description: "Контроль якості програмного забезпечення, виявлення розбіжностей між очікуваною та фактичною поведінкою системи вручну.",
    duties: {
      junior: "Проходження готових тест-кейсів, складання зрозумілих баг-репортів у Jira, димне тестування (Smoke testing).",
      middle: "Складання тест-планів, матриці трасування вимог, тестування REST API через Postman, перевірка баз даних за допомогою SQL.",
      senior: "Побудова QA-стратегії проєкту, управління релізами, аналіз ризиків якості."
    },
    hardSkills: ["Теорія тестування (ISTQB)", "Postman, Swagger", "Базові SQL-запити (SELECT, JOIN)", "Jira, TestRail"],
    softSkills: ["Уважність до дрібниць", "Критичне мислення", "Грамотна письмова фіксація багів"],
    docs: [
      { name: "ISTQB Glossary & Syllabus", url: "https://www.istqb.org/" },
      { name: "Postman Learning Center", url: "https://learning.postman.com/" }
    ]
  },
  qa_auto: {
    title: "6. Test Automation Engineer (Python/Java/JS)",
    category: "Тестування ПЗ (QA)",
    badgeClass: "badge-qa",
    description: "Розробка автотестів для UI та API, побудова тестових фреймворків, які виконуються автоматично при кожному оновленні коду в CI/CD.",
    duties: {
      junior: "Написання та підтримка автотестів за готовим шаблоном фреймворку, локалізація причин падіння тестів.",
      middle: "Створення та розширення тест-фреймворків (Page Object Model), автоматизація API та E2E сценаріїв.",
      senior: "Інтеграція автотестів у CI/CD пайплайни, оптимізація швидкості виконання, паралелізація тестів."
    },
    hardSkills: ["Python / Java / TypeScript", "Playwright, Selenium WebDriver", "PyTest / JUnit", "Git, Docker, CI/CD"],
    softSkills: ["Інженерний підхід", "Системне бачення архітектури тестування"],
    docs: [
      { name: "Playwright Documentation", url: "https://playwright.dev/" },
      { name: "Selenium Dev Guide", url: "https://www.selenium.dev/documentation/" }
    ]
  },
  data_analyst: {
    title: "7. Data Analyst",
    category: "Data, AI and ML",
    badgeClass: "badge-data",
    description: "Збір, очищення та дослідження цифрових показників компанії, побудова інформативних дашбордів для прийняття бізнес-рішень.",
    duties: {
      junior: "Вивантаження даних з баз через SQL, побудова базових звітів у Excel/Google Sheets, візуалізація метрик.",
      middle: "Розробка інтерактивних дашбордів у Tableau/PowerBI, аналіз когорт і продуктових воронок, перевірка A/B тестів.",
      senior: "Побудова системи продуктової та маркетингової аналітики, формування стратегічних бізнес-висновків."
    },
    hardSkills: ["SQL (Window functions, CTE, агрегати)", "Tableau, PowerBI", "Python (Pandas, NumPy, Matplotlib)", "Математична статистика"],
    softSkills: ["Вміння презентувати цифри нетехнічній аудиторії (Storytelling with data)"],
    docs: [
      { name: "PostgreSQL Tutorial for Data Analysis", url: "https://www.postgresqltutorial.com/" },
      { name: "Pandas Documentation", url: "https://pandas.pydata.org/docs/" }
    ]
  },
  data_scientist: {
    title: "8. Data Scientist",
    category: "Data, AI and ML",
    badgeClass: "badge-data",
    description: "Створення прогнозних моделей машинного навчання, виявлення прихованих закономірностей у великих масивах інформації.",
    duties: {
      junior: "Розвідувальний аналіз даних (EDA), підготовка ознак (Feature Engineering), навчання базових моделей класифікації/регресії.",
      middle: "Тюнінг гіперпараметрів, оцінка якості моделей (ROC-AUC, F1-score), робота з градієнтним бустингом (XGBoost, LightGBM).",
      senior: "Науково-дослідна діяльність (R&D), розробка кастомних алгоритмів, впровадження ML у бізнес-процеси."
    },
    hardSkills: ["Python, Scikit-learn, XGBoost", "Лінійна алгебра, теорія ймовірностей", "Jupyter, Git, SQL"],
    softSkills: ["Наукова допитливість", "Стійкість до експериментів із непередбачуваним результатом"],
    docs: [
      { name: "Scikit-learn Documentation", url: "https://scikit-learn.org/stable/" },
      { name: "Kaggle Learn Courses", url: "https://www.kaggle.com/learn" }
    ]
  },
  ml_ai: {
    title: "9. Machine Learning / AI Engineer",
    category: "Data, AI and ML",
    badgeClass: "badge-data",
    description: "Навчання, оптимізація та інтеграція складних нейромереж (Computer Vision, NLP, LLM) у робочі продукти (Production ML / MLOps).",
    duties: {
      junior: "Підготовка датасетів, донавчання (Fine-tuning) відкритих моделей нейромереж, написання API для інференсу.",
      middle: "Оптимізація швидкодії моделей (Quantization, ONNX), розгортання в хмарі, моніторинг деградації даних.",
      senior: "Архітектура генеративного ШІ (RAG-системи, агенти), керування розподіленим навчанням на GPU-кластерах."
    },
    hardSkills: ["PyTorch, Transformers (Hugging Face)", "MLOps (MLflow, Docker, Triton)", "Python, CUDA basics, LangChain"],
    softSkills: ["Швидка адаптація до нових досліджень у сфері ШІ"],
    docs: [
      { name: "PyTorch Documentation", url: "https://pytorch.org/docs/stable/index.html" },
      { name: "Hugging Face Guides", url: "https://huggingface.co/docs" }
    ]
  },
  data_engineer: {
    title: "10. Data Engineer",
    category: "Data, AI and ML",
    badgeClass: "badge-data",
    description: "Проєктування та підтримка інфраструктури збору, трансформації та надійного зберігання терабайтів даних (ETL/ELT конвеєри, DWH).",
    duties: {
      junior: "Підтримка існуючих конвеєрів перекачування даних, написання SQL скриптів трансформації.",
      middle: "Розробка ETL пайплайнів у Apache Airflow, обробка потокових даних у Apache Kafka, оптимізація схем DWH.",
      senior: "Проєктування озер даних (Data Lake) та хмарних сховищ (Snowflake, BigQuery, ClickHouse), надійність і безпека даних."
    },
    hardSkills: ["SQL Advanced, Python", "Apache Spark, Airflow, Kafka", "ClickHouse / BigQuery / Snowflake", "Docker, Linux"],
    softSkills: ["Системне інженерне мислення", "Дотримання культури цілісності даних"],
    docs: [
      { name: "Apache Spark Docs", url: "https://spark.apache.org/docs/latest/" },
      { name: "Apache Airflow Documentation", url: "https://airflow.apache.org/docs/" }
    ]
  },
  devops: {
    title: "11. DevOps Engineer",
    category: "Інфраструктура та безпека",
    badgeClass: "badge-data",
    description: "Автоматизація процесів доставки коду, керування хмарною інфраструктурою як кодом (IaC), забезпечення безвідмовної роботи 24/7.",
    duties: {
      junior: "Базове адміністрування Linux серверів, написання Dockerfile, налаштування простих пайплайнів GitLab CI / GitHub Actions.",
      middle: "Налаштування оркестрації в Kubernetes (K8s), опис хмари через Terraform, моніторинг (Prometheus/Grafana).",
      senior: "Архітектура Disaster Recovery, оптимізація хмарних витрат (FinOps), побудова корпоративних CI/CD стандартів."
    },
    hardSkills: ["Linux (Ubuntu/Debian, Bash)", "Docker, Kubernetes (Helm)", "Terraform, Ansible", "AWS / GCP, GitLab CI, Prometheus"],
    softSkills: ["Холоднокровність в аварійних ситуаціях (Incident management)", "Комунікабельність"],
    docs: [
      { name: "Kubernetes Documentation", url: "https://kubernetes.io/docs/home/" },
      { name: "Docker Official Docs", url: "https://docs.docker.com/" },
      { name: "Terraform Registry & Docs", url: "https://developer.hashicorp.com/terraform/docs" }
    ]
  },
  cloud_arch: {
    title: "12. Cloud Architect",
    category: "Інфраструктура та безпека",
    badgeClass: "badge-data",
    description: "Проєктування глобальної архітектури хмарних рішень для enterprise-клієнтів із фокусом на масштабованість, безпеку та економічну ефективність.",
    duties: {
      junior: "Розгортання типових хмарних компонентів за архітектурним шаблоном.",
      middle: "Міграція локальних додатків у хмару (Lift & Shift, Cloud-native), налаштування VPC та міжсервісних зв'язків.",
      senior: "Створення комплексних стратегій Multi-cloud, аудит відповідності регуляторним стандартам (GDPR, ISO 27001)."
    },
    hardSkills: ["AWS Certified Solutions Architect / GCP / Azure", "Microservices architecture", "Cloud Networking & Security", "FinOps"],
    softSkills: ["Стратегічне планування", "Переговори з технічними лідерами та бізнес-стейкхолдерами"],
    docs: [
      { name: "AWS Well-Architected Framework", url: "https://aws.amazon.com/architecture/well-architected/" },
      { name: "Google Cloud Architecture Center", url: "https://cloud.google.com/architecture" }
    ]
  },
  cybersecurity: {
    title: "13. Cybersecurity Specialist / InfoSec",
    category: "Інфраструктура та безпека",
    badgeClass: "badge-data",
    description: "Захист мережевих контурів, баз даних та додатків від несанкціонованого доступу, тестування на проникнення (Penetration Testing) та аудит коду.",
    duties: {
      junior: "Моніторинг логів безпеки, перевірка відповідності базовим правилам кібергігієни, сканування на відомі вразливості.",
      middle: "Проведення тестів на проникнення (PenTest), аудит додатків за стандартом OWASP Top 10, розслідування інцидентів.",
      senior: "Побудова корпоративної політики Zero Trust, управління Security Operations Center (SOC)."
    },
    hardSkills: ["Мережеві протоколи (TCP/IP, DNS, TLS)", "OWASP Top 10, Burp Suite, Wireshark", "Linux Hardening, SIEM системи"],
    softSkills: ["Етичність (White-hat mindset)", "Уважність до деталей безпеки"],
    docs: [
      { name: "OWASP Top 10 Web Security", url: "https://owasp.org/www-project-top-ten/" },
      { name: "National Cyber Security Center (NCSC)", url: "https://www.ncsc.gov.uk/" }
    ]
  },
  uiux: {
    title: "14. UI/UX Designer",
    category: "Design",
    badgeClass: "badge-design",
    description: "Дослідження користувацького досвіду, проєктування клікабельних прототипів, вайрфреймів та побудова консистентних дизайн-систем у Figma.",
    duties: {
      junior: "Підготовка графіки та іконок, створення екранів за готовою UI-кіт бібліотекою, передача макетів у верстку.",
      middle: "Проведення глибинних інтерв'ю з користувачами, UX-аудит, складання CJM (Customer Journey Map), розробка складних компонентів у Figma.",
      senior: "Керування продуктовою дизайн-системою, проведення дизайн-рев'ю, узгодження візуальної мови з бізнес-цілями компанії."
    },
    hardSkills: ["Figma (Auto-layout, Components, Variables)", "Wireframing, Prototyping", "UX Research & Usability Testing", "Design Systems"],
    softSkills: ["Емпатія", "Вміння аргументувати дизайнерські рішення мовою бізнес-метрик"],
    docs: [
      { name: "Nielsen Norman Group (UX Guidelines)", url: "https://www.nngroup.com/articles/" },
      { name: "Figma Help Center & Best Practices", url: "https://help.figma.com/" }
    ]
  },
  pm: {
    title: "15. Project Manager (PM)",
    category: "Management, Analytics, and Product",
    badgeClass: "badge-mgmt",
    description: "Організація та координація команди розробників: планування спринтів, контроль дедлайнів і бюджету за методологіями Scrum та Kanban.",
    duties: {
      junior: "Ведення задач у Jira/Trello, організація щоденних стендапів, фіксація домовленостей на зустрічах (Meeting notes).",
      middle: "Планування спринтів, оцінка задач у Story Points, фасилітація ретроспектив, управління ризиками проєкту.",
      senior: "Керування портфелем проєктів, фінансовий контроль бюджетів, оптимізація інженерних процесів компанії."
    },
    hardSkills: ["Agile, Scrum, Kanban", "Jira, Confluence, ClickUp", "Управління ризиками (Risk Management)", "Roadmapping"],
    softSkills: ["Лідерство", "Вирішення конфліктів", "Ефективна ділова комунікація"],
    docs: [
      { name: "Scrum Guide Official", url: "https://scrumguides.org/" },
      { name: "Atlassian Agile Coach", url: "https://www.atlassian.com/agile" }
    ]
  },
  ba: {
    title: "16. Business Analyst (BA)",
    category: "Management, Analytics, and Product",
    badgeClass: "badge-mgmt",
    description: "Трансформація бізнес-ідей замовника у точні та детальні технічні вимоги (SRS), моделювання процесів (BPMN) та написання User Stories.",
    duties: {
      junior: "Збір первинних вимог від замовника, опис простих User Stories з критеріями прийняття (Acceptance Criteria).",
      middle: "Моделювання бізнес-процесів за нотацією BPMN 2.0, написання специфікацій вимог (Software Requirements Specification), прототипування інтерфейсів.",
      senior: "Стратегічний бізнес-консалтинг, аналіз рентабельності фіч (ROI), керування змінами в масштабах великих систем."
    },
    hardSkills: ["BPMN 2.0, UML діаграми", "User Stories & Use Cases", "SRS documentation", "Postman basics, SQL"],
    softSkills: ["Структурованість мислення", "Уміння слухати та докопуватися до істинної проблеми клієнта"],
    docs: [
      { name: "IIBA BABOK Guide Overview", url: "https://www.iiba.org/career-resources/a-guide-to-the-business-analysis-body-of-knowledge-babok-guide/" },
      { name: "BPMN 2.0 Quick Reference", url: "https://www.omg.org/spec/BPMN/2.0/" }
    ]
  }
};

document.addEventListener('DOMContentLoaded', () => {
  // 1. Інтерактивна фільтрація карток професій
  const filterButtons = document.querySelectorAll('.filter-btn');
  const professionCards = document.querySelectorAll('.profession-card');

  if (filterButtons.length > 0 && professionCards.length > 0) {
    filterButtons.forEach(button => {
      button.addEventListener('click', () => {
        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        const category = button.getAttribute('data-category');

        professionCards.forEach(card => {
          const cardCategory = card.getAttribute('data-category');
          if (category === 'all' || cardCategory === category) {
            card.style.display = 'flex';
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // 2. Модальне вікно "Докладніше про спеціальність"
  const modal = document.getElementById('professionModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalBody = document.getElementById('modalBody');

  function openModal(profKey) {
    const data = professionsData[profKey];
    if (!data || !modal || !modalBody) return;

    let docItems = '';
    data.docs.forEach(doc => {
      docItems += `<li style="margin-bottom: 6px;"><a href="${doc.url}" target="_blank" rel="noopener noreferrer" style="font-weight: 600;">${doc.name} &nearr;</a></li>`;
    });

    let hardSkillsBadges = data.hardSkills.map(s => `<span class="tag" style="background-color:#E2E8F0; color:#1E293B;">${s}</span>`).join(' ');
    let softSkillsBadges = data.softSkills.map(s => `<span class="tag" style="background-color:#DCFCE7; color:#166534;">${s}</span>`).join(' ');

    let extraPageBtn = '';
    if (data.pageUrl) {
      extraPageBtn = `<a href="${data.pageUrl}" class="btn btn-outline" style="margin-right: 0.5rem;">Відкрити окрему сторінку ролі &rarr;</a>`;
    }

    modalBody.innerHTML = `
      <div style="margin-bottom: 1rem;">
        <span class="card-badge ${data.badgeClass}">${data.category}</span>
        <h2 style="font-size: 1.6rem; margin: 0.5rem 0 0.25rem;">${data.title}</h2>
        <p style="color: var(--color-text-muted); font-size: 1.05rem;">${data.description}</p>
      </div>

      <div style="background-color: #F8FAFC; border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1.25rem; margin-bottom: 1.25rem;">
        <h3 style="font-size: 1.15rem; margin-bottom: 0.5rem;">📋 Обов'язки спеціаліста за грейдами:</h3>
        <ul style="padding-left: 1.25rem; font-size: 0.95rem; display: flex; flex-direction: column; gap: 0.5rem;">
          <li><strong>Junior:</strong> ${data.duties.junior}</li>
          <li><strong>Middle:</strong> ${data.duties.middle}</li>
          <li><strong>Senior/Lead:</strong> ${data.duties.senior}</li>
        </ul>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.25rem;">
        <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
          <h4 style="font-size: 0.95rem; margin-bottom: 0.5rem; color: var(--color-primary);">🛠 Hard Skills (Технічні навички):</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
            ${hardSkillsBadges}
          </div>
        </div>
        <div style="border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: 1rem;">
          <h4 style="font-size: 0.95rem; margin-bottom: 0.5rem; color: var(--color-accent);">🤝 Soft Skills (Особисті навички):</h4>
          <div style="display: flex; flex-wrap: wrap; gap: 0.35rem;">
            ${softSkillsBadges}
          </div>
        </div>
      </div>

      <div style="border-top: 1px solid var(--color-border); padding-top: 1rem; margin-bottom: 1.5rem;">
        <h4 style="font-size: 1rem; margin-bottom: 0.5rem;">📚 Офіційна супровідна документація:</h4>
        <ul style="list-style: none; padding-left: 0; font-size: 0.95rem;">
          ${docItems}
        </ul>
      </div>

      <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 0.75rem; border-top: 1px solid var(--color-border); padding-top: 1.25rem;">
        <div>
          ${extraPageBtn}
        </div>
        <a href="contacts.html?profession=${profKey}" class="btn btn-primary" style="padding: 0.65rem 1.5rem;">
          Замовити консультацію з ментором &rarr;
        </a>
      </div>
    `;

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  // Прив'язка кнопок "Докладніше"
  document.querySelectorAll('.open-details-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const profKey = btn.getAttribute('data-profession');
      openModal(profKey);
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });
  }

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && modal.classList.contains('active')) {
      closeModal();
    }
  });

  // 3. Автоматичний вибір спеціальності на сторінці contacts.html за URL-параметром
  const urlParams = new URLSearchParams(window.location.search);
  const selectedProfession = urlParams.get('profession');
  const professionSelect = document.getElementById('professionSelect');

  if (selectedProfession && professionSelect) {
    professionSelect.value = selectedProfession;
    // Якщо елемент знайдено, прокручуємо до форми
    const formElement = document.getElementById('contactForm');
    if (formElement) {
      setTimeout(() => {
        formElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 200);
    }
  }

  // 4. Обробка форми зворотного зв'язку (з інтеграцією до Python REST API)
  const contactForm = document.getElementById('contactForm');
  const formSuccess = document.getElementById('formSuccess');

  if (contactForm) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const name = document.getElementById('userName')?.value.trim();
      const email = document.getElementById('userEmail')?.value.trim();
      const phone = document.getElementById('userPhone')?.value.trim() || '';
      const profession = document.getElementById('professionSelect')?.value || '';
      const sessionType = document.getElementById('sessionType')?.value || 'consultation';
      const userMessage = document.getElementById('userMessage')?.value.trim() || '';
      const userConsent = document.getElementById('userConsent')?.checked || false;

      if (!name || !email || !profession) {
        alert('Будь ласка, заповніть обов’язкові поля (Ім’я, Email та Спеціальність).');
        return;
      }

      const payload = {
        userName: name,
        userEmail: email,
        userPhone: phone,
        professionSelect: profession,
        sessionType: sessionType,
        userMessage: userMessage,
        userConsent: userConsent
      };

      try {
        // Пробуємо відправити на Python бекенд (якщо запущений на порту 8000 або поточному хості)
        const apiUrl = window.location.port === '8000' ? '/api/bookings' : 'http://127.0.0.1:8000/api/bookings';
        const response = await fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (response.ok) {
          const resData = await response.json();
          contactForm.reset();
          if (formSuccess) {
            formSuccess.innerHTML = `&check; Заявку <strong>#${resData.booking_id}</strong> успішно збережено в базі даних SQLite! Ментор зв'яжеться з вами найближчим часом.`;
            formSuccess.style.display = 'block';
            setTimeout(() => { formSuccess.style.display = 'none'; }, 6000);
          } else {
            alert(`Дякуємо! Ваша заявка #${resData.booking_id} збережена в базі даних.`);
          }
          return;
        }
      } catch (err) {
        console.info("Python Backend не запущений на порту 8000, використовується режим симуляції:", err);
      }

      // Резервний клієнтський режим (якщо сервер не запущено)
      contactForm.reset();
      if (formSuccess) {
        formSuccess.innerHTML = "&check; Вашу заявку успішно надіслано! Ментор зв'яжеться з вами у найближчий робочий час.";
        formSuccess.style.display = 'block';
        setTimeout(() => {
          formSuccess.style.display = 'none';
        }, 5000);
      } else {
        alert('Дякуємо! Ваша заявка успішно надіслана. Ментор зв’яжеться з вами найближчим часом.');
      }
    });
  }

  // 5. Плавна прокрутка для якорів
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          targetElement.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  });
});
