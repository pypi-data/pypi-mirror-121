from decimal import *
from web3 import Web3,HTTPProvider
import json
import os
from hexbytes import HexBytes

class ERC20Transfer:
  SEND = 1
  RECEIVE = 2

  WETH_CONTRACT_ADDRESS = '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
  WETH_DEPOSIT_TOPIC =    '0xe1fffcc4923d04b559f4d29a8bfc6cda04eb5b0d3c460751c2402c5c5cc9109c'
  WETH_WITHDRAWAL_TOPIC = '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65'

  ERC20_TRANSFER_TOPIC = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'

  settings = json.loads(open('%s/../settings.json' % os.path.dirname(__file__)).read())
  web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/%s' % settings['infra_key']))
  erc20_abi = json.loads(open('%s/erc20_abi.json' % os.path.dirname(__file__)).read())
  getcontext().prec = 50

  def __init__(self, transfer):
    self.transfer = transfer
    self.decimal = None
    self.symbol = None
    self.contract = ERC20Transfer.web3.eth.contract(address=Web3.toChecksumAddress(transfer['address'].lower()), abi=ERC20Transfer.erc20_abi)

  @classmethod
  def get_erc20_transfers(cls, tx, direction):
    if direction not in [cls.SEND, cls.RECEIVE]:
      raise ValueError('invalid direction is set. Put ERC20Transfer.SEND or ERC20Transfer.RECEIVE')
    logs = tx['logs']
    address = tx['from'].lower()
    logs = cls.__merge_weth_transfer(logs, address)
    transfers = list(filter(lambda item: (item['topics'][0].hex().lower() == cls.ERC20_TRANSFER_TOPIC and '0x' + item['topics'][direction].hex().lower()[26:] == address), logs))
    transfers = list(map(lambda item: ERC20Transfer(item), transfers))
    return transfers

  @classmethod
  def __merge_weth_transfer(cls, logs, address):
    for i_log in logs:
      if i_log['address'].lower() == cls.WETH_CONTRACT_ADDRESS and i_log['topics'][0].hex().lower() == cls.WETH_DEPOSIT_TOPIC:
        for index, j_log in enumerate(logs):
          if j_log['address'].lower() == cls.WETH_CONTRACT_ADDRESS and j_log['topics'][0].hex().lower() == cls.ERC20_TRANSFER_TOPIC and j_log['topics'][cls.SEND].hex().lower()[26:] == i_log['topics'][1].hex().lower()[26:] and i_log['data'] == j_log['data']:
            logs[index]['topics'][1] = HexBytes('000000000000000000000000' + address[2:])

      if i_log['address'].lower() == cls.WETH_CONTRACT_ADDRESS and i_log['topics'][0].hex().lower() == cls.WETH_WITHDRAWAL_TOPIC:
        for index, j_log in enumerate(logs):
          if j_log['address'].lower() == cls.WETH_CONTRACT_ADDRESS and j_log['topics'][0].hex().lower() == cls.ERC20_TRANSFER_TOPIC and j_log['topics'][cls.RECEIVE].hex().lower()[26:] == i_log['topics'][1].hex().lower()[26:] and i_log['data'] == j_log['data']:
            logs[index]['topics'][2] = HexBytes('000000000000000000000000' + address[2:])

    return logs

  def get_erc20_decimals(self):
    if self.decimal == None:
      decimal = self.contract.functions.decimals().call()
      self.decimal = Decimal(decimal)
    return self.decimal

  def get_erc20_amount(self):
    self.decimal = self.get_erc20_decimals()
    amount = Decimal(int(self.transfer['data'], 0)) / Decimal(pow(10, self.decimal))
    return amount

  def get_erc20_address(self):
    address = self.transfer['address'].lower()
    return address

  def get_erc20_from(self):
    src = '0x' + self.transfer['topics'][1].hex().lower()[26:]
    return src

  def get_erc20_to(self):
    dst = '0x' + self.transfer['topics'][2].hex().lower()[26:]
    return dst

  def get_erc20_symbol(self):
    if self.symbol == None:
      self.symbol = self.contract.functions.symbol().call()
    return self.symbol
