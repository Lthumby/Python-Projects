

from cmath import cos
from shutil import ExecError
from tokenize import Double, String
from unicodedata import decimal


class Calculate:
    def __init__(self): 
        self.deductable = int(input("Enter Deductable: "))
        self.coInsurance = input("Enter Co-Insurance Split (0.0,0.0): ")
        self.visits = int(input("Enter # of visits: "))
        self.visitCost = str(input("Enter visit costs (100,100,100,100): "))
        self.coPays = str(input("Enter all copays ($25,$25,$25): "))
        self.stopLoss = False
        '''self.deductable = 500
        self.coInsurance = "0.8,0.2"
        self.visits = 4
        self.visitCost = "250,1200,400,800"
        self.coPays = "25,50,50,100"'''
        self.stopLoss = False
        # Gathering total copays
        cpay = self.coPays.split(",")
        cpayMap = map(int, cpay)
        self.coPay = list(cpayMap) # <- list of all copays
        # Gathering total vist costs
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



        def splitCalcs(deductable, coSplit, vCosts, vNum, coPay, billStart):
            total = 0
            bIndex = billStart * coSplit
            youCosts = 0
           # print(bIndex, "bindex")
            for x in range(len(vCosts)):
                try:
                    youCost = vCosts[x + 1] * coSplit
                    youCosts = youCosts + youCost
                except Exception as e:
                    pass
                
            total = total + bIndex + youCosts
            return total
            

        def calcs(deductable, coSplit, vCosts, vNum, coPay):
            
            for copays in coPay: # grabs total copay
                self.coPayTotal = self.coPayTotal + copays
            for visits in range(vNum): 
                
                if deductable > 0:
                    try:   
                        if deductable - vCosts[visits] <= 0:
                            pass
                        else:
                            deductable = deductable - vCosts[visits]
                           
                            self.visitCosts.remove(vCosts[visits])
                            
                    except Exception as e:
                        print("ERROR CALCULATING DEDUCTABLE")

                billStart = self.visitCosts[0] - deductable
                youData = splitCalcs(self.deductable, self.coSplit[1], self.visitCosts, self.visits, self.coPay, billStart)
                youTotal = youData + self.deductable + self.coPayTotal
                self.youTotal = youTotal
                insureData = splitCalcs(self.deductable, self.coSplit[0], self.visitCosts, self.visits, self.coPay, billStart)
                self.insureTotal = insureData

            

        calcs(self.deductable, 0.2, self.visitCosts, self.visits, self.coPay)
        print("User:",self.youTotal)
        print("Insurance: ",self.insureTotal)
        

Calculate()

