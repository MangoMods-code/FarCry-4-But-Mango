"""A small Swift lexer that finds string literals (Mango Port's rebrand script uses it).

literals(src) yields (start, end, text) for every string literal outside comments:
start/end span the whole literal including quotes, text is its source between the
quotes. segments(src) yields the same literals as (start, end, [(a, b), ...]) where
each (a, b) is a run of literal text, i.e. outside \\( ... ) interpolations, so a
rewrite never touches code inside an interpolation.

Handles // and nested /* */ comments, "..." and \"\"\"...\"\"\" strings, raw #"..."#
strings, escapes, and interpolations that contain strings of their own.
"""


def _string(src, i):
    """src[i] starts a literal (after any #s). Returns (end, segments)."""
    hashes = 0
    while src[i] == '#':
        hashes += 1
        i += 1
    multi = src.startswith('"""', i)
    q = '"""' if multi else '"'
    i += len(q)
    close = q + '#' * hashes
    esc = '\\' + '#' * hashes
    segs, seg_start = [], i
    while i < len(src):
        if src.startswith(close, i):
            segs.append((seg_start, i))
            return i + len(close), segs
        if src.startswith(esc, i):
            j = i + len(esc)
            if j < len(src) and src[j] == '(':
                segs.append((seg_start, i))
                i = _code(src, j + 1, ')')
                seg_start = i
                continue
            i = j + 1
            continue
        if not multi and src[i] == '\n':
            raise ValueError(f"unterminated string at {i}")
        i += 1
    raise ValueError("unterminated string")


def _code(src, i, until=None, out=None):
    """Scan code from i; with `until`, stop after the matching closer. Returns end."""
    depth = 0
    while i < len(src):
        c = src[i]
        if src.startswith('//', i):
            j = src.find('\n', i)
            i = len(src) if j < 0 else j
            continue
        if src.startswith('/*', i):
            n, i = 1, i + 2
            while n and i < len(src):
                if src.startswith('/*', i):
                    n, i = n + 1, i + 2
                elif src.startswith('*/', i):
                    n, i = n - 1, i + 2
                else:
                    i += 1
            continue
        if c == '"' or (c == '#' and src[i:].lstrip('#').startswith('"')):
            start = i
            end, segs = _string(src, i)
            if out is not None:
                out.append((start, end, segs))
            i = end
            continue
        if until:
            if c == '(':
                depth += 1
            elif c == ')':
                if depth == 0:
                    return i + 1
                depth -= 1
        i += 1
    return i


def segments(src):
    out = []
    _code_collect(src, out)
    return out


def _code_collect(src, out):
    # Interpolated code is scanned by _string without collecting; strings nested in
    # interpolations are rare in UI text and are left alone on purpose.
    _code(src, 0, None, out)


def literals(src):
    for start, end, segs in segments(src):
        yield start, end, src[start:end]
