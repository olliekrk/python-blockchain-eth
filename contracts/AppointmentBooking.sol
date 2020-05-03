pragma solidity >=0.4.25 <0.7.0;
pragma experimental ABIEncoderV2;

contract AppointmentBooking {
    string public name;

    mapping(uint256 => Appointment) appointments;
    uint256[] dates;
    address payable public doctor;

    struct Appointment {
        uint256 date;
        string name;
        uint price;
        address payable patient;
        bool isCreated;
    }

    event AppointmentCreated(
        uint256 date,
        string name,
        uint price,
        address payable patient
    );

    event AppointmentBooked(
        uint256 date,
        string name,
        uint price,
        address payable patient
    );

    constructor(string memory _data) public {
        name = "Book some appointments";
        doctor = msg.sender;
    }


    function printAppointments() public view
        returns (string[] memory ,uint256[] memory,uint[] memory) {



            uint256[] memory result_dates = new uint256[](dates.length);
            string[] memory names = new string[](dates.length);
            uint[] memory prices = new uint[](dates.length);

            for (uint i = 0; i < dates.length; i++) {
                Appointment storage appointment = appointments[dates[i]];
                result_dates[i] = appointment.date;
                names[i] = appointment.name;
                prices[i] = appointment.price;
            }

            return (names, result_dates, prices);
    }

    function createAppointment(string memory _name, uint256 _date, uint _price) public {
        require(!appointments[_date].isCreated);
        require(
            msg.sender == doctor,
            "Only owner can add an appointment"
        );


        require(bytes(_name).length > 0);

        require(_price > 0);

        appointments[_date] = Appointment(_date, _name, _price, address(0),true);

        dates.push(_date);
        emit AppointmentCreated(_date, _name, _price, address(0));
    }


    function bookAppointment(uint256 _date) public payable {

        require(appointments[_date].isCreated,
        "This date doesn't exist");

        Appointment memory _appointment = appointments[_date];
        require(_appointment.patient == address(0),
        "This appointment is reserved");

        require(msg.value >= _appointment.price,
        "The price is to small");
        require(doctor != msg.sender,
        "Doctor can't reserve own visit");


        _appointment.patient = msg.sender;

        appointments[_date] = _appointment;

        address(doctor).transfer(msg.value);

        emit AppointmentBooked(_appointment.date, _appointment.name, _appointment.price, msg.sender );
    }
}