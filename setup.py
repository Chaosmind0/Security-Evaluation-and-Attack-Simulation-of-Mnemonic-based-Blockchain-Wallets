from setuptools import setup, find_packages

setup(
    name="bip39-brute-force",
    version="1.0.0",
    author="Chaosmind0",
    description="BIP39 Mnemonic Brute-Force Attack learning tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Chaosmind0/Security-Evaluation-and-Attack-Simulation-of-Mnemonic-based-Blockchain-Wallets",
    
    # Key configuration: Specified package directory
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Include data files in the package
    include_package_data=True,
    package_data={
        "": ["report/*.csv", "report/images/*"]
    },
    
    # Requirements
    install_requires=[
        "bip39>=0.1",
        "mnemonic>=0.20",
        "pycryptodome>=3.10.1",
        "seaborn>=0.11.2",
        "pandas>=1.3.4",
        "PyQt5>=5.15.6",
    ],
    
    # Scripts
    entry_points={
        "gui_scripts": [
            "bip39-gui = gui_main:main"
        ],
        "console_scripts": [
            "bip39-simulate = simulate_brute_force_attack:main"
        ]
    },
    
    # Classifiers
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography"
    ],
    python_requires=">=3.8",
)