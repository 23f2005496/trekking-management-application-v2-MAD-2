# 🥾 Trekking Management Application - V2

A full-stack **Trekking Management Application** built using **Vue.js** and **Flask REST APIs**. The application allows trekkers to book treks, staff to manage assigned treks, and admins to manage the complete trekking system. It also includes **Redis caching**, **Celery background tasks**, **scheduled email reminders**, and **monthly activity reports**.

---

# 🚀 Features

## 🛠️ Admin Features

- Admin Dashboard
- Add new trek
- Edit trek
- Delete trek
- Upload trek images
- Manage trek staff
- Approve or reject staff
- Assign staff to treks
- View all users (staff and trekkers)
- View all bookings
- View trekking statistics

---

## 🧑‍💼 Staff Features

- Register
- Login (Only after admin approval)
- View assigned treks
- View trek details
- Update available slots
- Change trek status
- View trek participants

---

## 👤 Trekker Features

- Register and Login
- View available treks
- Search and filter treks
- View trek details
- Book a trek
- Cancel booking
- View current bookings
- View booking history
- Export booking history as CSV
- Update profile
- Change password

---

## ⚡ Background Jobs (Celery)

### 📄 CSV Export by Trekker

- Export booking history as CSV
- Processed asynchronously using Celery
- Download generated CSV after completion

### 📧 Daily Reminder Emails

- Automatically sends reminder emails to trekkers about upcoming treks.
- Includes:
  - Trek details
  - Trek start date
  - Days remaining
  - Trek instructions
  - Scheduled using Celery Beat

### 📊 Monthly Activity Report

Automatically sends an HTML report of every month to the Admin containing:

- Total treks conducted
- Total participants
- Total bookings
- Most popular trek
- Top 3 popular treks
- Trek-wise participation statistics

---

## ⚡ Redis Caching

- Redis-based caching
- Improves API performance
- Reduces unnecessary database queries

---

# ⚙️ Technologies Used

## Frontend

- Vue.js
- Vue Router
- Axios
- Bootstrap
- HTML
- CSS
- JavaScript

## Backend

- Flask
- Flask REST API
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Mail
- Flask-Caching
- SQLite
- Redis
- Celery
- Celery Beat
- Python-dotenv
- Werkzeug
- pytz

---

# 📁 Project Structure

```text
trekking-management-application-v2-MAD-2/

│
├── README.md
├── .gitignore
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── static/
│   │   │   └── images/
│   │   ├── tasks/
│   │   ├── templates/
│   │   │   └── emails/
│   │   ├── utils/
│   │   ├── cache.py
│   │   ├── celery_app.py
│   │   └── __init__.py
│   │
│   ├── config/
│   ├── exports/
│   ├── instance/
│   ├── migrations/
│   ├── .env
│   ├── requirements.txt
│   ├── celery_worker.py
│   └── run.py
│
└── frontend/
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   ├── router/
    │   ├── services/
    │   ├── views/
    │   ├── App.vue
    │   └── main.js
    │
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    └── index.html
```

---

# ⚙️ Prerequisites

Before running the project, make sure the following software is installed:

- Python 3.11 or later
- Node.js (v18 or later)
- npm
- Git
- Redis (Memurai on Windows or Redis on macOS)

---

# ⚙️ How to Run the Project

## Step 1 : Clone the Repository or download zip file

```bash
git clone https://github.com/23f2005496/trekking-management-application-v2-MAD-2.git
```

Go inside the project folder.

```bash
cd trekking-management-application-v2-MAD-2
```

---

# Backend Setup

Go to the backend folder.

```bash
cd backend
```

---

## Step 2 : Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

Activate it

```bash
.venv\Scripts\activate
```

### macOS

```bash
python3 -m venv .venv
```

Activate it

```bash
source .venv/bin/activate
```

---

## Step 3 : Install Required Packages

```bash
pip install -r requirements.txt
```

---

## Step 4 : Configure Environment Variables

Create a `.env` file inside the **backend** folder.

Example:

```env
SECRET_KEY=your_secret_key

SQLALCHEMY_DATABASE_URI=sqlite:///trekking.db

# Admin Credentials

ADMIN_EMAIL=admin@trek.com
ADMIN_FULL_NAME=Admin
ADMIN_PASSWORD=admin123

# For Gmail SMTP configuration

MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_gmail_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

---

## Step 5 : Database

This project uses **SQLite**.

If the database already exists, no setup is required.

Otherwise,

Create a new database:

```bash
flask db init
```
It will create a "instance" and "migrations" folders. then run,

---

```bash
flask create-db
```
It will create a new database with schema and tables and also add "admin" in database with credentials from ".env" file. then run,

---

```bash
flask seed-db
```
It will add "sample data" of all tables in database. then run,

---

"one special command"

```bash
flask reset-db
```
Use it wisely because it will "completely delete" your old database and "create a fresh" one from scratch with "admin".
It also asks for confirmation before excecute (y/n)

---

## Step 6 : Install Redis

### Windows

Install **Memurai Community Edition** (Redis-compatible for Windows).

After installation, start the Memurai service.

Verify Redis is running:

```bash
netstat -ano | findstr 6379
```

---

### macOS

Install Redis using Homebrew.

```bash
brew install redis
```

Start Redis.

```bash
brew services start redis
```

Verify installation.

```bash
redis-cli ping
```

Expected output:

```
PONG
```

---

## Step 7 : Start Redis

Make sure Redis is running before starting Celery Worker and Celery Beat.

---

## Step 8 : Start Celery Worker

Open new terminal and cd to /backend/ and activate .venv then run following command.

```bash
python -m celery -A celery_worker.celery worker --pool=solo --loglevel=info
```

---

## Step 9 : Start Celery Beat

Open new terminal and cd to /backend/ and activate .venv then run following command.

```bash
python -m celery -A celery_worker.celery beat --loglevel=info
```

---

## Step 10 : Run Flask Backend

```bash
python run.py
```

The backend will run at:

```
http://127.0.0.1:5000
```

---

# Frontend Setup

Open a new terminal.

Go to the frontend folder.

```bash
cd frontend
```

---

## Step 11 : Install Frontend Dependencies

```bash
npm install
```

---

## Step 12 : Run Vue Application

```bash
npm run dev
```

The frontend will run at:

```
http://localhost:5173
```

---

# 🔐 Login Credentials

## Admin look in .env file

```
Email: admin@trek.com

Password: admin123
```

---

## Staff & Trekkers

Refer to the seed data in the seed.py file in config folder.

---

# 👨‍💻 Developed By

**Tushar Sharma**

Student, IIT Madras

---

# 📄 License

This project is developed for educational purposes as part of the **IIT Madras Diploma in Programming (MAD 2 Project)**.