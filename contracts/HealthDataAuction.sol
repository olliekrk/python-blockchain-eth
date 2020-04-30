pragma solidity >=0.4.25 <0.7.0;

// Institutions or patients may bid medical data of other patients.
contract HealthDataAuction {

    address payable public beneficiary;
    uint public auctionEndTime;
    bool end;

    address public highestBidder;
    uint public highestBid;

    mapping(address => uint) pendingReturns;

    event AuctionEnd(address _winner, uint _amount);
    event BidIncrease(address _bidder, uint _amount);

    constructor(uint _auctionDuration, address payable _beneficiary) public {
        beneficiary = _beneficiary;
        auctionEndTime = now + _auctionDuration;
    }

    function bid() public payable {
        require(
            now <= auctionEndTime,
            "Auction has ended!"
        );
        require(
            msg.value > highestBid,
            "The best bid is already higher!"
        );

        if (highestBid != 0) {
            pendingReturns[highestBidder] += highestBid;
        }

        highestBidder = msg.sender;
        highestBid = msg.value;
        emit BidIncrease(msg.sender, msg.value);
    }

    function withdraw() public returns (bool) {
        uint amount = pendingReturns[msg.sender];
        if (amount > 0) {
            pendingReturns[msg.sender] = 0;
            if (!msg.sender.send(amount)) {
                pendingReturns[msg.sender] = amount;
                return false;
            }
        }
        return true;
    }

    function auctionComplete() public {
        require (now >= auctionEndTime, "Auction has not ended");
        require (!end, "Auction has already been paid");
        end = true;
        emit AuctionEnd(highestBidder, highestBid);
        beneficiary.transfer(highestBid);
    }
}