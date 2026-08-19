#!/usr/bin/env python3
import json
import time
import requests

# 1. BNB CHAIN CONFIGURATION
# -------------------------------------------------------------------------
RPC_URL = 'https://binance.org'
TOKEN_CONTRACT = '0xb8309421B0603fEbbc370A6B0C5c59d3aF202759'
TOTAL_SUPPLY = 1_000_000_000_000_000  # 1 Quadrillion Max Supply
TOKEN_SYMBOL = 'P3NGUIN'
BURN_ADDRESS = '0x000000000000000000000000000000000000dead'

# LOOP INTERVAL TIME (In Seconds: 180 seconds = 3 minutes)
LOOP_INTERVAL = 180

# 2. CONSTRUCT THE LOW-LEVEL ETH_CALL HEX PAYLOAD
# -------------------------------------------------------------------------
clean_burn_address = BURN_ADDRESS[2:].lower()
padded_address = clean_burn_address.zfill(64)
hex_payload = f"0x70a08231{padded_address}"

json_payload = {
    "jsonrpc": "2.0",
    "method": "eth_call",
    "params": [{"to": TOKEN_CONTRACT, "data": hex_payload}, "latest"],
    "id": 1
}

print(f"🚀 Tracker active. Polling network updates every 3 minutes...")
print("Press Ctrl + C in the terminal to stop at any time.\n")

while True:
    try:
        print(f"[{time.strftime('%H:%M:%S')}] Connecting to BNB Smart Chain...")
        response = requests.post(RPC_URL, json=json_payload, timeout=10)
        response.raise_for_status()
        
        # SAFETY CHECK: If the public server drops HTML, catch it here instead of crashing the program
        try:
            res_data = response.json()
        except Exception:
            print("⚠️ Server sent an invalid webpage response right now. Waiting for next cycle...")
            res_data = {}

        # 4. PARSE RESULTS & CALCULATE DEFLATION
        # -------------------------------------------------------------------------
        if 'result' in res_data and res_data['result'] != '0x':
            raw_hex_balance = res_data['result']
            raw_burned_tokens = int(raw_hex_balance, 16)
            
            decimals = 18
            burned_tokens = raw_burned_tokens / (10**decimals)
            
            burn_percentage = (burned_tokens / TOTAL_SUPPLY) * 100
            circulating_supply = TOTAL_SUPPLY - burned_tokens
            
            print("==========================================")
            print(f"       {TOKEN_SYMBOL} METRICS DASHBOARD       ")
            print("==========================================")
            print(f"Tokens Burned:      {burned_tokens:,.0f}")
            print(f"Circulating Supply: {circulating_supply:,.0f}")
            print(f"Percentage Burned:  {burn_percentage:.4f}%")
            print("==========================================")

            # 5. GENERATE DOCUMENTATION
            # -------------------------------------------------------------------------
            output_file = "TOKEN_METRICS.md"
            with open(output_file, 'w', encoding='utf-8') as fh:
                fh.write("# 📊 Token Metrics Report\n\n")
                fh.write(f"This documentation is automatically compiled from live BNB Smart Chain data.\n\n")
                fh.write("### 📈 Current Status\n")
                fh.write("| Metric | Value |\n")
                fh.write("| :--- | :--- |\n")
                fh.write(f"| **Token Symbol** | {TOKEN_SYMBOL} |\n")
                fh.write(f"| **Initial Total Supply** | {TOTAL_SUPPLY:,} |\n")
                fh.write(f"| **Tokens Burned** | {burned_tokens:,.2f} |\n")
                fh.write(f"| **Current Circulating Supply** | {circulating_supply:,.2f} |\n")
                fh.write(f"| **Burn Progress** | {burn_percentage:.4f}% |\n\n")
                fh.write("---\n")
                fh.write(f"*Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} UTC*\n")
                fh.write("\n*Generated independently via Python using direct JSON-RPC node polling.*\n")
                
            print(f"Report successfully updated in '{output_file}'")
        else:
            if res_data:
                print("⚠️ RPC Error: Node returned empty fields.")

    except requests.exceptions.RequestException as e:
        print(f"❌ Connection dropped momentarily. Staying alive...")
    
    print(f"Sleeping for 3 minutes...\n")
    time.sleep(LOOP_INTERVAL)
