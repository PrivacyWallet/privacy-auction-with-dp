pragma solidity >0.5.0;
import "./DataBuyerInterface.sol";

struct DataOwner {
  int encrypted_data;
  uint price;
  uint epsilon;
}

struct IndexValue { uint keyIndex; DataOwner value; }
struct KeyFlag { address key; bool deleted; }

struct itmap {
    mapping(address => IndexValue) data;
    KeyFlag[] keys;
    uint size;
}

library IterableMapping {
    function insert(itmap storage self, address key, DataOwner memory value) internal returns (bool replaced) {
        uint keyIndex = self.data[key].keyIndex;
        self.data[key].value = value;
        if (keyIndex > 0)
            return true;
        else {
            self.keys.push();
            keyIndex = self.keys.length;
            self.data[key].keyIndex = keyIndex + 1;
            self.keys[keyIndex].key = key;
            self.size++;
            return false;
        }
    }

    function remove(itmap storage self, address key) internal returns (bool success) {
        uint keyIndex = self.data[key].keyIndex;
        if (keyIndex == 0)
            return false;
        delete self.data[key];
        self.keys[keyIndex - 1].deleted = true;
        self.size --;
    }

    function contains(itmap storage self, address key) internal view returns (bool) {
        return self.data[key].keyIndex > 0;
    }

    function iterate_start(itmap storage self) internal view returns (uint keyIndex) {
        return iterate_next(self, uint(-1));
    }

    function iterate_valid(itmap storage self, uint keyIndex) internal view returns (bool) {
        return keyIndex < self.keys.length;
    }

    function iterate_next(itmap storage self, uint keyIndex) internal view returns (uint r_keyIndex) {
        keyIndex++;
        while (keyIndex < self.keys.length && self.keys[keyIndex].deleted)
            keyIndex++;
        return keyIndex;
    }

    function iterate_get(itmap storage self, uint keyIndex) internal view returns (address key, DataOwner storage value) {
        key = self.keys[keyIndex].key;
        value = self.data[key].value;
    }
}
contract Calculator {
  uint constant upper_bound = 10000000;
  address calculator;

  struct DataBuyer {
    DataBuyerInterface buyer_contract;
    address[] selected_owner;
    uint[] selected_prices;
    uint budget;
  }

  itmap public data;
  using IterableMapping for itmap;
  mapping(address => DataBuyer) public transactions;


  // step 1
  // calculator provide construct it's contract.
  constructor() public {
    calculator = msg.sender;
  }

  // step 2
  // send encrypted data and epsilon.
  function set_data(uint price, int encrypted_data, uint epsilon, address payable _address) public {
    // TODO: assert

    DataOwner memory data_owner = DataOwner(
      encrypted_data,
      price,
      epsilon
    );
    data.insert(_address, data_owner);
  }

  // step 7
  // event to notify off-chain calculator.
  event data_selected(int[] owners_data, uint[] owners_epsilon);

  // step 4
  // data buyer provide it's budget by `payable`.
  // also, one should also privide where it selection contract is.
  function bid(DataBuyerInterface data_buyer_contract) public payable {

    // store contract address
    transactions[msg.sender].buyer_contract = data_buyer_contract;
    
    // step 5, 6
    // calculator call data_buyer's contract 
    // to provide epsilon's and budget number,
    // and waiting for result.
    uint[] memory price_vec = new uint[](data.size);
    uint[] memory epsilon_vec = new uint[](data.size);
    int[] memory data_vec = new int[](data.size);
    address[] memory address_vec = new address[](data.size);
    for(uint i = data.iterate_start();
       data.iterate_valid(i);
       (i = data.iterate_next(i), i++)) {
         (address _address,DataOwner storage data_owner) = data.iterate_get(i);
         price_vec[i] = data_owner.price;
         epsilon_vec[i] = data_owner.epsilon;
         data_vec[i] = data_owner.encrypted_data;
         address_vec[i] = _address;
    }

    uint[] memory results = DataBuyerInterface(data_buyer_contract).send_budget_and_epsilons(msg.value, epsilon_vec, price_vec);

    // select data we want.
    address[] memory result_addresses = new address[](results.length);
    int[] memory result_data = new int[](results.length);
    uint[] memory result_epsilons = new uint[](results.length);
    uint[] memory result_prices = new uint[](results.length);
    for(uint i = 0; i < results.length; i++ ){
      result_addresses[i] = address_vec[results[i]];
      result_data[i] = data_vec[results[i]];
      result_epsilons[i] = epsilon_vec[results[i]];
      result_prices[i] = price_vec[results[i]];
    }

    // suspend this transactions
    transactions[msg.sender].selected_owner = result_addresses;
    transactions[msg.sender].selected_prices = result_prices;
    transactions[msg.sender].budget = msg.value;

    // step 7
    // trigger the event, tell the calculator
    // that he may continue the computation.
    
    emit data_selected(result_data,price_vec);
    
  }

  // step 9, 10
  // send money to buyer & owner.
  function bidEnd(address data_buyer,int encrypted_result) public {

    uint sum = 0;
    for(uint i = 0; i < transactions[data_buyer].selected_prices.length; i++){
      transactions[data_buyer].selected_owner[i].call{value:transactions[data_buyer].selected_prices[i] }("");
      sum += transactions[data_buyer].selected_prices[i];
    }
    transactions[data_buyer].buyer_contract.send_result(encrypted_result);
    data_buyer.call{value: transactions[data_buyer].budget-sum}("");

  }

   //say hello world
  function say() public pure returns (string memory) {
    return "Hello World";
  }
}
