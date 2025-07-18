# 🔐 Security Evaluation and Attack Simulation of Mnemonic-Based Blockchain Wallets

## 📘 Overview

This project evaluates the security of blockchain wallets that rely on **mnemonic phrases** (per [BIP39](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki)) for key generation and recovery. It includes practical tools and experimental simulations to assess how weakly generated or partially known mnemonic phrases can be attacked using brute-force techniques.

---

## 🎯 Objectives

- ✅ Implement BIP39 mnemonic generation and seed derivation
- ✅ Derive Bitcoin / Ethereum wallets using BIP32/BIP44 standards
- ✅ Simulate brute-force attacks using both **random** and **exhaustive** strategies
- ✅ Evaluate entropy and success probability under different configurations
- ✅ Provide GUI and analytical tools for experimentation and visualization

---

## 🧠 Key Concepts

- **Mnemonic Phrases**: Human-readable representations of entropy used to generate cryptographic keys.
- **BIP39**: Bitcoin Improvement Proposal for generating mnemonic-based seeds.
- **HD Wallets**: Hierarchical Deterministic wallets (BIP32/BIP44) supporting key derivation paths.
- **Low Entropy Attacks**: Attacks that exploit weak or predictable word selection by users.

---

## 🛠️ Project Structure
```
├──src/
│ ├── bip39_mnemonic_generator.py # Mnemonic generation (BIP39)
│ ├── wallet_key_deriver.py # Seed and key derivation with validation
│ ├── unsafe_wallet_key_deriver.py # Key derivation without mnemonic checksum validation
│ ├── attack_core.py # Core logic for brute-force attack
│ ├── attack_factory.py # Strategy selector (random/exhaustive)
│ ├── random_attack.py # Random brute-force strategy
│ ├── exhaustive_attack.py # Exhaustive brute-force strategy
│ ├── simulate_brute_force_attack.py # Batch testing & report generation
│ ├── analysis.py # CSV-based visual analysis with Seaborn
│ └── gui_main.py # PyQt5 GUI interface
├── report/
│ ├── Brute force theoretical results.csv
│ ├── Brute force actual decryption results.csv
│ └── images/
├── data/
│ └── english.txt # BIP39 English wordlist
└── README.md
```
---


---

## 🖥️ GUI Interface

A PyQt5-based GUI is included for end-to-end interaction:

- 🔐 Generate 12 or 24-word mnemonics
- 🧬 Derive wallet address and keys
- 💥 Launch brute-force simulation with adjustable parameters:
  - Attack mode: `random` / `exhaustive`
  - Word count, prefix, weak pool size, start index
  - Repetition allowance, target coin, max attempts
- 📊 Live progress bar and logs
- 💾 Export results to CSV

---

## 🧪 Attack Simulation Example

Simulated attack configuration:

| Parameter        | Value                          |
|------------------|--------------------------------|
| Mnemonic Length  | 12 words                       |
| Prefix           | abandon abandon abandon        |
| Remaining Words  | 9                              |
| Weak Pool Size   | 64                             |
| Repeats Allowed  | ✅ Yes                         |
| Max Attempts     | 1,000,000                      |
| Target Coin      | ETH                            |

Despite 1 million attempts, the mnemonic was **not recovered**, confirming the high difficulty with a modest pool and partial knowledge.

---

## 📊 Analysis Results

Theoretical simulations show how different parameters affect attack feasibility:

- 24-word mnemonics provide **strong** security by default
- Long prefixes significantly reduce entropy
- Weak pools < 64 words are unsafe
- Allowing or disallowing word repeats has minor impact

---

## 🔎 Validation

Wallet derivation results are validated against [iancoleman.io BIP39 tool](https://iancoleman.io/bip39):

- ✅ Ethereum and Bitcoin addresses match
- ✅ Seed, public/private keys verified across formats

---

## 📚 Academic Relevance

This project aligns with academic coursework in:

- **Cyber Security Fundamentals**
- **Cryptography and Secure Development**
- **Applied Blockchain Security**

It also supports applications for roles in **FinTech security**, **crypto auditing**, and **blockchain key management**.

---

## 🧰 Technologies & Standards

- **Python** (3.8+), **PyQt5**
- `bip_utils`, `hashlib`, `secrets`, `tqdm`
- **BIP39 / BIP32 / BIP44**
- Seaborn & Matplotlib for analysis
- Modular OOP strategy pattern for attack simulation

---

## 🚀 Run the Project

### CLI mode

```bash
# Download the requirements
pip install -r requirements.txt

# Generate wallet keys
python src/wallet_key_deriver.py

# Simulate attack
python src/simulate_brute_force_attack.py

python src/gui_main.py
