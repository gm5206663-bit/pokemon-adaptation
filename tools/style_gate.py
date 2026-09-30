#!/usr/bin/env python3
"""style_gate.py - the gate for the Bagon serial.

Stdlib only. Run:  python3 tools/style_gate.py chapters/Chapter_01_*.md
Self-test:        python3 tools/style_gate.py --selftest

Every check maps to a rail in foundation/RAILS.md. A check that cannot fail on a
bad input is not a check, which is why --selftest injects a defect for each one.
"""
import re
import sys
import unicodedata

BAND_MIN, BAND_MAX = 2400, 3400          # k01
AVG_MIN, AVG_MAX = 14, 18                # k01
SENTENCE_MAX = 60                        # k01
THE_WAY_MAX = 0                          # k01
BARE_MAX = 0                             # k01

# k02 - no count-numbers in prose
DIGIT = re.compile(r'\d')

# gate 1, borrowed from the Control Centre validator
CJK = re.compile(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]')

# k10 / POWER_LAW - no System vocabulary, even as metaphor
SYSTEM_WORDS = [
    r'\bsystem\b', r'\bmenu\b', r'\bscreen\b', r'\bstatus bar\b', r'\blevel up\b',
    r'\bleveling up\b', r'\bpercentage\b', r'\bpercent\b', r'\bgauge\b',
    r'\bstat sheet\b', r'\binterface\b', r'\bprogress bar\b', r'\bHUD\b',
]

# k13, and the struck names
BANNED_TOKENS = [
    'Hoenn', 'Storm-Vault Drake', 'Sky-Breaker Sovereign', 'Aether-Crown Wyrm',
    'Cliff-Breaker', 'Boulder-Cleaver', 'Sky-Sunder', 'Heaven-Cleaver',
    'Hunter\'s Eye', 'Battle Sense', 'War Mind',
]

# k05/k06 - no panels
PANEL = re.compile(r'^\s*[-|].*\b\d+\s*%')

NGRAM = 12                               # canon-copy gate


def strip_md(text):
    """Drop headings, blockquotes, tables and fences so only prose is measured."""
    out = []
    in_fence = False
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if s.startswith(('#', '>', '|')) or s.startswith('---'):
            continue
        out.append(line)
    return '\n'.join(out)


def sentences(prose):
    """Split into sentences. Dialogue keeps its own punctuation."""
    prose = re.sub(r'\s+', ' ', prose)
    parts = re.split(r'(?<=[.!?])\s+', prose)
    return [p for p in (x.strip(' "\'') for x in parts) if p]


def words(s):
    return re.findall(r"[A-Za-z']+", s)


