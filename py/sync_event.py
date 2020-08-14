# coding=utf-8
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
import base64
import traceback
from pprint import pprint as print
from datetime import datetime


global w3 
w3 = Web3(HTTPProvider('http://localhost:8545'))
print(f"connected to {w3}")
contractAddress = '0xF8e52501e00aFe56EEc7ccB63B94550c5B231c30'
contract = w3.eth.contract(address=contractAddress, abi=contract_abi.abi)

accounts = w3.eth.accounts
#改第一个私钥就可以,还得改contractaddress,也就是calc合约地址
private_keys=['60099cf62c84d7ffb23c9bf4b42b3fb27b8a5893c5d005ece1d8808ea984bc24']

def handle_event(event):
    db = mdb.connect(host='ali.fkynjyq.com', port=3306, user='root', passwd='example', db='privace', charset='utf8')
    receipt = w3.eth.waitForTransactionReceipt(event['transactionHash'])
    #print(receipt)
    result = contract.events.data_selected().processReceipt(receipt)
    print("=======================收到新交易===========================")
    print("交易信息如下：")
    print("数据购买者账户地址:"+str(result[0]['args']['data_buyer']))
    print("本次数据购买交易id:"+str(result[0]['transactionHash'])+",Calc合约地址:"+str(result[0]['args']['data_buyer_contract'])+",数据购买者合约地址:"+str(result[0]['args']['data_buyer_contract']))
    print("选中的数据者如下：")
    print(result[0]['args']['owners_address'])
    print("数据所有者的隐私保护参数(epsilon):")
    print(result[0]['args']['owners_epsilon'])
    print("数据所有者的价格(price):")
    print(result[0]['args']['owners_price'])
    print("数据所有者的数据(加密的):")
    print(result[0]['args']['owners_data'])
    data=[]
    nums_destination=[]
    nums_days=[]
    nums_price=[]
    epsilon=[]
    owners_address=[]
    owners_price=[]
    length1=len(result[0]['args']['owners_epsilon'])
    for i in range (0,length1):
        data.append(base64.b64decode(result[0]['args']['owners_data'][i]))
        epsilon.append(result[0]['args']['owners_epsilon'][i])
        owners_address.append(result[0]['args']['owners_address'][i])
        owners_price.append(result[0]['args']['owners_price'][i])
    data_buyer_contract=result[0]['args']['data_buyer_contract']
    buyer_contract = w3.eth.contract(address=data_buyer_contract, abi=contract_abi.abi1)
    data_buyer=result[0]['args']['data_buyer']
    Calc_address=result[0]['args']['params'][0]
    bidstart=result[0]['transactionHash']
    hs=''.join(['%02x' %x  for x in bidstart])
    bidstart='0x'+hs
    requirement=json.loads(result[0]['args']['requirements'])
    print("使用中间计算者私钥解密数据...")
    with open("priv_mid.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        for i in range(0,length1):
            data[i] = cipher_private.decrypt(data[i], Crypto.Random.new().read)
            data[i] = data[i].decode('utf-8')
    print("解密后的结果为:")
    print(data)
    # if(result[0]['args']['result_type']=="median"):
    #     res_destination=dp.count(nums_destination,epsilon)
    # elif(result[0]['args']['result_type']=="count"):
    #     res_days=dp.mean(nums_days,epsilon)
    # elif(result[0]['args']['result_type']=="mean"):
    #     res_price=dp.median(nums_price,epsilon)
    selectType=requirement['queryType']
    resultType=requirement['resultType']
    buyerRSAPub=requirement['publickey']
    print("本次请求的参数为:"+str(selectType)+"请求的结果类型为:"+str(resultType))
    num_median=[]
    num_count=[]
    res=0
    if(resultType=="中位数"):
        for i in range(0,length1):
            temp=json.loads(data[i])
            num_median.append(temp[selectType])
        res=dp.median(num_median,epsilon)
    elif(resultType=="统计个数"):
        for i in range(0,length1):
            temp=json.loads(data[i])
            query=requirement['query']
            if(temp[selectType]==query):
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
    print("差分隐私的结果为:"+str(res)+",将结果保存到合约")
    
    cipher_public = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(buyerRSAPub))
    cipher_text=cipher_public.encrypt(str(res).encode('utf-8')) # 使用公钥进行加密
    cipher_text=binascii.b2a_hex(cipher_text).decode('utf-8')
    print("加密后的结果为:"+str(cipher_text))
    
    tran=contract.functions.bidEnd(data_buyer,cipher_text).buildTransaction({
    'gas':3000000,
    'gasPrice': w3.toWei('1', 'gwei'),
    'from':accounts[0],
    'nonce' : w3.eth.getTransactionCount(accounts[0])
    })
    sign_txn=w3.eth.account.signTransaction(tran,private_key=private_keys[0])
    send_txn=w3.eth.sendRawTransaction(sign_txn.rawTransaction)
    hs=''.join(['%02x' %x  for x in send_txn])
    bidend='0x'+hs
    result=binascii.a2b_hex(buyer_contract.functions.get_result().call())
    #print(result)
    with open("priv_buyer.pem", "rb") as x:
        a = x.read()
        cipher_private = Crypto.Cipher.PKCS1_v1_5.new(Crypto.PublicKey.RSA.importKey(a))
        result=cipher_private.decrypt(result, Crypto.Random.new().read) 
        
    print("从合约中获取结果并解密读取结果为:"+str(result))
    trandatas=[]
    for i in range(0,length1):
        trandata={ 'to': owners_address[i],'payment': owners_price[i],}
        trandatas.append(trandata)
    trandatastr=json.dumps(trandatas)
    cursor = db.cursor()
    dt=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    result=str(result)
    #Calc_address=" "
    sql="insert into databuyer values(NULL,'"+bidstart+"','"+bidend+"','"+dt+"','ok','"+Calc_address+"','"+data_buyer_contract+"','"+trandatastr+"','"+str(cipher_text)+"','"+data_buyer+"')"
    print("将结果保存到数据库,sql语句为:"+str(sql))
    cursor.execute(sql)
    db.commit()
    for i in range(0,length1):
        sql="insert into dataowner values(NULL,'"+dt+"','ok','"+str(owners_price[i])+"','"+data_buyer+"','"+data_buyer_contract+"','"+owners_address[i]+"','"+bidstart+"')"
        print("将结果保存到数据库,sql语句为:"+str(sql))
        cursor.execute(sql)
        db.commit()
    print("=======================交易完成!===========================")

def log_loop(event_filter, poll_interval):
    try:
        while True:
            for event in event_filter.get_new_entries():
                handle_event(event)
                time.sleep(poll_interval)
    except Exception as e:
        print("error!" + str(e))
        e.with_traceback()
        #traceback.print_exc()
        #print ('traceback.format_exc():\n%s' % traceback.format_exc())
block_filter = w3.eth.filter({'fromBlock':'latest', 'address':contractAddress})
log_loop(block_filter, 2)
