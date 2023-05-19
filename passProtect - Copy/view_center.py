import time
import subprocess
import database

from os import system


    
def viewCenter(access = False):
    #auth = database.auth()
    system('mode con: cols=40 lines=20')
    if access == True or database.auth() == True:
        subprocess.call("cls", shell=True)
        print(f'''

    |---------Select Option---------|
    |                               |
    |  1. View Accounts             |
    |  2. Add New Account           |
    |                               |
    |                               |
    |                               |
    |                               |
    |-------------------------------|
''')
    selection = str(input("    <: "))
    if selection == "1":
        database.accountDisplay()
    elif selection == "2":
        database.addInfo()
        print('\n\n ADDING INFO')
        time.sleep(1)
        viewCenter(access=True)
    else:
        print("Please enter a valid entry")
        time.sleep(0.5)
        viewCenter()

viewCenter(access=False)