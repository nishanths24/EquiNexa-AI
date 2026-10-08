import os
import re

def resolve_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # We want to keep the HEAD block (our work) and discard the remote block.
    # Pattern looks like:
    # <<<<<<< HEAD
    # our content
    # =======
    # their content
    # >>>>>>> origin/main

    pattern = re.compile(r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> [^\n]+\n', re.DOTALL)
    
    new_content, count = pattern.subn(r'\1\n', content)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Resolved {count} conflicts in {filepath}")

if __name__ == "__main__":
    for root, dirs, files in os.walk('.'):
        if '.git' in root or 'node_modules' in root or 'test_venv' in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            try:
                resolve_file(filepath)
            except Exception as e:
                pass
