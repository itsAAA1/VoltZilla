import unittest
from unittest.mock import patch
from solana_snapshot import inspect_mint, MINT_1M, AUTHORITY_1M

class RpcTests(unittest.TestCase):
    @patch('solana_snapshot.call_rpc')
    def test_confirmed_1m_mint_and_delta(self, rpc):
        rpc.side_effect=[{'value':{'owner':'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA','data':{'parsed':{'info':{'supply':'1000000000000000','mintAuthority':AUTHORITY_1M,'freezeAuthority':None}}}}}, {'value':{'amount':'1000000000000000','decimals':9,'uiAmountString':'1000000'}}]
        result=inspect_mint(MINT_1M)
        self.assertEqual(result['remaining_to_target_raw'],'6000000000000000')
        self.assertTrue(result['can_propose_issuance'])
        self.assertFalse(result['transaction_created'])

    @patch('solana_snapshot.call_rpc')
    def test_conflicting_chain_reads_fail(self, rpc):
        rpc.side_effect=[{'value':{'data':{'parsed':{'info':{'supply':'1','mintAuthority':None}}}}}, {'value':{'amount':'2','decimals':9,'uiAmountString':'0.000000002'}}]
        with self.assertRaises(RuntimeError): inspect_mint(MINT_1M)

if __name__=='__main__':unittest.main()
