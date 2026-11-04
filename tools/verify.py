"""Independent check of a corpus.d part against the cached pages: the standard library's HTMLParser (not the
parser's regexes) reads each page's text; every paragraph's letters and digits must occur in it, in order; the
letters and digits the page holds between the law's first and last paragraph and not in ours are counted. Private."""
import hashlib, json, sys
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(HERE.parent / 'world-law'))
import ba_lib  # noqa: E402
import lawpage  # noqa: E402


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style') and self.skip:
            self.skip -= 1

    def handle_data(self, d):
        if not self.skip:
            self.out.append(d)


def main(part):
    c = json.loads((HERE / 'corpus.d' / part).read_text(encoding='utf-8'))
    bad = 0
    for a in c['acts']:
        v = a['versions'][0]
        p = HERE / '.cache' / 'by-url' / hashlib.sha256(v['source_url'].encode()).hexdigest()
        assert ba_lib.sha256(p) == v['sha256']
        t = Text()
        t.feed(lawpage.decode(p.read_bytes()))
        src = ' '.join(t.out)
        paras = [l for u in v['units'].values() for l in u['text'].splitlines()]
        missing, ours, _ = ba_lib.check_present(paras, src)
        inorder, _, _ = ba_lib.check_in_order(paras, src)
        s = ba_lib.letters_digits(src)
        first, last = ba_lib.letters_digits(paras[0]), ba_lib.letters_digits(paras[-1])
        i, j = s.find(first), s.rfind(last)
        span = (j + len(last) - i) if i >= 0 and j >= 0 else -1
        exact = i >= 0 and s[i:j + len(last)] == ''.join(ba_lib.letters_digits(x) for x in paras)
        ok = not missing and exact
        bad += not ok
        print('OK  ' if ok else 'FAIL', a['slug'][:45], f'present {len(paras) - len(missing)}/{len(paras)}, in order {inorder}, ours {ours}, page span {span}, exact {exact}')
        for m in missing[:3]:
            print('      ', m[:150])
    print('acts failing:', bad)


if __name__ == '__main__':
    main(sys.argv[1])
