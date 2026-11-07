#!/usr/bin/env python3
"""Server-side export of the Firestore `press_releases` collection to a JSON file.

Credentials come ONLY from the environment variable FIREBASE_SERVICE_ACCOUNT
(the JSON text of a service account; store it as a GitHub Actions secret).
Nothing is printed except counts. The key is never written to disk.

Privacy: for documents that are not published only {slug, status} is exported,
so draft/review text can never reach the repository.

Exit codes: 0 ok, 1 failure (no output file is written on failure).
Requires: pip install firebase-admin
"""
import json
import os
import sys


def main(out):
    raw = os.environ.get('FIREBASE_SERVICE_ACCOUNT', '').strip()
    if not raw:
        print('FIREBASE_SERVICE_ACCOUNT is not set', file=sys.stderr)
        return 1
    try:
        info = json.loads(raw)
        import firebase_admin
        from firebase_admin import credentials, firestore
        firebase_admin.initialize_app(credentials.Certificate(info))
        docs = list(firestore.client().collection('press_releases').stream())
    except Exception as e:  # never echo secrets: report the error class only
        print(f'Firestore export failed ({type(e).__name__})', file=sys.stderr)
        return 1
    rels = []
    for d in docs:
        data = d.to_dict() or {}
        slug = data.get('slug') or d.id
        if data.get('status') != 'published':
            rels.append({'slug': slug, 'status': data.get('status', '')})
            continue
        rec = {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in data.items()}
        rec['slug'] = slug
        rels.append(rec)
    if not any(r.get('status') == 'published' for r in rels):
        print('export contains no published releases; refusing to write', file=sys.stderr)
        return 1
    tmp = out + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'releases': rels}, f, ensure_ascii=False, indent=1)
    os.replace(tmp, out)
    print(f'exported {len(rels)} documents')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'press-releases-export.json'))
