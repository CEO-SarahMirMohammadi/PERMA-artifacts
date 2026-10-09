// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";

/// @title TradeLoggerV2
/// @notice Allows an owner to authorize loggers and limits trade logging to trusted addresses.
contract TradeLoggerV2 is Ownable {
    mapping(address => bool) public authorizedLoggers;

    event LoggerAdded(address indexed logger);
    event LoggerRemoved(address indexed logger);
    event TradeLogged(
        address indexed logger,
        address indexed trader,
        string symbol,
        uint256 quantity,
        uint256 price,
        uint256 timestamp
    );

    constructor() Ownable(msg.sender) {
        authorizedLoggers[msg.sender] = true;
        emit LoggerAdded(msg.sender);
    }

    modifier onlyAuthorizedLogger() {
        require(
            authorizedLoggers[msg.sender],
            "TradeLoggerV2: caller is not an authorized logger"
        );
        _;
    }

    function addLogger(address logger) external onlyOwner {
        require(logger != address(0), "TradeLoggerV2: logger cannot be zero address");
        if (!authorizedLoggers[logger]) {
            authorizedLoggers[logger] = true;
            emit LoggerAdded(logger);
        }
    }

    function removeLogger(address logger) external onlyOwner {
        require(logger != address(0), "TradeLoggerV2: logger cannot be zero address");
        require(logger != owner(), "TradeLoggerV2: owner cannot remove itself as a logger");

        if (authorizedLoggers[logger]) {
            authorizedLoggers[logger] = false;
            emit LoggerRemoved(logger);
        }
    }

    function logTrade(
        address trader,
        string calldata symbol,
        uint256 quantity,
        uint256 price
    ) external onlyAuthorizedLogger {
        require(trader != address(0), "TradeLoggerV2: trader cannot be zero address");
        require(bytes(symbol).length > 0, "TradeLoggerV2: symbol is required");
        require(quantity > 0, "TradeLoggerV2: quantity must be greater than zero");
        require(price > 0, "TradeLoggerV2: price must be greater than zero");

        emit TradeLogged(msg.sender, trader, symbol, quantity, price, block.timestamp);
    }
}
