//const DataBuyerInterface = artifacts.require("DataBuyerInterface");
const IterableMapping = artifacts.require("IterableMapping")
const DataBuyer = artifacts.require("DataBuyer");
const Calculator = artifacts.require("Calculator");
const Calculator2 = artifacts.require("Calculator");

module.exports = function(deployer) {
  //deployer.deploy(DataBuyerInterface)
  deployer.deploy(DataBuyer);
  //deployer.link(DataBuyerInterface, Calculator);
  deployer.deploy(IterableMapping)
  deployer.link(IterableMapping, Calculator)
  deployer.deploy(Calculator);
  deployer.link(IterableMapping, Calculator2)
  deployer.deploy(Calculator2);
}
