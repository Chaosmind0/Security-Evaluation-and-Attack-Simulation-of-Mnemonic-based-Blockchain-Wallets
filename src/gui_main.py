import os
import sys
import pkgutil

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
src_path = os.path.join(project_root, "src")
sys.path.insert(0, src_path)

from utils import resource_path

import threading
import csv
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QMessageBox,
    QLineEdit,
    QCheckBox,
    QProgressBar,
    QGroupBox,
    QGridLayout,
    QFileDialog,
)
from PyQt5.QtCore import QObject, pyqtSignal


from bip39_mnemonic_generator import BIP39MnemonicGenerator
from wallet_key_deriver import WalletKeyDeriver
from attack_factory import get_attack_strategy
from attack_core import estimate_brute_force_security, check_parameters


class WorkerSignals(QObject):
    """

    Defines the signals available from a running worker thread.

    """

    progress = pyqtSignal(int, int)
    log = pyqtSignal(str)
    error = pyqtSignal(str)


class WalletGUI(QWidget):
    def __init__(self):
        """

        Constructor for the WalletGUI class.

        """

        super().__init__()
        self.setWindowTitle("Mnemonic Wallet Toolkit")
        self.setGeometry(200, 100, 1200, 700)
        self.generator = BIP39MnemonicGenerator()
        self.signals = WorkerSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.log.connect(self.attack_output_append)
        self.attack_results = []
        self.signals.error.connect(self.show_error_message)
        self.init_ui()

    def init_ui(self):
        """

        Initializes the user interface.

        """

        main_layout = QHBoxLayout()

        left_panel = QVBoxLayout()
        left_panel.addWidget(self.build_mnemonic_group())
        left_panel.addWidget(self.build_derivation_group())

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.build_attack_group())

        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(right_panel, 2)

        self.setLayout(main_layout)

    def build_mnemonic_group(self):
        """

        Builds the group for generating and displaying the mnemonic phrase.

        """

        group = QGroupBox("Mnemonic and Address")
        layout = QVBoxLayout()

        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("Word count"))
        self.word_count_box = QComboBox()
        self.word_count_box.addItems(["12", "24"])
        count_layout.addWidget(self.word_count_box)
        self.generate_btn = QPushButton("Generate")
        self.generate_btn.clicked.connect(self.generate_mnemonic)
        count_layout.addWidget(self.generate_btn)
        layout.addLayout(count_layout)

        self.mnemonic_label = QLabel("Mnemonic Phrase")
        layout.addWidget(self.mnemonic_label)
        self.mnemonic_output = QTextEdit()
        self.mnemonic_output.setReadOnly(True)
        layout.addWidget(self.mnemonic_output)

        self.seed_label = QLabel("BIP39 Seed")
        layout.addWidget(self.seed_label)
        self.seed_output = QTextEdit()
        self.seed_output.setReadOnly(True)
        layout.addWidget(self.seed_output)

        group.setLayout(layout)
        return group

    def build_derivation_group(self):
        """

        Builds the group for deriving the wallet addresses.

        """

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
        """

        Builds the group for simulating the brute-force attack.

        """

        group = QGroupBox("Brute-force Attack Simulator")
        layout = QGridLayout()

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

        layout.addWidget(QLabel("Prefix (space-separated):"), 1, 0, 1, 2)
        self.prefix_input = QLineEdit("abandon abandon abandon")
        layout.addWidget(self.prefix_input, 1, 2, 1, 6)

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
        layout.addWidget(self.attack_btn, 2, 6)

        self.save_btn = QPushButton("Save as")
        self.save_btn.clicked.connect(self.save_result_as_csv)
        layout.addWidget(self.save_btn, 2, 7)

        self.attack_output = QTextEdit()
        self.attack_output.setReadOnly(True)
        layout.addWidget(self.attack_output, 3, 0, 1, 8)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar, 4, 0, 1, 8)

        group.setLayout(layout)
        return group

    def generate_mnemonic(self):
        """

        Generates a new mnemonic phrase and displays it in the GUI.

        """

        count = int(self.word_count_box.currentText())
        mnemonic = self.generator.generate_mnemonic(count)
        self.mnemonic_output.setText(mnemonic)
        deriver = WalletKeyDeriver(mnemonic)
        self.seed_output.setText(deriver.get_seed_hex())

    def derive_wallet(self):
        """

        Derives the wallet addresses from the given mnemonic phrase and displays them in the GUI.

        """

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
        """

        Starts a new thread to simulate the brute-force attack.

        """

        t = threading.Thread(target=self.simulate_attack)
        t.start()

    def update_progress(self, current: int, total: int):
        """

        Updates the progress bar in the GUI.

        """

        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)

    def attack_output_append(self, msg: str):
        """

        Appends a message to the attack output in the GUI.

        """

        self.attack_output.append(msg)

    def thread_safe_progress(self, current: int, total: int):
        """

        Emits a progress signal from a thread-safe context.

        """

        self.signals.progress.emit(current, total)

    def save_result_as_csv(self):
        """

        Saves the attack results as a CSV file.

        """

        if not self.attack_results:
            QMessageBox.warning(self, "Warning", "No attack result to save.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Save CSV", "", "CSV Files (*.csv)")
        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                fieldnames = self.attack_results[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for r in self.attack_results:
                    writer.writerow(r)
            QMessageBox.information(self, "Success", f"All results saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save file:\n{str(e)}")

    def show_error_message(self, msg: str):
        """

        Displays an error message in the GUI.

        """

        QMessageBox.critical(self, "Error", msg)

    def simulate_attack(self):
        """

        Simulates the brute-force attack and displays the result in the GUI.

        """

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
            self.signals.error.emit(f"Input Error: {str(e)}")
            return

        try:
            check_parameters(prefix, word_count, weak_pool_size, pool_start)
        except AssertionError as ae:
            self.signals.error.emit(f"Parameter Error: {str(ae)}")
            return

        estimate = estimate_brute_force_security(
            pool_size=weak_pool_size,
            word_count=word_count,
            prefix_length=len(prefix),
            max_attempts=max_attempts,
            allow_repeats=allow_repeats,
        )

        self.signals.log.emit("=== Brute-force Estimation ===")
        self.signals.log.emit(f"Total combinations: {estimate['total_combinations']}")
        self.signals.log.emit(f"Entropy (bits): {estimate['entropy_bits']:.2f}")
        self.signals.log.emit(f"Success Probability: {estimate['success_probability']:.2e}\n")

        strategy = get_attack_strategy(mode)
        result = strategy.run(
            word_count=word_count,
            weak_pool_size=weak_pool_size,
            pool_start=pool_start,
            prefix=prefix,
            allow_repeats=allow_repeats,
            target_coin=target_coin,
            max_attempts=max_attempts,
            progress_callback=self.thread_safe_progress,
        )

        self.attack_results.append(result)

        self.signals.log.emit("=== Attack Result ===")
        self.signals.log.emit(f"Success: {result['success']}")
        self.signals.log.emit(f"Target Address: {result['target_address']}")
        self.signals.log.emit(
            f"Recovered Mnemonic: {result.get('mnemonic') or result.get('recovered_mnemonic')}"
        )
        self.signals.log.emit(f"Attempts: {result['attempts']}")
        self.signals.log.emit(f"Time Elapsed: {result['time_elapsed_sec']:.2f} sec\n")
        self.progress_bar.setValue(100)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = WalletGUI()
    gui.show()
    sys.exit(app.exec_())
