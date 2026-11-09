"""대사 문체 수정 후 검사: python3 script/check_style.py script/partN/epXX.md [...]
- 턴 수·번호·화자가 git HEAD 버전과 같은지
- 장면 표시(【場面…】) 개수가 같은지
- 대사 안 괄호 여부
- 턴당 「……」·「、」 밀도
"""
import re, subprocess, sys, os

TURN = re.compile(r'^(\d{3}) ([^：]+)：(.*)$')

def turns(text):
    return [TURN.match(l).groups() for l in text.splitlines() if TURN.match(l)]

def scenes(text):
    return sum(1 for l in text.splitlines() if l.startswith('【'))

ok_all = True
root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
for path in sys.argv[1:]:
    new = open(path, encoding='utf-8').read()
    rel = os.path.relpath(os.path.abspath(path), root)
    old = subprocess.run(['git', 'show', f'HEAD:{rel}'], capture_output=True, text=True, cwd=root).stdout
    nt, ot = turns(new), turns(old)
    errs = []
    if len(nt) != 180: errs.append(f'turns={len(nt)}')
    if [t[0] for t in nt] != [f'{i:03d}' for i in range(1, len(nt) + 1)]: errs.append('numbering')
    if ot and [t[1] for t in nt] != [t[1] for t in ot]:
        diff = [(a[0], b[1], a[1]) for a, b in zip(nt, ot) if a[1] != b[1]][:5]
        errs.append(f'speakers changed {diff}')
    if ot and scenes(new) != scenes(old): errs.append(f'scenes {scenes(old)}->{scenes(new)}')
    paren = [t[0] for t in nt if re.search(r'[（(]', t[2])]
    if paren: errs.append(f'parens in {paren[:5]}')
    body = ''.join(t[2] for t in nt)
    n = max(len(nt), 1)
    dots, commas = body.count('……') / n, body.count('、') / n
    flag = '' if dots <= 0.6 and commas <= 3.0 else '  <- density high'
    status = 'OK ' if not errs else 'ERR'
    if errs: ok_all = False
    print(f'{status} {rel}  dots/turn={dots:.2f} commas/turn={commas:.2f}{flag}  {"; ".join(errs)}')
sys.exit(0 if ok_all else 1)
