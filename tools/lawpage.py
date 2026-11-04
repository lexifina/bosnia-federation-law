"""One FBiH Government law page (fbihvlada.gov.ba) -> units. Private.

The page gives the text as published in Sluzbene novine FBiH: the President's decree (ukaz) promulgating the law,
then the law, then the signatures. Units: ukaz, clan-NNN (article headings, chapter headings before them), potpis.
"""
import datetime as dt
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'world-law'))
import ba_lib  # noqa: E402

BLOCK = re.compile(r'(?i)</(p|div|li|h\d|tr|table|ul|ol)>|<br\b[^>]*>|<(p|div|li|h\d|tr)\b[^>]*>')
ART = re.compile(r'^(Član|Članak)\s+(\d+)\s*\.?\s*([a-z]?)\s*\.?\s*(\(.*\))?\s*$')
ART_INLINE = re.compile(r'^(Član|Članak)\s+(\d+)\s*([a-z]?)\s*\.\s*(\S.*)$')
SIGN = re.compile(r'(?i)^(predsjedavaj|predsjednik|predsjednica|potpredsjednik)')
ORD = {'prvog': 1, 'drugog': 2, 'trećeg': 3, 'petog': 5, 'osmog': 8, 'desetog': 10, 'petnaestog': 15,
       'tridesetog': 30, 'narednog': 1, 'sljedećeg': 1, 'slijedećeg': 1, 'idućeg': 1}


def decode(raw: bytes) -> str:
    """New pages are UTF-8; the old Word-exported pages declare windows-1250."""
    head = raw[:2000].lower()
    if b'windows-1250' in head:
        return raw.decode('cp1250', errors='replace')
    return raw.decode('utf-8', errors='replace')


def region(page_html):
    i = page_html.find('content-article')
    if i >= 0:
        j = page_html.find('Aktuelno', i)
        return page_html[page_html.find('>', i) + 1:j] if j > 0 else None
    b = re.search(r'(?is)<body[^>]*>(.*)</body>', page_html)  # old Word-exported page: the whole body
    return b.group(1) if b else None


def lines_of(page_html):
    r = region(page_html)
    if r is None:
        return None
    r = re.sub(r'(?s)<script.*?</script>|<style.*?</style>', '', r)
    if 'content-article' not in page_html:
        r = re.sub(r'\s+', ' ', r)  # old Word-exported page: raw newlines are soft wraps
    r = BLOCK.sub('\n', r)
    r = html.unescape(re.sub(r'<[^>]+>', '', r))
    out = [ba_lib.clean(l) for l in r.split('\n')]
    # the region ends inside the sidebar heading: drop trailing layout lines
    return [l for l in out if l]


def units_of(lines):
    """-> (units dict, in_force_days or None, title)"""
    # the law starts at the line 'ZAKON' (or 'ZAKON O ...') after the decree
    z = next((i for i, l in enumerate(lines) if re.match(r'^ZAKON\b', l) and i > 0), None)
    if z is None:
        z = next((i for i, l in enumerate(lines) if re.match(r'^ZAKON\b', l)), None)
    if z is None:
        return None, None, None
    units, labels = {}, {}
    if z > 0:
        units['ukaz'] = lines[:z]
        labels['ukaz'] = 'Ukaz o proglašenju'
    key, cur, pending = 'naslov', [], []
    labels['naslov'] = 'Naslov'
    sign_at = None
    for i in range(z, len(lines)):
        l = lines[i]
        m = ART.match(l) or ART_INLINE.match(l)
        if m:
            units[key] = cur
            n, suf = int(m.group(2)), m.group(3) or ''
            key = ba_lib.art_key(n, suf)
            if key in units:
                return None, None, None  # a duplicate number: not a simple law page
            labels[key] = f'Član {n}{suf}.'
            cur = pending + [l]
            pending = []
            continue
        if SIGN.match(l) and key != 'naslov':
            sign_at = i
            break
        if re.match(r'^(GLAVA|POGLAVLJE|DIO)\b', l) or (l.isupper() and len(l) > 3 and key != 'naslov' and not re.match(r'^[IVX]+\.?$', l)):
            pending.append(l)
            continue
        if pending:  # a heading inside an article stays where it stands
            cur += pending
            pending = []
        cur.append(l)
    units[key] = cur + pending
    if sign_at is not None:
        units['potpis'] = lines[sign_at:]
        labels['potpis'] = 'Potpisi'
    title = ' '.join(units.get('naslov', [])[:2])
    # in force: the article saying 'stupa na snagu'
    days = None
    for k in reversed([k for k in units if k.startswith('clan-')]):
        t = ' '.join(units[k])
        mm = re.search(r'stupa na snagu\s+(\w+)\s+dana\s+od\s+dana\s+(?:njegovog\s+|njegove\s+)?objav', t)
        w = re.sub(r'oga$', 'og', mm.group(1).lower()) if mm else ''
        if mm and w in ORD:
            days = ORD[w]
        elif re.search(r'stupa na snagu\s+(?:danom|na dan)\s+(?:njegovog\s+)?objav', t):
            days = 0
        if 'stupa na snagu' in t:
            if re.search(r'primjenjiva|primjenjuje se od|prestaje da važi|prestaje važiti', t):
                pass
            break
    out = {}
    for k, ls in units.items():
        if not ls:
            continue
        kind = 'art' if k.startswith('clan-') else ('note' if k in ('ukaz', 'potpis') else 'heading')
        out[k] = {'label': labels[k], 'kind': kind, 'text': '\n'.join(ls) + '\n'}
    return out, days, title


def in_force(published: str, days: int) -> str:
    return (dt.date.fromisoformat(published) + dt.timedelta(days=days)).isoformat()
