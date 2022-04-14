## Goals
1. swap some eth to weth
2. deposit some eth/weth into aave
3. borrow some asset withe the eth collateral
   1. sell that borrowed asset (short selling)
4. repay everything back
5. prarswap uniswap

## Testing

Integration test: Kovan
Unit test: Mainnet-fork *because there would be no interaction with oracles, thus no need to deploy mock contracts.*

## Resources
- kovan weth source code https://kovan.etherscan.io/address/0xd0a1e359811322d97991e03f863a0c30c2cf029c#code
- weth contract on kovan
https://kovan.etherscan.io/token/0xd0a1e359811322d97991e03f863a0c30c2cf029c
- aave docs https://docs.aave.com/developers/v/1.0/developing-on-aave/the-protocol/lendingpool
- aave code https://github.com/aave/protocol-v2 interface included

## Skills
### How to interact with interface
1. create interface files into interfaces directory. Interface files can be found on github project source codes, or can be translated from abis, get from etherscan.
2. from brownie import interface
3. create contract objects using contract = interface.InterfaceName(address)
4. interact with contract object. Contract.function(input)

### How to borrow on aave
1. What you need
   1. Lending pool provider address and interface 
   2. deposit erc20 token address
   3. borrow erc20 token address
   4. pricefeed for the token you want to borrow, AggregatorV3Interface address and interface
2. approve aave to spend some amount of deposit erc20 token, using erc20 function approve
3. Lending pool object
   1. deposit using lending_pool.deposit()
   2. get account data using lending_pool.getUserAccountData
   3. borrow using lending_pool.borrow()
   4. repay using leding_pool.repay()

### Brownie console --network kovan 

### Brownie test

### Error
- gas fee error, usually is caused by wrong contract address, rather than gas.