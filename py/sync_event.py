from web3 import Web3, HTTPProvider
import time
import json
import contract_abi
import dp
import binascii
import Crypto.PublicKey.RSA
import Crypto.Cipher.PKCS1_v1_5
import Crypto.Random
import Crypto.Signature.PKCS1_v1_5
import Crypto.Hash
import json
import pymysql as mdb
from datetime import datetime
db = mdb.connect(host='ali.fkynjyq.com', port=3306, user='root', passwd='example', db='privace', charset='utf8')

global w3 
w3= Web3(HTTPProvider('http://localhost:9545'))
contractAddress = '0xffEaDD49a5D8862A55798F7D126D356B95057d03'
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
    print(result[0])
    data=[]
    nums_destination=[]
    nums_days=[]
    nums_price=[]
    epsilon=[]
    owners_address=[]
    owners_price=[]
    #length1=len(result[0]['args']['owners_epsilon'])
    length1=5
    for i in range (0,length1):
        data.append(binascii.a2b_hex(result[0]['args']['owners_data'][i]))
        epsilon.append(result[0]['args']['owners_epsilon'][i])
        owners_address.append(result[0]['args']['owners_address'][i])
        owners_price.append(result[0]['args']['owners_price'][i])
    data_buyer_contract=result[0]['args']['data_buyer_contract']
    data_buyer=result[0]['args']['data_buyer']
    Calc_address=result[0]['args']['params'][0]
    bidstart=result[0]['transactionHash']
    hs=''.join(['%02x' %x  for x in bidstart])
    bidstart='0x'+hs
    requirement=json.loads(result[0]['args']['requirement'])
    print(hs)
    with open("priv_mid.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        for i in range(0,length1):
            data[i] = cipher_private.decrypt(data[i], Crypto.Random.new().read) 
            data[i] =str(data[i] , encoding = "utf-8")

    # if(result[0]['args']['result_type']=="median"):
    #     res_destination=dp.count(nums_destination,epsilon)
    # elif(result[0]['args']['result_type']=="count"):
    #     res_days=dp.mean(nums_days,epsilon)
    # elif(result[0]['args']['result_type']=="mean"):
    #     res_price=dp.median(nums_price,epsilon)
    selectType=requirement['queryType']
    resultType=requirement['resultType']
    num_median=[]
    num_count=[]
    res=-1
    if(resultType=="中位数")：
        for i in range(0,length1):
            temp=json.loads(data[i])
            num_median.append(temp[selectType])
        res=dp.median(num_median,epsilon)
    elif(resultType=="统计个数")：
        for i in range(0,length1):
            temp=json.loads(data[i])
            query=requirement['query']
            if(data[i]==query):
                num_count.append(1)
            else:
                num_count.append(0)
        res=dp.count(num_count,epsilon)
    res_data = {
    'queryType' :requirement['queryType'],
    'resultType' :requirement['resultType'],
    'query' : requirement['query'],
    'result':int(res)
    }
    res=json.dumps(res_data)
    print("send result= "+str(res)+" to contract")
    with open("pub_buyer.pem", "rb") as x:
        b = x.read()
        cipher_public = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(b))
        cipher_text=cipher_public.encrypt(str(res).encode('utf-8')) # 使用公钥进行加密
        cipher_text=binascii.b2a_hex(cipher_text).decode('utf-8')
        print(cipher_text)
    
    for i in range(0,length1):
        balance=w3.eth.getBalance(accounts[i])
        print("before buy owner balance is "+str(balance)) 
    balance=w3.eth.getBalance(accounts[5])
    print("before buy buyer balance is "+str(balance))  
    tran=contract.functions.bidEnd(accounts[5],cipher_text).buildTransaction({
    'gas':3000000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'from':accounts[5],
    'nonce' : w3.eth.getTransactionCount(accounts[5])
    })
    sign_txn=w3.eth.account.signTransaction(tran,private_key=private_keys[5])
    send_txn=w3.eth.sendRawTransaction(sign_txn.rawTransaction)
    hs=''.join(['%02x' %x  for x in send_txn])
    bidend='0x'+hs
    result=binascii.a2b_hex(buyer_contract.functions.get_result().call())
    #print(result)
    with open("priv_buyer.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        result=cipher_private.decrypt(result, Crypto.Random.new().read) 
        
    print("result is "+str(result))
    for i in range(0,length1):
        balance=w3.eth.getBalance(accounts[i])
        print("after buy owner balance is "+str(balance)) 
    balance=w3.eth.getBalance(accounts[5])
    print("after buy buyer balance is "+str(balance))
    trandatas=[]
    for i in range(0,length1):
        trandata={ 'to': owners_address[i],'payment': owners_price[i],}
        trandatas.append(trandata)
    trandatastr=json.dumps(trandatas)
    cursor = db.cursor()
    date = datetime.now().strftime("%Y-%m-%d")
    print(date)
    result=str(result)
    print(result)
    #Calc_address=" "
    sql="insert into databuyer values(NULL,'"+bidstart+"','"+bidend+"',str_to_date('"+date+"','%Y-%m-%d'),'ok','"+Calc_address+"','"+data_buyer_contract+"','"+trandatastr+"','"+result[2:-1]+"','"+data_buyer+"')"
    print(sql)
    cursor.execute(sql)
    db.commit()
    for i in range(0,length1):
        sql="insert into dataowner values(NULL,str_to_date('"+date+"','%Y-%m-%d'),'ok','"+str(owners_price[i])+"','"+data_buyer+"','"+data_buyer_contract+"','"+owners_address[i]+"','"+bidstart"')"
        print(sql)
        cursor.execute(sql)
        db.commit()

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
            time.sleep(poll_interval)

block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
log_loop(block_filter, 2)