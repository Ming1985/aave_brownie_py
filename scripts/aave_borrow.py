from configparser import ConverterMapping
from brownie import config, network, interface
from scripts.get_weth import get_weth
from scripts.helpful_scripts import get_account
from web3 import Web3

amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    # interact with aave lending_pool contract.
    # functions: deposit, withdraw etc.
    # abi, address
    lending_pool = get_lending_pool()
    # print(lending_pool)
    # before deposit / sending out a erc20 token, you need to first approve it
    # lending_pool.address: the interface object is actually the contract
    approve_erc20(amount, lending_pool.address, erc20_address, account)
    # deposit(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)
    print("Depositing...")
    tx = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account, "gas_price":10000000000}
    )
    tx.wait(1)
    print("Deposited!")
    # get some user data onchain
    # getUserAccountData() from LendingPool contract
    (borrowable_eth, total_debt) = get_borrowable_data(lending_pool, account)
    print("Let's borrow!")
    # borrow DAI, calculate DAI in terms of ETH
    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )
    # borrow 95% of borrowable eth
    amount_dai_to_borrow = (1 / dai_eth_price) * borrowable_eth * 0.95
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")

    # execute the borrow
    dai_address = config["networks"][network.show_active()]["dai_token"]

    # borrow function's parameters:
    #   asset address,
    #   amount,
    #   interestRateMode(1 for stable interest rate, 2 for variable interest rate)
    #   referral code , use 0 for no referral code
    #   onBehalfof address, msg.sender
    borrow_tx = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account.address,
        {"from": account},
    )
    borrow_tx.wait(1)
    print("We borrowed some DAI")
    get_borrowable_data(lending_pool, account)
    repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_pool, account)
    # print("You just deposited, borrowed, and repayed with Aave, brownie and Chainlink")
    # get_borrowable_data(lending_pool, account)


def get_lending_pool():
    # use lending_pool address provider contract to get address
    # getLendingPool() function from addresses provider
    # need abi and address of address provider contract
    # use interface of address provider
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    print('the lending pool address is', lending_pool_address)
    # create an interface object to interact as a contract
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 token...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved!")
    return tx
    # need abi and address of the token contract
    # need the interface of erc20 token. in IERC20.sol


def get_borrowable_data(lending_pool, account):
    # getUserAccountData() from LendingPool contract
    # https://docs.aave.com/developers/v/1.0/developing-on-aave/the-protocol/lendingpool
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of Eth deposite")
    print(f"You have {total_debt_eth} worth of Eth debt")
    print(f"You have {available_borrow_eth} worth of Eth borrow power")
    print(f"Current liquidation threshold {current_liquidation_threshold}")
    print(f"ltv {ltv}")
    print(f"health factor {health_factor}")
    return (float(available_borrow_eth), float(total_debt_eth))


def get_asset_price(price_feed_address):
    # ABI Address. Use interface
    dai_eth_price_feed = interface.AggregatorV3Interface(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account
    )
    # repay function parameters
    # asset address
    # amount
    # rateMode 1 for stable 2 for variable
    # address onBehalfOf who do you repay
    repay_tx = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_tx.wait(1)
    print("Repayed!")
