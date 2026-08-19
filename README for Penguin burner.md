# 🐧 Space P3NGUIN Burn Tracker

A robust Python script that communicates directly with the BNB Smart Chain to track the live deflation and burn metrics of the **Space P3NGUIN ($P3NGUIN)** token contract.

## 🚀 Features
- **Zero API Keys Required:** Operates strictly over public, open-access JSON-RPC node infrastructure.
- **Fail-Safe Loop Automation:** Built-in error catching intercepts public server congestion or HTML responses to ensure continuous looping without terminal crashes.
- **Auto-Compiling Documentation:** Dynamically generates a local markdown report (`TOKEN_METRICS.md`) updated in real-time.

## 🛠️ Requirements
Ensure you have the `requests` library installed:
```bash
pip install requests
```

## 💻 How To Run
Execute the tracking script from your terminal:
```bash
python "Penguin burner.py"
```
*Press `Ctrl + C` at any time to safely terminate the polling loop.*
