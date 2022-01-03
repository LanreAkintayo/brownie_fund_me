from brownie import accounts, network, config, MockV3Aggregator
from web3 import Web3


DECIMALS = 18
STARTING_PRICE = 2000
FORKED_BLOCKCHAIN_ENVIRONMENTS = ["mainnet-fork","mainnet-fork-dev"]  # copy of real blockchain environment
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    if len(MockV3Aggregator) <= 0:
        # MockV3Aggregator is a list that contains all the MockV3Aggregator deployed to a network.
        # We only want to deploy a MockV3Aggregator if there is no MockV3Aggregator in a network.

        print("Deployng mocks..")
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
        print("Mock deployed to the network.")
