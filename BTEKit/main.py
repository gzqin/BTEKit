import subprocess
import shutil
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'scripts')  # linux -- /public/home/weiyi22
# scripts/test/etikt/etkit/script

# Main script categories
main_script_mapping = {
    1: "phonopy calculation",  # Phonopy-related tasks
    2: "3rd_order calculation",  # Third-order tasks
    3: "BTE relative results read",  # BTE-related tasks
    4: "elastic_constants calculation submit",  # Elastic constants
    5: "epsilon-born results read"
}

# Phonopy-related task mapping
phonopy_script_mapping = {
    0: "phonopy-command",  # doesn't need to be edited, but need to be executed manually
    1: "Loop-phonopy.sh",  # Copy Loop-phonopy.sh to current directory, doesn't need to be edited
    2: "band-example.conf",
    3: "mesh-example.conf",
    4: "GruneisenPlot.sh", 
}

third_script_mapping = {
    0: "3rd-command",  # doesn't need to be edited
    1: "Loop-3rd.sh",  # Copy Loop-phonopy.sh to current directory, doesn't need to be edited
    2: "checkpend.sh",  # in case of the queue system down, doesn't need to be edited
    3: "BTE-copy3rd.sh",  # Construct the 3rd files(BTE input) based on the finished calculations,
    # doesn't need to be edited
    4: "traceIFC-distance.sh"  # Get the data of IFC-distance, need to be further edited
}


# BTE sub-category mapping
bte_script_mapping = {
    1: "BTE2quantity.sh",  # output velocity, relaxation time, gruneisen, P3, kappa, doesn't need to be edited
    2: "BTE-boundaryRescale.sh",  # get the kappa-size curve.(Contains anisotropy), need to be further edited(choose)
    3: "BTE-poscar.sh",  # get the poscar lattice for CONTROL
    4: "BTE-RestructBTE.sh",  # need to be further edited, bte calculation preprocess for different 3rd files
    5: "BTE-scatter-process.sh",  # need to be further edited, Get scatter.dat containing scattering channels
    5: "BTE-scatterNU.py",  # < 1e-5,  doesn't need to be edited
    6: "BTE-scatterNU-new.py",  # abs(q_dis) < 0.000000000000000000001 or abs(q_dis) > 27
    7: "BTE-scatter-process.sh",  # need to be further edited, Get scatter.dat containing scattering channels
    # Calculate the scatter rate of absorption, emission, N and U process
    8: "BTE-T-inc.sh",  # Increase the temperature and do ShengBTE calculation, TEMP_INC need to be edited
    9: "BTE-T-inc-collect.sh",  # calculation results collection script, TEMP_INC need to be edited
    10: "BTE-testQgrid.sh",  
    11: "BTE-gruneisen.py"  # similar bandplot, for gruneisen
}

bte_additional_files = {
    "BTE2quantity.sh": [
        "BTE-velocity.py",
        "BTE-relaxationTime.py",
        "BTE-P3.py",
        "BTE-kappa.py"
    ],
   "BTE-boundaryRescale.sh":[
       "BTE-boundaryRescale.py", 
       "BTE-boundaryRescale2.py"
   ],
    "BTE-scatter-process.sh": [
        "BTE-scatter.py",  # name={0: 'O', 1: 'ZA', 2: 'TA', 3: 'LA'}
        "BTE-scatter2.py",  # name={0: 'A', 1: 'O1', 2: 'O2'}
        "BTE-scatter3.py",  # name={0: 'O', 1: 'ZA', 2: 'TA/LA'}
        "BTE-scatter4.py",  # name={0: 'O', 1: 'ZA', 2: 'TA', 3: 'LA', 4: 'TOz', 5: 'TOx', 6: 'LOy'}
        "BTE-scatter5.py",  # name={0: 'O', 1: 'FA', 2: 'TA', 3: 'LA', 4: 'FO', 5: 'TO', 6: 'LO'}
    ]
}


elastic_script_mapping = {
    1: "cal_ela.sh"  # energy-strain
}

