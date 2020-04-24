const DataBuyerInterface = artifacts.require("DataBuyerInterface");
const DataBuyer = artifacts.require("DataBuyer");
const Calculator = artifacts.require("Calculator");

module.exports = function(deployer) {
  //deployer.link(DataBuyerInterface, DataBuyer);
  deployer.deploy(DataBuyer);
  //deployer.link(DataBuyerInterface, Calculator);
  deployer.deploy(Calculator);
}
