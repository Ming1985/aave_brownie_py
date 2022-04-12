# utility scripts.
from brownie import (
    accounts,
    network,
    config,
    Contract,
)
from pyparsing import java_style_comment

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "mainnet-fork", "hardhat", "local-ganache"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

# get account according to current network
def get_account(index=None, id=None):

    # accounts.add(config)
    # accounts.load("id")
    if index:
        return accounts[index]  # accounts is imported from brownie, test account array
    if id:
        return accounts.load(id)  # accounts.load, load preset id from brownie. see roam
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(
        config["wallets"]["from_key"]
    )  # load from config file, brownie-config.yaml

