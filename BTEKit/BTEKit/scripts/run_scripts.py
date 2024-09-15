import subprocess
import shutil
import os

# Main script categories
main_script_mapping = {
    1: "phonopy",  # Phonopy-related tasks
    2: "3rd_order",  # Third-order tasks
    3: "BTE",  # BTE-related tasks
    4: "elastic_constants",  # Elastic constants
}

# Phonopy-related task mapping
phonopy_script_mapping = {
    1: "Loop-phonopy.sh",  # Copy Loop-phonopy.sh to current directory
}

# BTE sub-category mapping
bte_script_mapping = {
    1: "BTE-EpsilonBorn.sh",  # 介电常数
    2: "BTE-kappa.py",
    3: "BTE-scatter5.py",
    4: "BTE2quantity.sh",
    5: "BTE-boundaryRescale.sh",
    6: "BTE-boundaryRescale.py",
    7: "BTE-calckappa.py",
    8: "BTE-calckappa2.py",
    9: "BTE-copy3nd.sh",
    10: "BTE-gruneisen.py",
    11: "BTE-P3.py",
    12: "BTE-poscar.sh",
    13: "BTE-relaxationTime.py",
    14: "BTE-RestructBTE.sh",
    15: "BTE-scatter.py",
    16: "BTE-scatter2.py",
    17: "BTE-scatter3.py",
    18: "BTE-scatter4.py",
    19: "BTE-scatterNU.py",
}


def execute_script(script_path):
    """Execute the selected script."""
    try:
        subprocess.run(script_path, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")


def copy_script(script_name):
    """Copy the selected script to the current directory."""
    try:
        current_dir = os.getcwd()
        shutil.copy(script_name, current_dir)
        print(f"{script_name} has been copied to {current_dir}")
    except FileNotFoundError as e:
        print(f"Script not found: {e}")
    except Exception as e:
        print(f"An error occurred while copying the script: {e}")


def main():
    print("Select a category:")
    for key, value in main_script_mapping.items():
        print(f"{key}: {value}")

    category_choice = int(input("Enter the number for the category you want to choose: "))

    if category_choice == 1:  # Phonopy-related tasks
        print("\nSelect a Phonopy-related task:")
        for key, value in phonopy_script_mapping.items():
            print(f"{key}: {value}")

        phonopy_choice = int(input("Enter the number for the task you want to execute: "))
        if phonopy_choice in phonopy_script_mapping:
            copy_script(phonopy_script_mapping[phonopy_choice])
        else:
            print("Invalid choice.")

    elif category_choice == 3:  # BTE category
        print("\nSelect a BTE-related task:")
        for key, value in bte_script_mapping.items():
            print(f"{key}: {value}")

        bte_choice = int(input("Enter the number for the BTE task you want to execute: "))
        if bte_choice in bte_script_mapping:
            execute_script(bte_script_mapping[bte_choice])
        else:
            print("Invalid choice.")

    else:
        print("This category is not yet implemented.")


if __name__ == "__main__":
    main()
