import os
from os import system
import requests
from bs4 import BeautifulSoup
import yaml
import ctypes
import time
import tkinter as tk
from tkinter import filedialog
import subprocess
import zipfile

class AutoDownloadManager:
    def __init__(self):
        ctypes.windll.kernel32.SetConsoleTitleW("AutoLoad | dev: lthum")
        system('mode con: cols=70 lines=20')
        self.user_home_dir = os.path.expanduser("~")
        self.config_dir = os.path.join(self.user_home_dir, "auto_start_config.yml")

    def select_folder(self):
        print("Select desired path")
        time.sleep(1)  # Wait for 2 seconds
        folder_path = filedialog.askdirectory()
        if folder_path:
            print("Selected folder:", folder_path)
        else:
            print("No folder selected.")
        return folder_path

    def edit_config(self):
        username = input("Enter rc display name: ")
        password = input("Enter rc password: ")
        # Folder select
        path = self.select_folder()

        account_content = {
            "username": username,
            "password": password,
            "path": path,
        }
        if os.path.exists(self.config_dir):
            os.remove(self.config_dir)
            print("Deleted and recreating file now")
        # Creating and dumping data into the config file
        with open(self.config_dir, "w") as file:
            file.write(yaml.dump(account_content))
        try:
            # Get the file attributes
            attrs = ctypes.windll.kernel32.GetFileAttributesW(self.config_dir)

            # Add the hidden attribute (bitwise OR with 2)
            attrs |= 0x2

            # Set the updated attributes
            ctypes.windll.kernel32.SetFileAttributesW(self.config_dir, attrs)

        except Exception as e:
            print(f"Error setting hidden attribute: {e}")

    def setup_config(self):
        if not os.path.exists(self.config_dir):
            print("< Username and password are only stored on your local machine >")
            username = input("Enter rc display name: ")
            password = input("Enter rc password: ")

            # Folder select
            path = self.select_folder()
            account_content = {
                "username": username,
                "password": password,
                "path": path,
            }
            # Creating and dumping data into the config file
            with open(self.config_dir, "w") as file:
                file.write(yaml.dump(account_content))
            try:
                # Get the file attributes
                attrs = ctypes.windll.kernel32.GetFileAttributesW(self.config_dir)

                # Add the hidden attribute (bitwise OR with 2)
                attrs |= 0x2

                # Set the updated attributes
                ctypes.windll.kernel32.SetFileAttributesW(self.config_dir, attrs)

            except Exception as e:
                print(f"Error setting hidden attribute: {e}")

    def get_account_data(self):
        user, pword, path = "", "", ""
        if os.path.exists(self.config_dir):
            with open(self.config_dir, 'r') as file:
                acc_service = yaml.safe_load(file)
                user = acc_service.get("username", "")
                pword = acc_service.get("password", "")
                path = acc_service.get("path", "")
        return user, pword, path

    def display_account_data(self):
        username, password, path = self.get_account_data()
        print(f'''
CURRENT:
[*] Username: {username}
[*] Password: {password}
[*] Desired Path: {path}
              ''')

    def auto_download(self):
        username, password, path = self.get_account_data()
        if not username or not password or not path:
            print("Account data not found. Please set up your account first.")
            return

        login_url = 'https://recoil.club/forums/index.php?/login/'
        session = requests.session()

        try:
            response = session.get(login_url)
            response.raise_for_status()  # Check if the initial request was successful
        except requests.exceptions.RequestException as e:
            print(f"Failed to access login URL: {e}")
            time.sleep(2)
            return

        soup = BeautifulSoup(response.text, "html.parser")
        csrf_token = soup.find("input", {"name": "csrfKey"})["value"]
        ref_value = soup.find("input", {"name": "ref"})["value"]

        payload = {
            'auth': username,
            'password': password,
            'csrfKey': csrf_token,
            'ref': ref_value,
            '_processLogin': 'usernamepassword',
        }

        try:
            # Use the existing session for the POST request
            r = session.post(login_url, data=payload, allow_redirects=True)
            r.raise_for_status()  # Check if the login request was successful
        except requests.exceptions.RequestException as e:
            print(f"Failed to login: {e}")
            time.sleep(2)
            return

        print(f"Login status code: {r.status_code}")

        download_url = "https://recoil.club/forums/PH/ph_download.php"

        try:
            download_response = session.get(download_url)
            download_response.raise_for_status()  # Check if the download request was successful
            
        except requests.exceptions.RequestException as e:
            print(f"Failed to download: {e}")
            time.sleep(2)
            return


        # Get the content size of the downloaded file in bytes
        file_size = len(download_response.content)

        # Convert the size to kilobytes (KB)
        file_size_kb = file_size / 1024

        # Check if the file size is less than 3000 KB
        if file_size_kb < 3000:
            print(f"File size is less than 3000 KB. Login may not have been successful.")
            time.sleep(2)
            return


        # Save the downloaded file to your local system
        download_path = os.path.join(path, 'loader.zip')
        with open(download_path, 'wb') as file:
            file.write(download_response.content)

        print("Download completed successfully!")

        # Attempt to unzip the downloaded file
        try:
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(path)
            print("File successfully unzipped.")
        except zipfile.BadZipFile:
            print("Downloaded file is not a valid ZIP file.")
        except Exception as e:
            print(f"Error while unzipping the file: {e}")

        # Remove the downloaded ZIP file
        os.remove(download_path)
        print("Downloaded ZIP file removed.")

        time.sleep(1)
        print("Exiting Program...")
        time.sleep(0.5)
        exit(1)

if __name__ == "__main__":
    manager = AutoDownloadManager()
    manager.setup_config()

    while True:
        subprocess.call('cls', shell=True)
        manager.display_account_data()
        user_select = input(f'''
[1] Download loader
[2] Edit Config
<: ''')

        if user_select == "1":
            subprocess.call('cls', shell=True)
            print("Downloading loader.zip from https://recoil.club/forums/")
            manager.auto_download()
        elif user_select == "2":
            subprocess.call('cls', shell=True)
            manager.edit_config()
            subprocess.call('cls', shell=True)
        else:
            subprocess.call('cls', shell=True)
            print("Invalid option. Please try again.")
            time.sleep(0.5)
