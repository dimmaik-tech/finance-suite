import os
from pathlib import Path

MARKER = "# 🔐 Login Protection (auto)"
AUTH_IMPORT = "from auth import require_login, show_logout_button, admin_badge"
AUTH_CALLS_TEMPLATE = """{marker}
{import_line}

require_login("{app_name}")
admin_badge()
show_logout_button(key="{logout_key}")

"""

def is_python_file(p: Path) -> bool:
    return p.is_file() and p.suffix == ".py"

def already_protected(text: str) -> bool:
    return MARKER in text or "require_login(" in text

def inject_protection(text: str, app_name: str, logout_key: str) -> str:
    # Put protection AFTER initial imports block (best practice)
    lines = text.splitlines()
    i = 0

    # Skip shebang/encoding lines
    while i < len(lines) and (lines[i].startswith("#!") or "coding" in lines[i]):
        i += 1

    # Consume initial import block (import/from ... lines and blank lines)
    while i < len(lines):
        line = lines[i].strip()
        if line == "" or line.startswith("import ") or line.startswith("from "):
            i += 1
            continue
        break

    header = AUTH_CALLS_TEMPLATE.format(
        marker=MARKER,
        import_line=AUTH_IMPORT,
        app_name=app_name,
        logout_key=logout_key,
    ).rstrip() + "\n\n"

    # Insert header at position i (after imports)
    new_lines = lines[:i] + [header.rstrip("\n")] + lines[i:]
    return "\n".join(new_lines) + ("\n" if not text.endswith("\n") else "")

def protect_file(path: Path, app_name: str):
    text = path.read_text(encoding="utf-8", errors="ignore")
    if already_protected(text):
        print(f"Already protected: {path}")
        return

    logout_key = f"logout_{path.stem.lower()}"
    new_text = inject_protection(text, app_name=app_name, logout_key=logout_key)
    path.write_text(new_text, encoding="utf-8")
    print(f"Protected: {path}")

def main():
    repo = Path(".")
    pages_dir = repo / "pages"
    targets = []

    # Root entry points (Streamlit multipage uses Home.py often)
    for root_file in ["Home.py", "app.py"]:
        p = repo / root_file
        if is_python_file(p):
            targets.append(p)

    # All pages/*
    if pages_dir.exists():
        for p in sorted(pages_dir.glob("*.py")):
            if is_python_file(p):
                targets.append(p)

    if not targets:
        print("No targets found (Home.py/app.py/pages/*.py).")
        return

    app_name = os.getenv("APP_NAME", "Finance Suite")
    print("🔐 Protecting Streamlit files...")
    for p in targets:
        protect_file(p, app_name=app_name)
    print("✅ DONE.")

if __name__ == "__main__":
    main()
