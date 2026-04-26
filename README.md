# 🏟️ BVRIT Sports Complex Management System

<p align="center">
  <b>🚀 Smart Sports Facility & Slot Booking Platform</b><br>
  Built to streamline sports activities, events, and court bookings at BVRIT
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Flask-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Database-SQLite-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge">
</p>

---

## Overview

The **BVRIT Sports Complex Management System** is a full-stack web application that digitalizes sports operations including:

* 🏸 Court Booking
* 📅 Event Management
* 🏅 Sports Scheduling
* 👤 Role-Based Access

It ensures a seamless experience for **students, faculty, and administrators**.

---

## Key Highlights

✔️ Real-time slot booking system
✔️ Faculty vs Student court access logic
✔️ OTP-based authentication
✔️ Dynamic event management
✔️ Responsive UI design
✔️ Booking cancellation system

---

##  Features

###  Home & About

* Welcome dashboard
* Vision & objectives
* Sports committee details

---

###  Sports Module

*  Timetable (Morning & Evening sessions)
*  Individual & Team sports
*  Training & coaching programs

---

###  Events System

*  Upcoming Events (Card UI)
*  Past Events (Achievements)
*  Event Gallery

---

### 🎟️ Slot Booking (Core Module)

#### 🔐 Authentication

* Email login
* OTP verification system

#### ⚙️ Booking Flow

```text
Select Sport → Select Date → Select Court → Select Time → Confirm Booking
```

#### 🏟️ Smart Rules

* Court 1 → Faculty only
* Opens to students **10 mins before if free**
* Courts 2–4 → Students

####  Features

* Real-time slot updates
* Disabled booked slots
* My Bookings dashboard
* Cancel booking option

---

### 📞 Contact & FAQ

* Contact form
* Working hours
* Booking rules & FAQs

---

## 🛠️ Tech Stack

| Layer    | Technology            |
| -------- | --------------------- |
| Frontend | HTML, CSS, JavaScript |
| Backend  | Flask (Python)        |
| Database | SQLite                |
| ORM      | SQLAlchemy            |

---

## 📸 Screenshots

### 🏠 Home Page

![Home](screenshots/home.png)

### ℹ️ About Page

![About](screenshots/about.png)

### 🏅 Facilities

![Facilities](screenshots/facilities.png)

### 📅 Events

![Events](screenshots/events.png)

### 📊 Timetable

![Timetable](screenshots/timetable.png)

### 🎟️ Booking Entry

![Booking](screenshots/booking-entry.png)

### 🎯 Select Sport

![Select Sport](screenshots/select-sport.png)

### 🏸 Booking UI

![Booking UI](screenshots/booking-ui.png)

### 📋 My Bookings

![My Bookings](screenshots/my-bookings.png)

### 🔐 OTP Verification

![OTP](screenshots/otp.png)

### 📞 Contact Page

![Contact](screenshots/contact.png)

### ❓ FAQ

![FAQ](screenshots/faq.png)

---

## ⚙️ Installation

### 1️⃣ Clone Repo

```bash
git clone https://github.com/your-username/bvrit-sports-complex.git
cd bvrit-sports-complex
```

### 2️⃣ Setup Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run App

```bash
python app.py
```

### 🌐 Open

```
http://127.0.0.1:5000/
```

---

## 📂 Project Structure

```bash
BVRIT-Sports-Complex/
│
├── static/
├── templates/
├── screenshots/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🔐 Admin Capabilities

* 📊 View all bookings
* 📁 Export to Excel
* 🔒 Restricted admin access

---

## 📈 Future Improvements

* 💳 Payment integration
* 📱 Mobile app
* 🔔 Notifications system
* 📊 Analytics dashboard
* 🤖 Smart booking suggestions

---

## 👩‍💻 Author

**Thanuja**

---

## ⭐ Support

If you like this project:

🌟 Star the repo
🍴 Fork it
📢 Share it

---

## 📜 License

This project is for educational purposes.
