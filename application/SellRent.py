import os

# Define the directory containing the HTML files
directory = '/var/www/csc648-sp24-03-team03/application/public/html/about'

# Define the strings to be replaced
old_string = 'Sell.html'
new_string = 'SellRent.html'

# Function to replace old string with new string in a file
def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    updated_content = file_content.replace(old_string, new_string)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

# Iterate over all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        file_path = os.path.join(directory, filename)
        replace_string_in_file(file_path, old_string, new_string)

print("String replacement completed.")
