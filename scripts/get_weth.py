from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    """
    Mints weth by depositing eth
    """
    # abi
    # address
    account = get_account()
    # create an interface object to interact
    # interface.interfaceName(address)
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    # interact with interface as if it's a contract
    # weth.deposit deposit eth into weth contract and get weth back
    tx = weth.deposit({"from": account, "value": 0.1 * (10**18)})
    tx.wait(1)
    print("received 0.1 weth")
    return tx
