import re
from collections import defaultdict
import glob

def parse_cpin_file(cpin_file):
    """
    Parse the CPIN file to extract residue mappings.

    Args:
    cpin_file (str): Path to the CPIN file.

    Returns:
    dict: Mapping of residue indices to (residue name, residue number).
    """
    residue_mapping = {}
    with open(cpin_file, 'r') as file:
        content = file.read()
        resname_match = re.search(r"RESNAME=(.*?)\n RESSTATE=", content, re.DOTALL)
        if resname_match:
            resnames = resname_match.group(1).replace("'", "").split(',')
            filtered_resnames = [res for res in resnames if "System: Unknown" not in res]
            for index, res in enumerate(filtered_resnames):
                match = re.match(r"Residue: (\w+) (\d+)", res.strip())
                if match:
                    residue_mapping[index] = (match.group(1), int(match.group(2)))
    return residue_mapping

def parse_cpout_files(cpout_files):
    """
    Parse the CPOUT files to extract residue states and time steps.

    Args:
    cpout_files (list of str): List of paths to CPOUT files.

    Returns:
    tuple: (combined_residue_states, time_mapping)
        combined_residue_states (dict): Mapping of residue index to list of states.
        time_mapping (list of str): List of time values for each frame.
    """
    combined_residue_states = defaultdict(list)
    time_mapping = []
    cpout_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))  # Sort files numerically
    for cpout_file in cpout_files:
        with open(cpout_file, 'r') as file:
            content = file.read()
            time_steps = content.split('Solvent pH:')[1:]
            for step in time_steps:
                time_match = re.search(r"Time:\s+([\d\.]+)", step)
                if time_match:
                    time_mapping.append(time_match.group(1))
                residues = re.findall(r"Residue\s+(\d+)\s+State:\s+(\d+)", step)
                for res in residues:
                    combined_residue_states[int(res[0])].append(int(res[1]))
    return combined_residue_states, time_mapping

def generate_cpinutil_command(cpin_file, cpout_files, frame_number):
    """
    Generate the command to run cpinutil.py based on the residue states at a given frame.

    Args:
    cpin_file (str): Path to the CPIN file.
    cpout_files (list of str): List of paths to CPOUT files.
    frame_number (int): Frame number to extract states from (1-based indexing).

    Prints:
    str: Generated command to run cpinutil.py.
    """
    residue_mapping = parse_cpin_file(cpin_file)
    combined_residue_states, time_mapping = parse_cpout_files(cpout_files)

    resnums = []
    states = []
    frame_index = frame_number - 1  # Adjust for 1-based indexing
    for index, (res_name, res_num) in residue_mapping.items():
        if index in combined_residue_states:
            if frame_index < len(combined_residue_states[index]):
                resnums.append(res_num)
                states.append(combined_residue_states[index][frame_index])
            else:
                print(f"Warning: Frame number {frame_number} exceeds the available frames for residue {index}.")
        else:
            print(f"Warning: Residue index {index} not found in cpout files.")

    resnums_str = ", ".join(map(str, resnums))
    states_str = " ".join(map(str, states))

    command = f"cpinutil.py -p hal_cterm.parm7 -o hal_cterm.cpin -resnums {resnums_str} -states {states_str}"

    if frame_index < len(time_mapping):
        print(f"Time for frame {frame_number}: {time_mapping[frame_index]}")
    else:
        print(f"Warning: Frame number {frame_number} exceeds the available time steps.")

    print("Generated command:")
    print(command)

def main():
    """
    Main function to generate the cpinutil.py command for a specified frame.

    Modify the `frame_number` variable to the desired frame (1-based indexing) before running.
    """
    cpin_file = "hal_cterm.cpin"
    cpout_files = glob.glob("hal_cterm.amd.array_*.cpout")
    frame_number = 1  # Change this to the desired frame number (1-based indexing)

    generate_cpinutil_command(cpin_file, cpout_files, frame_number)

if __name__ == "__main__":
    main()
