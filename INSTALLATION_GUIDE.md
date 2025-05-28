# 🚀 Quick Start Guide for Non-Technical Users

> **A step-by-step guide to get the Risk Management System running on your computer**

## 📋 What You'll Need

- A computer with Windows, Mac, or Linux
- About 30 minutes of your time
- An internet connection for downloading

## 🛠️ Step-by-Step Installation

### Step 1: Install Python

**Python** is the programming language that powers our application.

1. **Download Python**:
   - Go to [python.org/downloads](https://python.org/downloads/)
   - Click the big yellow "Download Python" button
   - This will download Python 3.12 or newer

2. **Install Python**:
   - Run the downloaded file
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" during installation
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation**:
   - Open Command Prompt (Windows) or Terminal (Mac/Linux)
   - Type: `python --version`
   - You should see something like "Python 3.12.x"

### Step 2: Download the Project

1. **Download the Code**:
   - Go to the GitHub repository page
   - Click the green "Code" button
   - Select "Download ZIP"
   - Extract the ZIP file to your Desktop or Documents folder

### Step 3: Set Up the Application

1. **Open Command Prompt/Terminal**:
   - Navigate to the project folder
   - Type: `cd path/to/risk-management-system`
   - (Replace "path/to" with the actual location where you extracted the files)

2. **Install Required Packages**:
   ```bash
   pip install -r requirements.txt
   ```
   - This will download and install all necessary components
   - It may take a few minutes

3. **Set Up the Database**:
   ```bash
   python manage.py migrate
   ```
   - This creates the database structure

4. **Create Your Admin Account**:
   ```bash
   python manage.py createsuperuser
   ```
   - Enter your desired username, email, and password
   - Remember these credentials - you'll need them to log in

### Step 4: Start the Application

1. **Start the Server**:
   ```bash
   python manage.py runserver
   ```
   - You should see a message saying the server is running

2. **Open Your Browser**:
   - Go to: `http://127.0.0.1:8000`
   - You should see the Risk Management System homepage

3. **Log In**:
   - Click "Login" in the top navigation
   - Use the username and password you created in Step 3.4

## 🎉 Congratulations!

You now have the Risk Management System running on your computer!

## 🔄 How to Use It Again Later

Whenever you want to use the application:

1. Open Command Prompt/Terminal
2. Navigate to the project folder: `cd path/to/risk-management-system`
3. Start the server: `python manage.py runserver`
4. Open your browser to: `http://127.0.0.1:8000`

## 🆘 Troubleshooting

### Problem: "Python is not recognized"
**Solution**: You need to add Python to your PATH. Reinstall Python and make sure to check "Add Python to PATH".

### Problem: "pip is not recognized"
**Solution**: This usually means Python wasn't installed correctly. Try reinstalling Python.

### Problem: "Port already in use"
**Solution**: Try using a different port: `python manage.py runserver 8001`

### Problem: Can't access the website
**Solution**: Make sure the server is running and try these URLs:
- `http://127.0.0.1:8000`
- `http://localhost:8000`

## 📞 Need Help?

If you encounter any issues:

1. Check the error message carefully
2. Try restarting your computer and following the steps again
3. Contact the developer (see main README for contact information)

## 🔒 Security Note

This setup is for **development and testing only**. For production use in a business environment, additional security configuration is required.
