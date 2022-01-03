// SPDX-License-Identifier: MIT
// 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e

pragma solidity ^0.6.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    uint256 currentAmount;
    address public owner;
    address[] public funders;
    AggregatorV3Interface priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minimumUSD = 50 * 10**18;
        // Make sure that the amount sent by user must be greater than 50 USD
        // But both the amount sent by user and 50 USD are in wei units.
        require(
            getConversionRate(msg.value) >= minimumUSD,
            "You need to spend more ETH"
        );
        // addressToAmountFunded[msg.sender] = address(msg.sender).balance - msg.value;
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);

        // msg.sender represents the current account that is interacting with this smart contract
    }

    function getVersion() public view returns (uint256) {
        // The current version of this priceFeed will be returned.
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        // The address in this method is the price feed address of ETH/USD
        (, int256 answer, , , ) = priceFeed.latestRoundData();

        return uint256(answer * 10**10);
        /* answer holds the currrent value of USD that corresponds to ETH (in GWEI), i.e,
         2,482.55877123 USD = 1 ETH
         248255877123 GWEI = 2,482.55877123 USD

        answer stores 248255877123 GWEI (i.e. approximately $2482.6 is the actual USD value accompanied with 8 decimals
        and starting price is 248255877123)

        So, If I want to create a fake priceFeed with MockAggregator and I want 1 ETH to equal $2000, my starting price
        will be 2000+"00000000" = 200000000000 and decimals will be 8

        answer * 10000000000 = 2482558771230000000000
        i.e, = 2482558771230000000000 WEI = 2,482.55877123 USD

         Because we want our return value to be in WEI, we multiply answer by 10000000000 
         */
    }

    function getEntranceFee() public view returns (uint256) {
        // We convert minimum USD, i.e 50 dollars to ether.
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 10**18;
        return ((minimumUSD * precision) / price) + 100;
    }

    function getConversionRate(uint256 etherAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        return (etherAmount * ethPrice) / 10**18;

        // Output: 2533894899860

        /*
      Note that solidity does not return number with decimal point. So, The actual value is this;
      0.000002533894899860 dollars

      /what solidity does is that it will return the dollar value in wei.

      */
    }

    function getEtherAmount() public view returns (uint256) {
        return currentAmount;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "ETH can only be withdrawn by the owner");
        _;
    }

    function withdraw() public payable onlyOwner {
        payable(msg.sender).transfer(address(this).balance);

        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        // initializing the address array
        funders = new address[](0);
    }
}
