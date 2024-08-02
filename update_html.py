import os

# Define the directories to be scanned
directories = {
    "Coding Projects": "Coding Projects",
    "Research": "Research"
}

# Function to generate HTML for a list of files
def generate_file_list_html(folder, files):
    file_links = [f'<a href="{folder}/{file}">{file}</a>' for file in files]
    return '\n'.join(f'<div>{link}</div>' for link in file_links)

def ensure_placeholders(lines):
    # Define the placeholders and the divs where they should be placed
    placeholders = [
        ('<!-- Coding Projects Start -->', '<!-- Coding Projects End -->', 'coding-projects-files'),
        ('<!-- Research Start -->', '<!-- Research End -->', 'research-files')
    ]
    for start, end, div_id in placeholders:
        if start not in lines:
            print(f"Adding missing placeholder: {start.strip()}")
            # Find the index of the <div> by id
            div_start = next(i for i, line in enumerate(lines) if f'id="{div_id}"' in line)
            lines.insert(div_start + 1, f'{start}\n')
            lines.insert(div_start + 2, f'{end}\n')
    return lines

# Read the current index.html
with open('index.html', 'r') as file:
    lines = file.readlines()

# Ensure placeholders exist in the HTML
lines = ensure_placeholders(lines)

try:
    # Find the placeholders in the HTML where the file lists will be inserted
    coding_projects_start = lines.index('<!-- Coding Projects Start -->\n')
    coding_projects_end = lines.index('<!-- Coding Projects End -->\n')
    research_start = lines.index('<!-- Research Start -->\n')
    research_end = lines.index('<!-- Research End -->\n')

    # Generate the new HTML content for each directory
    coding_projects_files = os.listdir(directories['Coding Projects'])
    research_files = os.listdir(directories['Research'])

    coding_projects_html = generate_file_list_html(directories['Coding Projects'], coding_projects_files)
    research_html = generate_file_list_html(directories['Research'], research_files)

    # Update the HTML content
    lines[coding_projects_start + 1:coding_projects_end] = [coding_projects_html + '\n']
    lines[research_start + 1:research_end] = [research_html + '\n']

    # Write the updated HTML back to the file
    with open('index.html', 'w') as file:
        file.writelines(lines)

    print("index.html has been updated successfully.")
except ValueError as e:
    print(f"Error: {e}")
    print("Please ensure that the placeholders <!-- Coding Projects Start -->, <!-- Coding Projects End -->, <!-- Research Start -->, and <!-- Research End --> are present in the index.html file.")
