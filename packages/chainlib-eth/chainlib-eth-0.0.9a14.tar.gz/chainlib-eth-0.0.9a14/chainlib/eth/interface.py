# external imports
from chainlib.interface import ChainInterface
from chainlib.encode import TxHexNormalizer

# local imports
from .block import (
        block_latest,
        block_by_number,
        block_by_hash,
        Block,
        )
from .tx import (
        transaction,
        transaction_by_block,
        receipt,
        raw,
        pack,
        unpack,
        Tx,
        )
from .address import (
        AddressChecksum,
        )


class EthChainInterface(ChainInterface):
    
    def __init__(self):
        self._block_latest = block_latest
        self._block_by_hash = block_by_hash
        self._block_by_number = block_by_number
        self._block_from_src = Block.from_src
        #self._block_to_src = self.__unimplemented
        self._tx_by_hash = transaction
        self._tx_by_block = transaction_by_block
        self._tx_receipt = receipt
        self._tx_raw = raw
        self._tx_pack = pack
        self._tx_unpack = unpack
        self._tx_from_src = Tx.from_src
        #self._tx_to_src = self.__unimplemented
        self._address_safe = AddressChecksum.sum
        self._address_normal = TxHexNormalize.wallet_address
        self._src_normalize = Tx.src_normalize


chain_interface = EthChainInterface()
