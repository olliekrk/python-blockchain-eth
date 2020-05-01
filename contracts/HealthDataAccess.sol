pragma solidity >=0.4.25 <0.7.0;

contract HealthDataAccess {

    mapping(address => bool) private userAccess;
    HeartMeasurement[] private measurements;
    string data; // simulates pointer to data stored in a external secured storage
    address public owner;

    event DataAccessed(address _user);
    event AccessGranted(address _user);
    event AccessRevoked(address _user);
    event MeasurementCreated (
        uint256 timestamp,
        uint bpm
    );

    struct HeartMeasurement {
        uint256 timestamp;
        uint bpm;
    }

    constructor (string memory _data) public {
        data = _data;
        owner = msg.sender;
        userAccess[owner] = true;
    }

    function addMeasurement(uint _bpm, uint256 _timestamp) public {
        require(
            msg.sender == owner,
            "Only owner can add a measurement"
        );
        require(_bpm > 0);
        measurements.push(HeartMeasurement({
                timestamp: _timestamp,
                bpm: _bpm
            }));
        emit MeasurementCreated(_timestamp, _bpm);
    }

    function getLastMeasurement() public view
        returns (uint256 timestamp, uint _bpm) {
            require(
                userAccess[msg.sender] == true,
                "No access"
            );
            uint lastIndex = measurements.length - 1;
            HeartMeasurement memory measurement = measurements[lastIndex];


            return (measurement.timestamp, measurement.bpm);
    }

    function getMeasurements() public view
        returns (uint256[] memory, uint[] memory) {

            require(
                userAccess[msg.sender] == true,
                "No access"
            );

            uint256[] memory timestamps = new uint256[](measurements.length);
            uint[]    memory bpms = new uint[](measurements.length);

            for (uint i = 0; i < measurements.length; i++) {
                HeartMeasurement storage measurement = measurements[i];
                timestamps[i] = measurement.timestamp;
                bpms[i] = measurement.bpm;
            }

            return (timestamps, bpms);
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

}



