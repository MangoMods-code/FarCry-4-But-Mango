#!/usr/bin/env python3
"""Rename the Madeira app to Mango Port where people see it, in a Madeira checkout.

    python3 scripts/rebrand.py madeira            rewrite the checkout in place
    python3 scripts/rebrand.py madeira --dry-run  list what would change

Only on-screen text changes: string literals in the app's Swift files, the strings
catalog (its English keys and every translation, so translations still match), and
the user-facing Info.plist descriptions. Left alone on purpose:
  - code names, file and folder names (madeira.cfg, the "Madeira" library folders),
    keychain services, notification names, error domains, user agents, the JIT
    pairing host name: the app and other people's setups depend on them;
  - log lines, the session summary and madeira.cfg's header, so Madeira's
    troubleshooting guide and the host tests still match them;
  - "Madeira JIT", the name of the Shortcut the app runs by name;
  - the per-game settings text (GameRecommendations.swift: the host tests read it)
    and the generated settings catalog (developer notes, regenerated upstream);
  - every credit to Madeira: Settings › Credits (its people and what they built in Madeira,
    and its footer) stays as it is, and the About text is rewritten to credit it.

"Madeira Dock" becomes "Mango Dock". The app icon becomes mango/icon/AppIcon-1024.png. scripts/make-rebrand-patch.sh turns the result
into mango/patches/0004-on-screen-rebrand.patch.
"""
import json
import shutil
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from swiftstrings import segments  # noqa: E402

NEW = "Mango Port"
# The word Madeira on its own: not part of a path, identifier or file name.
# "Madeira JIT" stays: it is the name of the Shortcut people install and the app runs it by that name.
WORD = re.compile(r"(?<![\w/.\-])Madeira(?![\w\-/]|\.\w| JIT\b)")
FILES_PATH = re.compile(r"(?<![\w/.\-])Madeira(?=/wine\b)")
DOCK = re.compile(r"(?<![\w/.\-])Madeira Dock\b")

SKIP_FILES = {"GameRecommendations.swift", "ConfigCatalog.generated.swift", "ClaudeHelp.swift",
              "LogSummary.swift", "LogStore.swift", "MadeiraConfig.swift"}
# A literal passed straight to one of these, or assigned to one of these names, is not on-screen text.
SKIP_CALL = re.compile(
    r"(?:\blog|\bLogStore\.shared\.log|NSError|Notification\.Name|graphQL|setValue|appendingPathComponent"
    r"|beginBackgroundTask(?:WithName)?|\bprint|fputs|debugPrint|os_log|NSLog|dprintf)\s*\(\s*(?:\w+\s*:\s*)?$")
SKIP_ASSIGN = re.compile(r"\b(?:service|userAgent|hostName|domain|identifier|key|suiteName)\s*[:=][^=\n]*$")
# Texts about Madeira itself, which stay as they are.
KEEP = {
    "Madeira is built on Wine, FEX-Emu, DXMT by Feifan He (3Shain) with the Direct3D 9 frontend by David Acevedo (dacevedo12), rpmalloc by Mattias Jansson, StikDebug, StikJIT and idevice. Thank you to everyone who contributes to these projects.",
}
# Hand-written replacements, applied before the word rule (exact literal text, quotes excluded).
EXACT = {
    "Madeira is a proof-of-concept for running x86 Windows games on iOS using FEX-Emu, Wine, and Metal-based graphics translation.":
        "Mango Port is built on Madeira by Will Faust (github.com/willfaust/Madeira), a proof-of-concept for running "
        "x86 Windows games on iOS using FEX-Emu, Wine, and Metal-based graphics translation. "
        "Mango Port is free software under the GPL-3.0; its source is at github.com/MangoMods-code/FarCry-4-But-Mango.",
}


_SRC = "github.com/willfaust/Madeira"
_OURS = "github.com/MangoMods-code/FarCry-4-But-Mango"
# The About credit in the app's other five languages plus Chinese (the catalog's check wants all six).
EXACT_TRANSLATIONS = {
    next(iter(EXACT)): {
        "de": f"Mango Port basiert auf Madeira von Will Faust ({_SRC}), einem Proof of Concept, das x86-Windows-Spiele "
              f"mit FEX-Emu, Wine und einer Grafikübersetzung auf Metal-Basis unter iOS ausführt. Mango Port ist freie "
              f"Software unter der GPL-3.0; der Quellcode liegt auf {_OURS}.",
        "es": f"Mango Port está basado en Madeira, de Will Faust ({_SRC}), una prueba de concepto para ejecutar juegos "
              f"x86 de Windows en iOS con FEX-Emu, Wine y traducción de gráficos basada en Metal. Mango Port es software "
              f"libre bajo la GPL-3.0; su código fuente está en {_OURS}.",
        "ko": f"Mango Port는 Will Faust의 Madeira({_SRC})를 바탕으로 만들어졌습니다. Madeira는 FEX-Emu, Wine, Metal 기반 "
              f"그래픽 변환을 사용해 iOS에서 x86 Windows 게임을 실행하는 개념 증명 프로젝트입니다. Mango Port는 GPL-3.0 "
              f"자유 소프트웨어이며 소스 코드는 {_OURS}에 있습니다.",
        "pt-BR": f"O Mango Port é baseado no Madeira, de Will Faust ({_SRC}), uma prova de conceito para rodar jogos x86 "
                 f"de Windows no iOS usando FEX-Emu, Wine e tradução de gráficos baseada em Metal. O Mango Port é software "
                 f"livre sob a GPL-3.0; o código-fonte está em {_OURS}.",
        "ru": f"Mango Port основан на Madeira от Will Faust ({_SRC}) — экспериментальном проекте для запуска x86-игр "
              f"для Windows на iOS с помощью FEX-Emu, Wine и трансляции графики на Metal. Mango Port — свободное ПО "
              f"под лицензией GPL-3.0; исходный код находится на {_OURS}.",
        "zh-Hans": f"Mango Port 基于 Will Faust 的 Madeira（{_SRC}）构建。Madeira 是一个概念验证项目，借助 FEX-Emu、Wine "
                   f"和基于 Metal 的图形转译在 iOS 上运行 x86 Windows 游戏。Mango Port 是基于 GPL-3.0 的自由软件，"
                   f"源代码位于 {_OURS}。",
    }
}


