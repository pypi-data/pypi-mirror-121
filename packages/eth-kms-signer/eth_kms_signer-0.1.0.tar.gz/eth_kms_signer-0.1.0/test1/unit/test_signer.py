import unittest
from unittest import mock

from eth_account._utils.typed_transactions import DynamicFeeTransaction
from eth_kms_signer import sign_dynamic_fee_transaction, sign_legacy_transaction
from eth_utils import keccak

TYPED_TXN_TEST_CASE = {
    "expected_type": DynamicFeeTransaction,
    "expected_hash": "0xd8d2708ac891248e2ef13d2c8a39b83fd5d296db2a058b74533fc7aef9c6f8ea",
    "unsigned_tx_hash": "a1ea3121940930f7e7b54506d80717f14c5163807951624c36354202a8bffda6",
    "transaction": {
        "gas": 100000,
        "maxFeePerGas": 2000000000,
        "maxPriorityFeePerGas": 2000000000,
        "data": "0x5544",
        "nonce": "0x2",
        "to": "0x96216849c49358B10257cb55b28eA603c874b05E",
        "value": "0x5af3107a4000",
        "type": "0x2",
        "chainId": "0x539",
    },
}

LEGACY_TXN_TEST_CASE = {
    "expected_hash": "0x8228595080323934219aabc2629910e765d96166487bc613aec75b38228d1a99",
    "unsigned_tx_hash": "4a1b248a77d82640e1bb1e855a73e56649b78da87861417574fb2a040e15ca0e",
    "transaction": {
        "to": "0xF0109fC8DF283027b6285cc889F5aA624EaC1F55",
        "value": 1000000000,
        "gas": 2000000,
        "gasPrice": 234567897654321,
        "nonce": 0,
        "chainId": 1,
    },
}


class TestKmsSigner(unittest.TestCase):
    @mock.patch("eth_kms_signer.signer.client.get_public_key")
    @mock.patch("eth_kms_signer.signer.client.sign")
    def test_sign(self, mock_boto3_cli_sign, mock_boto3_cli_get_pub_key):
        key_id = "8459385b-bc65-4222-966d-7efbfd8be447"
        pub_key_pem = b'0V0\x10\x06\x07*\x86H\xce=\x02\x01\x06\x05+\x81\x04\x00\n\x03B\x00\x04\xbb\x81\x06\xe2\x141\xe3\x9cS/9S"\xd2\x07\xfd\x17\xc8\x81\xeeeH\x96r\x9f\x13c\x17\x82\xab\x93L\xdd\x8a\x90D:\xcf\x86\xae\x90\x00:\xe6\xbd\x1f\x87(Q5\xa9\xf4\xb9`\xa2\xcf\x0b\xb4$x\x17r\xdcQ'
        sig_der = b"0E\x02 q\xda\xe6\x1d^?\xaf\x85\xf4\x98y\xeb\xe4L#\x19\xa2\x0b\x86\xda,\xc9\xcf\x9d$\x98\x05\xf42\xbb\xb2\xbb\x02!\x00\xad(\xc3V\xefY\t\xeeA\xed\xf3l\xd0\xae\xb2\x14\x95x&\x82F\xd2\xa5\xe7\xde\xc1s\x08\xaf\xf3\n\x10"

        mock_boto3_cli_sign.return_value = {"Signature": sig_der}
        mock_boto3_cli_get_pub_key.return_value = {"PublicKey": pub_key_pem}
        txn = sign_dynamic_fee_transaction(TYPED_TXN_TEST_CASE["transaction"], key_id)
        # assert raw transaction serialization hash and the key id being passed correctly
        mock_boto3_cli_sign.assert_called_with(
            KeyId=key_id,
            Message=bytes.fromhex(TYPED_TXN_TEST_CASE["unsigned_tx_hash"]),
            MessageType="DIGEST",
            SigningAlgorithm="ECDSA_SHA_256",
        )
        # assert signed txn hash
        assert "0x" + keccak(txn).hex() == TYPED_TXN_TEST_CASE.get("expected_hash")

    @mock.patch("eth_kms_signer.signer.client.get_public_key")
    @mock.patch("eth_kms_signer.signer.client.sign")
    def test_legacy_sign(self, mock_boto3_cli_sign, mock_boto3_cli_get_pub_key):
        key_id = "8459385b-bc65-4222-966d-7efbfd8be447"
        pub_key_pem = b'0V0\x10\x06\x07*\x86H\xce=\x02\x01\x06\x05+\x81\x04\x00\n\x03B\x00\x04\xbb\x81\x06\xe2\x141\xe3\x9cS/9S"\xd2\x07\xfd\x17\xc8\x81\xeeeH\x96r\x9f\x13c\x17\x82\xab\x93L\xdd\x8a\x90D:\xcf\x86\xae\x90\x00:\xe6\xbd\x1f\x87(Q5\xa9\xf4\xb9`\xa2\xcf\x0b\xb4$x\x17r\xdcQ'
        sig_der = b"0F\x02!\x00\x8e\x01\\J,D\xd5\xa8T\x015\x06\x1e_\xf2B\x8c\xc4\x9c\x04f\xe4\xa9\xda\xad`\x93\xd5\x17\xed\xfb\x1f\x02!\x00\xcc\xdbp\x07\xf8\xe1~$=\xb1K\x88,\xcd\xa0\xd3\x7f\xbcT\x1e\xd46\xa1l\xd2\xf5z\xddhRX2"

        mock_boto3_cli_sign.return_value = {"Signature": sig_der}
        mock_boto3_cli_get_pub_key.return_value = {"PublicKey": pub_key_pem}
        txn = sign_legacy_transaction(LEGACY_TXN_TEST_CASE["transaction"], key_id)
        # assert raw transaction serialization hash and the key id being passed correctly
        mock_boto3_cli_sign.assert_called_with(
            KeyId=key_id,
            Message=bytes.fromhex(LEGACY_TXN_TEST_CASE["unsigned_tx_hash"]),
            MessageType="DIGEST",
            SigningAlgorithm="ECDSA_SHA_256",
        )
        # assert signed txn hash
        assert "0x" + keccak(txn).hex() == LEGACY_TXN_TEST_CASE.get("expected_hash")
