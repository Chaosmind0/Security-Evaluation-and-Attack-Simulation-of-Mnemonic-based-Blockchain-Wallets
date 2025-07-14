import sys
import os
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from wallet_key_deriver import WalletKeyDeriver


class TestWalletKeyDeriver(unittest.TestCase):
    """
    
    Test suite for the WalletKeyDeriver class.

    """

    def test_derive_eth_address(self):
        """
        
        Test that the Ethereum address and private key can be derived from the BIP39 mnemonic phrase.

        """
        
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        deriver = WalletKeyDeriver(mnemonic)

        # Test default values of ETHEREUM derivation
        eth = deriver.derive_eth_address()
        self.assertEqual(eth['coin'], 'ETHEREUM')
        self.assertEqual(eth['path'], "m/44'/60'/0'/0/0")
        self.assertEqual(eth['address'], '0x9858EfFD232B4033E47d90003D41EC34EcaEda94')
        self.assertEqual(eth['private_key'], '1ab42cc412b618bdea3a599e3c9bae199ebf030895b039e9db1e30dafb12b727')
        self.assertEqual(eth['public_key'], '0237b0bb7a8288d38ed49a524b5dc98cff3eb5ca824c9f9dc0dfdb3d9cd600f299')
    
    def test_derive_btc_address(self):
        """
        
        Test that the Bitcoin address and private key can be derived from the BIP39 mnemonic phrase.
        
        """
        
        mnemonic = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
        deriver = WalletKeyDeriver(mnemonic)

        # Test custom values of BITCOIN derivation
        bit = deriver.derive_btc_address()
        self.assertEqual(bit['coin'], 'BITCOIN')
        self.assertEqual(bit['path'], "m/44'/0'/0'/0/0")
        self.assertEqual(bit['address'], '1LqBGSKuX5yYUonjxT5qGfpUsXKYYWeabA')
        self.assertEqual(bit['private_key'], 'e284129cc0922579a535bbf4d1a3b25773090d28c909bc0fed73b5e0222cc372')
        self.assertEqual(bit['public_key'], '03aaeb52dd7494c361049de67cc680e83ebcbbbdbeb13637d92cd845f70308af5e')

    def test_invalid_mnemonic(self):
        """
        
        Test that an invalid mnemonic raises a ValueError.
        
        """
        
        with self.assertRaises(ValueError):
            WalletKeyDeriver("invalid mnemonic words here")

if __name__ == '__main__':
    unittest.main()
