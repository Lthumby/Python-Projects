


from shutil import ExecError
from tempfile import TemporaryFile
from urllib.request import proxy_bypass
import multiprocessing
import os
import win32console

win32console.SetConsoleTitle("Mr.Naber LOL")
os.system('mode 40, 20')
os.system("cls")
# NORMAL/NO STOPLOSS

class Calculate:
    def __init__(self):
        # basic inputs
        self.deductable = int(input(f'''
ENTER DEDUCTABLE
----------------
'''))
        self._deductable = self.deductable
        self.coInsurance = input(f'''
ENTER CO-INSURANCE SPLIT
-------0.0,0.0----------
''')
        self.visitCost = str(input(f'''
ENTER VISIT COSTS
------0,0,0,0-----
'''))
        self.visitCost2 = self.visitCost
        self.coPays = str(input(f'''
ENTER ALL CO-PAYS
----0,0,0------
'''))
        self.stopLoss = int(input(f'''
ENTER STOPLOSS
----0 if none----
'''))
        self.newCost = []
        # debug inputs
        '''self.deductable = 5000
        self._deductable = self.deductable
        self.coInsurance = "0.7,0.3"
        self.visitCost = "3000,800,8000"
        self.visitCost2 = self.visitCost
        self.coPays = "25,50,100"
        self.stopLoss = 0
        '''
        # Co-Pay Map
        cpay = self.coPays.split(",")
        cpayMap = map(int, cpay)
        self.coPay = list(cpayMap) # <- list of all copays
        # Visit Costs Map
        vcosts = self.visitCost.split(",")
        visitMap = map(int, vcosts)
        self.visitCosts = list(visitMap) # <- list of all visit costs
        # Gathering Co-Insurance split
        coinsures = self.coInsurance.split(",")
        coinsMap = map(float, coinsures)
        self.coSplit = list(coinsMap)# <- list of the coInsurance
        # Blanks
        self.coPayTotal = 0
        self.youTotal = 0
        self.insureTotal = 0

        # Co-Pay = self.coPay (list)
        # Visit Cost = self.visitCosts (list)
        # Co-Insurance Split = self.coSplit (list)


        def coPayTotal(coPay):
            total = 0
            for x in range(len(coPay)):
                #print(x)
                total = total + coPay[x]
            return int(total)
            
        def deductableCalc(deductable, visitCost):

            #print(deductable, visitCost)
            for x in range(len(visitCost)):
                if deductable > 0:
                    try:
                        if deductable - visitCost[x] <= 0:
                            pass
                        # problem here: if deductable limit isnt reached, program must ensure insurance doesn't get involved !FIXED
                        elif deductable - visitCost[x] > 0:
                            deductable = deductable - visitCost[x]
                            
                            visitCost.remove(visitCost[x])
                    except Exception as e:
                        pass
            
            billStart = visitCost[0] - deductable
            return billStart # returns next visitCost - what is left of deductable

        def splitCalc(coSplit, stopLoss, deductable, visitCost, user, coPay):
            bill = deductableCalc(deductable, visitCost)
            total = 0
            cPay = coPayTotal(coPay)
            # grabs first index split
            billStart = bill * coSplit 
            #print(billStart)
            for x in range(len(visitCost)):
                try:
                    allCosts = visitCost[x + 1] * coSplit
                    
                    total += allCosts
                   
                except:
                    pass
            if user == True:
                total += deductable + cPay  
            total += billStart

            return total
        
        # To prevent corrupted {self.visitCosts} list
        for x in range (len(self.visitCosts)):
            self.newCost.append(self.visitCosts[x])

        dTotal = 0
        dLen = self.visitCost2.split(",")
        for x in range(len(dLen)):
            #print(dLen[x])
            dTotal = dTotal + int(dLen[x])


        if dTotal < self.deductable: # checking if all visits are LESS than total deductable
            cPay = coPayTotal(self.coPay)
            newTotal = dTotal + cPay
            os.system("cls")
            print(f'''
========================================
|           USER: ${newTotal}           |
|           INSURANCE: $0               |
========================================
                ''')
        else:
            uTotal = splitCalc(self.coSplit[1], self.stopLoss, self.deductable, self.visitCosts, True, self.coPay)
            iTotal = splitCalc(self.coSplit[0], self.stopLoss, self.deductable, self.newCost, False, self.coPay)
            cPay = coPayTotal(self.coPay)
            

            deduct = deductableCalc(self.deductable, self.visitCosts)
            
            if self.stopLoss > 0  and self.stopLoss < uTotal: # if there is a stoploss
                
                f1 = self.stopLoss + cPay
                toSub = uTotal - f1
                uTotal -= toSub
                iTotal += toSub
                os.system("cls")
                print(f'''
========================================
|           USER: ${uTotal}            |
|           INSURANCE: ${iTotal}       |
========================================
                ''')
                
                
            else:
                os.system("cls")
                print(f'''
========================================
|           USER: ${uTotal}            |
|           INSURANCE: ${iTotal}       |
========================================
                ''')
        input("\nPress ENTER to exit...")
        os.system("cls")
        #Calculate()
        
if __name__ == "__main__":
    c = Calculate()
     
        
       
   
