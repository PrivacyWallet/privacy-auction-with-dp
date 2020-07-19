const abi = require('./abi.js')
var NodeRSA = require('node-rsa')
var fs = require('fs')
var Tx = require('ethereumjs-tx');
async function deployBuyer()
{
  
}
async function createNewTransaction(   filter,
    selectType,
    queryType,
    budget,
    calculatorAddress,bindata)
    {
      myContract.deploy({
        data: bindata,
    })
    .send({
        from: window.web3.eth.coinbase,
        gas: 1500000,
        gasPrice: '30000000000000'
    }, function(error, transactionHash){ ... })
    .on('error', function(error){ ... })
    .on('transactionHash', function(transactionHash){ ... })
    .on('receipt', function(receipt){
       console.log(receipt.contractAddress) // 收据中包含了新的合约地址
    })
    .on('confirmation', function(confirmationNumber, receipt){ ... })
    .then(function(newContractInstance){
        console.log(newContractInstance.options.address) // 新地址的合约实例
    });
        contract=new web3.eth.Contract(abi.Calc, calculatorAddress)
        await contract.methods.bid(calculatorAddress,"median").send(
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
          'from':web3.eth.defaultAccount,
        }
      ).on('receipt', function(receipt){
        // receipt example
        //console.log(receipt);
      }
    )
      .on('error',console.error);
      }
    async function  getTransactionsAsDataOwner()
          {
            if (endBlockNumber == null) {
                endBlockNumber = eth.blockNumber;
                console.log("Using endBlockNumber: " + endBlockNumber);
              }
              if (startBlockNumber == null) {
                startBlockNumber = 0;
                console.log("Using startBlockNumber: " + startBlockNumber);
              }
              console.log("Searching for transactions to/from account \"" + myaccount + "\" within blocks "  + startBlockNumber + " and " + endBlockNumber);
            
              for (var i = startBlockNumber; i <= endBlockNumber; i++) {
                if (i % 1000 == 0) {
                  console.log("Searching block " + i);
                }
                var block = eth.getBlock(i, true);
                if (block != null && block.transactions != null) {
                  block.transactions.forEach( function(e) {
                    if (myaccount == "*" || myaccount == e.from || myaccount == e.to) {
                      console.log("  tx hash          : " + e.hash + "\n"
                        + "   nonce           : " + e.nonce + "\n"
                        + "   blockHash       : " + e.blockHash + "\n"
                        + "   blockNumber     : " + e.blockNumber + "\n"
                        + "   transactionIndex: " + e.transactionIndex + "\n"
                        + "   from            : " + e.from + "\n" 
                        + "   to              : " + e.to + "\n"
                        + "   value           : " + e.value + "\n"
                        + "   time            : " + block.timestamp + " " + new Date(block.timestamp * 1000).toGMTString() + "\n"
                        + "   gasPrice        : " + e.gasPrice + "\n"
                        + "   gas             : " + e.gas + "\n"
                        + "   input           : " + e.input);
                    }
                  })
                }
              }
          }
       Array<{
        date
        status
        deployedContract
        calculatorAddress
        transactions
      }>