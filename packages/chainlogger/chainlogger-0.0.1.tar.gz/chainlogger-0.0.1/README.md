# chainlogger-python
Simple Python package for using Chain Logger on omChain Jupiter

### ABI:
```json
[{"type":"constructor","stateMutability":"nonpayable","inputs":[]},{"type":"event","name":"LogRegistered","inputs":[{"type":"address","name":"_vendorAddress","internalType":"address","indexed":true},{"type":"uint256","name":"_projectId","internalType":"uint256","indexed":false},{"type":"uint256","name":"_projectLogCounter","internalType":"uint256","indexed":false},{"type":"bytes32","name":"_data","internalType":"bytes32","indexed":true}],"anonymous":false},{"type":"event","name":"VendorRegistered","inputs":[{"type":"uint256","name":"_id","internalType":"uint256","indexed":true},{"type":"address","name":"_vendorAddress","internalType":"address","indexed":true}],"anonymous":false},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"_changeOwner","inputs":[{"type":"address","name":"toOwner","internalType":"address"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"getLog","inputs":[{"type":"address","name":"vendorAddress","internalType":"address"},{"type":"uint256","name":"projectId","internalType":"uint256"},{"type":"uint256","name":"logId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"numVendors","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"owner","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"address","name":"","internalType":"address"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"uint256","name":"","internalType":"uint256"},{"type":"bytes32","name":"","internalType":"bytes32"}],"name":"registerLog","inputs":[{"type":"uint256","name":"projectId","internalType":"uint256"},{"type":"bytes32","name":"data","internalType":"bytes32"}]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"registerProject","inputs":[]},{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"registerVendor","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"vendorAddress","internalType":"address"},{"type":"uint256","name":"projectCounter","internalType":"uint256"}],"name":"vendorLogs","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"vendors","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"vendorsReverse","inputs":[{"type":"address","name":"","internalType":"address"}]}]
        
```

## Installation

```
pip install chainlogger
```

After installing via pip, you can include the Chain Logger on your projects as following

```python
import chainlogger as Logger

logger = Logger()
logger.set_provider('YOUR_PROVIDER_URL')
logger.set_abi('CONTRACT_ABI')
logger.set_eth_signer('YOUR_ETH_SIGNER_PROVIDER')
logger.set_contract('CONTRACT_ADDRESS')
logger.set_send_contract('CONTRACT_ADDRESS')
logger.set_web3()
logger.set_salt("MY_SECRET_SALT")
logger.set_account('YOUR_WALLET_ADDRESS')
```

## Registering vendor

```python
logger.register_vendor()

#Returns the txHash of the call
```

## Registering project

```python
logger.register_project()

#Returns the txHash of the call
```

## Registering a log

```python
logger.register_log(project_id, raw_data);

#Returns the txHash of the call
```

## Getting tx receipt for registerLog method

```python
logger.get_transaction_receipt(tx_id);
```

## Verifying data from blockchain

```python
logger.verify_data(hashed_data_from_blockchain, raw_input, salt)

#Returns boolean
```