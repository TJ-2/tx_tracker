from web3 import Web3

# Connect to Telos EVM endpoint (replace with actual endpoint)
telos_rpc = "https://mainnet.telos.net/evm"
web3 = Web3(Web3.HTTPProvider(telos_rpc))

# ERC-20 contract ABI (minimal ABI to fetch decimals and symbol)
erc20_abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

def fetch_tx(tx_hash):
    tx = web3.eth.get_transaction(tx_hash)
    receipt = web3.eth.get_transaction_receipt(tx_hash)

    block = web3.eth.get_block(tx['blockNumber'])

    timestamp = block['timestamp']
    token_transferred = None

    for log in receipt['logs']:
        if log['topics'][0].hex() == web3.keccak(text='Transfer(address,address,uint256)').hex():
            from_address = '0x' + log['topics'][1].hex()[26:]
            to_address = '0x' + log['topics'][2].hex()[26:]
            value = int(log['data'], 16)
            token_address = log['address']
            token_contract = web3.eth.contract(address=token_address, abi=erc20_abi)
            decimals = token_contract.functions.decimals().call()
            symbol = token_contract.functions.symbol().call()
            value = value / (10 ** decimals)
            token_transferred = {
                'from': from_address,
                'to': to_address,
                'value': value,
                'token_address': token_address,
                'symbol': symbol
            }
            break

    print(f"Timestamp: {timestamp}")
    if token_transferred:
        print(f"Token Transferred: {token_transferred}")
        return timestamp, token_transferred
    else:
        print("No token transfer detected in the transaction.")
        return None

# Example usage
tx_hash = "0xe8ff319c41c7f1a06087bcb2eae6c61d6919d242eee1df87382503e54101d0c3"
fetch_tx(tx_hash)