born_script_mapping = {
    1: "BTE-EpsilonBorn.sh"  # Obtain dielectric constant and Born effective charge
}


def execute_script(script_name):
    current_dir = os.getcwd()
    script_path = os.path.join(current_dir, script_name)
    try:
        if script_name.endswith('.py'):
            subprocess.run(f"python {script_path}", shell=True, check=True)
        elif script_name.endswith('.sh'):
            subprocess.run(f"bash {script_path}", shell=True, check=True)
        else:
            print(f"Unsupported script type for {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the script: {e}")


def copy_script(script_name):
    try:
        current_dir = os.getcwd()
        src_path = os.path.join(SCRIPTS_DIR, script_name)
        dest_path = os.path.join(current_dir, script_name)

        shutil.copy(src_path, dest_path)
        print(f"{script_name} has been generated in {current_dir}")

        if script_name.endswith('.sh'):
            subprocess.run(f"chmod u+x {dest_path}", shell=True, check=True)
            print(f"Execution permission has been granted to {script_name}")

        if script_name in bte_additional_files:
            for additional_file in bte_additional_files[script_name]:
                src_additional_path = os.path.join(SCRIPTS_DIR, additional_file)
                dest_additional_path = os.path.join(current_dir, additional_file)
                shutil.copy(src_additional_path, dest_additional_path)
                print(f"{additional_file} has been generated in {current_dir}")

    except FileNotFoundError as e:
        print(f"Script not found: {e}")
    except Exception as e:
        print(f"An error occurred while generating the script: {e}")


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

    elif category_choice == 2:  # 3rd-order related tasks
        print("\nSelect a 3rd-order-related task:")
        for key, value in third_script_mapping.items():
            print(f"{key}: {value}")

        third_choice = int(input("Enter the number for the task you want to execute: "))
        if third_choice in third_script_mapping:
            copy_script(third_script_mapping[third_choice])
        else:
            print("Invalid choice.")
        # third_script_mapping = {
        #     0: "3rd-command",  # doesn't need to be edited
        #     1: "Loop-3rd.sh",  # Copy Loop-phonopy.sh to current directory, doesn't need to be edited
        #     2: "checkpend.sh",  # in case of the queue system down, doesn't need to be edited
        #     3: "BTE-copy3rd.sh",  # Construct the 3rd files(BTE input) based on the finished calculations,
        #     # doesn't need to be edited
        #     4: "traceIFC-distance.sh"  # Get the data of IFC-distance, need to be further edited
        # }

    elif category_choice == 3:  # BTE category
        print("\nSelect a BTE-related task:")
        for key, value in bte_script_mapping.items():
            print(f"{key}: {value}")

        bte_choice = int(input("Enter the number for the BTE task you want to execute: "))
        if bte_choice in bte_script_mapping:
            copy_script(bte_script_mapping[bte_choice])
            execute_script(bte_script_mapping[bte_choice])
        else:
            print("Invalid choice.")

    elif category_choice == 4:  # Elastic constants tasks
        print("\nSelect an Elastic-related task:")
        for key, value in elastic_script_mapping.items():
            print(f"{key}: {value}")

        elastic_choice = int(input("Enter the number for the task you want to execute: "))
        if elastic_choice in elastic_script_mapping:
            copy_script(elastic_script_mapping[elastic_choice])
            # execute_script(elastic_script_mapping[elastic_choice])
        else:
            print("Invalid choice.")

    elif category_choice == 5:  # Epsilon-Born tasks
        print("\nSelect an Epsilon-Born-related task:")
        for key, value in born_script_mapping.items():
            print(f"{key}: {value}")

        born_choice = int(input("Enter the number for the task you want to execute: "))
        if born_choice in born_script_mapping:
            copy_script(born_script_mapping[born_choice])
            # execute_script(born_script_mapping[born_choice])
        else:
            print("Invalid choice.")

    else:
        print("This category is not yet implemented.")


if __name__ == "__main__":
    main()

