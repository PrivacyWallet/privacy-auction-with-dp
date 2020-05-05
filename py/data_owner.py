from web3 import Web3, HTTPProvider
import time
import json
import contract_abi
global w3 
w3= Web3(HTTPProvider('http://localhost:9545'))
contractAddress = '0xf71087bABcC601Cf6a6F21C44Aa529447E8612c9'
buyerAddress='0xbB098067655a0c4a35BcB121C775f3FB2237B348'
contract = w3.eth.contract(address=contractAddress, abi=contract_abi.abi)
accounts = w3.eth.accounts
private_keys=['bea9bf4e01dc9ff582f4fa8a535a1dcdf637bfbe27667f0d4ad46f1e45535675'
, '3c2df8e0ef721b197c9e1fba2062675927125860eac71edca7dd23f3e62bea3c'
, 'abe4e5a5972c6a6383b30e439d8f820145f3c35c09c2c6c3b630c444e2577e36'
, '7975186f9faa4c494ad7e58638640c0e223d4aea6154b55b77ff61bc12ca9a40'
, '66a55c5f943118e284f74e64f5c8be5cffe55ab7ae045c3ec603efbdf14e7797'
, '5786411c8be0ee30e88f3eb6e9d30d86c14828d7d0c7b1b257fc2da58116e5c6'
, 'dce48224fa51ec3c14c48fc22610100e385bf3a345482394984b421092fed51d'
, '95efd413c2c28396fe8f6d57220dfa8500a63836c2af1c6236a2b2300b693566'
, '748738d532d170e98c9e8a6fecdce52ae70e5830819c70e208637c5604a3dcd5'
, 'b816c10ce07861c789d2188805554153aaff462a1fd3c6caa07891f1ed1602b1']
data=[1,2,3,4,5]
epsilon=[23,69,86,74,96]
price=[1000000,3000000,5000000,7000000,9000000]
for i in range(0,5):
    print(i)
    tran=contract.functions.set_data(epsilon[i],data[i],price[i],accounts[i]).buildTransaction({
        'gas':1000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from':accounts[i],
        'nonce' : w3.eth.getTransactionCount(accounts[i])})
    sign_txn=w3.eth.account.signTransaction(tran,private_key=private_keys[i])
    send_txn=w3.eth.sendRawTransaction(sign_txn.rawTransaction)
tran=contract.functions.bid(buyerAddress).buildTransaction({
'gas':3000000,
'gasPrice': w3.toWei('1', 'gwei'),
'from':accounts[5],
'nonce' : w3.eth.getTransactionCount(accounts[5]),
'value':12000000})
sign_txn=w3.eth.account.signTransaction(tran,private_key=private_keys[5])
send_txn=w3.eth.sendRawTransaction(sign_txn.rawTransaction)



    
