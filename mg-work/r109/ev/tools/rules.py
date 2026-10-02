# -*- coding: utf-8 -*-
import io, sys, re
def load(p):
    return io.open(p, encoding='utf-8', newline='').read().replace('\r\n', '\n')
def rules(p, kw, pad=0):
    """print every {...} block whose selector (or preceding comment tail) mentions kw"""
    s = load(p)
    n = 0
    for m in re.finditer(r'\{', s):
        # find matching close
        i = m.start()
        depth = 0
        j = i
        while j < len(s):
            if s[j] == '{':
                depth += 1
            elif s[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        blk = s[i:j+1]
        # selector = text between previous '}' or ';' and this '{'
        k = s.rfind('}', 0, i)
        k2 = s.rfind('\n\n', 0, i)
        head = s[max(0, k+1, k2-pad):i]
        if kw in head or kw in blk[:400]:
            n += 1
            print('@@ #%d  %s' % (n, head.strip()[-400:]))
            print(blk[:1400])
            print('-----')
    print('total blocks:', n)
if __name__ == '__main__':
    rules(sys.argv[1], sys.argv[2])
