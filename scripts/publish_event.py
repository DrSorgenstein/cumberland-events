"""Validate an approved issue and add or update its public event record."""
import datetime as dt
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parents[1]
issue = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())['issue']
body = issue.get('body') or ''
fields = dict(re.findall(r'^### (.+?)\s*\n\s*(.*?)(?=\n### |\Z)', body, re.M | re.S))
fields = {key: val.strip() for key, val in fields.items()}
labels = {'Event title': 'title', 'Category': 'category', 'Start (Eastern Time)': 'start', 'End (Eastern Time)': 'end', 'Town': 'town', 'Venue or public location': 'venue', 'Description': 'description', 'Public event URL': 'url'}
event = {'id': str(issue['number'])}
for label, key in labels.items():
    value = fields.get(label, '')
    if not value or value == '_No response_' or len(value) > (1200 if key == 'description' else 160):
        raise ValueError(f'Invalid {label}: missing or too long')
    event[key] = value
for key in ('start', 'end'):
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}', event[key]):
        raise ValueError(f'{key} must use YYYY-MM-DDTHH:MM')
start, end = [dt.datetime.strptime(event[key], '%Y-%m-%dT%H:%M') for key in ('start', 'end')]
if end <= start or end-start > dt.timedelta(days=7):
    raise ValueError('End must be after start and within seven days')
if start.date() < dt.datetime.now(dt.timezone.utc).date() - dt.timedelta(days=1):
    raise ValueError('Past events cannot be approved as new submissions')
parsed = urlparse(event['url'])
if parsed.scheme != 'https' or not parsed.netloc or parsed.username or parsed.password:
    raise ValueError('Event URL must be a public HTTPS URL')
if event['category'] not in {'Arts & Music','Community','Education','Family','Food','Government','Outdoors','Sports','Other'}:
    raise ValueError('Unknown category')
path = root / 'data/events.json'
events = json.loads(path.read_text())
events = [e for e in events if e['id'] != event['id']]
events.append(event)
events.sort(key=lambda e: e['start'])
path.write_text(json.dumps(events, indent=2, ensure_ascii=False) + '\n')
print(f'Published event #{event["id"]}')
