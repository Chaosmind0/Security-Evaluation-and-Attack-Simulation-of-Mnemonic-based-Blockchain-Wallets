import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

def theoretical_results_analysis(path_to_csv: str = "report/Brute force theoretical results.csv", 
                                 output_dir: str = "report/images"):
    
    os.makedirs(output_dir, exist_ok=True)

    # Load the CSV again to ensure it's in fresh state
    assert os.path.exists(path_to_csv), f"File not found: {path_to_csv}"
    df = pd.read_csv(path_to_csv)

    # Create output directory for plots
    os.makedirs(output_dir, exist_ok=True)

    # Plot 1: word_count vs security level
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="word_count", hue="security level", palette="Set2")
    plt.title("Security Level by Word Count")
    plt.xlabel("Word Count")
    plt.ylabel("Count")
    plt.legend(title="Security Level")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/word_count_vs_security_level.png")
    plt.close()

    # Plot 2: prefix_length vs security level
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="prefix_length", hue="security level", palette="Set2")
    plt.title("Security Level by Prefix Length")
    plt.xlabel("Prefix Length")
    plt.ylabel("Count")
    plt.legend(title="Security Level")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/prefix_length_vs_security_level.png")
    plt.close()

    # Plot 3: allow_repeats vs security level
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="allow_repeats", hue="security level", palette="Set2")
    plt.title("Security Level by Allow Repeats")
    plt.xlabel("Allow Repeats")
    plt.ylabel("Count")
    plt.xticks([0, 1], ["False", "True"])
    plt.legend(title="Security Level")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/allow_repeats_vs_security_level.png")
    plt.close()

    # Plot 4: weak_pool_size vs security level
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="weak_pool_size", hue="security level", palette="Set2")
    plt.title("Security Level by Pool Size")
    plt.xlabel("Weak Pool Size")
    plt.ylabel("Count")
    plt.legend(title="Security Level")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/pool_size_vs_security_level.png")
    plt.close()


if __name__ == "__main__":
    theoretical_results_analysis("report/Brute force theoretical results.csv", "report/images")
