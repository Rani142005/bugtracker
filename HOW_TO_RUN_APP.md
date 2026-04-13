# How To Run This App

This guide is for your current setup using the existing conda environment: computer_vision.

## 1. Open Terminal
Open a terminal in:
C:/Users/acer/Downloads/bug_project


## 2. Activate Environment
Use your existing environment:
conda activate computer_vision


## 3. Run the Server (Recommended Command)
Run from project root using full manage.py path:
python bugtracker/manage.py runserver

Then open:
http://127.0.0.1:8000/


## 4. Alternative Run Method
You can also cd into app folder first:
cd bugtracker
python manage.py runserver

This is equivalent to the recommended command.


## 5. Why You Saw "manage.py not found" Earlier
That happens when command is run from:
C:/Users/acer/Downloads/bug_project
with this command:
python manage.py runserver

In that folder, manage.py does not exist directly.
It exists at:
C:/Users/acer/Downloads/bug_project/bugtracker/manage.py


## 6. First-Time Setup (If Needed)
Only if database/migrations are not ready:
1. conda activate computer_vision
2. python bugtracker/manage.py migrate
3. python bugtracker/manage.py createsuperuser
4. python bugtracker/manage.py runserver


## 7. Verify App Health
Run check command:
python bugtracker/manage.py check

Expected output:
System check identified no issues (0 silenced).


## 8. Stop the Server
In the terminal where runserver is active, press:
Ctrl + C

If a background server process remains, stop it in PowerShell:
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*manage.py*runserver*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }


## 9. Common Troubleshooting
### Problem: Address already in use
Use another port:
python bugtracker/manage.py runserver 8001

### Problem: Module not found / Django not found
Ensure correct environment is active:
conda activate computer_vision

### Problem: Static or media files not showing
Confirm DEBUG=True in settings for development and use the runserver command from this guide.

### Problem: Login works but page data looks wrong
Make sure you are logged in as the expected user (notifications and assignments are user-specific).


## 10. Quick Command Reference
- Start server:
  python bugtracker/manage.py runserver
- Run checks:
  python bugtracker/manage.py check
- Apply migrations:
  python bugtracker/manage.py migrate
- Create admin:
  python bugtracker/manage.py createsuperuser


## 11. Admin Credentials (Current Database)
Current admin accounts found in this project database:
- Username: admin
  - Email: admin@gmail.com
- Username: rani
  - Email: rani@gmail.com

Note:
- Passwords are securely hashed in Django and cannot be viewed directly.
- If you need login access, reset password using:
  - python bugtracker/manage.py changepassword admin
  - python bugtracker/manage.py changepassword rani
