const truffleAssert = require("truffle-assertions");
const cliProgress = require("cli-progress")
let Calculator = artifacts.require("Calculator");
let DataBuyer = artifacts.require("DataBuyer");

contract("DataOwner", async (accounts) => {
  it("upload data", async () => {
    let calculator = await Calculator.deployed();
    const bar1 = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic)
    const total = accounts.length
    console.log(total)
    bar1.start(total, 0)
    console.time("upload data")
    for (let i in accounts) {
      let result = await calculator.set_data(
        1,
        "encrypted_data",
        "params",
        3,
        accounts[i]
      );
      bar1.increment()
    }
    console.timeEnd("upload data")
    bar1.stop()
    assert.equal("end", "end");
  });

  it("bid", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();

    let json = JSON.stringify({
      hello: "world",
    });

    await databuyer.set_requirements(json);

    console.time("bid")
    let result = await calculator.bid(databuyer.address, {
      from: accounts[0],
      gas: 300000000,
      value: 1.2e7,
    });
    console.timeEnd("bid")
    assert.equal("end", "end");
  })
});
