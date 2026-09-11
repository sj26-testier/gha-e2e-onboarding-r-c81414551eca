"""Executed on hosted native checkout; no credentials are printed or persisted."""
import hashlib
import json
import os
from pathlib import Path
import subprocess

event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
result = {
    'context': json.loads(os.environ['DELETE_CONTEXT']),
    'checkout': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
    'fixture': Path('delete-fixture.txt').read_text().strip(),
    'workflow_marker': os.environ['DELETE_WORKFLOW_MARKER'],
    'token_present': bool(os.environ.get('GITHUB_TOKEN')),
    'event_file': {
        'sha256': hashlib.sha256(json.dumps(event, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
        'action_present': 'action' in event,
        'repository': event.get('repository', {}).get('full_name'),
        'ref': event.get('ref'), 'ref_type': event.get('ref_type'),
    },
}
print('DELETE_' + 'E2E_RESULT=' + json.dumps(result, sort_keys=True), flush=True)
