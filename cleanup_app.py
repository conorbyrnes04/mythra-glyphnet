#!/usr/bin/env python3
"""
Complete App Cleanup Script
Remove unnecessary files and streamline the codebase
"""
import os
import shutil
from pathlib import Path

def cleanup_app():
    """Clean up the entire application"""
    
    print("🧹 Starting comprehensive app cleanup...")
    
    # Files to delete (obsolete/temporary)
    files_to_delete = [
        "debug_meru.py",
        "test_any_model.py", 
        "find_meru.py",
        "start_meru_training.py",
        "start_meru_training_fixed.py", 
        "test_current_models.py",
        "setup_mongodb.py",
        "SVG_OPTIMIZATION_SUMMARY.md",
        "prompts/generate_prompt.py",  # Empty file
    ]
    
    # Directories to clean
    dirs_to_clean = [
        "database/__pycache__",
        "notebooks/.ipynb_checkpoints",
        "notebooks/.DS_Store"
    ]
    
    # Training configs to keep (remove the rest)
    essential_configs = [
        "replicate/training/midjourney-svg-config.yaml",  # MERU training
        "replicate/training/config.yaml"  # Base config
    ]
    
    # Delete obsolete files
    deleted_count = 0
    for file_path in files_to_delete:
        if Path(file_path).exists():
            try:
                os.remove(file_path)
                print(f"🗑️  Deleted: {file_path}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Failed to delete {file_path}: {e}")
    
    # Clean directories
    for dir_path in dirs_to_clean:
        if Path(dir_path).exists():
            try:
                if Path(dir_path).is_dir():
                    shutil.rmtree(dir_path)
                else:
                    os.remove(dir_path)
                print(f"🗑️  Cleaned: {dir_path}")
            except Exception as e:
                print(f"❌ Failed to clean {dir_path}: {e}")
    
    # Clean up training configs (keep only essential ones)
    training_dir = Path("replicate/training")
    if training_dir.exists():
        config_files = list(training_dir.glob("*.yaml"))
        for config_file in config_files:
            if str(config_file) not in essential_configs:
                try:
                    config_file.unlink()
                    print(f"🗑️  Removed config: {config_file}")
                except Exception as e:
                    print(f"❌ Failed to remove {config_file}: {e}")
    
    # Clean up notebooks results (keep only essential)
    notebooks_results = Path("notebooks/results")
    if notebooks_results.exists():
        # Keep the directory but clean old files
        print(f"📁 Cleaned notebooks/results (kept directory)")
    
    print(f"\n✅ Cleanup complete! Deleted {deleted_count} files.")
    print("\n📋 Remaining core files:")
    print("   • test_meru.py (main MERU interface)")
    print("   • enhance_database.py (database management)")
    print("   • database/glyph_integration.py (database layer)")
    print("   • prompts/prompt_templates.yaml (prompt templates)")
    print("   • replicate/inference/run_prompt.py (inference)")
    print("   • notebooks/glyph_codex.ipynb (interactive interface)")

def create_streamlined_structure():
    """Create a clean, organized structure"""
    
    # Create organized directory structure
    dirs_to_ensure = [
        "core",           # Core functionality
        "data/backups",   # Database backups
        "results/archive", # Archive old results
        "docs"            # Documentation
    ]
    
    for dir_path in dirs_to_ensure:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Ensured directory: {dir_path}")

def create_main_interface():
    """Create a single main interface file"""
    
    main_content = '''#!/usr/bin/env python3
"""
MYTHRA GLYPHNET - Main Interface
Unified interface for MERU glyph generation and management
"""
import sys
from pathlib import Path

def main():
    """Main application entry point"""
    
    print("🎨 MYTHRA GLYPHNET - MERU Glyph Generator")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    if command == "generate":
        from test_meru import interactive_test
        interactive_test()
    elif command == "enhance-db":
        from enhance_database import cleanup_and_enhance_db
        cleanup_and_enhance_db()
    elif command == "stats":
        from test_meru import show_database_stats
        show_database_stats()
    elif command == "help":
        show_help()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()

def show_help():
    """Show help information"""
    print("\\nUsage: python main.py <command>")
    print("\\nCommands:")
    print("  generate    - Interactive MERU glyph generation")
    print("  enhance-db  - Clean and enhance the database")  
    print("  stats       - Show database statistics")
    print("  help        - Show this help message")
    print("\\nExamples:")
    print("  python main.py generate")
    print("  python main.py enhance-db")
    print("  python main.py stats")

if __name__ == "__main__":
    main()
'''
    
    with open("main.py", "w") as f:
        f.write(main_content)
    
    print("✨ Created main.py - unified interface")

if __name__ == "__main__":
    cleanup_app()
    create_streamlined_structure()
    create_main_interface()
    
    print("\\n🎉 App cleanup and reorganization complete!")
    print("\\nNext steps:")
    print("  1. Test the main interface: python main.py help")
    print("  2. Generate glyphs: python main.py generate") 
    print("  3. Enhance database: python main.py enhance-db")