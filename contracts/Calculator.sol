pragma solidity >0.5.0;
import "./DataBuyerInterface.sol";

contract Calculator {
  uint constant factor = 10000000;
  address calculator;

  struct DataOwner {
    uint price;
    int encrypted_data;
    uint epsilon;
  }

  struct DataBuyer {
    DataBuyerInterface buyer_contract;
  }

  mapping(address => DataOwner) public data;
  mapping(address => DataBuyer) public buyers;


  // step 1
  // calculator provide construct it's contract.
  constructor() public {
    calculator = msg.sender;
  }

  // step 2
  // send encrypted data and epsilon.
  function set_data(uint price, int encrypted_data, uint epsilon, address payable _address) public {
    // TODO: assert
    data[_address].encrypted_data = encrypted_data; 
    data[_address].epsilon = epsilon;
    data[_address].price = price;
  }

  // step 7
  // event to notify off-chain calculator.
  event data_selected(int[] owners_data, int[] owners_epsilon);

  // step 4
  // data buyer provide it's budget by `payable`.
  // also, one should also privide where it selection contract is.
  function bid(DataBuyerInterface data_buyer_contract) public payable {

    // store contract address
    buyers[msg.sender].buyer_contract = data_buyer_contract;
    
    // step 5, 6
    // calculator call data_buyer's contract 
    // to provide epsilon's and budget number,
    // and waiting for result.
    // TODO: we mock it currently
    int[] memory temp = new int[](100);
    for(uint i = 0; i < temp.length; i++){
      temp[i] = int(i);
    }

    DataBuyerInterface(data_buyer_contract).send_budget_and_epsilons(1, temp);

    int[] memory a = new int[](100);

    for(uint i = 0; i < a.length; i++){
      a[i] = int(i);
    }
    
    // step 7
    // trigger the event, tell the calculator
    // that he may continue the computation.
    
    emit data_selected(a,a);
    
  }

  // step 9, 10
  function bidEnd(address data_buyer,int encrypted_result) public {

    

  }
   //say hello world
  function say() public pure returns (string memory) {
    return "Hello World";
  }
}