def ngrams(ws, n=NGRAM):
    return {' '.join(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def check(text, canon_text=None, name='chapter', skip=()):
    """Return (errors, warnings, stats).

    ``skip`` disables named check groups so the selftest can isolate one rule.
    It exists for tests only - no chapter is ever gated with skip set.
    Valid groups: 'metrics' (band, average, sentence length, house-words).
    """
    errs, warns = [], []
    prose = strip_md(text)
    ss = sentences(prose)
    wc = [len(words(s)) for s in ss]
    total = sum(wc)
    avg = (total / len(ss)) if ss else 0.0
    over = [w for w in wc if w > SENTENCE_MAX]

    theway = len(re.findall(r'\bthe way\b', prose, re.I))
    bare = len(re.findall(r'\bbare\b', prose, re.I))

    if 'metrics' not in skip:
        if total < BAND_MIN:
            errs.append(f'word count {total} is under the band {BAND_MIN}-{BAND_MAX} (k01)')
        if total > BAND_MAX:
            errs.append(f'word count {total} is over the band {BAND_MIN}-{BAND_MAX} (k01)')
        if ss and not (AVG_MIN <= avg <= AVG_MAX):
            errs.append(f'sentence average {avg:.2f} is outside {AVG_MIN}-{AVG_MAX} (k01)')
        if over:
            errs.append(f'{len(over)} sentence(s) over {SENTENCE_MAX} words, longest {max(over)} (k01)')
        if theway > THE_WAY_MAX:
            errs.append(f'"the way" appears {theway}x, limit {THE_WAY_MAX} (k01)')
        if bare > BARE_MAX:
            errs.append(f'"bare" appears {bare}x, limit {BARE_MAX} (k01)')

    digs = DIGIT.findall(prose)
    if digs:
        i = DIGIT.search(prose).start()
        errs.append(f'{len(digs)} digit(s) in prose, first near: ...{prose[max(0,i-40):i+20]!r}... (k02)')

    m = CJK.search(text)
    if m:
        errs.append(f'CJK/kana/hangul {m.group()!r} (gate 1 - never ships)')

    for pat in SYSTEM_WORDS:
        hit = re.search(pat, prose, re.I)
        if hit:
            errs.append(f'System vocabulary {hit.group()!r} (k10 - no System in this serial)')

    for tok in BANNED_TOKENS:
        if tok.lower() in prose.lower():
            errs.append(f'banned token {tok!r} (k13 / struck names)')

    # NOTE: this runs on the RAW text on purpose. strip_md() removes table rows,
    # so a panel-shaped row would be stripped before this check ever saw it.
    for ln, line in enumerate(text.split('\n'), 1):
        if PANEL.match(line):
            errs.append(f'panel-shaped line {ln}: {line.strip()[:60]!r} (k06)')
            break

    if canon_text:
        a = ngrams(words(prose))
        b = ngrams(words(strip_md(canon_text)))
        shared = a & b
        if shared:
            sample = sorted(shared)[0]
            errs.append(f'{len(shared)} {NGRAM}-gram run(s) shared with canon ore, e.g. {sample!r} (V3)')

    stats = {'words': total, 'sentences': len(ss), 'avg': round(avg, 1),
             'longest': max(wc) if wc else 0, 'over60': len(over),
             'the-way': theway, 'bare': bare, 'digits': len(digs)}
    return errs, warns, stats


# --------------------------------------------------------------------------- #
# selftest - every check gets a bad case and a good case
# --------------------------------------------------------------------------- #

def _good_body(n_words=2600):
    """Prose that passes every check.

    Sentences average fifteen words, which sits inside the 14-18 band. The first
    version of this fixture averaged 7.6 and the gate correctly rejected it -
    which is the gate working, and the reason the selftest exists.
    """
    unit = (
        'The rock was cold and the dust came off its brow in a thin grey fall. '   # 16
        'It hit the stone again and nothing gave, so it hit the stone again. '     # 14
        'Far below the ridge something moved and stopped and did not come closer. '# 14
        'The air smelled of wet stone and old leaf and nothing ever kind. '        # 14
    )
    body = ''
    while len(words(body)) < n_words:
        body += unit
    return body


def selftest():
    good = _good_body()
    cases = []

    def case(label, text, must_fail, canon=None, expect=None, skip=()):
        errs, _, _ = check(text, canon_text=canon, skip=skip)
        if must_fail and expect is not None:
            # the case must fail FOR THE RIGHT REASON, not incidentally
            ok = any(expect in e for e in errs)
            cases.append((ok, label, errs[:2]))
        else:
            ok = bool(errs) == must_fail
            cases.append((ok, label, errs[:2]))

    case('clean prose passes', good, False)
    case('under the band is caught', _good_body(900), True, expect='under the band')
    case('over the band is caught', _good_body(4200), True, expect='over the band')
    case('a sentence over sixty words is caught',
         good + ' ' + ('and '.join(['word'] * 70)) + '.', True,
         expect='over 60 words')
    case('"the way" is caught', good + ' That was the way of it. ' * 4, True,
         expect='the way')
    case('"bare" is caught', good + ' The stone was bare.', True, expect='bare')
    case('a digit in prose is caught', good + ' It was 40 percent done.', True,
         expect='digit')
    case('a count-number alone is caught', good + ' There were 12 of them.', True,
         expect='digit')
    case('CJK is caught', good + ' \u68a6\u60f3', True, expect='CJK')
    case('kana is caught', good + ' \u30e6\u30a1\u30e1', True, expect='CJK')
    for w in ['system', 'menu', 'screen', 'level up', 'gauge', 'interface']:
        case(f'System word {w!r} is caught', good + f' The {w} opened.', True,
             expect='System vocabulary')
    for t in ['Hoenn', 'Storm-Vault Drake', 'Cliff-Breaker']:
        case(f'banned token {t!r} is caught', good + f' It came from {t}.', True,
             expect='banned token')
    case('a panel line is caught', good + '\n\n| Hard Head | 40% | open |\n', True,
         expect='panel-shaped')

    # canon-copy gate
    ore = 'The boy overslept on the morning he was due to receive his first creature.'
    case('a 12-gram run shared with ore is caught',
         good + ' ' + ore, True, canon=ore, expect='shared with canon ore',
         skip=('metrics',))
    # Isolated: the copy gate is tested on its own, so the word band cannot
    # make this case fail for a reason it was not written to test.
    case('a rewritten beat passes the copy gate',
         good + ' Someone in the town below had slept too long that morning.',
         False, canon=ore, skip=('metrics',))

    # markdown must not be measured as prose
    case('a digit inside a heading is not a prose digit',
         '# Notes 2026\n\n' + good, False)
    case('a table row with digits is not prose',
         good + '\n\n| a | 12 |\n|---|---|\n| b | 30 |\n', False)

    passed = sum(1 for ok, _, _ in cases if ok)
    print('STYLE GATE SELFTEST')
    print('-' * 60)
    for ok, label, err in cases:
        print(f'  {"ok  " if ok else "FAIL"} {label}' + ('' if ok else f'  -> {err}'))
    print('-' * 60)
    print(f'  {passed}/{len(cases)} checks passed')
    return 0 if passed == len(cases) else 1


def main(argv):
    if '--selftest' in argv:
        return selftest()
    paths = [a for a in argv[1:] if not a.startswith('--')]
    if not paths:
        print(__doc__)
        return 2
    canon = None
    try:
        canon = open('canon_extract/IL001.txt', encoding='utf-8').read()
    except OSError:
        pass
    rc = 0
    for p in paths:
        text = open(p, encoding='utf-8').read()
        errs, warns, st = check(text, canon_text=canon, name=p)
        print(f'=== {p} ===')
        print('  ' + '  '.join(f'{k}={v}' for k, v in st.items()))
        for e in errs:
            print(f'  FAIL  {e}')
        for w in warns:
            print(f'  warn  {w}')
        print(f'  {"FAIL" if errs else "PASS"}')
        if errs:
            rc = 1
    return rc


if __name__ == '__main__':
    sys.exit(main(sys.argv))
