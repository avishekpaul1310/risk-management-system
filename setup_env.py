#!/usr/bin/env python
"""
Script to set up the environment file for the Risk Management System.
This will create a .env file based on the .env.example template.
"""
import os
import shutil
import random
import string
import sys

# Function to generate a random Django secret key
def generate_secret_key(length=50):
    """Generate a random Django secret key."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*(-_=+)"
    return ''.join(random.choice(chars) for _ in range(length))

def setup_env_file():
    """Set up the .env file from .env.example"""
    # Check if .env.example exists
    if not os.path.exists('.env.example'):
        print("Error: .env.example file not found.")
        return False
    
    # Check if .env already exists and ask before overwriting
    if os.path.exists('.env'):
        choice = input(".env file already exists. Overwrite? (y/n): ")
        if choice.lower() != 'y':
            print("Setup cancelled.")
            return False
    
    # Copy .env.example to .env
    try:
        shutil.copy('.env.example', '.env')
        print(".env file created from template.")
    except Exception as e:
        print(f"Error creating .env file: {e}")
        return False
    
    # Generate a Django secret key
    secret_key = generate_secret_key()
    
    # Read the .env file and uncomment/update the SECRET_KEY
    try:
        with open('.env', 'r') as file:
            lines = file.readlines()
        
        with open('.env', 'w') as file:
            for line in lines:
                if line.startswith('# SECRET_KEY='):
                    # Uncomment and replace the secret key
                    file.write(f'SECRET_KEY={secret_key}\n')
                else:
                    file.write(line)
        
        print("Django SECRET_KEY generated and added to .env file.")
        print("")
        print("IMPORTANT: You need to add your Google Gemini API key in the .env file:")
        print("1. Get an API key from https://makersuite.google.com/app/apikey")
        print("2. Edit the .env file and update the GEMINI_API_KEY value")
        print("")
        
        return True
    
    except Exception as e:
        print(f"Error updating .env file: {e}")
        return False

if __name__ == "__main__":
    print("Setting up environment for Risk Management System...")
    if setup_env_file():
        print("Setup complete!")
    else:
        print("Setup failed.")
        sys.exit(1)
