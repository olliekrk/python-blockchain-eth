pragma solidity >=0.4.25 <0.7.0;

contract HealthDataAccess {

    mapping(address => bool) public userAccess;
    string data; // simulates pointer to data stored in a external secured storage
    address public owner;

    event DataAccessed(address _user);
    event AccessGranted(address _user);
    event AccessRevoked(address _user);

    constructor (string memory _data) public {
        data = _data;
        owner = msg.sender;
        userAccess[owner] = true;
    }

    function grantAccess(address _user) public {
        require(
            msg.sender == owner,
            "Only owner can grant access to the data."
        );
        emit AccessGranted(_user);
        userAccess[_user] = true;
    }

    function revokeAccess(address _user) public {
        require(
            msg.sender == owner,
            "Only owner can revoke access to the data."
        );
        emit AccessRevoked(_user);
        userAccess[_user] = false;
    }

    function hasAccess(address _user) public view returns (bool){
        return userAccess[_user];
    }

    function accessData() public returns (string memory) {
        require(
            userAccess[msg.sender] == true,
            "No access"
        );
        emit DataAccessed(msg.sender);
        return data;
    }

}