pragma solidity >=0.4.25 <0.7.0;
pragma experimental ABIEncoderV2;

contract AppointmentBooking {
    string public name;
    string[] private dates;
    mapping(string => Appointment) appointments;

    struct Appointment {
        string date;
        string name;
        uint price;
        address payable patient;
        address payable doctor;
        bool isCreated;
    }

    event AppointmentCreated(
        string date,
        string name,
        uint price,
        address payable patient,
        address payable doctor
    );

    event AppointmentBooked(
        string date,
        string name,
        uint price,
        address payable patient,
        address payable doctor
    );

    constructor() public {
        name = "Book some appointments";
    }


    function printAppointments() public view
        returns (string[] memory, string[] memory ,uint[] memory) {



            string[] memory result_dates = new string[](dates.length);
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

    function createAppointment(string memory _name, string memory _date, uint _price) public {
        require(!appointments[_date].isCreated);


        require(bytes(_name).length > 0);

        require(_price > 0);

        appointments[_date] = Appointment(_date, _name, _price, address(0), msg.sender, true);
        dates.push(_date);

        emit AppointmentCreated(_date, _name, _price, address(0), msg.sender);
    }


    function bookAppointment(string memory _date) public payable {

        require(appointments[_date].isCreated);

        Appointment memory _appointment = appointments[_date];
        require(_appointment.patient == address(0));

        require(msg.value >= _appointment.price);


        _appointment.patient = msg.sender;

        appointments[_date] = _appointment;

        address(_appointment.doctor).transfer(msg.value);

        emit AppointmentBooked(_appointment.date, _appointment.name, _appointment.price, msg.sender, _appointment.doctor );
    }
}