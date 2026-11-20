"""Read-only canonical Solana RPC snapshot: no wallets, private keys or network writes."""
import argparse, json, urllib.request

DEFAULT_RPC = 'https://api.mainnet-beta.solana.com'
MINT_1M = 'DHxStA9nRq6DdhBKT89s38fpxD9wE7MtyMn9HMuWeyN9'
MINT_GDY = 'GDYcemcZozG9ijhEZioRLRgNMtoxh1BBuV7nvdf1pump'
AUTHORITY_1M = '28fU8SDMKLXe8hqmdy9dxYNHeddm7xQRzkxK16JLUpi4'

def call_rpc(method, params, rpc_url=DEFAULT_RPC, timeout=12):
    body=json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode('utf-8')
    req=urllib.request.Request(rpc_url,body,{'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=timeout) as response: data=json.load(response)
    if 'error' in data: raise RuntimeError(f"RPC failure: {data['error']}")
    return data['result']

def inspect_mint(mint=MINT_1M, rpc_url=DEFAULT_RPC):
    value=call_rpc('getAccountInfo',[mint,{'encoding':'jsonParsed','commitment':'confirmed'}],rpc_url)
    mint_info=((value or {}).get('value') or {}).get('data',{}).get('parsed',{}).get('info')
    if not isinstance(mint_info,dict) or 'supply' not in mint_info: raise RuntimeError('Not an SPL mint or RPC unable to parse mint')
    supply=call_rpc('getTokenSupply',[mint,{'commitment':'confirmed'}],rpc_url)['value']
    if mint_info['supply'] != supply['amount']:
        raise RuntimeError('Inconsistent supply between RPC reads: retry on stable commitment')
    result={'network':'solana-mainnet','mint':mint,'program_owner':(value or {}).get('value',{}).get('owner'),
            'raw_supply':supply['amount'],'decimals':supply['decimals'],
            'ui_supply':supply['uiAmountString'],'mint_authority':mint_info.get('mintAuthority'),
            'freeze_authority':mint_info.get('freezeAuthority'),'transaction_created':False,
            'message':'Read-only RPC observation; never sign or send from this script'}
    if mint==MINT_1M:
        raw_delta=7_000_000*(10**9)-int(supply['amount'])
        result['target_ui_supply']='7000000'
        result['remaining_to_target_raw']=str(raw_delta) if raw_delta>=0 else None
        result['authority_matches_observed']=mint_info.get('mintAuthority')==AUTHORITY_1M
        result['can_propose_issuance']=raw_delta>=0 and result['authority_matches_observed']
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser(description='Real read-only Solana RPC mint check')
    p.add_argument('--mint', choices=[MINT_1M,MINT_GDY],default=MINT_1M)
    p.add_argument('--rpc',default=DEFAULT_RPC)
    args=p.parse_args()
    try: print(json.dumps(inspect_mint(args.mint,args.rpc),ensure_ascii=False,indent=2))
    except Exception as e: p.exit(1,'RPC verification failed: '+str(e)+'\n')
