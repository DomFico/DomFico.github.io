import os

# Define the directories to be scanned
directories = {
    "Coding Projects": "Coding Projects",
    "Research": "Research"
}

def generate_file_list_html(folder, files):
    file_links = [f'        <li><a href="{folder}/{file}">{file}</a></li>' for file in sorted(files)]
    return '    <ul>\n' + '\n'.join(file_links) + '\n    </ul>'

def remove_existing_placeholders(content):
    placeholders = [
        ('<!-- Coding Projects Start -->', '<!-- Coding Projects End -->'),
        ('<!-- Research Start -->', '<!-- Research End -->')
    ]
    for start, end in placeholders:
        start_index = content.find(start)
        end_index = content.find(end)
        if start_index != -1 and end_index != -1:
            content = content[:start_index] + content[end_index + len(end):]
    return content

def ensure_placeholders(content):
    placeholders = [
        ('<!-- Coding Projects Start -->', '<!-- Coding Projects End -->', 'coding-projects-files'),
        ('<!-- Research Start -->', '<!-- Research End -->', 'research-files')
    ]
    for start, end, div_id in placeholders:
        div_start = content.find(f'id="{div_id}"')
        if div_start != -1:
            div_end = content.find('>', div_start) + 1
            content = (
                content[:div_end] + 
                f'\n                <div class="connection-line"></div>\n' +
                f'                {start}\n' +
                f'                {end}\n' + 
                content[div_end:]
            )
    return content

def update_index_html():
    try:
        # Read the current index.html
        with open('index.html', 'r') as file:
            content = file.read()

        # Remove existing placeholders and their content
        content = remove_existing_placeholders(content)

        # Ensure placeholders exist in the HTML
        content = ensure_placeholders(content)

        # Generate the new HTML content for each directory
        for directory_name, directory_path in directories.items():
            files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
            html_content = generate_file_list_html(directory_path, files)
            
            start_placeholder = f'<!-- {directory_name} Start -->'
            end_placeholder = f'<!-- {directory_name} End -->'
            
            start_index = content.find(start_placeholder) + len(start_placeholder)
            end_index = content.find(end_placeholder)
            
            if start_index != -1 and end_index != -1:
                content = content[:start_index] + '\n' + html_content + '\n                ' + content[end_index:]

        # Write the updated HTML back to the file
        with open('index.html', 'w') as file:
            file.write(content)

        print("index.html has been updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure that the index.html file exists and has the correct structure.")

if __name__ == "__main__":
    update_index_html()