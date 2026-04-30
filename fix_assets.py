import re

with open('app/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix href="assets/..."
content = re.sub(r'href="assets/([^"]+)"', r'href="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

# Fix src="assets/..."
content = re.sub(r'src="assets/([^"]+)"', r'src="{{ url_for(\'static\', filename=\'assets/\1\') }}"', content)

with open('app/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Assets replaced successfully.")
