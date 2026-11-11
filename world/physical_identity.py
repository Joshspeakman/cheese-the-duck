"""Save-stable identities for physical belongings, independent of their location."""
import json
from uuid import uuid4, uuid5, NAMESPACE_URL


def new_identity():
    return uuid4().hex


def saved_identity(data, scope, index=0):
    value = data.get('instance_id')
    if isinstance(value, str) and value and len(value) <= 128:
        return value
    # Loading an old save twice must produce exactly the same migration.
    payload = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return uuid5(NAMESPACE_URL, 'cheese:' + scope + ':' + str(index) + ':' + payload).hex
