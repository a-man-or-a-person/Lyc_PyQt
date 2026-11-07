import os
import tempfile
from pathlib import Path

_data = tempfile.TemporaryDirectory()
os.environ['EXPENSE_DB_PATH'] = str(Path(_data.name) / 'test.db')
os.environ['QT_QPA_PLATFORM'] = 'offscreen'
