# DomFico.github.io

Website link: https://domfico.github.io/


To ensure that the script continues to update the HTML file properly when creating a custom layout, you need to follow these key guidelines. Firstly, include distinct comment placeholders for each directory or subdirectory in the format <!-- Directory Name Start --> and <!-- Directory Name End --> exactly matching the case and spacing. These placeholders mark where the dynamic content will be inserted. Each directory's content div should have a unique ID consistent with these placeholders. For instance, a directory named "Coding Projects" should have a div with the ID "coding-projects-files" and corresponding placeholders. Additionally, the HTML structure should be consistent, including necessary divs and spans to maintain proper layout. Ensure the toggleFiles function in your main.js handles the show/hide behavior of the directory contents, and it is correctly linked in your HTML. By adhering to these guidelines, you can create a custom layout that still allows the script to dynamically update the HTML with the correct file and folder listings.
