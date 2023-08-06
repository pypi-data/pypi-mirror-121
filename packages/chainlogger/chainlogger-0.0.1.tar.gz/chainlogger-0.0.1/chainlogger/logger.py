from chainlogger.hasher import Hasher
from chainlogger.parser_class import ParserClass
from chainlogger.contract import Contract


class Logger(Contract):
    """
        A class to contain logging logics.
        ...
        Methods
        -------
        create()

        set_gas(string)

        set_gas_price(string)

        set_account(string)

        set_salt(string)

        register_vendor()

        register_project()

        register_log(int, string)

        get_transaction_receipt(string)

        get_batch_transaction_receipt(list)

        parse_data(string)

        parse_batch_data(list)

        verify_data(string, string, string)
    """

    account = None
    salt = "CHANGE_ME"
    gas = "0x3d090"
    gas_price = "0x174876e800"

    @staticmethod
    def create():
        """
        Static function that returns the Logger instance.
        Returns:
            value (object): Logger instance
        """
        return Logger()

    def set_gas(self, gas):
        """
        Sets the gas.
        """
        self.gas = gas

    def set_gas_price(self, gas_price):
        """
        Sets the gas price.
        """
        self.gas_price = gas_price

    def set_account(self, account):
        """
        Sets the user's account from EthSigner.
        """
        self.account = account

    def set_salt(self, salt):
        """
        Sets the salt.
        """
        self.salt = salt

    def register_vendor(self):
        """
        Calls the registerVendor method on the omChain
        Returns the transaction hash or throws error
        Takes gasPrice and gas as hexadecimal
        Returns:
            value (string): transaction hash
        """
        parameters = {
            'from': self.account,
            'gasPrice': self.gas_price,
            'gas': self.gas
        }
        try:
            tx_hash = self.send_contract.functions.registerVendor().transact(parameters)
        except Exception as e:
            print(str(e))
            raise

        return tx_hash

    def register_project(self):
        """
        Registers a project
        Returns:
            value (string): transaction hash
        """
        parameters = {
            'from': self.account,
            'gasPrice': self.gas_price,
            'gas': self.gas
        }
        try:
            tx_hash = self.send_contract.functions.registerProject().transact(parameters)
        except Exception as e:
            print(str(e))
            raise

        return tx_hash

    def register_log(self, project_id, raw_data):
        """
        Registers a log
        Returns:
            value (string): transaction hash
        """
        parameters = {
            'from': self.account,
            'gasPrice': self.gas_price,
            'gas': self.gas
        }
        hasher = Hasher(self.salt)
        to_chain_data = ParserClass.json_encode(raw_data)
        to_chain_data = hasher.hash_with_salt(to_chain_data)
        to_chain_data = Hasher.add0x(to_chain_data)

        try:
            tx_hash = self.send_contract.functions.registerLog(project_id, to_chain_data).transact(parameters)
        except Exception as e:
            print(str(e))
            raise

        tx_hash = self.web3.toHex(tx_hash)
        return tx_hash

    def get_transaction_receipt(self, tx_id):
        """
        Gets transaction receipt with events
        Returns:
            value (dict): data dictionary
        """
        receipt = self.web3.eth.get_transaction_receipt(tx_id)
        result = self.contract.events.LogRegistered().processReceipt(receipt)
        if len(result) == 0:
            raise
        event_log_data_ls = []
        for log in result:
            data_dict = {
                "_data": self.web3.toHex(log["args"]["_data"]),
                "_projectId": log["args"]["_projectId"],
                "_projectLogCounter": log["args"]["_projectLogCounter"],
                "_vendorAddress": log["args"]["_vendorAddress"]
            }
            event_log_data_ls.append({
                "transactionHash": self.web3.toHex(log['transactionHash']),
                "blockHash": self.web3.toHex(log['blockHash']),
                "blockNumber": log['blockNumber'],
                "data": data_dict
            })

        return event_log_data_ls[0]

    def get_batch_transaction_receipt(self, tx_ids):
        """
        Get Batch Transaction Receipts
        Returns:
            value (list): data dictionary list
        """
        return_array = []
        for tx_id in tx_ids:
            return_array.append(self.get_transaction_receipt(tx_id))

        return return_array

    @staticmethod
    def parse_data(block_data):
        """
        Parses the transaction receipt's data column
        to return string instead of hexadecimal
        Returns:
            value (list): parsed data
        """
        if not isinstance(block_data, list):
            return block_data
        return_data = []
        for block in block_data:
            return_data.append(block)

        return return_data

    def parse_batch_data(self, block_data_array):
        """
        Parse Batch Block Data
        Returns:
            value (list): parsed data list
        """
        return_data = []
        for block_data in block_data_array:
            return_data.append(self.parse_data(block_data))

        return return_data

    def verify_data(self, hashed_data, raw_input, salt=None):
        """
        Verify integrity of blockchain record
        Returns:
            value (bool): is verify value
        """
        if salt:
            hasher = Hasher.create(salt)
        else:
            hasher = Hasher.create(self.salt)

        to_chain_data = ParserClass.json_encode(raw_input)
        to_chain_data = hasher.hash_with_salt(to_chain_data)
        to_chain_data = Hasher.add0x(to_chain_data)

        if hashed_data == to_chain_data:
            return True
        else:
            return False
