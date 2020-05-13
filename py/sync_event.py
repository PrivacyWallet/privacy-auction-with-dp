from web3 import Web3, HTTPProvider
import time
import json
import contract_abi
import dp
global w3 
w3= Web3(HTTPProvider('http://localhost:9545'))
contractAddress = '0xf71087bABcC601Cf6a6F21C44Aa529447E8612c9'
buyerAddress='0xbB098067655a0c4a35BcB121C775f3FB2237B348'
contract = w3.eth.contract(address=contractAddress, abi=contract_abi.abi)
buyer_contract = w3.eth.contract(address=buyerAddress, abi=contract_abi.abi1)
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

def handle_event(event):
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    #print(receipt)
    result = contract.events.data_selected().processReceipt(receipt)
    print(result[0]['args'])
    nums=[]
    epsilon=[]
    for i in range (0,len(result[0]['args']['owners_epsilon'])):
        nums.append(binascii.a2b_hex(result[0]['args']['owners_data'][i]))
        epsilon.append(result[0]['args']['owners_epsilon'][i])
    with open("priv_mid.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        for i in range(0,5):
            nums[i] = cipher_private.decrypt(nums[i], Crypto.Random.new().read) 
            nums[i]=int(nums[i])
    if(result[0]['args']['result_type']=="median"):
        res=dp.median(nums,epsilon)
    elif(result[0]['args']['result_type']=="count"):
        res=dp.count(nums,epsilon)
    elif(result[0]['args']['result_type']=="mean"):
        res=dp.mean(nums,epsilon)
    print("send result= "+str(res)+" to contract")
    with open("pub_databuyer.pem", "rb") as x:
        b = x.read()
        cipher_public = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(b))
        for i in range(0,5):
            cipher_text=cipher_public.encrypt(str(data[i]).encode('utf-8')) # 使用公钥进行加密
            #cipher_text[i]=int(binascii.b2a_hex(cipher_text[i]).decode('utf-8'),16)
            print(cipher_text)  
    tran=contract.functions.bidEnd(accounts[5],cipher_text).buildTransaction({
    'gas':3000000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'from':accounts[5],
    'nonce' : w3.eth.getTransactionCount(accounts[5])
    })
    sign_txn=w3.eth.account.signTransaction(tran,private_key=private_keys[5])
    send_txn=w3.eth.sendRawTransaction(sign_txn.rawTransaction)
    result=buyer_contract.functions.get_result().call()
    with open("priv_mid.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        result= cipher_private.decrypt(result, Crypto.Random.new().read) 
        result=int(result)
    print("result is "+str(result))

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
log_loop(block_filter, 2)