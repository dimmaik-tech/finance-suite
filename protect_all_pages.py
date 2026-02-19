import os

AUTH_BLOCK = """import streamlit as st
from auth import require_login, show_logout_button, admin_badge

require_login("Finance Suite")
admin_badge()
show_logout_button(key="{key}")

"""

PAGES_FOLDER = "pages"


def protect_file(filepath, keyname):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # If already protected, skip
    if "require_login(" in content:
        print("Already protected:", filepath)
        return

    new_content = AUTH_BLOCK.format(key=keyname) + "\n" + content

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("Protected:", filepath)


def main():
    print("🔐 Protecting all Streamlit pages...\n")

    if not os.path.isdir(PAGES_FOLDER):
        print(f"❌ Folder '{PAGES_FOLDER}' not found. Run this from repo root.")
        return

    for filename in os.listdir(PAGES_FOLDER):
        if filename.endswith(".py"):
            filepath = os.path.join(PAGES_FOLDER, filename)
            keyname = filename.replace(".py", "")
            protect_file(filepath, keyname)

    print("\n✅ DONE. All pages are now password protected.")


if __name__ == "__main__":
    main()
