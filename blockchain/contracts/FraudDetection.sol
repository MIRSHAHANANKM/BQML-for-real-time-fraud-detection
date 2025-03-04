// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract FraudDetection {
    struct FraudRecord {
        uint256 transactionId;
        address user;
        uint256 amount;
        string riskLevel;
        uint256 timestamp;
    }

    mapping(uint256 => FraudRecord) public fraudRecords;
    uint256 public fraudCount;

    event FraudDetected(uint256 transactionId, address user, uint256 amount, string riskLevel, uint256 timestamp);

    function reportFraud(uint256 _transactionId, address _user, uint256 _amount, string memory _riskLevel) public {
        fraudRecords[fraudCount] = FraudRecord(_transactionId, _user, _amount, _riskLevel, block.timestamp);
        emit FraudDetected(_transactionId, _user, _amount, _riskLevel, block.timestamp);
        fraudCount++;
    }

    function getFraudRecord(uint256 _id) public view returns (uint256, address, uint256, string memory, uint256) {
        FraudRecord memory record = fraudRecords[_id];
        return (record.transactionId, record.user, record.amount, record.riskLevel, record.timestamp);
    }
}
