#!/usr/bin/env python3
"""
Nirikshan — Project Initialization Script
Creates all required project directories and __init__.py package files.
"""

import os
import sys

def init_project():
    print("🚀 Initializing Nirikshan project structure...\n")

    # Determine base directory (project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    print(f"📁 Project Root: {base_dir}\n")

    # List of directories to ensure
    directories = [
        os.path.join(base_dir, "backend"),
        os.path.join(base_dir, "backend", "app"),
        os.path.join(base_dir, "backend", "app", "api"),
        os.path.join(base_dir, "backend", "app", "core"),
        os.path.join(base_dir, "backend", "app", "vision"),
        os.path.join(base_dir, "backend", "app", "rules"),
        os.path.join(base_dir, "backend", "app", "reports"),
        os.path.join(base_dir, "datasets"),
        os.path.join(base_dir, "datasets", "raw_samples"),
        os.path.join(base_dir, "docker"),
        os.path.join(base_dir, "scripts"),
        os.path.join(base_dir, "storage"),
        os.path.join(base_dir, "storage", "uploads"),
        os.path.join(base_dir, "storage", "evidence"),
        os.path.join(base_dir, "storage", "generated_reports"),
        os.path.join(base_dir, "web"),
        os.path.join(base_dir, "web", "static"),
        os.path.join(base_dir, "web", "static", "css"),
        os.path.join(base_dir, "web", "static", "js"),
        os.path.join(base_dir, "web", "templates"),
    ]

    print("📂 Creating directories:")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        rel_path = os.path.relpath(directory, base_dir)
        print(f"  ✅ Directory verified: {rel_path}/")

    print("\n📦 Ensuring Python package __init__.py files:")
    init_files = [
        os.path.join(base_dir, "backend", "app", "__init__.py"),
        os.path.join(base_dir, "backend", "app", "api", "__init__.py"),
        os.path.join(base_dir, "backend", "app", "core", "__init__.py"),
        os.path.join(base_dir, "backend", "app", "vision", "__init__.py"),
        os.path.join(base_dir, "backend", "app", "rules", "__init__.py"),
        os.path.join(base_dir, "backend", "app", "reports", "__init__.py"),
    ]

    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, "w", encoding="utf-8") as f:
                f.write(f'"""Package initialization for {os.path.basename(os.path.dirname(init_file))}."""\n')
            rel_path = os.path.relpath(init_file, base_dir)
            print(f"  ✨ Created: {rel_path}")
        else:
            rel_path = os.path.relpath(init_file, base_dir)
            print(f"  ✅ Exists: {rel_path}")

    print("\n🎉 Nirikshan directory structure initialized successfully!")
    print("👉 Next step: Run setup_env script or start the server using uvicorn.")

if __name__ == "__main__":
    init_project()
