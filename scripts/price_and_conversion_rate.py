from brownie import FundMe
def getPrice():
    fund_me = FundMe[-1]
    print(f"Current Price of 1 Eth: {fund_me.getPrice()}")


    
def main():
    getPrice()