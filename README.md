# 🐞 Advanced Bug Tracker & Task Management System

An advanced web-based Bug Tracker and Task Management System developed using Django to help teams manage bugs, tasks, assignments, priorities, deadlines, notifications, and project progress efficiently.

---

## 📌 Project Overview

The Advanced Bug Tracker & Task Management System is designed to provide a centralized platform for managing software development tasks and bugs.

The system provides separate functionalities for administrators and users, allowing administrators to manage users, tasks, and bugs while users can view and manage their assigned work.

---

## 🎯 Objectives

- Manage software bugs efficiently
- Create and assign tasks to users
- Track task and bug status
- Manage priorities and severity levels
- Provide role-based access
- Notify users about important activities
- Monitor project progress through dashboards
- Provide analytical insights using charts
- Maintain an organized workflow for software development teams

---

## ✨ Key Features

### 👨‍💼 Admin Dashboard

- View total users
- View total tasks
- View total bugs
- Manage users
- Create and assign tasks
- Assign bugs to users
- Monitor task and bug status
- View project analytics
- View charts and statistics

### 👤 User Dashboard

- View assigned tasks
- View assigned bugs
- Update task status
- Update bug status
- View deadlines
- Receive notifications
- Track personal work progress

### 🐞 Bug Management

- Create bugs
- Assign bugs to users
- Set bug priority
- Set bug severity
- Track bug status
- Update bug information
- Archive bugs
- Maintain bug timestamps

### ✅ Task Management

- Create tasks
- Assign tasks
- Set task deadlines
- Set task priority
- Track task status
- Monitor task progress

### 🔔 Notification System

The system provides notifications to users for relevant task and bug-related activities.

### 📊 Analytics & Visualization

The dashboard provides visual insights into project activities, including task and bug statistics.

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

### Backend
- Python
- Django

### Database
- SQLite

### Deployment
- Render

### Development Tools
- Git
- GitHub
- Visual Studio Code

---

## 🏗️ System Architecture

```text
User
  │
  ▼
Web Interface
  │
  ▼
Django Application
  │
  ├── Authentication & Authorization
  ├── User Management
  ├── Task Management
  ├── Bug Management
  ├── Notification System
  └── Analytics Dashboard
  │
  ▼
SQLite Database
