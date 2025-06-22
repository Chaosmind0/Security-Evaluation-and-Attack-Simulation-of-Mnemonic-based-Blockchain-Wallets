# Project Title
Security Evaluation and Attack Simulation of Mnemonic-based Blockchain Wallets

## Project Description

This project focuses on the **security evaluation of blockchain wallets** that rely on **mnemonic phrases** for key generation and recovery, following the BIP39 standard. Mnemonic-based wallets are widely used in decentralized applications and digital asset storage, yet often rely on user-generated phrases that may suffer from **low entropy**, **predictable patterns**, or **social engineering risks**.

The project involves:

- **Implementing mnemonic phrase generation and wallet derivation** using Python-based cryptographic tools (bip-utils, web3.py);
- **Simulating brute-force attacks** on weak mnemonic phrases to evaluate how easily poorly chosen wallets can be compromised;
- **Testing recovery scenarios** for improperly stored or phished seed phrases;
- **Analyzing the entropy space** of common user-generated phrases (e.g., 12-word vs. 24-word mnemonics);
- **Providing security recommendations** for users and developers on how to mitigate risks related to wallet recovery mechanisms.

Through this project, I developed a deeper understanding of:

- Hierarchical Deterministic (HD) wallet architecture (BIP32, BIP44);
- Practical threats to decentralized key management;
- The trade-offs between usability and security in wallet design.

## Skills & Tools

- Python, bip_utils, web3.py, hashlib, secrets
- BIP39, BIP32, BIP44 standards
- Cryptographic hash functions (SHA-256, HMAC)
- Brute-force attack simulation and entropy analysis
- Markdown documentation & technical writing

## Academic Relevance

This project extends my learning from university courses on **Cyber Security Fundamentals** and **Cryptography and Secure Development**, bridging theoretical understanding with real-world applications in blockchain and FinTech security.

It also strengthens my portfolio for postgraduate study and future roles in **blockchain security, FinTech risk analysis**, or **applied cryptography**.