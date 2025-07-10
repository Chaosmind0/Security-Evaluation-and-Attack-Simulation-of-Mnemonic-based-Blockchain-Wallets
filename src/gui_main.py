import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QTextEdit, QVBoxLayout,
    QHBoxLayout, QComboBox, QMessageBox, QLineEdit, QCheckBox, QProgressBar
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
        self.setGeometry(300, 200, 900, 700)

        self.generator = BIP39MnemonicGenerator()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # ---------- 助记词生成 ----------
        layout.addWidget(QLabel("1. Mnemonic Generator"))

        self.word_count_box = QComboBox()
        self.word_count_box.addItems(["12", "24"])
        layout.addWidget(self.word_count_box)

        self.generate_btn = QPushButton("Generate Mnemonic")
        self.generate_btn.clicked.connect(self.generate_mnemonic)
        layout.addWidget(self.generate_btn)

        self.mnemonic_output = QTextEdit()
        self.mnemonic_output.setReadOnly(True)
        layout.addWidget(self.mnemonic_output)

        # ---------- 钱包推导 ----------
        layout.addWidget(QLabel("2. Wallet Derivation"))

        self.mnemonic_input = QTextEdit()
        self.mnemonic_input.setPlaceholderText("Paste your BIP39 mnemonic phrase here...")
        layout.addWidget(self.mnemonic_input)

        self.derive_btn = QPushButton("Derive ETH & BTC Address")
        self.derive_btn.clicked.connect(self.derive_wallet)
        layout.addWidget(self.derive_btn)

        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)
        layout.addWidget(self.result_output)

        # ---------- 破解模拟 ----------
        layout.addWidget(QLabel("3. Brute-force Attack Simulator"))

        self.mode_box = QComboBox()
        self.mode_box.addItems(["random", "exhaustive"])
        layout.addWidget(QLabel("Mode:"))
        layout.addWidget(self.mode_box)

        self.prefix_input = QLineEdit("abandon abandon abandon")
        layout.addWidget(QLabel("Prefix (space-separated):"))
        layout.addWidget(self.prefix_input)

        self.pool_size_input = QLineEdit("64")
        layout.addWidget(QLabel("Weak Pool Size:"))
        layout.addWidget(self.pool_size_input)

        self.pool_start_input = QLineEdit("0")
        layout.addWidget(QLabel("Pool Start Index:"))
        layout.addWidget(self.pool_start_input)

        self.allow_repeats_box = QCheckBox("Allow Repeats")
        self.allow_repeats_box.setChecked(True)
        layout.addWidget(self.allow_repeats_box)

        self.target_coin_box = QComboBox()
        self.target_coin_box.addItems(["ETHEREUM", "BITCOIN"])
        layout.addWidget(QLabel("Target Coin:"))
        layout.addWidget(self.target_coin_box)

        self.max_attempts_input = QLineEdit("10000")
        layout.addWidget(QLabel("Max Attempts:"))
        layout.addWidget(self.max_attempts_input)

        self.attack_word_count_box = QComboBox()
        self.attack_word_count_box.addItems(["12", "24"])
        layout.addWidget(QLabel("Attack Mnemonic Word Count:"))
        layout.addWidget(self.attack_word_count_box)

        self.start_attack_btn = QPushButton("Start Brute-force Attack")
        self.start_attack_btn.clicked.connect(self.start_attack_thread)
        layout.addWidget(self.start_attack_btn)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.attack_output = QTextEdit()
        self.attack_output.setReadOnly(True)
        layout.addWidget(self.attack_output)

        self.setLayout(layout)

    def generate_mnemonic(self):
        count = int(self.word_count_box.currentText())
        mnemonic = self.generator.generate_mnemonic(count)
        self.mnemonic_output.setText(mnemonic)

    def derive_wallet(self):
        mnemonic = self.mnemonic_input.toPlainText().strip()
        try:
            deriver = WalletKeyDeriver(mnemonic)
            eth = deriver.derive_eth_address()
            btc = deriver.derive_btc_address()
            result = f"[Ethereum]\\nAddress: {eth['address']}\\nPrivate Key: {eth['private_key']}\\n\\n"
            result += f"[Bitcoin]\\nAddress: {btc['address']}\\nPrivate Key: {btc['private_key']}\\n"
            self.result_output.setText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Wallet derivation failed:\\n{str(e)}")

    def start_attack_thread(self):
        t = threading.Thread(target=self.simulate_attack)
        t.start()

    def simulate_attack(self):
        # 获取参数
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

        # 安全估计
        estimate = estimate_brute_force_security(
            pool_size=weak_pool_size,
            word_count=word_count,
            prefix_length=len(prefix),
            max_attempts=max_attempts,
            allow_repeats=allow_repeats
        )

        self.attack_output.append(f"=== Brute-force Estimation ===")
        self.attack_output.append(f"Total combinations: {estimate['total_combinations']}")
        self.attack_output.append(f"Entropy (bits): {estimate['entropy_bits']:.2f}")
        self.attack_output.append(f"Success Probability: {estimate['success_probability']:.2e}\\n")

        # 执行攻击
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
        self.attack_output.append(f"Time Elapsed: {result['elapsed_time']:.2f} sec\\n")

        self.progress_bar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WalletGUI()
    window.show()
    sys.exit(app.exec_())