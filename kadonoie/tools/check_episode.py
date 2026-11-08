"""Check a 角の家 episode: 120 JP turns, 120 KR turns, consistent speaker mapping."""
import re, sys

def section(text, start, end=None):
    s = text.index(start)
    e = text.index(end, s) if end else len(text)
    return text[s:e]

ok = True
for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    jp = section(t, "## 본문", "## 낭독 포인트")
    kr = section(t, "## 한글 해석")
    jl = [m.group(1) for m in re.finditer(r"^([^\s：【#|>\-]{1,12})：\S", jp, re.M)]
    kl = [m.group(1) for m in re.finditer(r"^([^\s:\[#|>\-][^:\n]{0,11}): \S", kr, re.M)]
    js = len(re.findall(r"^【場面：", jp, re.M)); ks = len(re.findall(r"^\[장면: ", kr, re.M))
    msg = []
    if len(jl) != 120: msg.append(f"JP turns {len(jl)}")
    if len(kl) != 120: msg.append(f"KR turns {len(kl)}")
    if js != ks: msg.append(f"scenes JP {js} KR {ks}")
    m = {}
    for i, (a, b) in enumerate(zip(jl, kl), 1):
        if m.setdefault(a, b) != b:
            msg.append(f"speaker mismatch at turn {i}: {a}->{b} (was {m[a]})"); break
    print(path, "OK" if not msg else "FAIL: " + "; ".join(msg), "| speakers:", m)
    ok = ok and not msg
sys.exit(0 if ok else 1)
