from firebase import Firebase
import pyrebase
from collections.abc import Mapping, MutableMapping


# colors
from colorama import Fore, Style, init

# control
import os
from os import path
import subprocess
import time
import socket

# files
import json
from main import *

class auth:
	def __init__(self):
		# color
		self.r = Fore.RED
		self.g = Fore.GREEN
		self.y = Fore.YELLOW
		self.b = Fore.BLUE
		self.m = Fore.MAGENTA
		self.c = Fore.CYAN
		self.w = Fore.WHITE

		self.default = "blue"
		self.out = self.b
		self.inside = self.c

		firebaseConfig = {
			"apiKey": "",
    		"authDomain": "",
    		"databaseURL": "",
    		"projectId": "",
    		"storageBucket": "",
    		"messagingSenderId": "",
    		"appId": "",
    		"measurementId": ""
		}
		firebase = pyrebase.initialize_app(firebaseConfig) # loads config

		db = firebase.database() # database
		#db_data = {}





################################################################################################################################################################




# AUTHENTICATION ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
		auth = firebase.auth() # authentication
	
		def is_user(username, password):
			# checking if {username} is in database
			if path.exists("details.txt"):
				usernames = db.child('users').get()
				with open("details.txt", "r") as file:
					x = file.read()
					uname = x.split(":")[0]
					time.sleep(1)
					pword = x.split(":")[1]
					#uemail = x.split(":")[2]
				u_included = False
				valid_user = False
				for user_n in usernames.each():
					users = user_n.val()
					u_user = str(users)

					#print(users)
					if username == uname:
						if username in u_user:
							try:
								u_included = True
								if u_included == True:
									# what to do when {username} IS found in database
									#print(f"{self.g}{username}, was found in the database")
									valid_user = True

								else:
									u_included = False
							except:
								u_included = False
				if u_included == False:
					# what to do when {username} is NOT found in database
					#print(f"{self.out}{username}, was not found in the database")
					time.sleep(2)
					valid_user = False
					auth_page()

				# checking if {password} is in {username} database

				passwords = db.child('users').child(username).get()
				p_included = False
				valid_pass = False
				for pass_w in passwords.each():
					passw = pass_w.val()
					u_pass = str(passw)
					if pword == password:
						if password in u_pass:
							try:
								p_included = True
								if p_included == True:
									# what to do when {password} IS found in the database
									#print(password, "was found in the database")
									valid_pass = True
								else:
									p_included = False
							except:
								p_included = False
				if p_included == False:
					# what to do when  {password} is NOT found in database
					#print(password, "was not found in the database")
					time.sleep(2)
					valid_pass = False
					auth_page()

				# once valid_user and valid_pass are both true it checks desktop name and machine id
				if valid_user and valid_pass == True:
					id_name = db.child('users').child(username).get()
					current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip() # grabs user hwid
					hostname = socket.gethostname() # grabs users desktopname
					c_included = False
					confirmed_user = False
					for m_id in id_name.each():
						n_id = m_id.val()
						u_id = str(n_id)
						if current_machine_id in u_id:
							try:
								# what to do when {machine_id} IS found in the database
								c_included = True
								if c_included == True:
									#print(current_machine_id, "was found in users database")
									confirmed_user = True
								else:
									c_included = False
							except:
								c_included = False
					if c_included == False:
						# what to do when {machine_id} is NOT found in database
						#print(current_machine_id, "was not found in the users database")
						time.sleep(2)
						confirmed_user = False
						auth_page()

				if confirmed_user == True:
					return True # user can continue into the program
				else:
					return False # user cannot continue into the program
			else:
				print(f"\n{self.out}Missing details.txt file")



		def get_id(): # grabs user's
			current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
			return current_machine_id

		def get_ip():
			hostname = socket.gethostname()
			ipAddr = socket.gethostbyname(hostname)
			return ipAddr

		def get_name():
			hostname = socket.gethostname()
			return hostname


		def valid_token(token):
			#reading through tokens
			#token = "e8UP0Z5VHFcHzIb_GhyBB5dyZbunoLMpsmWyVHaQFDqAStE"
			keys = db.child('tokens').get()
			in_token = False
			for key in keys.each(): # checks to see if token is in the token list
				k_v = key.val()
				if k_v in token:
					in_token =  True

			if in_token == True:
				return True
			else:
				return False
			return False

		def used_token(token):
			used_tokens = db.child('used_tokens').get()
			works = True
			for used_token in used_tokens.each(): # takes the valid token and puts it into used_tokens
				ut_v = used_token.val()
				utv = str(ut_v)
				#print(utv)
				#print(utv, "WORK")

				if token in utv: # looping throuhg {used_tokens} and checks if they are in there
					try:
						works = False
						if works == False:
							#print(token, " doesnt work")
							return False
						else:
							works = True
					except:
						works = True
						#print("works")
			if works == True:
				#print(token, " works")
				return True



		def taken_user(username):
			user_info = db.child('users').get()
			taken_user = False
			for user in user_info.each():
				u_name = user.val()
				uname = str(u_name)
				if username in uname:
					try:
						taken_user = True
						if taken_user == True:
							return True 		#if True, the username cannon be used
						else:
							return False # username ISNT taken
					except:
						taken_user = False
			if taken_user == False:
				return False

		def token_mover(token):
			token_data = {username:token}
			db.child("used_tokens").set(token_data) # creates a path to {used_tokens} and puts the used token in there

		

		def auth_ans():
			a_ans = input(f"{self.out}[{self.inside}>{self.out}]{self.w} ")

			# login
			if a_ans == "1":
				count = 0
				subprocess.call("cls", shell=True)
				if path.exists("details.txt"):
					try:
						with open("details.txt", "r") as file:
							x = file.read()
							username = x.split(":")[0]
							password = x.split(":")[1]
							email = x.split(":")[2]
							if is_user(username, password) == True:
								
								auth.sign_in_with_email_and_password(email,password)
								print(f"{self.g}Welcome ", username)
								time.sleep(2)
								main()
							elif is_user(username, password) != True:
								print(f"{self.r}Incorrect username or password\nTry again...")
								time.sleep(2)
								#auth_page()
								sys.exit(1)
								'''
							else:
								print(f"{self.out}\nAn error has occured\nPlease try again...")
								time.sleep(1)
								'''

					except:
						print(f"{self.r}\nAn error has occured\nPlease try again... FOUND IT")
						time.sleep(2)
						auth_page()
				elif path.exists("details.txt","r") != True:
					subprocess.call("cls", shell=True)
					u_input = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your username: {self.w}")
					e_input = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your email: {self.w}")
					p_input = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your password: {self.w}")
					if is_user(u_input, p_input) == True:
						print(e_input,"\n", p_input)
						auth.sign_in_with_email_and_password(e_input, p_input)
						print(f"{self.g}Welcome ", username)
						time.sleep(2)
						main()
					else:
						print(f"missing details.txt")
						time.sleep(2.5)
						auth_page()
				else:
					print("error code 404")



			# register
			elif a_ans == "2":
				subprocess.call("cls", shell=True)
				user_token = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your token: {self.w}")
				json_file = False
				if len(user_token) <= 47:
					if valid_token(user_token) == True:
						if used_token(user_token) == True:
							username = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter a username: {self.w}")
							if taken_user(username) == False:
								email = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your email: {self.w}")
								password = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Enter your password: {self.w}")
								confirmpass = input(f"{self.out}[{self.inside}*{self.out}]{self.inside}Confirm your password: {self.w}")
								if password == confirmpass:
									print(f"{self.g}Passwords match!")
									print(f"{self.g}Creating User...\n")
									token_data = {username:user_token}
									user_id = get_id()
									user_ip = get_ip()
									user_name = get_name()
									try:
										json_file = True
										auth.create_user_with_email_and_password(email,password)
										with open("details.txt", "w") as file:
											file.write(f"{username}:{password}:{email}")
										print(f"{self.g}User Created!")
										db.child("used_tokens").child(username).set(token_data)
										user_data = {'email':email, 'password':password, 'token':user_token, 'user_machine_id':user_id, 'user_ip': user_ip, 'user_name':user_name}
										db.child("users").child(username).child(username).set(user_data) # creates a path for {username} and sorts their email\password
										time.sleep(1.5)
										auth_page()
									except:
										json_file = False
										print(f"{self.out}Email is already taken\nTry Again...")
										time.sleep(2)
										auth_page()
								
								elif valid_token(user_token) == False or used_token(user_token) == False:
									if valid_token(user_token) == False:
										print(f"{self.r}This token isn't a valid token\n\nTry Again...")
										time.sleep(2)
									elif used_token(user_token) == False:
										print(f"{self.r}This token has already been activated\n\nTry Again...")
									else:
										print(f"{self.r}INVALID TOKEN\n\nTry Again...")

								
								

								else:
									print(f"{self.r}Passwords don't match\nTry again...")
									time.sleep(2)
									auth_page()
							else:
								print(f"{self.r}Username already taken")
								time.sleep(2)
								auth_page()

						else:
							print(f"{self.r}Your token is already in-use\nTry Again...")
							time.sleep(2.3)
							auth_page()
					else:
						print(f"{self.r}Token isn't valid\nTry again...")
						time.sleep(2)
						auth_page()
				else:
					print(f"{self.r}Token isn't valid\nTry again...")
					time.sleep(2)
					auth_page()
				if json_file == True:
					with open("settings.json") as f:
						data = json.load(f)
						settings_default = {"color":"RED"}
					with open("settings.json", "w") as ff:
						json.dump(data, f, indent=4)




				

			elif a_ans == "3": # exit
				pass



			elif a_ans =="4": # admin-login
				pass

			else:
				auth_page()








		def auth_page():
			subprocess.call("cls", shell=True)
			self.auth_content = print(f'''{self.out}
[{self.inside}1{self.out}]{self.inside} Login	| {self.out}
[{self.inside}2{self.out}]{self.inside} Register	| {self.out}
[{self.inside}3{self.out}]{self.inside} Exit	| 	  {self.out}

[{self.inside}4{self.out}]{self.inside} Admin	| 	  {self.out}
''')
			auth_ans()
			return self.auth_content # cant use print otherwise "none" prints with it
			

		auth_page()
		
auth()