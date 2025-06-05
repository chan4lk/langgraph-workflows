import subprocess
import os
def extract_mermaid_block(text):
    import re
    match = re.search(r"```mermaid\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    raise ValueError("No Mermaid diagram found")

def save_mermaid_to_png(mermaid_code, output_path="diagram.png"):
    try:
        current_dir = os.getcwd()
        with open(os.path.join(current_dir, "temp_diagram.mmd"), "w") as f:
            f.write(mermaid_code)
        subprocess.run([
            "mmdc",
            "-i",   os.path.join(current_dir, "temp_diagram.mmd"),
            "-o", os.path.join(current_dir, output_path),
            "--quiet"
        ], check=True)
        return os.path.join(current_dir, output_path)
    except Exception as e:
        print(f"Error saving Mermaid diagram to PNG: {e}")
        return None
        