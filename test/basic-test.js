const truffleAssert = require("truffle-assertions");
let Calculator = artifacts.require("Calculator");
let DataBuyer = artifacts.require("DataBuyer");

contract("Calculator", async (accounts) => {
  it("should say 'hello world'", async () => {
    let i = await Calculator.deployed();
    let result = await i.say();
    assert.equal(result, "Hello World");
  });
});

contract("DataOwner", async (accounts) => {
  it("created by accounts[0]", async () => {
    let calculator = await Calculator.deployed();
    let address = await calculator.calculator();
    assert.notStrictEqual(address, accounts[1]);
    assert.strictEqual(address, accounts[0]);
  });

  it("should say 'hello world' again", async () => {
    let calculator = await Calculator.deployed();
    let result = await calculator.say();
    assert.equal(result, "Hello World");
  });

  it("can set data", async () => {
    let calculator = await Calculator.deployed();
    let data = await calculator.data();
    assert.strictEqual(data.words[0], 0);
    let result = await calculator.set_data(
      1,
      "encrypted_data",
      "params",
      3,
      accounts[0]
    );
    assert.equal(result.receipt.status, true);
    data = await calculator.data();
    assert.strictEqual(data.words[0], 1);
    result = await calculator.set_data(
      2,
      "encrypted_data hi",
      "params",
      8,
      accounts[0]
    );
    assert.equal(result.receipt.status, true);
    data = await calculator.data();
    assert.strictEqual(data.words[0], 1);
    result = await calculator.set_data(
      1,
      "encrypted_data",
      "params",
      3,
      accounts[2]
    );
    assert.equal(result.receipt.status, true);
    data = await calculator.data();
    assert.strictEqual(data.words[0], 2);
  });

  it("can get data", async () => {
    let calculator = await Calculator.deployed();
    let data = await calculator.get_data({ from: accounts[0] });
    assert.equal(data.price, 2);
    assert.equal(data.encrypted_data, "encrypted_data hi");
    assert.equal(data.epsilon, 8);
    data = await calculator.get_data({ from: accounts[2] });
    assert.equal(data.price, 1);
    assert.equal(data.encrypted_data, "encrypted_data");
    assert.equal(data.epsilon, 3);
  });
});

contract("DataBuyer", async (accounts) => {
  it("should say 'hello world'", async () => {
    let i = await Calculator.deployed();
    let result = await i.say();
    assert.equal(result, "Hello World");
  });

  // TODO should failed

  it("should bid normaly with data given", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();
    await calculator.set_data(
      1,
      "encrypted_data 2",
      "params",
      1e6,
      accounts[1]
    );
    await calculator.set_data(
      2,
      "encrypted_data 3",
      "params",
      3e6,
      accounts[2]
    );
    await calculator.set_data(
      1,
      "encrypted_data 2",
      "params",
      5e6,
      accounts[3]
    );
    await calculator.set_data(
      4,
      "encrypted_data 2",
      "params",
      7e6,
      accounts[4]
    );
    await calculator.set_data(
      4,
      "encrypted_data 2",
      "params",
      9e6,
      accounts[5]
    );

    for await (const b of accounts) {
      let t = await web3.eth.getBalance(b);
      console.debug(t);
    }
    let data = await calculator.get_data({ from: accounts[1] });
    assert.equal(data.price, 1);
    data = await calculator.get_data({ from: accounts[2] });
    assert.equal(data.price, 2);
    data = await calculator.get_data({ from: accounts[3] });
    assert.equal(data.price, 1);
    data = await calculator.get_data({ from: accounts[4] });
    assert.equal(data.price, 4);

    let result = await calculator.bid(databuyer.address, {
      from: accounts[0],
      gas: 3000000,
      value: 1.2e7,
    });

    let theta_vec = await databuyer.get_theta_vec();
    //console.debug(theta_vec.map(v=>v.toNumber()))
    cmp_list = [2427, 1887, 1348, 809, 269];
    for (let i = 0, len = theta_vec.length; i < len; i++) {
      n = theta_vec[i].toNumber();
      assert.equal(Math.abs(n - cmp_list[i]) < 100, true);
    }
    //console.debug(result)
    //truffleAssert.eventEmitted(result, 'data_selected', (ev) => {
    ////console.debug(ev);
    //return ev.owners_data.length === 4;
    //})
    for await (const b of accounts) {
      let t = await web3.eth.getBalance(b);
      console.debug(t);
    }

    //calculator.getPastEvents("allEvents", {fromBlock: 0, toBlock: "latest"})
    //.then(console.debug)
  });

  it("should overwrite older record", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();
    await calculator.set_data(
      10,
      " encrypted_data 2",
      "params",
      1e6,
      accounts[1]
    );
    await calculator.set_data(
      20,
      " encrypted_data 3",
      "params",
      3e6,
      accounts[2]
    );
    await calculator.set_data(
      10,
      " encrypted_data 2",
      "params",
      1e6,
      accounts[1]
    );
    await calculator.set_data(
      20,
      " encrypted_data 3",
      "params",
      3e6,
      accounts[2]
    );
    await calculator.set_data(
      10,
      " encrypted_data 2",
      "params",
      5e6,
      accounts[3]
    );
    await calculator.set_data(
      40,
      " encrypted_data 2",
      "params",
      7e6,
      accounts[4]
    );
    await calculator.set_data(
      40,
      " encrypted_data 2",
      "params",
      7e6,
      accounts[5]
    );

    let result = await debug(
      calculator.bid(databuyer.address, {
        from: accounts[0],
        gas: 3000000,
        value: 1.2e7,
      })
    );

    let theta_vec = await databuyer.get_theta_vec();
    //console.debug(theta_vec)
    truffleAssert.eventEmitted(result, "data_selected", (ev) => {
      //console.debug(ev.owners_data.map(e=> e.toNumber()));
      console.log(ev)
      
      return ev.owners_data.length === 5 && ev.owners_epsilon.length === 5 && ev.data_buyer === accounts[0] && ev.data_buyer_contract === databuyer.address;
    });
  });

  it("should set requirements correctly", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();

    let json = JSON.stringify({
      hello: "world",
    });

    await databuyer.set_requirements(json);

    let result = await calculator.bid(databuyer.address, {
      from: accounts[0],
      gas: 3000000,
      value: 1.2e7,
    });

    truffleAssert.eventEmitted(result, "data_selected", (ev) => {
      //console.debug(ev.owners_data.map(e=> e.toNumber()));
      return ev.requirements == json;
    });

  });

  it("should send results normaly", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();
    await calculator.set_data(
      1,
      "encrypted_data 2",
      "params",
      1e6,
      accounts[1]
    );
    let res = "encrypted_data 12312414";
    let bidEndResult = await calculator.bidEnd(accounts[0], res);
    console.log(bidEndResult);

    let result = await databuyer.get_result();

    assert.equal(result, res);

    for (const a of accounts) {
      let b = await web3.eth.getBalance(a);
      console.log(b);
    }
  });

  it("can get transaction info", async ()=>{
    let databuyer = await DataBuyer.deployed();
    let calculator = await Calculator.deployed();

    let result = await calculator.getDataBuyerTransactionInfo(accounts[0])
    console.log(result)
    assert.equal(result.selected_owner.length, 5)
  })
});
