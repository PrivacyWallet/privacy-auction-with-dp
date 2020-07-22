+const abi = require('./abi.js')

async function createNewTransaction(
  filter,
  selectType,
  queryType,
  budget,
  calculatorAddress,
  bindata,
  onsuccess,
  onfail,
) {
  const web3 = window.web3
  const myContract = web3.eth.contract(abi.Inter)
  await myContract
    .deploy({
      data: bindata,
    })
    .send(
      {
        from: web3.eth.coinbase,
        gas: 1500000,
        gasPrice: '30000000000000',
      },
      function(error, transactionHash) {
        console.log(error)
      }
    )
    .on('error', function(error) {
      console.log(error)
    })
    .on('transactionHash', function(transactionHash) {})
    .on('receipt', function(receipt) {
      console.log(receipt.contractAddress) // 收据中包含了新的合约地址
    })
    .on('confirmation', function(confirmationNumber, receipt) {})
    .then(function(newContractInstance) {
      console.log(newContractInstance.options.address) // 新地址的合约实例
    })
  const contract = new web3.eth.Contract(abi.Calc, calculatorAddress)
  await contract.methods
    .bid(myContract.address, 'median')
    .send({
      gas: 3000000,
      gasPrice: web3.utils.toWei('1', 'gwei'),
      from: window.web3.eth.coinbase,
      // 'nonce' : web3.eth.getTransactionCount(this.account.address),
      value: budget,
    })
    .on('receipt', onsuccess)
    .on('error', onfail)
}

async function uploadNewData(data, epsilon, price, calculatorAddress, onsuccess, onfail) {
  const rsadata =
    '-----BEGIN RSA PUBLIC KEY-----\n' +
    'MIIBCgKCAQEAqymJH1pMkr4F9NR8nze09w+iMMejql4bk7GpVa0xjilCDsvVHvxD\n' +
    'FhVHVRxpuZyM5p684sUGleV0qZXBXFuBzSLrY7n6GqlgP5qQorhCkQP7q05sqGtU\n' +
    '95dYbn3LjEzYs14XtTCXZvO6zHzABoLceKzeYGHjahtKLIitLR1NbNYbrgKCMlQE\n' +
    'JEvxQrYBYs7cbGY/PIRCft+F28VwUAilHLRNLpME+CAPI35VV6K+oVeEbBFiEgbE\n' +
    'Wss++52Tjy6knCeb7a+aaEPsEu5+0Q6zTVauCTRBCEDngj13DbeBQsEitcOW8g11\n' +
    'rpGLCqiFJsFrJLuKcxHyNefiALufEACeVwIDAQAB\n' +
    '-----END RSA PUBLIC KEY-----'
  const web3 = window.web3
  const contract = new web3.eth.Contract(abi.Calc, calculatorAddress)
  const account = await web3.eth.getCoinbase()
  const encrypt = new JSEncrypt()
  encrypt.setPublicKey(rsadata)
  const cipherText = encrypt.encrypt(data)
  const params = ' '
  contract.methods
    .set_data(price, cipherText, params, epsilon, account)
    .send({
      gas: 1000000,
      gasPrice: web3.utils.toWei('1', 'gwei'),
      from: account,
    })
    .on('receipt', onsuccess)
    .on('error', onfail)
}


