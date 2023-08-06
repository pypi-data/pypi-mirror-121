import unittest
from unittest import mock

from eth_utils import keccak

from eth_kms_signer import EthKmsClient

TEST_CASE = [
    {
        "transaction": {
            "to": "0xF0109fC8DF283027b6285cc889F5aA624EaC1F55",
            "value": 1000000000,
            "gas": 2000000,
            "gasPrice": 234567897654321,
            "nonce": 0,
            "chainId": 1,
        },
        "public_key": "8886d5e33436eb1bb5cd9aa0ccceeb9c0edadf0866a709028b7afe9b349ff5fb34f1ce87e4fed2b75c7198f4320d73374add862d4966b716923d74ea0ce4c2cf",
        "expected_raw_tx": "f86a8086d55698372431831e848094f0109fc8df283027b6285cc889f5aa624eac1f55843b9aca008025a009ebb6ca057a0535d6186462bc0b465b561c94a295bdb0621fc19208ab149a9ca0440ffd775ce91a833ab410777204d5341a6f9fa91216a6f3ee2c051fea6a0428",
        "r": 4487286261793418179817841024889747115779324305375823110249149479905075174044,
        "s": 30785525769477805655994251009256770582792548537338581640010273753578382951464,
        "v": 37,
        "tx_hash": "0xd8f64a42b57be0d565f385378db2f6bf324ce14a594afc05de90436e9ce01f60",
    }
]


class TestKmsSigner(unittest.TestCase):
    key_id = "8459385b-bc65-4222-966d-7efbfd8be447"
    cli = EthKmsClient("us-east-2")

    def test_sign(self):
        for each in TEST_CASE:
            mock.patch.object(EthKmsClient, "_raw_sign", return_value=(each["r"], each["s"], each["v"]))
            mock.patch.object(EthKmsClient, "get_public_key", return_value=bytes.fromhex(each["public_key"]))
            txn = self.cli.sign_transaction(each["transaction"], self.key_id)
            # assert signed txn hash
            print("0x" + keccak(txn).hex())
            assert "0x" + keccak(txn).hex() == each.get("tx_hash")
