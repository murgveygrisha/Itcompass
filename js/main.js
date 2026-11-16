/* ==========================================================================
   ITCompass — main.js
   Лабораторна робота №4: Основи JavaScript.
   Робота з DOM, подіями та динамічним контентом.

   Модулі:
     1. Маніпуляція елементами DOM (querySelectorAll, createElement, append)
     2. Динамічний контент (дата у футері, акордеон «Показати більше»)
     3. Події (перемикач теми, підсвітка меню, клавіатура ArrowUp/ArrowDown)
     4. Форми та клієнтська валідація (submit, preventDefault, власні перевірки)
     5. LocalStorage (збереження теми та імені користувача) — бонус
   ========================================================================== */

'use strict';

/* Константи localStorage */
const STORAGE_THEME_KEY = 'itcompass-theme';
const STORAGE_NAME_KEY = 'itcompass-user-name';

/* Межі розміру шрифту для керування з клавіатури, px */
const FONT_MIN = 12;
const FONT_MAX = 22;
const FONT_STEP = 1;

document.addEventListener('DOMContentLoaded', () => {
  initCardHighlight();
  initAppendedParagraph();
  initFooterDate();
  initAccordion();
  initThemeToggle();
  initNavHighlight();
  initFontSizeKeys();
  initContactForm();
});

/* ==========================================================================
   1. Маніпуляція елементами DOM
   ========================================================================== */

/**
 * 2.1а. Знаходимо на сторінці всі елементи з класом .card
 * і змінюємо їм стиль — додаємо фірмову верхню смужку та легку тінь.
 */
function initCardHighlight() {
  const cards = document.querySelectorAll('.card');
  cards.forEach((card) => {
    card.style.borderTop = '3px solid var(--color-primary)';
    card.style.boxShadow = 'var(--shadow-md)';
  });
}

/**
 * 2.1б. Створюємо новий елемент <p> через createElement()
 * і додаємо його в кінець основного контейнера <main> через append().
 */
function initAppendedParagraph() {
  const main = document.querySelector('main');
  if (!main) return;

  const cardsCount = document.querySelectorAll('.card').length;

  const note = document.createElement('p');
  note.className = 'js-generated-note container';
  note.textContent =
    `⚡ Цей блок створено динамічно за допомогою JavaScript (createElement + append). ` +
    `Карток на сторінці: ${cardsCount}.`;

  main.append(note);
}

/* ==========================================================================
   2. Динамічна зміна контенту
   ========================================================================== */

/**
 * 2.2а. Автоматично показуємо поточну дату у футері сайту.
 */
