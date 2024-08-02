import os
import re

# Define the directories to be scanned
directories = {
    "Coding Projects": "Coding Projects",
    "Research": "Research"
}

def generate_file_list_html(folder, path):
    """Generate HTML list items for files and folders in the specified path."""
    items = sorted(os.listdir(path))
    file_links = []
    
    for item in items:
        item_path = os.path.join(path, item)
        if os.path.isfile(item_path):
            file_links.append(f'                    <li class="file"><span></span><i class="fas fa-file"></i> <a href="{folder}/{item}" target="_blank">{item}</a></li>')
        elif os.path.isdir(item_path):
            folder_id = f'{folder.replace(" ", "-").lower()}-{item.replace(" ", "-").lower()}'
            file_links.append(f'''                    <li class="folder">
                        <span></span><i class="fas fa-folder" onclick="toggleFiles('{folder_id}')"></i> {item}
                        <ul class="files" id="{folder_id}" style="display: none;">
                            <!-- {folder_id} Start -->
                            {generate_file_list_html(f"{folder}/{item}", item_path)}
                            <!-- {folder_id} End -->
                        </ul>
                    </li>''')
    
    return '\n'.join(file_links)

def remove_existing_placeholders(content):
    """Remove existing placeholders and their content from the HTML content."""
    # Remove main directories placeholders
    content = re.sub(r'<!-- Coding Projects Start -->.*<!-- Coding Projects End -->', '<!-- Coding Projects Start --><!-- Coding Projects End -->', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Research Start -->.*<!-- Research End -->', '<!-- Research Start --><!-- Research End -->', content, flags=re.DOTALL)
    
    # Remove dynamic folder placeholders
    content = re.sub(r'<!-- ([\w-]+) Start -->.*<!-- \1 End -->', r'<!-- \1 Start --><!-- \1 End -->', content, flags=re.DOTALL)
    
    return content

def update_index_html():
    """Update the index.html file with the list of files and folders from the specified directories."""
    try:
        # Read the current index.html
        with open('index.html', 'r') as file:
            content = file.read()

        # Remove existing placeholders and their content
        content = remove_existing_placeholders(content)

        # Generate the new HTML content for each directory
        for directory_name, directory_path in directories.items():
            if os.path.exists(directory_path):
                html_content = generate_file_list_html(directory_path, directory_path)
                
                start_placeholder = f'<!-- {directory_name} Start -->'
                end_placeholder = f'<!-- {directory_name} End -->'
                
                content = re.sub(f'({re.escape(start_placeholder)}).*({re.escape(end_placeholder)})', f'\\1\n{html_content}\n                \\2', content, flags=re.DOTALL)

        # Write the updated HTML back to the file
        with open('index.html', 'w') as file:
            file.write(content)

        print("index.html has been updated successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please ensure that the index.html file exists and has the correct structure.")

if __name__ == "__main__":
    update_index_html()
