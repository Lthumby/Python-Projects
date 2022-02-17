


from shutil import ExecError
from tempfile import TemporaryFile
from urllib.request import proxy_bypass
import multiprocessing
import os

class Calculate:
    def __init__(self):
        # basic inputs
        '''self.deductable = int(input("Enter Deductable: "))
        self.coInsurance = input("Enter Co-Insurance Split (0.0,0.0): ")
        self.visits = int(input("Enter # of visits: "))
        self.visitCost = str(input("Enter visit costs (0,0,0,0): "))
        self.coPays = str(input("Enter all copays (0,0,0,0): "))
        self.stopLoss = int(input("Enter Stop-Loss: "))'''
        # debug inputs
        self.deductable = 500
        self._deductable = self.deductable
        self.coInsurance = "0.8,0.2"
        self.visits = 4
        self.visitCost = "250,1200,400,800"
        self.coPays = "25,50,50,100"
        self.stopLoss = 0
        self.newCost = []
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
                        else:
                            deductable = deductable - visitCost[x]
                            visitCost.remove(visitCost[x])
                            #print(deductable, visitCost)
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

        print("USER:", splitCalc(self.coSplit[1], self.stopLoss, self.deductable, self.visitCosts, True, self.coPay))
        print("INSURANCE:", splitCalc(self.coSplit[0], self.stopLoss, self.deductable, self.newCost, False, self.coPay))
        input("\nPress ENTER to exit...")
        
if __name__ == "__main__":
    c = Calculate()
    
