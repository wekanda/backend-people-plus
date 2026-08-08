import shutil
from pathlib import Path

root = Path(__file__).resolve().parents[1]
removed = []
for p in root.rglob('__pycache__'):
    try:
        shutil.rmtree(p)
        removed.append(str(p))
    except Exception as e:
        print('could not remove', p, e)
for f in root.rglob('*.pyc'):
    try:
        f.unlink()
        removed.append(str(f))
    except Exception as e:
        print('could not remove', f, e)
print('removed_count', len(removed))
for r in removed:
    print(r)
