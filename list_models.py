import os
import sys
from dotenv import load_dotenv

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend', '.env'))
load_dotenv(dotenv_path=dotenv_path)

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key or "YOUR_API_KEY_HERE" in api_key:
    print("No valid key found in backend/.env")
    sys.exit(1)

from google import genai
client = genai.Client(api_key=api_key)

print("Available Models:")
for m in client.models.list():
    if "flash" in m.name.lower():
        print(f"Name: {m.name}, Display Name: {m.display_name}")
