from brownie import FundMe, MockV3Aggregator, network, accounts, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # price_feed_address represents the conversion rate between ether and dollars.
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print(f"The active network is {network.show_active()}")
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

        # Fetch the latest MockV3Aggregator deployed to the network. and get the address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(
        f"Contract deployed to {fund_me.address} \nCurrent dollar price is {fund_me.getPrice()}\nEntrance Fee: {fund_me.getEntranceFee()}"
    )
    return fund_me


def main():
    deploy_fund_me()
