"""Validation and merge helpers for JKMVS press releases (standard library only).

Used by build_press.py and by the tests. No Firebase code lives here.
"""
import datetime
import json
import re
from urllib.parse import urlparse

SLUG_RE = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


class ExportError(Exception):
    """The export file is unreadable or has an unusable shape."""


def valid_date(s):
    """Strict YYYY-MM-DD. Returns the string or None."""
    if not isinstance(s, str):
        return None
    s = s.strip()[:10]
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', s):
        return None
    try:
        datetime.date.fromisoformat(s)
    except ValueError:
        return None
    return s


def norm_slug(s):
    if not isinstance(s, str):
        return None
    s = s.strip().lower()
    return s if SLUG_RE.match(s) else None


def valid_https(u):
    if not isinstance(u, str) or not u.strip():
        return None
    p = urlparse(u.strip())
    if p.scheme != 'https' or not p.netloc or any(c in u for c in '"<> \n\r\t'):
        return None
    return u.strip()


def _s(v):
    return v.strip() if isinstance(v, str) else ''


def normalise(rec, org, report):
    """Return a cleaned *published-ready* record, or None (reason is appended to report)."""
    if not isinstance(rec, dict):
        report.append('skipped: record is not an object')
        return None
    raw_slug = rec.get('slug') or rec.get('id')
    slug = norm_slug(raw_slug)
    label = str(raw_slug)[:60]
    if not slug:
        report.append(f'skipped "{label}": missing or invalid slug (use a-z, 0-9, hyphen)')
        return None
    title = _s(rec.get('title'))
    content = _s(rec.get('content')).replace('\r\n', '\n').replace('\r', '\n')
    category = _s(rec.get('category'))
    date = valid_date(rec.get('date'))
    for name, val in (('title', title), ('content', content), ('category', category), ('date', date)):
        if not val:
            report.append(f'skipped "{slug}": missing or invalid {name}')
            return None
    out = dict(rec)
    out.pop('id', None)
    out['slug'] = slug
    out['title'] = title
    out['content'] = content
    out['category'] = category
    out['date'] = date
    out['status'] = 'published'
    excerpt = _s(rec.get('excerpt'))
    if not excerpt:
        flat = ' '.join(content.split())
        excerpt = flat[:157].rstrip() + ('…' if len(flat) > 157 else '')
        report.append(f'note "{slug}": excerpt derived from content')
    out['excerpt'] = excerpt
    mod = valid_date(rec.get('modified'))
    if rec.get('modified') and not mod:
        report.append(f'note "{slug}": invalid modified date ignored')
    out['modified'] = mod if mod and mod >= date else date
    img = valid_https(rec.get('featuredImage'))
    if rec.get('featuredImage') and not img:
        report.append(f'note "{slug}": featuredImage is not a valid https URL; fallback logo used')
    out['featuredImage'] = img or ''
    pdf = valid_https(rec.get('pdfUrl'))
    out['pdfUrl'] = pdf or ''
    out['author'] = _s(rec.get('author')) or org
    tags = rec.get('tags')
    out['tags'] = [str(t).strip() for t in tags if str(t).strip()] if isinstance(tags, list) else []
    hl = rec.get('highlights')
    out['highlights'] = [str(t).strip() for t in hl if str(t).strip()] if isinstance(hl, list) else []
    qs = []
    for q in rec.get('quotes') if isinstance(rec.get('quotes'), list) else []:
        if isinstance(q, dict) and _s(q.get('text')):
            qs.append({'text': _s(q.get('text')), 'by': _s(q.get('by'))})
    out['quotes'] = qs
    for k in ('location', 'referenceNumber', 'seoTitle', 'seoDescription'):
        out[k] = _s(rec.get(k))
    sd = out.get('schemaType')
    out['schemaType'] = sd if sd in ('NewsArticle', 'Article') else 'Article'
    return out


def load_export(path):
    """Read an export file: a list, or {"releases": [...]}. Raises ExportError."""
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise ExportError(f'cannot read export {path}: {e}')
    if isinstance(data, dict):
        data = data.get('releases')
    if not isinstance(data, list):
        raise ExportError('export must be a list or {"releases": [...]}')
    return data


def merge(base, export, org, report):
    """Merge committed archive `base` with `export` (Firestore snapshot).

    - export record with status 'published' replaces the base record of the same slug (updates win)
    - export record with any other status removes that slug (unpublished / draft / review)
    - invalid published export record: previous version is kept and the problem is reported
    - duplicate slugs inside the export: the later one wins and a note is reported
    Returns a deterministic list (date desc, slug asc).
    """
    cur = {}
    for rec in base:
        if isinstance(rec, dict) and rec.get('status') == 'published':
            n = normalise(rec, org, report)
            if n:
                cur[n['slug']] = n
    seen = set()
    for rec in export:
        if not isinstance(rec, dict):
            report.append('skipped: export record is not an object')
            continue
        slug = norm_slug(rec.get('slug') or rec.get('id'))
        if slug and slug in seen:
            report.append(f'note "{slug}": duplicate slug in export, later record wins')
        if slug:
            seen.add(slug)
        if rec.get('status') != 'published':
            if slug:
                cur.pop(slug, None)
            continue
        n = normalise(rec, org, report)
        if n:
            cur[n['slug']] = n
    return sorted(cur.values(), key=lambda r: (-int(r['date'].replace('-', '')), r['slug']))
