import glob
import os

files = glob.glob(r"c:\Users\nisha\OneDrive\Desktop\EquiNexa AI\frontend\src\pages\*.tsx")
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace("import React from 'react';\n\n", "")
    content = content.replace("import React from 'react';\n", "")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Fixed imports")
