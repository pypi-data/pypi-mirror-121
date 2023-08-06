from web3 import Web3
from web3.middleware import geth_poa_middleware


class Contract:
    """
    A class to initialize contracts, gets the provider and abi information about the contract.
    Initializes web3 instances.
    ...
    Methods
    -------
    set_provider(string)

    set_abi(string)

    set_eth_signer(string)

    set_contract(string)

    set_send_contract(string)

    set_web3(string)

    get_contract()

    get_send_contract()

    get_web3()
    """
    provider = None
    abi = None
    eth_signer = None
    contract = None
    send_contract = None
    web3 = None

    @staticmethod
    def check_connection_urls(provider, abi):
        """
        Checks all the variables exists
        Parameters:
            provider (string): provider url
            abi (string): abi
        """
        if provider is None:
            raise Exception("You must set the provider first")
        if abi is None:
            raise Exception("You must set the abi of the contract first")

    def set_provider(self, provider):
        """
        Sets the provider
        Parameters:
            provider (string): provider url
        """
        self.provider = provider

    def set_abi(self, abi):
        """
        Sets the abi
        Parameters:
            abi (string): contract abi
        """
        self.abi = abi

    def set_eth_signer(self, eth_signer):
        """
        Sets the eth signer
        Parameters:
            eth_signer (string): eth signer url
        """
        self.eth_signer = eth_signer

    def set_contract(self, at_address):
        """
        Sets the deployed contract
        Parameters:
            at_address (string): deployed contract address
        """
        self.check_connection_urls(self.provider, self.abi)
        web3_instance = Web3(Web3.HTTPProvider(self.provider))
        if not web3_instance.isConnected():
            raise ConnectionError
        web3_instance.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.contract = web3_instance.eth.contract(address=web3_instance.toChecksumAddress(at_address), abi=self.abi)

    def set_send_contract(self, send_contract_address):
        """
        Sets the transaction sending contract using EthSigner provider
        Parameters:
            send_contract_address (string): sender contract address
        """
        self.check_connection_urls(self.provider, self.abi)
        eth_signer_instance = Web3(Web3.HTTPProvider(self.eth_signer))
        if not eth_signer_instance.isConnected():
            raise ConnectionError
        eth_signer_instance.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.send_contract = eth_signer_instance.eth.contract(
            address=eth_signer_instance.toChecksumAddress(send_contract_address),
            abi=self.abi)

    def set_web3(self):
        """
        Sets the Web3 object
        """
        if self.provider is None:
            raise Exception("You must set the provider first")
        self.web3 = Web3(Web3.HTTPProvider(self.provider))
        if not self.web3.isConnected():
            raise ConnectionError

    def get_contract(self):
        """
            Gets the contract
        """
        return self.contract

    def get_send_contract(self):
        """
            Gets the contract
        """
        return self.send_contract

    def get_web3(self):
        """
            Gets the Web3 object
        """
        return self.web3
