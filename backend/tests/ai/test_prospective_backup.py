import pytest
import os
import json
import sys
import tarfile

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from backend.app.ai.research.backup_tool import BackupTool, BackupError
from backend.app.ai.research.monitor import ObservationMonitor

def test_backup_and_restore(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    
    backups = tmp_path / "backups"
    restore_target = tmp_path / "restore"
    
    # Create valid ledger
    ledger = registry / "prospective_ledger.jsonl"
    with open(ledger, "w") as f:
        f.write(json.dumps({
            "prediction_id": "1", "model_version": "1.0.0", "_idempotency_key": "k1",
            "prediction_timestamp": "2022-01-01T00:00:00+00:00"
        }) + "\n")
        
    tool = BackupTool(registry_dir=str(registry))
    tar_path = tool.create_backup(str(backups))
    
    assert os.path.exists(tar_path)
    
    # Restore
    res = tool.restore_backup(tar_path, str(restore_target))
    assert res is True
    
    restored_ledger = restore_target / "prospective_ledger.jsonl"
    assert os.path.exists(restored_ledger)
    with open(restored_ledger, "r") as f:
        data = json.loads(f.readline())
        assert data["model_version"] == "1.0.0"

def test_corruption_hash_mismatch(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    backups = tmp_path / "backups"
    restore_target = tmp_path / "restore"
    
    ledger = registry / "prospective_ledger.jsonl"
    with open(ledger, "w") as f:
        f.write('{"id": 1}\n')
        
    tool = BackupTool(registry_dir=str(registry))
    tar_path = tool.create_backup(str(backups))
    
    # Intentionally corrupt the tar
    temp_extract = tmp_path / "temp_extract"
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=str(temp_extract))
        
    # Corrupt the ledger
    with open(temp_extract / "prospective_ledger.jsonl", "a") as f:
        f.write('{"id": 2}\n')
        
    corrupted_tar = str(backups / "corrupted.tar.gz")
    with tarfile.open(corrupted_tar, "w:gz") as tar:
        for root, _, files in os.walk(temp_extract):
            for file in files:
                tar.add(os.path.join(root, file), arcname=file)
                
    with pytest.raises(BackupError, match="Hash mismatch"):
        tool.restore_backup(corrupted_tar, str(restore_target))

def test_corruption_jsonl_truncate(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    backups = tmp_path / "backups"
    restore_target = tmp_path / "restore"
    
    ledger = registry / "prospective_ledger.jsonl"
    with open(ledger, "w") as f:
        f.write('{"id": 1}\n')
        
    tool = BackupTool(registry_dir=str(registry))
    
    # Corrupt original BEFORE backup hash (makes the hash valid for the broken string)
    # Wait, the tool requires valid JSONL on restore.
    # We will write invalid JSON.
    with open(ledger, "w") as f:
        f.write('{"id": 1, "missing_brace": \n')
        
    tar_path = tool.create_backup(str(backups))
    
    with pytest.raises(BackupError, match="Corrupted JSONL record"):
        tool.restore_backup(tar_path, str(restore_target))

def test_restart_idempotency(tmp_path):
    registry = tmp_path / "registry"
    registry.mkdir()
    
    ledger = registry / "prospective_ledger.jsonl"
    outcomes = registry / "prospective_outcomes.jsonl"
    flag = registry / "phase9_review_flag.txt"
    
    with open(ledger, "w") as f:
        for i in range(100):
            f.write(json.dumps({
                "prediction_id": str(i), "model_version": "1.0.0", "_idempotency_key": str(i),
                "prediction_timestamp": "2022-01-01T00:00:00+00:00"
            }) + "\n")
    with open(outcomes, "w") as f:
        for i in range(100):
            f.write(json.dumps({
                "prediction_id": str(i), "evaluation_status": "EVALUATED",
                "outcome_timestamp": "2022-01-08T00:00:00+00:00"
            }) + "\n")
            
    monitor = ObservationMonitor(ledger_path=str(ledger), outcomes_path=str(outcomes), flag_path=str(flag))
    status = monitor.get_status()
    
    assert status['evaluated'] == 100
    assert os.path.exists(str(flag))
    
    # Run again, flag shouldn't crash or duplicate things
    status2 = monitor.get_status()
    assert status2['evaluated'] == 100
