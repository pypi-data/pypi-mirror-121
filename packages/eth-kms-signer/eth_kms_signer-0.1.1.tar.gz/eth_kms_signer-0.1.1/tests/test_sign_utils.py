import unittest

from eth_kms_signer.utils.signing import to_r_s_v


class AddressUtils(unittest.TestCase):
    pub_key = bytes.fromhex(
        "36758024bb7127ce31145f853b0f44f9f2a9407f5f77c9447b8fb255894b0068b45093295193a14b76356adc9777199d1231cfc220576436004a4ec734ee2fdc"
    )

    def test_get_address_from_pub_key(self):
        expected_address = get_address_from_pub(self.pub_key)
        assert expected_address == "0x539C58605e3FB9B024e8168b9F529B81586dee00"

    def test_get_compressed_pub_key(self):
        compressed = get_compressed_public_key(self.pub_key)
        assert compressed.hex() == "0236758024bb7127ce31145f853b0f44f9f2a9407f5f77c9447b8fb255894b0068"
