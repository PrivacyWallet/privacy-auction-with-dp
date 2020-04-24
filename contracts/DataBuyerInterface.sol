pragma solidity >0.5.0;

// declare interface
interface DataBuyerInterface {
  function send_budget_and_epsilons(int budget, int[] calldata epsilons) external view returns (uint[] memory);

  function send_result(int result) external;
}