def rename(text):
    text = DOCK.sub("Mango Dock", text)
    text = FILES_PATH.sub(NEW, text)   # "Madeira/wine/drive_c" in the Files app is the app's own folder
    return WORD.sub(NEW, text)


PAIRS = {}   # every on-screen text this run changed: old -> new (the host tests pin some)


def rewrite_swift(path, dry):
    src = path.read_text()
    edits = []
    for start, end, segs in segments(src):
        body = src[start:end]
        if "Madeira" not in body:
            continue
        before = src[max(0, start - 120):start]
        line_before = before.rsplit("\n", 1)[-1]
        if "MadeiraCredit(" in line_before:
            CREDIT_ROLES.add(src[start + 1:end - 1])
            continue   # credits name Madeira's own people and what they built in Madeira
        if SKIP_CALL.search(before) or SKIP_ASSIGN.search(line_before):
            continue
        if src[start + 1:end - 1] in KEEP:
            continue
        if line_before.rstrip().endswith("+"):
            # A continuation: judge it by the expression it continues.
            stmt = src[max(0, start - 600):start]
            if re.search(r"(?:\blog|LogStore\.shared\.log|print|fputs|NSLog)\s*\([^)]*$", stmt):
                continue
        for a, b in segs:
            old = src[a:b]
            new = EXACT.get(old) or rename(old)
            if new != old:
                edits.append((a, b, old, new))
                PAIRS[old] = new
    if not edits:
        return 0
    for a, b, old, new in sorted(edits, reverse=True):
        src = src[:a] + new + src[b:]
    if dry:
        for _, _, old, new in edits:
            print(f"{path.name}: {old[:100]!r}\n  -> {new[:100]!r}")
    else:
        path.write_text(src)
    return len(edits)


CREDIT_ROLES = set()   # the Credits roles found in the Swift files (rewrite_swift), kept in the catalog too


def rewrite_catalog(path, dry):
    data = json.loads(path.read_text())
    out, n = {}, 0
    for key, entry in data["strings"].items():
        new_key = key if key in KEEP or key in CREDIT_ROLES else (EXACT.get(key) or rename(key))
        n += new_key != key
        if key in EXACT_TRANSLATIONS:
            for lang, text in EXACT_TRANSLATIONS[key].items():
                entry.setdefault("localizations", {})[lang] = {"stringUnit": {"state": "translated", "value": text}}
            out[new_key] = entry
            continue
        for loc in ((entry.get("localizations") or {}).values() if new_key != key or key not in KEEP | CREDIT_ROLES else []):
            unit = loc.get("stringUnit")
            if unit and "Madeira" in unit.get("value", ""):
                unit["value"] = rename(unit["value"])
                n += 1
        out[new_key] = entry
    data["strings"] = out
    if not dry:
        # The catalog's own formatting (2-space indents, no final newline), so the diff is only the renames.
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2, separators=(",", ": ")))
    return n


def rewrite_plist(path, dry):
    src = path.read_text()
    new = re.sub(r"(<string>)([^<]*)(</string>)", lambda m: m.group(1) + rename(m.group(2)) + m.group(3), src)
    n = sum(1 for a, b in zip(src.splitlines(), new.splitlines()) if a != b)
    if not dry:
        path.write_text(new)
    return n


def rewrite_tests(root, dry):
    """Madeira's host tests check some on-screen sentences word for word: follow the renames."""
    n = 0
    pairs = sorted(((o, w) for o, w in PAIRS.items() if len(o) >= 15), key=lambda p: -len(p[0]))
    for f in sorted((root / "tests" / "host").glob("*.py")):
        src = new = f.read_text()
        for old, rep in pairs:
            for o, r in ((old, rep), (old.replace("'", "\\'"), rep.replace("'", "\\'"))):
                if o in new:
                    n += new.count(o)
                    new = new.replace(o, r)
        if new != src and not dry:
            f.write_text(new)
    return n


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "madeira")
    dry = "--dry-run" in sys.argv
    app = root / "app" / "Madeira"
    total = 0
    for f in sorted(app.rglob("*.swift")):
        if f.name not in SKIP_FILES:
            total += rewrite_swift(f, dry)
    cat = app / "Localizable.xcstrings"
    if cat.exists():
        total += rewrite_catalog(cat, dry)
    total += rewrite_plist(app / "Info.plist", dry)
    total += rewrite_tests(root, dry)
    icon = Path(__file__).resolve().parent.parent / "mango" / "icon" / "AppIcon-1024.png"
    target = app / "Assets.xcassets" / "AppIcon.appiconset" / "AppIcon-1024.png"
    if icon.exists() and target.exists() and icon.read_bytes() != target.read_bytes():
        total += 1
        if not dry:
            shutil.copyfile(icon, target)   # mango/icon/icon.svg is its source
    print(f"rebrand: {total} change(s){' (dry run)' if dry else ''}")


if __name__ == "__main__":
    main()
