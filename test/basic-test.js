const truffleAssert = require('truffle-assertions');
let Calculator = artifacts.require("Calculator");
let DataBuyer = artifacts.require("DataBuyer");

contract('Calculator', async accounts => {
  it("should say 'hello world'", async () => {
    let i = await Calculator.deployed()
    let result = await i.say()
    assert.equal(result, 'Hello World')
  })
});

contract('DataOwner', async accounts => {
  it("created by accounts[0]", async () => {
    let calculator = await Calculator.deployed()
    let address = await calculator.calculator()
    assert.notStrictEqual(address, accounts[1])
    assert.strictEqual(address, accounts[0])
  })

  it("should say 'hello world' again", async () => {
    let calculator = await Calculator.deployed()
    let result = await calculator.say()
    assert.equal(result, 'Hello World')
  })

  it("can set data", async () => {
    let calculator = await Calculator.deployed()
    let data = await calculator.data()
    assert.strictEqual(data.words[0], 0)
    let result = await calculator.set_data(1,2,3, accounts[0]);
    assert.equal(result.receipt.status, true)
    data = await calculator.data()
    assert.strictEqual(data.words[0], 1)
    result = await calculator.set_data(2,4,8, accounts[0]);
    assert.equal(result.receipt.status, true)
    data = await calculator.data()
    assert.strictEqual(data.words[0], 1)
    result = await calculator.set_data(1,2,3, accounts[2]);
    assert.equal(result.receipt.status, true)
    data = await calculator.data()
    assert.strictEqual(data.words[0], 2)
  })

  it("can get data", async () => {
    let calculator = await Calculator.deployed()
    let data = await calculator.get_data({from: accounts[0]})
    assert.equal(data.price, 2)
    assert.equal(data.encrypted_data, 4)
    assert.equal(data.epsilon, 8)
    data = await calculator.get_data({from: accounts[2]})
    assert.equal(data.price, 1)
    assert.equal(data.encrypted_data, 2)
    assert.equal(data.epsilon, 3)


  })
});

contract('DataBuyer', async accounts => {
  it("should say 'hello world'", async () => {
    let i = await Calculator.deployed()
    let result = await i.say()
    assert.equal(result, 'Hello World')
  })

  // TODO should failed 

  it("should bit with empty data given", async () => {
    let calculator = await Calculator.deployed()
    let databuyer = await DataBuyer.deployed()
    await calculator.set_data(1,2,3, accounts[1]);
    await calculator.set_data(2,3,4, accounts[2]);
    await calculator.set_data(1,2,3, accounts[3]);
    await calculator.set_data(4,2,3, accounts[4]);
    let data = await calculator.get_data({from: accounts[1]})
    assert.equal(data.price, 1)
    data = await calculator.get_data({from: accounts[2]})
    assert.equal(data.price, 2)
    data = await calculator.get_data({from: accounts[3]})
    assert.equal(data.price, 1)
    data = await calculator.get_data({from: accounts[4]})
    assert.equal(data.price, 4)
 
    let result = await calculator.bid(databuyer.address, {from:accounts[0], gas: 3000000, value: 100})
    //console.debug(result)
    truffleAssert.eventEmitted(result, 'data_selected', (ev) => {
      //console.debug(ev);
      return ev.owners_data.length === 4;
    })

    //calculator.getPastEvents("allEvents", {fromBlock: 0, toBlock: "latest"})
//.then(console.debug)

  })
});

