from pathlib import Path


text = Path("structured_texts/1_CApture_Network_Traffic_With_Timer.st").read_text()

def count_loc(text):
    loc = 0
    for ln in text.splitlines():
        s = ln.strip()
        print(f"Line: {repr(ln)} -> stripped: {repr(s)}")
        if not s:
            print("  Skipping empty")
            continue
        if s.startswith("//"):
            print("  Skipping comment")
            continue
        loc += 1
    return loc

print("LOC =", count_loc(text))
