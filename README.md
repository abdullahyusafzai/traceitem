# 📦 TraceItem

### A Digital Lost & Found Management System for Schools

TraceItem is a web-based application designed to modernize the traditional school Lost & Found process. It allows teachers to record found items digitally and enables students to view them easily through a clean and user-friendly interface.

---

## 🚀 Features

* Secure login system
* Role-based access (Teacher / Student)
* Add found items with details and images
* View items in a clean card-based layout
* Mark items as returned
* Delete returned items
* Responsive design (Desktop & Mobile)
* Online deployment support

---

## 👥 User Roles

### Teacher

* Log in to the system
* Add found items
* Upload item images
* Mark items as returned
* Delete returned items

### Student

* Log in to the system
* View all found items
* Check item details and status

---

## 🛠️ Technologies Used

* Python
* FastAPI
* SQLite
* HTML
* CSS
* Jinja2 Templates
* Git & GitHub

---

## 📂 Project Structure

```
traceitem/
│
├── main.py              # Main FastAPI application
├── models.py            # Database models
├── database.py          # Database connection
├── requirements.txt     # Project dependencies
│
├── templates/            # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   └── add_item.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── uploads/          # Uploaded item images
│
└── README.md
```

---

## ⚙️ Installation & Setup

Follow these steps to run TraceItem on your local computer.

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/traceitem.git
cd traceitem
```

---

### 2️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

Activate it:

**Windows**

```bash
venv\Scripts\activate
```

**Mac / Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install fastapi uvicorn sqlalchemy jinja2 python-multipart passlib[bcrypt]
```

---

### 4️⃣ Run the Application

```bash
uvicorn main:app --reload
```

---

### 5️⃣ Open in Browser

Visit:

```
http://127.0.0.1:8000
```

---

## 🔑 Default Login Credentials

You can create your own users, or use default test users if configured:

**Teacher**

```
Username: teacher1
Password: admin123
```

**Student**

```
Username: student1
Password: 1234
```

*(You can change these in the database or startup logic.)*

---

## 🗄️ Database

* The project uses **SQLite**
* Database file is created automatically on first run
* Tables are generated using SQLAlchemy models

---

## 🌐 Deployment

TraceItem can be deployed online using platforms such as:

* Render
* Railway
* Fly.io

Once deployed, the system runs independently and does not require the developer’s computer to be on.

---

## 📈 Future Improvements

* Student item claim request system
* Notification alerts
* Advanced search and filters
* Admin dashboard
* Multi-school support

---

## 🎓 Educational Purpose

This project is suitable for:

* School ICT projects
* English Program competitions
* Learning web development
* Demonstrating real-world problem solving

---

## 📜 License

This project is open for educational use.
You are free to modify and improve it for learning purposes.

---

## 🙏 Acknowledgement

Special thanks to teachers and mentors who supported the development of this project.

---

## 📬 Contact

If you have questions or suggestions, feel free to contact the project author.

---
