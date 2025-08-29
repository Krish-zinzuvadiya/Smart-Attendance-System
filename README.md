#🎓 Student Management System (Django)

## 📌 Summary
The **Student Management System** is a web-based application built with **Django** that simplifies the process of managing student information, attendance, and academic records. It provides an easy-to-use interface for administrators, teachers, and students to interact with the system. The system aims to reduce manual effort and bring automation to academic management.

## 📖 Introduction
Managing student records manually often leads to inefficiency and errors. The **Django Student Management System** automates critical operations like student registration, attendance tracking, course allocation, and performance evaluation.  
This project uses the **Django framework** to ensure a secure, scalable, and structured application. It is built with a modular approach where each stakeholder (Admin, Teacher, Student) has specific roles and access levels.

---

## 🚀 Project Setup Guide

Follow the steps below to run the project locally.

### 1️⃣ Create Django Project
This project is named **`smart_attendance`**.  
If you want to create it manually, use:
```python
django-admin startproject smart_attendance
```

### 2️⃣ Create Django App
The main application is named **`attendance`**.
To create it, run:
```python
cd smart_attendance
python manage.py startapp attendance
```

### ⚙️ Database Setup & Migration
Run the following commands to set up the database and apply migrations:
```python
python manage.py makemigrations
python manage.py migrate
```

### 👨‍💻 Create Superuser (Admin Panel Access)
You can create a superuser to access the Django Admin Panel:
```python
python manage.py createsuperuser
```
If you do not create one manually, you can use the default superuser credentials:
● Username: admin
● Password: 123

### ▶️ Run the Project
To start the development server, run:
```python
python manage.py runserver
```
Now open your browser and go to:
👉 http://127.0.0.1:8000/

### 👤 Author
Made by **`Krish Zinzuvadiya & Team`**<br>
All rights reserved.
