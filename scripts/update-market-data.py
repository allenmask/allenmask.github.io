#!/usr/bin/env python3
import json
import os
import urllib.request

SYMBOLS = ['SONO', 'ABNB', 'GOOGL', 'GS']
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(ROOT_DIR, 'market-data.json')

def fetch_quotes():
    results = {}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for s in SYMBOLS:
        url = f'https://api.nasdaq.com/api/quote/{s}/info?assetclass=stocks'
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                pd = data.get('data', {}).get('primaryData', {})
                net_change = pd.get('netChange', '0')
                pct_change = pd.get('percentageChange', '0%')
                direction = pd.get('deltaIndicator', 'neutral').lower()
                price = pd.get('lastSalePrice', 'N/A')
                results[s] = {
                    'price': price,
                    'netChange': net_change,
                    'percentageChange': pct_change,
                    'direction': direction,
                    'timestamp': pd.get('lastTradeTimestamp', '')
                }
        except Exception as e:
            print(f'Error fetching {s}: {e}')
            if os.path.exists(OUTPUT_PATH):
                try:
                    with open(OUTPUT_PATH, 'r') as f:
                        old = json.load(f)
                        if s in old:
                            results[s] = old[s]
                except Exception:
                    pass

    if len(results) == len(SYMBOLS):
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'Successfully updated market-data.json for {list(results.keys())}')
    else:
        print(f'Warning: only retrieved {len(results)}/{len(SYMBOLS)} symbols, skipping write.')

if __name__ == '__main__':
    fetch_quotes()
