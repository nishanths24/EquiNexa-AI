import os
import json
import hashlib
import tarfile
import shutil
from datetime import datetime

class BackupError(Exception):
    pass

class BackupTool:
    def __init__(self, registry_dir: str = "backend/app/ai/research/registry"):
        self.registry_dir = registry_dir

    def _hash_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            return ""
        hasher = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def create_backup(self, output_dir: str) -> str:
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"equinexa_backup_{timestamp}"
        manifest_path = os.path.join(output_dir, f"{backup_name}_manifest.json")
        tar_path = os.path.join(output_dir, f"{backup_name}.tar.gz")
        
        manifest = {
            "timestamp": timestamp,
            "files": {}
        }
        
        files_to_backup = [
            "prospective_ledger.jsonl",
            "prospective_outcomes.jsonl",
            "phase9_review_flag.txt"
        ]
        
        # Verify and hash
        for file in files_to_backup:
            fp = os.path.join(self.registry_dir, file)
            if os.path.exists(fp):
                manifest["files"][file] = self._hash_file(fp)
                
        # Write manifest
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=4)
            
        # Create tar
        with tarfile.open(tar_path, "w:gz") as tar:
            for file in manifest["files"].keys():
                fp = os.path.join(self.registry_dir, file)
                tar.add(fp, arcname=file)
            tar.add(manifest_path, arcname=f"{backup_name}_manifest.json")
            
        return tar_path

    def restore_backup(self, tar_path: str, target_dir: str) -> bool:
        if not os.path.exists(tar_path):
            raise BackupError("Tar file not found")
            
        os.makedirs(target_dir, exist_ok=True)
        
        temp_dir = os.path.join(target_dir, "_temp_extract")
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=temp_dir)
                
            # Find manifest
            manifest_file = next((f for f in os.listdir(temp_dir) if f.endswith("_manifest.json")), None)
            if not manifest_file:
                raise BackupError("Manifest missing from backup archive")
                
            with open(os.path.join(temp_dir, manifest_file), 'r') as f:
                manifest = json.load(f)
                
            # Validate hashes
            for file, expected_hash in manifest["files"].items():
                fp = os.path.join(temp_dir, file)
                if not os.path.exists(fp):
                    raise BackupError(f"File missing from backup: {file}")
                actual_hash = self._hash_file(fp)
                if actual_hash != expected_hash:
                    raise BackupError(f"Hash mismatch for {file}")
                    
                # Validate JSONL parseable if jsonl
                if file.endswith(".jsonl"):
                    with open(fp, 'r') as jf:
                        for line in jf:
                            if line.strip():
                                try:
                                    json.loads(line)
                                except json.JSONDecodeError:
                                    raise BackupError(f"Corrupted JSONL record in {file}")
                                    
            # If all valid, move to target
            for file in manifest["files"].keys():
                shutil.copy(os.path.join(temp_dir, file), os.path.join(target_dir, file))
                
            return True
            
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
