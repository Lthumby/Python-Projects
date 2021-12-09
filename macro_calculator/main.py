import subprocess
import numbers
import win32console
import time
import os
import keyboard
import sys
import pathlib
#import matplotlib.pyplot as plt 
#import numpy as np
# was going to add pie chart showing macro %, but couldn't get past bug while turning into exe
win32console.SetConsoleTitle("MACRO CALCULATOR")



class main():
	def __init__(self):
		self.bw = 0
		self.height = ""
		self.age = 0
		self.active_lvl = 0
		self.bmr = 0
		self.caloric_intake = 0
		self.choice = 0
		self.cmd_size = 'mode 40, 20'
		self.str_ = ""
		self.path = pathlib.Path(__file__).parent.resolve()
		print(self.path)
		os.system(self.cmd_size)
		self.make_dir = "info"
		self.folder = f'{self.path}/info/'

		try:
			os.mkdir(self.make_dir) # If folder not there, make it
		except:
			pass

		def bmr_calc(weight, height, age, active_lvl):
			bmr_find = 66 + (6.2 * int(weight)) + (12.7 * int(height)) - (6.76 * int(age))
			
			if active_lvl == 1: # Little to no exercise
				bmr_find *= 1.2

			elif active_lvl == 2: # Exercise 1-3x a week
				bmr_find *= 1.375

			elif active_lvl == 3: # Exercise 3-5x a week
				bmr_find *= 1.55

			elif active_lvl == 4: # Exercise 6-7x a week
				bmr_find *= 1.725

			elif active_lvl == 5: # INTENSE have exercise
				bmr_find *= 1.9

			else:
				print("Number out of range")
				time.sleep(1)
				subprocess.call("cls", shell=True)
				main_screen()

			return bmr_find


		def add_surplus(_bmr):
			surplus = _bmr + 300
			return surplus

		def add_deficit(_bmr):
			deficit = _bmr - 300
			return deficit

		def find_protein(weight):
			return weight # 1g protein per lb of bodyweight

		def find_fat(calories):
			fats = 0.25 * int(calories)
			fat_grams = fats / 9
			return int(fat_grams)

		def find_carbs(calories, protein, fat): #protein and fat CALORIES
			carb_add = int(protein) + int(fat)
			carb = int(calories) - int(carb_add)
			carb_grams = int(carb) / 4
			return int(carb_grams)

		def gram_to_calories(protein, fats, carbs, cals):
			fat = fats * 9
			carb = carbs * 4
			prot = protein * 4

			print(f'''
 MACROS VIEWED AS CALORIES
-------------------------
 PROTEIN: {prot} calories
 FAT: {fat} calories
 CARBS: {carb} calories
-------------------------
 TOTAL CALORIES:
 {int(cals)}	''')
			info_ = f'''
 MACROS VIEWED AS CALORIES
-------------------------
 PROTEIN: {prot} calories
 FAT: {fat} calories
 CARBS: {carb} calories
-------------------------
 TOTAL CALORIES:
 {int(cals)}'''
			with open(f"{self.folder}/MACROS.txt", "a") as f:
				f.write(info_)

		def val_error():
			print("Enter numbers, not letters")
			time.sleep(2)
			subprocess.call("cls", shell=True)
			main_screen()

		def macro_find(bodyweight, cal_intake):
			# IDENTIFYING MACROS
			protein = find_protein(bodyweight)
			fats = find_fat(cal_intake)

			#fat  +  protein calories
			protein_cal = protein * 4
			fat_cal = fats * 9

			carbs = find_carbs(cal_intake, protein_cal, fat_cal)
			carb_cal = carbs * 4

			print(f'''
 MACROS:
-------------------------
 Protein: {protein}g\n Fats: {fats}g\n Carbs: {carbs}g
-------------------------
''')
			info_ = f'''
 MACROS:
-------------------------
 Protein: {protein}g\n Fats: {fats}g\n Carbs: {carbs}g
-------------------------
'''

			with open("info/MACROS.txt", "w") as f:
				f.write(str(info_))
				#f.write(str(gram_to_calories(protein, fats, carbs, cal_intake)))

			gram_to_calories(protein, fats, carbs, cal_intake)

			# PIE CHART SHIT
			total_cals = cal_intake

			protein_1 = protein_cal / total_cals
			protein_prc = float(protein_1) * 100
			p_prc = round(protein_prc, 1)

			fats_1 = fat_cal / total_cals
			fats_prc = float(fats_1) * 100
			f_prc = round(fats_prc, 1)

			carbs_1 = carb_cal / total_cals
			carbs_prc = float(carbs_1) * 100
			c_prc = round(carbs_prc, 1)
			'''
			chart = np.array([protein_cal, fat_cal, carb_cal])
			labels = [f"Protein {p_prc}%", f"Fats {f_prc}%", f"Carbs {c_prc}%"]
			plt.pie(chart,  labels=labels)s
			plt.savefig("piechart.png")
			'''


		def user_info(weight, height, age, bmr, cals, act_lvl, option):
			if option == 1:
				self.str_ = "user_surplus = +"
			elif option == 2:
				self.str_ = "user_deficit = -"
			elif option == 3:
				self.str_ = "user_maintanence ="

			with open(f"{self.folder}user_info.txt", "w") as f:
				f.write(f'''
user_weight = {weight} lbs
user_height = {height} inches
user_age = {age} y/o

user_BMR = {bmr} calories
{self.str_}300
user_fat% = 25% of calories


Where did I get the calculations?
---------------------------------
LINK: https://www.youtube.com/watch?v=g8nFi6gCTYc


						''')

		def main_screen():
			subprocess.call("cls", shell=True)
			
			
			print(f'''
DEVELOPED BY: lthum
8==================D

				''')

			try:
				self.bw = int(input("How much do you weigh?: "))
				it_is = True
			except ValueError:
				it_is = False
				val_error()

			self.height = str(input("Enter Height ex.(6'2) OR (74): "))
			letter_ranges = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
			for x in letter_ranges:
				if x in self.height:
					val_error()
				
				

			

			try:
				self.age = int(input("Enter Age (15-99): "))
				it_is = True
			except ValueError:
				it_is = False
				val_error()


			if self.age < 15:
				print("Age out of range")
				time.sleep(1)
				subprocess.call("cls", shell=True)
				main_screen()
			elif self.age > 99:
				print("Age out of range")
				time.sleep(1)
				subprocess.call("cls", shell=True)
				main_screen()
			self.active_lvl = int(input(f'''
How active are you?
1. Little to no exercise
2. Exercise 1-3x a week
3. Exercise 3-5x a week
4. Exercise 6-7 a week
5. INTENSE exercise every day
: '''))


			subprocess.call("cls", shell=True)
			# If user puts {5'7} <- ex // as ans, converts to inches
			if "'" in self.height:
				height_conversion = self.height.split("'")
				self.height = int(height_conversion[0]) * 12 + int(height_conversion[1])
				
			c_1 = int(input(f'''
[1] BULKING
[2] CUTTING
[3] MAINTAINING
: '''))
			self.bmr = (bmr_calc(self.bw, self.height, self.age, self.active_lvl))

			if c_1 == 1: # BULKING
				subprocess.call("cls", shell=True)
				self.cmd_size = 'mode 30, 20'
				os.system(self.cmd_size)
				self.caloric_intake = add_surplus(self.bmr)
				macro_find(self.bw, self.caloric_intake)
				user_info(self.bw, self.height, self.age, self.bmr, self.caloric_intake, self.active_lvl, 1)



				while True: 
					if keyboard.is_pressed('q'):
						sys.exit()
					
				

				
			elif c_1 == 2: # CUTTING
				subprocess.call("cls", shell=True)
				self.cmd_size = 'mode 30, 20'
				os.system(self.cmd_size)
				self.caloric_intake = add_deficit(self.bmr)
				macro_find(self.bw, self.caloric_intake)
				user_info(self.bw, self.height, self.age, self.bmr, self.caloric_intake, self.active_lvl, 2)

				while True: 
					if keyboard.is_pressed('q'):
						sys.exit()
					
			elif c_1 == 3: # MAINTAINING
				subprocess.call("cls", shell=True)
				self.cmd_size = 'mode 30, 20'
				os.system(self.cmd_size)
				self.caloric_intake = self.bmr
				macro_find(self.bw, self.caloric_intake)
				user_info(self.bw, self.height, self.age, self.bmr, self.caloric_intake, self.active_lvl, 3)

				while True: 
					if keyboard.is_pressed('q'):
						sys.exit()
					


			else:
				print("VALUE NOT REGISTERED")
				time.sleep(1)
				subprocess.call("cls", shell=True)
				main_screen()
		


		main_screen()
main()
