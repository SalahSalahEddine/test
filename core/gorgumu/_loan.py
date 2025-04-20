import datetime
'''
Class Gives Client Get Ninja Loan For Couple Of Mounth With Conditions:
[1].Client Has More Than 20 Transaction
[2].Upload Client Data As Mortage
[3].Ninja Loan
[4].The Debts Calculate With Loan Amount Plus Interest Real
'''
class Loan:
    delta = datetime.timedelta(days=60)
    #Initilize Loan Class
    def __init__(self,amount,order):
        self.order = order
        self.amount = amount
        self.datetime = datetime.datetime.now().date()
        self.expire_date = self.datetime + self.delta