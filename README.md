# Goals
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
