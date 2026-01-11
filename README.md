# Django Full-Stack Professional Portfolio & CMS

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Sass](https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)

A production-ready, full-stack portfolio and Content Management System (CMS) built with **Django 5.x**. This platform features a dynamic blogging engine, an automated contact management system, and a modular SCSS architecture, all deployed on a custom domain via Render.

<img width="1871" height="921" alt="PortfolioHome" src="https://github.com/user-attachments/assets/c69bd461-b6e0-415c-83ff-6a6b77ccf4ba" />

[**www.giuseppemancini.dev**](https://www.giuseppemancini.dev)



## ✨ Key Features

* **Custom CMS:** A fully integrated Django Admin backend to manage projects and blog posts without touching the code.
* **Dynamic Blogging System:** Supports rich-text editing (CKEditor), tagging, and featured post logic.
* **Automated Contact Pipeline:** Custom contact form with database persistence and dual-SMTP email notifications (Admin alerts + User auto-replies).
* **Modular Sass (SCSS):** Organized using the **BEM methodology** and the 7-1 pattern for scalable, maintainable styling.
* **Responsive UI/UX:** Context-aware design that transitions between "Dark Mode" (Portfolio) and "Light Mode" (Blog).
* **Production DevOps:** Securely deployed on Render with SSL, custom DNS configuration, and environment variable protection.

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python / Django |
| **Frontend** | JavaScript (ES6+), HTML5 |
| **Styling** | Sass (SCSS) |
| **Database** | SQLite (Dev) / PostgreSQL (Production ready) |
| **Deployment** | Render (CI/CD) |
| **Tools** | WhiteNoise (Static files), Gunicorn, Git |

---

## 📂 Project Structure

```text
├── core/                # Project settings and WSGI/ASGI config
├── portfolio/           # Project showcase logic and templates
├── blog/                # CMS Blogging engine and logic
├── contact/             # Contact form processing and email services
├── static/              # Compiled CSS (from Sass), JS, and Images
│   └── scss/            # BEM-structured SCSS (Abstracts, Components, Layout)
├── templates/           # Global and modular HTML templates
└── manage.py            # Django CLI
```
### Engineering Highlight
* **MVT Architecture** : utilized Django’s Model-View-Template pattern to decouple data logic from presentation.
* **Sass Compilation** : implemented a modular SCSS structure to maintain design consistency across multiple Django apps.
* **Security** : Enforced CSRF protection, secure environment variable management, and production-grade static file handling.
