pragma solidity >=0.4.25 <0.7.0;

contract HealthDataCollected {

    address public owner;

    modifier ownerOnly() {require(msg.sender == owner, "Only owner is authorized"); _;}

    function accessData() public ownerOnly view returns (address) {
        return owner;
        // just mock, todo
    }


}