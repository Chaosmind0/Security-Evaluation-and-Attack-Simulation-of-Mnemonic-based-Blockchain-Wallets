# Simulate Brute-Force Attack on Mnemonic-Based Blockchain Wallets

# Experimental Objective

This experiment aims to evaluate the security of blockchain wallets based on low-entropy mnemonics against brute-force attacks. It simulates the process where real attackers, knowing part of the mnemonic prefix and limiting the size of the word pool, attempt to recover the wallet mnemonic and derive the target address.

# Experimental Context

The BIP39 mnemonic word standard is used to convert wallet keys into a set of memorable English words. However, in actual usage, some users may have the following weaknesses: 

- There are duplicate words in the mnemonic phrase (such as: "abandon abandon abandon") 
- Used common words or those with the first letters in a higher order (such as the first 128 words of BIP39) 
- Only the prefix part was used as a backup, while the remaining part relied on memory. 

The attackers can utilize this information to construct a weak entropy word pool, and then use brute-force cracking methods to attempt to recover the entire mnemonic phrase.

## Attack Model and Assumptions

- The attacker is aware of the mnemonic word prefix (for example, the first three words are "abandon abandon abandon") 
- The attacker knew that the mnemonic phrase used by the victim was 12 words long. 
- The attacker assumes that the remaining 9 words come from a weak entropy word pool, with a size of 64. 
- The attacker is allowed to have duplicate words in the mnemonic phrase (the combination number is 64^9) 
- The attacker attempts to combine the mnemonic words one by one, derives the address, and compares it with the target address.

## Experimental Parameter Settings

| Parameter item |  Value |
|--------|------|
| Mnemonic Length | 12 words |
| Fix Prefix | abandon abandon abandon |
| Remaining Compound Words | 9 |
| Size of the vocabulary pool | 64 |
| Repeat | Yes |
| Max Attempts | 10000 (adjustable) |
| Derived path | m/44'/60'/0'/0/0 (ETH address) |

## Experimental Methodology

The experiment is performed using the Python programming language. The `simulate_brute_force_attack.py` script is used to simulate the brute-force attack. The script takes the following steps:

1. Generate a target weak mnemonic and derive its address using the `BIP39MnemonicGenerator` class.
2. Generate a list of all possible combinations of the remaining 9 words using the `itertools.product` function.
3. For each combination, derive the address using the `WalletKeyDeriver` class and compare it with the target address.
4. Using the `tqdm` library, print the progress of the attack.
5. If the derived address matches the target address, print the combination and stop the attack.
6. If the maximum number of attempts is reached, print a message indicating that the attack has failed.

# Experimental Results

```
Target ETHEREUM address: 0x82d331e129df476e451493c6FC1E18cbDFAED08e
Target mnemonic: abandon abandon abandon accident account allow ability album afford alpha alien allow
Starting brute-force attack...

Brute-force progress: 100% 1000000/1000000 [46:33<00:00, 357.96it/s]
Failed to recover mnemonic within max attempts.
```

In 46 mins 33 seconds, the attacker have tried 1000000 (10^6) combinations of the 9 remaining words with 357.96 it/s (iterations per second) speed, and failed to recover the target mnemonic within the maximum number of attempts.

## Safety Analysis and Conclusion

### Estimation of Space Clearance

Select 9 words from the 64-word pool that allows repetition:

64^9 ≈ 2.81 x 10^16 combinations

The number of combinations that the attacker needs to try is extremely large. Without sufficient prior information (such as prefixes, narrowing the word pool, etc.), the success probability is extremely low.

In the situation of 10^6 combinations to try, the possibility of the attacker successfully cracking the code is extremely low, which only 2.81 x 10^(-10).

### Conclusion

If the mnemonic word has weak entropy characteristics (fixed prefix + small word pool + allowing repetition), brute-force cracking becomes feasible with reasonable computing resources.

If the mnemonic phrase uses the complete BIP39 word list (2048 words) without repetition or pattern, the cost of brute-force cracking would be extremely high and is currently not feasible with the current computing power. 

Whether it is successful or not is not the only measure of value. The "attempt count - success rate" relationship in brute-force attacks itself has significance for security assessment.

## Suggestion and Countermeasure

Users should avoid using repetitive or common initial words as mnemonic phrases. 

Use the standard mnemonic words generated from the full word list as much as possible 

Avoid merely recording some of the mnemonic words as a "backup". It is recommended to use the complete mnemonic words and store them securely. 

It is strongly recommended to enable the additional password (passphrase) function of the wallet. 

The wallet software can integrate mnemonic word strength detection and entropy value indication to prevent users from using weak mnemonic words.