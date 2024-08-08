import re
import numpy as np

def read_distance_file(file_path):
    """
    Reads a distance file and returns a dictionary with frame as key and distance as value.
    
    The .txt files were generated using cpptraj with commands like:
    distance :1032@OG1 :1056@PG out dist_res1032OG1_res1056PG.txt
    The files contain lines in the format: 'frame distance'
    """
    distances = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):  # Skip comment lines
                continue
            match = re.match(r'\s*(\d+)\s+([\d.]+)', line)  # Match lines with frame and distance
            if match:
                frame = int(match.group(1))
                distance = float(match.group(2))
                distances[frame] = distance
    print(f"Read {len(distances)} entries from {file_path}")
    return distances

def read_angle_file(file_path):
    """
    Reads an angle file and returns a dictionary with frame as key and angle as value.
    
    The .dat files were generated using cpptraj with commands like:
    angle angle_set1 :461@OG1 :1032@HA :1032@CA out dephosphorylation_1032.dat
    The files contain lines in the format: 'frame angle'
    """
    angles = {}
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#'):  # Skip comment lines
                continue
            match = re.match(r'\s*(\d+)\s+([\d.]+)', line)  # Match lines with frame and angle
            if match:
                frame = int(match.group(1))
                angle = float(match.group(2))
                angles[frame] = angle
    print(f"Read {len(angles)} entries from {file_path}")
    return angles

def find_ranked_frames_by_distance(dist_files):
    """
    Finds and ranks frames by their total distance from the provided distance files.
    Returns a sorted list of frames and their corresponding total distances.
    """
    distance_data = [read_distance_file(file) for file in dist_files]  # Read distance data from files

    # Convert to numpy array for easier manipulation
    frames = list(distance_data[0].keys())
    distances = np.array([[data[frame] for data in distance_data] for frame in frames])

    # Sum distances across all files for each frame
    total_distances = distances.sum(axis=1)
    
    # Calculate the standard deviation of distances for each frame
    std_devs = np.std(distances, axis=1)
    
    # Combine frame information, total distances, and standard deviations
    frame_info = [(frames[i], total_distances[i], distances[i], std_devs[i]) for i in range(len(frames))]

    # Sort frames by standard deviation (ascending), then by total distance (ascending)
    sorted_frames = sorted(frame_info, key=lambda x: (x[3], x[1]))

    return sorted_frames

def check_angles(frame, angle_data):
    """
    Checks if the angles at the given frame are above 140 degrees.
    Returns a tuple (True, angles) if both angles are above 140, otherwise (False, angles).
    """
    angles = []
    for data in angle_data:
        angle_at_frame = data.get(frame, None)
        angles.append(angle_at_frame)
        if angle_at_frame is None or angle_at_frame <= 140:
            return False, angles
    return True, angles

def check_distances(distances):
    """
    Checks if all distances are below 6 angstroms.
    Returns True if all distances are below 6, otherwise False.
    """
    return all(distance < 6 for distance in distances)

def main():
    # Define file paths for distance and angle files
    dist_files = ['dist_res1032OG1_res1056PG.txt', 'dist_res1032OG1_res296CG.txt', 'dist_res1032CA_res461CA.txt']
    angle_files = ['dephosphorylation_1032.dat', 'phosphorylation_1032.dat']

    # Read and cache angle data
    angle_data = [read_angle_file(file) for file in angle_files]

    # Find and rank frames by their total distance across all distance files
    ranked_frames = find_ranked_frames_by_distance(dist_files)

    # Iterate through ranked frames and check angles and distances
    for frame, total_distance, distances, std_dev in ranked_frames:
        if check_distances(distances):  # Check if all distances are below 6 angstroms
            angles_ok, angles = check_angles(frame, angle_data)  # Check if angles are above 140 degrees
            if angles_ok:
                # Print frames that meet all criteria
                print(f"Frame {frame} meets all criteria with total distance {total_distance}, distances {distances}, angles {angles}, and std deviation {std_dev}")

if __name__ == "__main__":
    main()
