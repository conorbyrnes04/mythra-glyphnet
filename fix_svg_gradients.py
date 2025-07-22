#!/usr/bin/env python3
"""
Fix SVG Gradient Structure
Fix the nested SVG tag issue in gradient and radial colored glyphs
"""
import re
from pathlib import Path

def fix_svg_gradient_structure(svg_path):
    """Fix broken SVG structure caused by nested svg tags"""
    
    with open(svg_path, 'r') as f:
        content = f.read()
    
    print(f"🔧 Fixing: {Path(svg_path).name}")
    
    # Check if this is a broken gradient SVG
    if '<svg><defs>' in content:
        print("   Found broken nested SVG structure")
        
        # Extract the gradient/defs content
        defs_match = re.search(r'<svg>(<defs>.*?</defs>)<svg', content, re.DOTALL)
        if defs_match:
            defs_content = defs_match.group(1)
            
            # Remove the broken nested structure
            content = re.sub(r'<svg><defs>.*?</defs><svg', '<svg', content, flags=re.DOTALL)
            
            # Insert defs properly after the first svg tag
            content = re.sub(r'(<svg[^>]*>)', rf'\1\n{defs_content}', content)
            
            print("   ✅ Fixed gradient structure")
        else:
            print("   ❌ Could not extract defs content")
            return False
    else:
        print("   ℹ️  No nested SVG structure found")
        return True
    
    # Write fixed content
    with open(svg_path, 'w') as f:
        f.write(content)
    
    print("   💾 Saved fixed SVG")
    return True

def fix_all_colored_svgs():
    """Fix all colored SVG files in results/glyphs/"""
    
    glyph_dir = Path("results/glyphs")
    colored_svgs = list(glyph_dir.glob("colored_*.svg"))
    
    if not colored_svgs:
        print("❌ No colored SVG files found")
        return
    
    print(f"🔧 Fixing {len(colored_svgs)} colored SVG files")
    print("=" * 50)
    
    fixed_count = 0
    for svg_file in colored_svgs:
        if fix_svg_gradient_structure(str(svg_file)):
            fixed_count += 1
        print()
    
    print(f"✅ Fixed {fixed_count}/{len(colored_svgs)} SVG files")

def test_svg_structure(svg_path):
    """Test if SVG has valid structure"""
    
    with open(svg_path, 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for nested svg tags
    svg_count = content.count('<svg')
    if svg_count > 1:
        issues.append(f"Multiple <svg> tags found ({svg_count})")
    
    # Check for proper defs placement
    if '<defs>' in content:
        if not re.search(r'<svg[^>]*>\s*<defs>', content):
            issues.append("Defs not properly placed after svg tag")
    
    # Check for valid gradient references
    gradient_refs = re.findall(r'fill="url\(#([^)]+)\)"', content)
    gradient_defs = re.findall(r'<(?:linear|radial)Gradient id="([^"]+)"', content)
    
    for ref in gradient_refs:
        if ref not in gradient_defs:
            issues.append(f"Gradient reference #{ref} not defined")
    
    return issues

if __name__ == "__main__":
    print("🔧 SVG Gradient Structure Fixer")
    print("=" * 40)
    
    # First, test current colored SVGs
    glyph_dir = Path("results/glyphs")
    colored_svgs = list(glyph_dir.glob("colored_*.svg"))
    
    print(f"📊 Testing {len(colored_svgs)} colored SVG files:")
    print()
    
    for svg_file in colored_svgs:
        issues = test_svg_structure(str(svg_file))
        print(f"📄 {svg_file.name}")
        if issues:
            for issue in issues:
                print(f"   ❌ {issue}")
        else:
            print(f"   ✅ Structure looks good")
        print()
    
    # Fix all issues
    fix_all_colored_svgs()
    
    print("\n🔍 Re-testing after fixes:")
    print("=" * 30)
    
    for svg_file in colored_svgs:
        issues = test_svg_structure(str(svg_file))
        print(f"📄 {svg_file.name}: {'✅ Fixed' if not issues else '❌ Still has issues'}") 