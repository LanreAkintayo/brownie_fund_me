from brownie import FundMe, network, accounts, exceptions
from scripts.deploy import deploy_fund_me
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee()
    fund_transaction = fund_me.fund({"from": account, "value": entrance_fee})
    fund_transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    withdraw_transaction = fund_me.withdraw({"from": account})
    withdraw_transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    fund_me = deploy_fund_me()
    account = accounts.add() # This gives a random account
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": account})  # A random account trying to withdraw all the money funded.
    


    