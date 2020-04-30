const HDAccess = artifacts.require("HealthDataAccess");
const HDAuction = artifacts.require("HealthDataAuction");

module.exports = function(deployer) {
  deployer.deploy(HDAccess);
  deployer.deploy(HDAuction);
};
