// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract AgentGuard {
    address public owner;
    address public agent;
    uint256 public perTxLimit;
    uint256 public dailyLimit;
    uint256 public sessionBudget;
    uint256 public spentToday;
    uint256 public spentInSession;
    uint256 public lastResetDay;
    mapping(address => bool) public whitelist;
    
    event TransactionExecuted(address indexed to, uint256 amount, uint256 timestamp);
    event TransactionRejected(address indexed to, uint256 amount, string reason, uint256 timestamp);
    event WhitelistUpdated(address indexed addr, bool status);
    
    modifier onlyAgent() {
        require(msg.sender == agent, "Not agent");
        _;
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }
    
    constructor(
        address _agent,
        uint256 _perTxLimit,
        uint256 _dailyLimit,
        uint256 _sessionBudget
    ) {
        owner = msg.sender;
        agent = _agent;
        perTxLimit = _perTxLimit;
        dailyLimit = _dailyLimit;
        sessionBudget = _sessionBudget;
        lastResetDay = block.timestamp / 1 days;
    }
    
    function _resetDailyIfNeeded() internal {
        uint256 currentDay = block.timestamp / 1 days;
        if (currentDay > lastResetDay) {
            spentToday = 0;
            lastResetDay = currentDay;
        }
    }
    
    function preCheck(address to, uint256 amount) 
        external 
        view 
        returns (bool, string memory) 
    {
        if (!whitelist[to]) return (false, "NOT_WHITELISTED");
        if (amount > perTxLimit) return (false, "EXCEEDS_PER_TX");
        if (spentToday + amount > dailyLimit) return (false, "EXCEEDS_DAILY");
        if (spentInSession + amount > sessionBudget) return (false, "EXCEEDS_SESSION");
        return (true, "OK");
    }
    
    function checkAndExecute(address to, uint256 amount) 
        external 
        onlyAgent 
        returns (bool) 
    {
        _resetDailyIfNeeded();
        
        if (!whitelist[to]) {
            emit TransactionRejected(to, amount, "NOT_WHITELISTED", block.timestamp);
            return false;
        }
        if (amount > perTxLimit) {
            emit TransactionRejected(to, amount, "EXCEEDS_PER_TX", block.timestamp);
            return false;
        }
        if (spentToday + amount > dailyLimit) {
            emit TransactionRejected(to, amount, "EXCEEDS_DAILY", block.timestamp);
            return false;
        }
        if (spentInSession + amount > sessionBudget) {
            emit TransactionRejected(to, amount, "EXCEEDS_SESSION", block.timestamp);
            return false;
        }
        
        spentToday += amount;
        spentInSession += amount;
        
        (bool sent, ) = to.call{value: amount}("");
        require(sent, "Transfer failed");
        
        emit TransactionExecuted(to, amount, block.timestamp);
        return true;
    }
    
    function addToWhitelist(address _addr) external onlyOwner {
        whitelist[_addr] = true;
        emit WhitelistUpdated(_addr, true);
    }
    
    function resetSession() external onlyOwner {
        spentInSession = 0;
    }
    
    function getStatus() external view returns (
        uint256 _spentToday,
        uint256 _spentInSession,
        uint256 _remainingDaily,
        uint256 _remainingSession
    ) {
        return (
            spentToday,
            spentInSession,
            dailyLimit > spentToday ? dailyLimit - spentToday : 0,
            sessionBudget > spentInSession ? sessionBudget - spentInSession : 0
        );
    }
    
    receive() external payable {}
}