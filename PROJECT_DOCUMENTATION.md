# Bug Tracker Project Documentation

## 0. Project Summary For Report

### 0.1 Abstract

The Bug Tracker project is a web-based issue and task management system developed using Django. The application helps teams create, assign, track, and resolve software bugs and operational tasks through role-based workflows. It centralizes status updates, comments, file attachments, notifications, and workload analytics in a single interface.

### 0.2 Problem Statement

Teams often manage bugs and tasks across disconnected channels, causing delayed updates, missing context, and poor visibility. This project addresses that gap by providing a structured platform where admins and assignees collaborate with traceable actions.

### 0.3 Objectives

-   Build a role-based system for issue and task lifecycle management.
-   Provide dashboards for operational visibility (open/closed bugs, workload, overdue tasks).
-   Enable collaboration through comments and file attachments.
-   Improve responsiveness with in-app notifications and read/unread controls.
-   Enforce safer admin actions for sensitive operations (deletions and user management).

### 0.4 Implementation Summary

The system is implemented with Django views, models, and template rendering. It uses SQLite for data persistence, Bootstrap-based responsive UI for usability, and server-side filtering/pagination for scalable list pages. Notifications are generated automatically on key events (assignment, comment, status change).

### 0.5 Key Outcomes

-   End-to-end bug and task workflows were implemented successfully.
-   Admin and regular-user permissions are separated by route-level checks.
-   Dashboards and notification center provide real-time operational visibility.
-   Attachment handling supports metadata display and image preview.
-   Critical destructive actions are restricted to POST-based confirmation flows.

### 0.6 Conclusion

The project delivers a practical and extensible foundation for team-level defect and task management. It is suitable for development/demo deployment and can be further expanded with API-first integration, audit history, and production-grade deployment settings.

## 1. Project Overview

This is a Django-based bug and task tracking web application with role-based access for admin and regular users.

Core capabilities:

-   User authentication (register, login, logout)
-   Bug management (create, list, update, delete)
-   Task management (create, list, update, delete)
-   Comments for bugs and tasks
-   File attachments for bugs with image preview and file metadata
-   Notification center with read/unread state
-   Admin user management (delete users, reset user passwords)
-   Dashboard metrics for workload and tracking
-   Light/dark theme toggle with persistence

## 2. Tech Stack

-   Backend framework: Django 5.1.2
-   Language: Python
-   Database (current default): SQLite (db.sqlite3)
-   UI: Django templates + Bootstrap 5 + Font Awesome
-   Image/file handling: Pillow
-   Optional dependencies present: djangorestframework, django-filter, psycopg

## 3. Project Structure

Top-level working project folder:

-   bugtracker/

Important files/folders inside it:

-   manage.py: Django management entry point
-   db.sqlite3: SQLite database file
-   bugtracker/settings.py: Django settings
-   bugtracker/urls.py: Root URL routes
-   tracker/models.py: Database models
-   tracker/views.py: View logic and business rules
-   tracker/urls.py: App routes
-   templates/: HTML templates
-   static/: static assets
-   media/: uploaded files (attachments)
-   tracker/migrations/: DB migrations

## 4. User Roles and Access

### Admin (superuser)

-   Access to admin dashboard
-   Add/edit/delete bugs and tasks
-   Manage users (delete user, change password)
-   Delete bug attachments
-   View global metrics and notifications

### Regular user

-   View/update assigned bugs and tasks
-   Add comments on assigned records
-   View own notifications
-   Cannot access admin-only actions

## 5. Data Model Summary

Defined in tracker/models.py.

### Bug

-   title, description
-   priority: Low/Medium/High
-   status: Open/In Progress/Closed
-   severity: Trivial/Minor/Major/Critical
-   assigned_to (User)
-   created_at, updated_at
-   archive fields: is_archived, archived_at, archived_by

### Task

-   title, description
-   status: Pending/In Progress/Done
-   assigned_to (User)
-   due_date
-   created_at, updated_at
-   archive fields: is_archived, archived_at, archived_by

### BugComment

-   bug, author, content, created_at

### TaskComment

-   task, author, content, created_at

### BugAttachment

-   bug, file, file_name, file_size, file_type, description, uploaded_by, created_at
-   helper properties:
    -   is_image
    -   size_label

### Notification

-   recipient, actor, message
-   optional links to bug/task
-   is_read, created_at

## 6. Main URL Endpoints

Defined in tracker/urls.py.

Auth and home:

-   / -> login
-   /register/ -> user registration
-   /logout/ -> logout

Dashboards:

-   /dashboard/
-   /admin-dashboard/

Bug flows:

-   /add-bug/
-   /bugs/
-   /update-bug//
-   /delete-bug// (POST)
-   /delete-attachment// (POST)

Task flows:

-   /add-task/
-   /tasks/
-   /update-task//
-   /delete-task// (POST)

Notifications:

-   /notifications/
-   /notifications//toggle/ (POST)
-   /notifications/mark-all/ (POST)

Admin user management:

-   /users/
-   /users/delete// (POST)
-   /users/change-password//

## 7. Functional Features

### 7.1 Dashboards

-   Bug counters (total/open/closed)
-   Task counters
-   Overdue tasks
-   Today workload
-   Unread notifications count

### 7.2 Bug and Task Lists

-   Search
-   Filtering (status, priority, assigned user where applicable)
-   Pagination (8 per page)

### 7.3 Update Pages

-   Status updates
-   Comments
-   Attachments for bugs
-   Notification generation on key events

### 7.4 Notifications

-   Unread badge in top bar
-   Notification list page
-   Toggle read/unread per item
-   Mark all as read action

### 7.5 Admin User Management

-   List non-superuser users
-   Change user password
-   Delete user with confirmation modal

## 8. Frontend and UX Notes

-   Base layout in templates/base_app.html
-   Separate auth layout in templates/base_auth.html
-   Theme toggle stores preference in localStorage key: bugtracker-theme
-   Bootstrap modals used for confirmation actions
-   Responsive behavior for sidebar/topbar on smaller screens

## 9. Security and Validation Notes

-   Admin-only endpoints protected with user_passes_test(is_admin)
-   Login required on user routes
-   Deletions are POST-based in critical places
-   CSRF tokens used in POST forms
-   Prevent self-delete and superuser delete in users management

## 10. Configuration Notes

From bugtracker/settings.py:

-   DEBUG = True (development mode)
-   ALLOWED_HOSTS = []
-   DB engine: sqlite3
-   Media:
    -   MEDIA_URL = /media/
    -   MEDIA_ROOT = BASE_DIR / media
-   Login redirects:
    -   LOGIN_URL = /
    -   LOGIN_REDIRECT_URL = /dashboard/
    -   LOGOUT_REDIRECT_URL = /

## 11. Requirements File

requirements.txt currently contains:

-   Django==5.1.2
-   reportlab==4.2.2
-   psycopg[binary]==3.2.4
-   djangorestframework==3.14.0
-   Pillow==10.2.0
-   django-filter==24.1

## 12. Development Workflow

Typical loop:

1.  Activate environment
2.  Run migrations
3.  Start server
4.  Test in browser
5.  Use manage.py check before finalizing changes

Useful commands:

-   python manage.py check
-   python manage.py makemigrations
-   python manage.py migrate
-   python manage.py createsuperuser

## 13. Current State Summary

The project is currently set up and functional with:

-   Working dashboards
-   Working notification system
-   Working user deletion flow via modal and POST
-   Working admin quick notification action in top bar dropdown
-   Existing data persisted in sqlite database