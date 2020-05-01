const HDAccess = artifacts.require("HealthDataAccess");
const HDAuction = artifacts.require("HealthDataAuction");
const AppointmentBooking = artifacts.require("AppointmentBooking");

module.exports = function(deployer) {

  deployer.deploy(AppointmentBooking);
  // deployer.deploy(HDAccess);
  // deployer.deploy(HDAuction);

};
