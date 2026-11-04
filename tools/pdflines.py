"""Body lines and footnotes of a text-layer PDF (pymupdf), by font size and the superscript flag. Shared by the
Bosnian entity builders."""
import re
import pymupdf


def read(path, body_min=10.6, skip_pages=()):
    d = pymupdf.open(path)
    body, notes = [], []
    for pno, page in enumerate(d):
        if pno in skip_pages:
            continue
        plines = []
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                bt, nt = '', ''
                for s in l['spans']:
                    sup = bool(s['flags'] & 1)
                    if s['size'] >= body_min and not sup:
                        bt += s['text']
                    elif s['size'] < body_min and not sup:
                        nt += s['text']
                    elif sup and s['size'] < body_min and nt == '' and bt == '' :
                        nt += '[' + s['text'].strip() + ']'
                    # superscript markers inside body text are dropped
                plines.append((bt, nt))
        # page number: last non-empty body line that is only digits
        for i in range(len(plines) - 1, -1, -1):
            if plines[i][0].strip():
                if re.fullmatch(r'\s*\d{1,3}\s*', plines[i][0]):
                    plines[i] = ('', plines[i][1])
                break
        for bt, nt in plines:
            if bt.strip():
                body.append(bt)
            if nt.strip():
                notes.append(nt)
    return body, notes
