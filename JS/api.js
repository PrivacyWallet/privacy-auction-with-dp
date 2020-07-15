const web3 = require('./Web3.js')
const abi = require('./abi.js')
var NodeRSA = require('node-rsa')
var fs = require('fs')
var Tx = require('ethereumjs-tx');
class Eth {

    constructor(prikey) {
        this.prikey=prikey
        this.CONTRACT_ADDRESS="0xf71087bABcC601Cf6a6F21C44Aa529447E8612c9"
        this.CONTRACT_ADDRESS_BUYER="0xbB098067655a0c4a35BcB121C775f3FB2237B348"
        this.contract=new web3.eth.Contract(abi.Calc, this.CONTRACT_ADDRESS)
        this.contract_buyer=new web3.eth.Contract(abi.Calc, this.CONTRACT_ADDRESS_BUYER)
        this.account = web3.eth.accounts.privateKeyToAccount(this.prikey) 
      }
    login () {
      console.log('[Eth] execute login')
      if(this.account.privateKey==this.prikey){
        return true
      }
      else{
        return false
      }     
    }
  

    async getAccount()
    {
        var balance=await web3.eth.getBalance(this.account.address)
        return { account: this.account.address, balance :balance}
    }
    // getTransactionsAsDataBuyer (): {
    //   id: String;
    //   date: Date;
    //   status: String;
    //   deployedContract: String;
    //   result: String;
    //   transactions: { to: String; payment: Number; data: String }[];
    // }[] {
    //   return [
    //     {
    //       id: 'id 1',
    //       date: new Date(),
    //       status: 'finished',
    //       deployedContract: 'Contract...',
    //       transactions: [
    //         {
    //           to: 'aaaa',
    //           payment: 0.3,
    //           data: 'data 1'
    //         },
    //         {
    //           to: 'bbb',
    //           payment: 0.5,
    //           data: 'data 2'
    //         }
    //       ],
    //       result: 'encrypted data'
    //     },
    //     {
    //       id: 'id 2',
    //       date: new Date(),
    //       status: 'finished',
    //       deployedContract: 'Contract...',
    //       transactions: [
    //         {
    //           to: 'aaaa',
    //           payment: 0.3,
    //           data: 'data 1'
    //         },
    //         {
    //           to: 'bbb',
    //           payment: 0.5,
    //           data: 'data 2'
    //         },
    //         {
    //           to: 'ccc',
    //           payment: 0.7,
    //           data: 'data 7'
    //         }
  
    //       ],
    //       result: 'encrypted data again'
    //     }
    //   ]
    // }
  
    async createNewTransaction (
      filter,
      selectType,
      queryType,
      budget
    ){
        await this.contract.methods.bid(this.account.address,"median").send(
            {
                'gas':3000000,
                'gasPrice': web3.utils.toWei('1', 'gwei'),
                'from':this.account.address,
                // 'nonce' : web3.eth.getTransactionCount(this.account.address),
                'value':12000000
            }
        ).on('receipt', function(receipt){
          // receipt example
          console.log(receipt);
          var tx = new Tx(rawTx);
      tx.sign(prikey);
      var serializedTx = tx.serialize();
      console.log(serializedTx.toString('hex'));
      web3.eth.sendRawTransaction(serializedTx.toString('hex'), function(err, hash) {
        if (!err)
          console.log(hash); // "0x7f9fade1c0d57a7af66ab4ead79fade1c0d57a7af66ab4ead7c2c2eb7b11a91385"
          else
          {
            console.log(err)
          }
        }
      );
        
        })
        .on('error',console.error);
    }
  
    // getTransactionsAsDataOwner (): {
    //   id: String;
    //   date: Date;
    //   status: String;
    //   payment: Number;
    //   from: String;
    // }[] {
    //   return [
    //     {
    //       id: 'id 111',
    //       date: new Date('2020-01-02'),
    //       status: 'finished',
    //       payment: 0.34,
    //       from: 'id xxxxxx01'
    //     },
    //     {
    //       id: 'id 114',
    //       date: new Date('2020-03-04'),
    //       status: 'finished',
    //       payment: 0.89,
    //       from: 'id xxxxxx01'
    //     }
    //   ]
    // }
  
