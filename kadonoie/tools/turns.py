"""List or drop turns (by 1-based index) from both JP body and KR translation.
usage: turns.py FILE list | turns.py FILE drop 3 17 40"""
import re, sys
path, cmd, *nums = sys.argv[1:]
lines = open(path, encoding="utf-8").read().split("\n")
def idx(start, end, pat):
    s = lines.index(start); e = lines.index(end) if end else len(lines)
    return [i for i in range(s, e) if re.match(pat, lines[i])]
jp = idx("## 본문", "## 낭독 포인트", r"^[^\s：【#|>\-]{1,12}：\S")
kr = idx("## 한글 해석", None, r"^[^\s:\[#|>\-][^:\n]{0,11}: \S")
if cmd == "list":
    for n, (a, b) in enumerate(zip(jp, kr), 1):
        print(n, lines[a][:40], "|", lines[b][:30])
else:
    drop = {jp[int(n)-1] for n in nums} | {kr[int(n)-1] for n in nums}
    open(path, "w", encoding="utf-8").write("\n".join(l for i, l in enumerate(lines) if i not in drop))
    print("dropped", nums)
