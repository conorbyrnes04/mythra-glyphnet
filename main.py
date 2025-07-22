#!/usr/bin/env python3
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
    print("\nUsage: python main.py <command>")
    print("\nCommands:")
    print("  generate    - Interactive MERU glyph generation")
    print("  enhance-db  - Clean and enhance the database")  
    print("  stats       - Show database statistics")
    print("  help        - Show this help message")
    print("\nExamples:")
    print("  python main.py generate")
    print("  python main.py enhance-db")
    print("  python main.py stats")

if __name__ == "__main__":
    main()