    // getData (): Array<Form> {
    //   return [
    //     {
    //       age: 32,
    //       education: '本科',
    //       gender: '男',
    //       hometown: '北京市',
    //       income: 3000,
    //       maritalStatus: '已婚',
    //       occupation: '学生',
    //       wentTo: '香港特别行政区'
    //     }
    //   ]
    // }
  
    async createNewData (data,epsilon,price){
        var cipherText
        var rsadata="-----BEGIN RSA PUBLIC KEY-----\nMIIBCgKCAQEAqymJH1pMkr4F9NR8nze09w+iMMejql4bk7GpVa0xjilCDsvVHvxD\nFhVHVRxpuZyM5p684sUGleV0qZXBXFuBzSLrY7n6GqlgP5qQorhCkQP7q05sqGtU\n95dYbn3LjEzYs14XtTCXZvO6zHzABoLceKzeYGHjahtKLIitLR1NbNYbrgKCMlQE\nJEvxQrYBYs7cbGY/PIRCft+F28VwUAilHLRNLpME+CAPI35VV6K+oVeEbBFiEgbE\nWss++52Tjy6knCeb7a+aaEPsEu5+0Q6zTVauCTRBCEDngj13DbeBQsEitcOW8g11\nrpGLCqiFJsFrJLuKcxHyNefiALufEACeVwIDAQAB\n-----END RSA PUBLIC KEY-----"
            var key = new NodeRSA(rsadata);
            cipherText = key.encrypt(data, 'base64');
            console.log(cipherText);

          var params=""
        await this.contract.methods.set_data(price,cipherText,params,epsilon,this.account.address).send({
            'gas':1000000,
            'gasPrice': web3.utils.toWei('1', 'gwei'),
            'from':this.account.address,
            // 'nonce':0
    }).on('receipt', function(receipt){
      // receipt example

      //console.log(receipt,"tert");
      var tx = new Tx(receipt);
      tx.sign(prikey);
      var serializedTx = tx.serialize();
      console.log(serializedTx.toString('hex'),"test");
      web3.eth.sendRawTransaction(serializedTx.toString('hex'), function(err, hash) {
        if (!err)
          console.log(hash); // "0x7f9fade1c0d57a7af66ab4ead79fade1c0d57a7af66ab4ead7c2c2eb7b11a91385"
      });
    })
    .on('error',console.error);
  }
}
var epsilons=[23,69,86,74,96]
var prices=[1000000,3000000,5000000,7000000,9000000]
var privs=['0xbea9bf4e01dc9ff582f4fa8a535a1dcdf637bfbe27667f0d4ad46f1e45535675'
, '0x3c2df8e0ef721b197c9e1fba2062675927125860eac71edca7dd23f3e62bea3c'
, '0xabe4e5a5972c6a6383b30e439d8f820145f3c35c09c2c6c3b630c444e2577e36'
, '0x7975186f9faa4c494ad7e58638640c0e223d4aea6154b55b77ff61bc12ca9a40'
, '0x66a55c5f943118e284f74e64f5c8be5cffe55ab7ae045c3ec603efbdf14e7797'
, '0x5786411c8be0ee30e88f3eb6e9d30d86c14828d7d0c7b1b257fc2da58116e5c6'
, '0xdce48224fa51ec3c14c48fc22610100e385bf3a345482394984b421092fed51d'
, '0x95efd413c2c28396fe8f6d57220dfa8500a63836c2af1c6236a2b2300b693566'
, '0x748738d532d170e98c9e8a6fecdce52ae70e5830819c70e208637c5604a3dcd5'
, '0xb816c10ce07861c789d2188805554153aaff462a1fd3c6caa07891f1ed1602b1']
for(var i=0;i<5;i++)
{
  var user=new Eth(privs[i])
console.log(user.account)
console.log(user.login())
user.getAccount().then(function (result){
    console.log(result);
  });
user.createNewData('{"destination": "Shanghai", "days": 18, "price": 2029}',epsilons[i],prices[i]).then(function (result){
    console.log(result);
  });
}

var user1=new Eth('0x3c2df8e0ef721b197c9e1fba2062675927125860eac71edca7dd23f3e62bea3c')
console.log(user1.account)
console.log(user1.login())
user1.getAccount().then(function (result){
    console.log(result);
  });
console.log(user1.createNewTransaction(0,0,0,0).then(function (result){
  console.log(result);
}))
