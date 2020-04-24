pragma solidity >0.5.0;
import "./DataBuyerInterface.sol";

contract DataBuyer is DataBuyerInterface {
    address dataBuyer;
    int result;

    // Constructor code is only run when the contract
    // is created
    constructor() public {
      // store self address
      dataBuyer = msg.sender;
    }

  function send_budget_and_epsilons(int budget, int[] calldata epsilons) external view returns (uint[] memory){
      // now we have epsilons and budget,
      // we select from them and return the index
      
      
    }

    function send_result(int _result) external{
      result = _result;
    }
}