function initFooterDate() {
  const footerBottom = document.querySelector('.footer-bottom');
  if (!footerBottom) return;

  const now = new Date();
  const formatted = now.toLocaleDateString('uk-UA', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const dateParagraph = document.createElement('p');
  dateParagraph.className = 'footer-date';
  dateParagraph.textContent = `Сьогодні: ${formatted}`;
  footerBottom.append(dateParagraph);
}

/**
 * 2.2б. Кнопка «Показати більше» — акордеон, що розкриває прихований
 * блок тексту (розмітка блоку — на головній сторінці index.html).
 */
function initAccordion() {
  const toggleButton = document.querySelector('.accordion-toggle');
  const content = document.querySelector('.accordion-content');
  if (!toggleButton || !content) return;

  toggleButton.addEventListener('click', () => {
    const isOpen = content.classList.toggle('open');
    toggleButton.textContent = isOpen ? 'Сховати ▲' : 'Показати більше ▼';
    toggleButton.setAttribute('aria-expanded', String(isOpen));
  });
}

/* ==========================================================================
   3. Події та обробники
   ========================================================================== */

/**
 * 3.1. Кнопка «Змінити тему»: створюється динамічно у шапці сайту;
 * при натисканні перемикає клас dark-theme на <body>.
 * Бонус (LocalStorage): обрана тема зберігається між відвідуваннями.
 */
function initThemeToggle() {
  const navActions = document.querySelector('.nav-actions');
  if (!navActions) return;

  const themeButton = document.createElement('button');
  themeButton.type = 'button';
  themeButton.className = 'btn theme-toggle';
  themeButton.setAttribute('aria-label', 'Змінити тему сайту');

  /* Відновлюємо тему, збережену в localStorage */
  const savedTheme = localStorage.getItem(STORAGE_THEME_KEY);
  if (savedTheme === 'dark') {
    document.body.classList.add('dark-theme');
  }
  themeButton.textContent = document.body.classList.contains('dark-theme') ? '☀️' : '🌙';

  themeButton.addEventListener('click', () => {
    const isDark = document.body.classList.toggle('dark-theme');
    themeButton.textContent = isDark ? '☀️' : '🌙';
    localStorage.setItem(STORAGE_THEME_KEY, isDark ? 'dark' : 'light');
  });

  navActions.prepend(themeButton);
}

/**
 * 3.2а. Підсвітка пунктів меню навігації при наведенні миші.
 * Реалізовано саме JS-класами (mouseover / mouseout + classList),
 * а не CSS-псевдокласом :hover.
 */
function initNavHighlight() {
  const navLinks = document.querySelectorAll('nav a');

  navLinks.forEach((link) => {
    link.addEventListener('mouseover', () => link.classList.add('js-nav-hover'));
    link.addEventListener('mouseout', () => link.classList.remove('js-nav-hover'));
  });
}

/**
 * 3.2б. Відстеження натискань клавіш: ArrowUp збільшує розмір шрифту
 * сторінки, ArrowDown — зменшує (в межах FONT_MIN…FONT_MAX px).
 */
function initFontSizeKeys() {
  document.addEventListener('keydown', (event) => {
    /* Не перехоплюємо стрілки під час набору тексту в полях форми */
    const tag = event.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;

    if (event.key !== 'ArrowUp' && event.key !== 'ArrowDown') return;
    event.preventDefault();

    const html = document.documentElement;
    const currentSize = parseFloat(getComputedStyle(html).fontSize);
    const nextSize = event.key === 'ArrowUp'
      ? Math.min(currentSize + FONT_STEP, FONT_MAX)
      : Math.max(currentSize - FONT_STEP, FONT_MIN);

    html.style.fontSize = `${nextSize}px`;
  });
}

/* ==========================================================================
   4. Робота з формами та валідацією
   ========================================================================== */

/**
 * Обробка події submit контактної форми (contacts.html):
 *  - скасовуємо стандартну відправку (event.preventDefault);
 *  - зчитуємо дані з усіх полів;
 *  - виконуємо власну JS-валідацію;
 *  - при помилках підсвічуємо поля та показуємо тексти помилок;
 *  - при успіху виводимо дані в консоль і блок повідомлень, очищаємо форму.
 */
function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  /* Вимикаємо вбудовану браузерну валідацію — перевіряємо самостійно */
  form.setAttribute('novalidate', 'novalidate');

  /* Блок повідомлень під формою */
  const statusBox = document.createElement('div');
  statusBox.className = 'form-status';
  statusBox.setAttribute('role', 'status');
  form.append(statusBox);

  /* Бонус (LocalStorage): підставляємо збережене ім'я користувача */
  const nameField = form.elements.userName;
  const savedName = localStorage.getItem(STORAGE_NAME_KEY);
  if (nameField && savedName) {
    nameField.value = savedName;
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault(); /* 4.1. Забороняємо стандартну відправку */

    /* 4.1. Зчитуємо дані з усіх полів форми */
    const formData = {
      userName: form.elements.userName.value.trim(),
      userEmail: form.elements.userEmail.value.trim(),
      userPhone: form.elements.userPhone.value.trim(),
      profession: form.elements.professionSelect.value,
      sessionType: form.elements.sessionType.value,
      userMessage: form.elements.userMessage.value.trim(),
      userConsent: form.elements.userConsent.checked,
    };

    /* 4.2. Клієнтська валідація на JavaScript */
    clearValidation(form);
    const errors = validateForm(formData);

    if (errors.length > 0) {
      errors.forEach(({ field, message }) => showFieldError(form, field, message));
      showStatus(statusBox, `Помилок у формі: ${errors.length}. Виправте підсвічені поля.`, 'error');
      return;
    }

    /* Успіх: виводимо дані в консоль та у блок повідомлень */
    console.log('Дані форми запису на консультацію:', formData);
    showStatus(statusBox, '✅ Форма успішно надіслана!', 'success');

    /* Бонус (LocalStorage): запам'ятовуємо ім'я користувача */
    localStorage.setItem(STORAGE_NAME_KEY, formData.userName);

    form.reset();
  });
}

/**
 * Власна логіка перевірок полів форми.
 * @returns {Array<{field: string, message: string}>} список помилок
 */
function validateForm(data) {
  const errors = [];

  /* Ім'я — мінімум 3 символи */
  if (data.userName.length < 3) {
    errors.push({ field: 'userName', message: "Ім'я має містити щонайменше 3 символи." });
  }

  /* Email — містить @ і домен (щонайменше name@host.tld) */
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
  if (!emailPattern.test(data.userEmail)) {
    errors.push({ field: 'userEmail', message: 'Email має містити символ @ і домен, наприклад name@example.com.' });
  }

  /* Телефон — необов'язковий, але якщо введений, перевіряємо формат */
  if (data.userPhone && !/^\+?[0-9\s\-()]{10,17}$/.test(data.userPhone)) {
    errors.push({ field: 'userPhone', message: 'Введіть номер у форматі +38 (0XX) XXX-XX-XX.' });
  }

  /* Спеціальність — обов'язковий вибір зі списку */
  if (!data.profession) {
    errors.push({ field: 'professionSelect', message: 'Оберіть спеціальність зі списку.' });
  }

  /* Повідомлення — довжина не менше 10 символів */
  if (data.userMessage.length < 10) {
    errors.push({ field: 'userMessage', message: 'Опишіть ваш запит докладніше (щонайменше 10 символів).' });
  }

  /* Згода на обробку персональних даних */
  if (!data.userConsent) {
    errors.push({ field: 'userConsent', message: 'Потрібна згода на обробку персональних даних.' });
  }

  return errors;
}

/** Підсвічує поле червоним і показує текст помилки під ним. */
function showFieldError(form, fieldName, message) {
  const field = form.elements[fieldName];
  if (!field) return;

  field.classList.add('field-invalid');

  const group = field.closest('.form-group');
  const errorMessage = group ? group.querySelector('.error-message') : null;
  if (errorMessage) {
    errorMessage.textContent = message;
    errorMessage.classList.add('visible');
  }
}

/** Прибирає підсвітку та повідомлення про помилки з усіх полів форми. */
function clearValidation(form) {
  form.querySelectorAll('.field-invalid').forEach((el) => el.classList.remove('field-invalid'));
  form.querySelectorAll('.error-message.visible').forEach((el) => el.classList.remove('visible'));
}

/** Показує підсумкове повідомлення під формою (успіх або помилка). */
function showStatus(statusBox, text, type) {
  statusBox.textContent = text;
  statusBox.className = `form-status ${type} visible`;
}
