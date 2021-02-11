const truffleAssert = require("truffle-assertions");
const cliProgress = require("cli-progress");
const NodeRSA = require("node-rsa");

const databuyer_keys = require("./data-buyer-keys");

let Calculator = artifacts.require("Calculator");
let DataBuyer = artifacts.require("DataBuyer");

const rsadata =
  "-----BEGIN PUBLIC KEY-----\n" +
  "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA61u0yB8hGtizMyNuPNvY\n" +
  "oGnhbVm55AmHpLBDXNOMks7l+InHyo6A1BchjxVQUNB+YKb1aV7UfHU1pJQ5fJYs\n" +
  "fOx+daK0C8NU30168diQ9E5Il6uhLG/OmnglqExJPsjorzd+smIyjdaWG8nJNJOL\n" +
  "VKOxiaJCCVTL+wH98BXjSRKaQ0437bCt1hxUSiHiuxvgFbZ6pp7e2WGftfkXIltc\n" +
  "LXzFPees0Zd1HZ/PDQzTkkRQ96ygw5hXZ6DnpSPl25H4ncRIgZgTD14fDE1EICND\n" +
  "6CFQXzK/GoX9dFNN/7ubaWLKVw7aMHK0B7TxyIwjqUt8gthOaT//XWk/IzntI6n+\n" +
  "JQIDAQAB\n" +
  "-----END PUBLIC KEY-----";

let encryptData = (text, pubkey) => {
  const encrypt = new NodeRSA(pubkey);
  return encrypt.encrypt(text, "base64");
};

let decryptData = (enc_text, privkey) => {
  const decrypt = new NodeRSA(privkey);
  return decrypt.decrypt(enc_text, "utf8");
};

let printGasUse = (number, result) => {
  console.log(`step${number}:`, result.receipt.gasUsed, result.receipt.cumulativeGasUsed)
}

contract("DataOwner", async (accounts) => {
  it("upload data", async () => {
    let calculator = await Calculator.deployed();

    let result
    // Step 1: 数据所有者加密并上传数据
    console.time("step1: upload data");
    for (let i in accounts) {
      result = await calculator.set_data(
        1,
        encryptData("unencrypted_data", rsadata),
        "params",
        3,
        accounts[i]
      );
    }
    console.timeEnd("step1: upload data");

    printGasUse(1, result)

    assert.equal("end", "end");
  });

  it("bid", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();

    let json = JSON.stringify({
      hello: "world",
    });

    await databuyer.set_requirements(json);

    // Step 2: 数据购买者发起购买请求，包括打钱
    console.time("step2: bid");
    let result = await calculator.bid(databuyer.address, {
      from: accounts[0],
      gas: 300000000,
      value: 1.2e7,
    });
    console.timeEnd("step2: bid");

    printGasUse(2, result)
  });

  it("get result", async () => {
    let calculator = await Calculator.deployed();
    let databuyer = await DataBuyer.deployed();

    // Step 4.1: 链下计算完成后，外包计算者上传数据
    console.time("step3: bidEnd");
    let raw_data = JSON.stringify({
      answer: 123123,
    });

    let enc_data = encryptData(raw_data, databuyer_keys.pubkey);
    let bidEndResult = await calculator.bidEnd(accounts[0], enc_data);
    console.timeEnd("step3: bidEnd");

    printGasUse(3, bidEndResult)


    // Step 4.2: 购买者获得数据并解密
    console.time("step4: get_result");
    let result = await databuyer.get_result();
    let r = decryptData(result, databuyer_keys.privkey);
    console.timeEnd("step4: get_result");
  });
});
