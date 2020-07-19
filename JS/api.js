const abi = require('./abi.js')
var NodeRSA = require('node-rsa')
var fs = require('fs')
var Tx = require('ethereumjs-tx');
async function createNewTransaction(   filter,
    selectType,
    queryType,
    budget,
    calculatorAddress,bindata)
    {
    const web3=window.web3;
    var myContract = web3.eth.contract(abi.Inter);
    await myContract.deploy({
      data: bindata,
  })
  .send({
      from: web3.eth.coinbase,
      gas: 1500000,
      gasPrice: '30000000000000'
  }, function(error, transactionHash){  })
  .on('error', function(error){  })
  .on('transactionHash', function(transactionHash){ })
  .on('receipt', function(receipt){
     console.log(receipt.contractAddress) // 收据中包含了新的合约地址
  })
  .on('confirmation', function(confirmationNumber, receipt){ })
  .then(function(newContractInstance){
      console.log(newContractInstance.options.address) // 新地址的合约实例
  });
        contract=new web3.eth.Contract(abi.Calc, calculatorAddress)
        await contract.methods.bid(myContract.address,"median").send(
            {
                'gas':3000000,
                'gasPrice': web3.utils.toWei('1', 'gwei'),
                'from':window.web3.eth.coinbase,
                // 'nonce' : web3.eth.getTransactionCount(this.account.address),
                'value':budget
            }
        ).on('receipt', function(receipt){
          // receipt example
          //console.log(receipt);
        }
      )
        .on('error',console.error);
    }
async function uploadNewData(
        data,
        epsilon,
        price,
        calculatorAddress,
        rsadata
      ){
        const web3=window.web3;
        contract=new web3.eth.Contract(abi.Calc, calculatorAddress)
        key = new NodeRSA(rsadata,'pkcs1-public-pem');
        var cipherText
        key.setOptions({encryptionScheme: 'pkcs1'});
        console.log(data)
        console.log(this.key.isPublic())
        cipherText = this.key.encrypt(data, 'hex');
        console.log(cipherText)
        var params=""
    await contract.methods.set_data(epsilon,cipherText,params,price,this.account.address).send(
        {
          'gas':1000000,
          'gasPrice': web3.utils.toWei('1', 'gwei'),
          'from':web3.eth.coinbase,
        }
      ).on('receipt', function(receipt){

      }
    )
      .on('error',console.error);
      }
