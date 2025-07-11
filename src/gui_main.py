import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox, QMessageBox, QLineEdit, QCheckBox, QProgressBar, QGroupBox, QGridLayout
)
from bip39_mnemonic_generator import BIP39MnemonicGenerator
from wallet_key_deriver import WalletKeyDeriver
from unsafe_wallet_key_deriver import UnsafeWalletKeyDeriver
from attack_factory import get_attack_strategy
from attack_core import estimate_brute_force_security


class WalletGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mnemonic Wallet Toolkit")
        self.setGeometry(200, 100, 1200, 700)
        self.generator = BIP39MnemonicGenerator()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Left: Mnemonic generation + Wallet derivation
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.build_mnemonic_group())
        left_panel.addWidget(self.build_derivation_group())

        # Right: Brute-force attack simulator
        right_panel = QVBoxLayout()
        right_panel.addWidget(self.build_attack_group())

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        self.setLayout(main_layout)

    def build_mnemonic_group(self):
        group = QGroupBox("Mnemonic and Address")
        layout = QVBoxLayout()

        # Word count + generate button
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Word count"))
        self.word_count_box = QComboBox()
        self.word_count_box.addItems(["12", "24"])
        count_layout.addWidget(self.word_count_box)
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_mnemonic)
        count_layout.addWidget(self.generate_btn)
        layout.addLayout(count_layout)

        # Output: mnemonic
        self.mnemonic_label = QLabel("<a href='#'>Mnemonic Phrase</a>")
        layout.addWidget(self.mnemonic_label)
        self.mnemonic_output = QTextEdit()
        self.mnemonic_output.setReadOnly(True)
        layout.addWidget(self.mnemonic_output)

        # Output: seed
        self.seed_label = QLabel("<a href='#'>BIP39 Seed</a>")
        layout.addWidget(self.seed_label)
        self.seed_output = QTextEdit()
        self.seed_output.setReadOnly(True)
        layout.addWidget(self.seed_output)

        group.setLayout(layout)
        return group

    def build_derivation_group(self):
        group = QGroupBox("Wallet Derivation")
        layout = QVBoxLayout()

        self.mnemonic_input = QTextEdit()
        self.mnemonic_input.setPlaceholderText("Paste your BIP39 mnemonic phrase here...")
        layout.addWidget(self.mnemonic_input)

        self.derive_btn = QPushButton("Generate")
        self.derive_btn.clicked.connect(self.derive_wallet)
        layout.addWidget(self.derive_btn)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        group.setLayout(layout)
        return group

    def build_attack_group(self):
        group = QGroupBox("Brute-force Attack Simulator")
        layout = QGridLayout()

        # Attack parameters row 1
        layout.addWidget(QLabel("Mode:"), 0, 0)
        self.mode_box = QComboBox()
        self.mode_box.addItems(["random", "exhaustive"])
        layout.addWidget(self.mode_box, 0, 1)

        layout.addWidget(QLabel("Weak Pool Size:"), 0, 2)
        self.pool_size_input = QLineEdit("64")
        layout.addWidget(self.pool_size_input, 0, 3)

        layout.addWidget(QLabel("Pool Start Index:"), 0, 4)
        self.pool_start_input = QLineEdit("0")
        layout.addWidget(self.pool_start_input, 0, 5)

        layout.addWidget(QLabel("Target Coin:"), 0, 6)
        self.target_coin_box = QComboBox()
        self.target_coin_box.addItems(["ETHEREUM", "BITCOIN"])
        layout.addWidget(self.target_coin_box, 0, 7)

        # Prefix
        layout.addWidget(QLabel("Prefix (space-separated):"), 1, 0, 1, 2)
        self.prefix_input = QLineEdit("abandon abandon abandon")
        layout.addWidget(self.prefix_input, 1, 2, 1, 6)

        # Row 3: word count, attempts, checkbox, start
        layout.addWidget(QLabel("Attack Mnemonic Word Count:"), 2, 0)
        self.attack_word_count_box = QComboBox()
        self.attack_word_count_box.addItems(["12", "24"])
        layout.addWidget(self.attack_word_count_box, 2, 1)

        layout.addWidget(QLabel("Max Attempts:"), 2, 2)
        self.max_attempts_input = QLineEdit("10000")
        layout.addWidget(self.max_attempts_input, 2, 3)

        self.allow_repeats_box = QCheckBox("Allow Repeats")
        self.allow_repeats_box.setChecked(True)
        layout.addWidget(self.allow_repeats_box, 2, 4)

        self.attack_btn = QPushButton("Generate")
        self.attack_btn.clicked.connect(self.start_attack_thread)
        layout.addWidget(self.attack_btn, 2, 6, 1, 2)

        # Output & progress
        self.attack_output = QTextEdit()
        self.attack_output.setReadOnly(True)
        layout.addWidget(self.attack_output, 3, 0, 1, 8)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 4, 0, 1, 8)

        group.setLayout(layout)
        return group

    def generate_mnemonic(self):
        count = int(self.word_count_box.currentText())
        mnemonic = self.generator.generate_mnemonic(count)
        self.mnemonic_output.setText(mnemonic)
        deriver = WalletKeyDeriver(mnemonic)
        self.seed_output.setText(deriver.get_seed_hex())

    def derive_wallet(self):
        mnemonic = self.mnemonic_input.toPlainText().strip()
        try:
            deriver = WalletKeyDeriver(mnemonic)
            eth = deriver.derive_eth_address()
            btc = deriver.derive_btc_address()
            result = f"Ethereum Address Info\ncoin: ETHEREUM\npath: {eth['path']}\naddress: {eth['address']}\nprivate_key: {eth['private_key']}\npublic_key: {eth['public_key']}\n\n"
            result += f"Bitcoin Address Info\ncoin: BITCOIN\npath: {btc['path']}\naddress: {btc['address']}\nprivate_key: {btc['private_key']}\npublic_key: {btc['public_key']}\n"
            self.result_output.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Wallet derivation failed:\n{str(e)}")

    def start_attack_thread(self):
        t = threading.Thread(target=self.simulate_attack)
        t.start()

    def simulate_attack(self):
        try:
            mode = self.mode_box.currentText()
            prefix = self.prefix_input.text().strip().split()
            weak_pool_size = int(self.pool_size_input.text())
            pool_start = int(self.pool_start_input.text())
            allow_repeats = self.allow_repeats_box.isChecked()
            target_coin = self.target_coin_box.currentText()
            max_attempts = int(self.max_attempts_input.text())
            word_count = int(self.attack_word_count_box.currentText())
        except Exception as e:
            QMessageBox.critical(self, "Input Error", str(e))
            return

        # Estimate
        estimate = estimate_brute_force_security(
            pool_size=weak_pool_size,
            word_count=word_count,
            prefix_length=len(prefix),
            max_attempts=max_attempts,
            allow_repeats=allow_repeats
        )

        self.attack_output.append("=== Brute-force Estimation ===")
        self.attack_output.append(f"Total combinations: {estimate['total_combinations']}")
        self.attack_output.append(f"Entropy (bits): {estimate['entropy_bits']:.2f}")
        self.attack_output.append(f"Success Probability: {estimate['success_probability']:.2e}\n")

        # Run attack
        strategy = get_attack_strategy(mode)
        result = strategy.run(
            word_count=word_count,
            weak_pool_size=weak_pool_size,
            pool_start=pool_start,
            prefix=prefix,
            allow_repeats=allow_repeats,
            target_coin=target_coin,
            max_attempts=max_attempts,
        )

        self.attack_output.append("=== Attack Result ===")
        self.attack_output.append(f"Success: {result['success']}")
        self.attack_output.append(f"Target Address: {result['target_address']}")
        self.attack_output.append(f"Recovered Mnemonic: {result.get('mnemonic') or result.get('recovered_mnemonic')}")
        self.attack_output.append(f"Attempts: {result['attempts']}")
        self.attack_output.append(f"Time Elapsed: {result['time_elapsed_sec']:.2f} sec\n")
        self.progress_bar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = WalletGUI()
    gui.show()
    sys.exit(app.exec_())
