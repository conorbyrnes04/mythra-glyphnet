#!/usr/bin/env python3
"""
Fix SVG Normalization - Proper ViewBox Handling
"""

import json
import sys
import os
from pathlib import Path
import re

class SVGNormalizationFixer:
    def __init__(self):
        self.input_dir = Path("results/gGlyphs_codex/archetypal_53")
        self.symbols = ["wolf", "lion", "bear", "fox"]
    
    def fix_single_svg_normalization(self, symbol_name: str) -> bool:
        """Fix normalization for a single symbol"""
        try:
            print(f"🔧 Fixing {symbol_name} graph SVG...")
            
            # Read the original B&W SVG
            bw_svg_path = self.input_dir / "svg_bw" / f"{symbol_name}.svg"
            normalized_svg_path = self.input_dir / "svg_normalized" / f"{symbol_name}_graph.svg"
            
            if not bw_svg_path.exists():
                print(f"❌ B&W SVG not found: {bw_svg_path}")
                return False
            
            with open(bw_svg_path, 'r') as f:
                svg_content = f.read()
            
            # Properly normalize by keeping the original viewBox but setting standard dimensions
            normalized_svg = re.sub(
                r'<svg[^>]*>',
                '<svg width="100" height="100" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">',
                svg_content,
                count=1
            )
            
            # Also ensure clean SVG structure by removing standalone declarations that might cause issues
            normalized_svg = re.sub(r'<\?xml[^>]*\?>\s*', '', normalized_svg)
            normalized_svg = re.sub(r'<!DOCTYPE[^>]*>\s*', '', normalized_svg)
            
            # Add clean XML declaration
            clean_svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + normalized_svg
            
            with open(normalized_svg_path, 'w') as f:
                f.write(clean_svg)
            
            print(f"✅ Fixed {symbol_name} graph SVG: {normalized_svg_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing {symbol_name}: {e}")
            return False
    
    def fix_all_svg_normalizations(self) -> list:
        """Fix normalization for all symbols"""
        print("🔧 Fixing SVG normalizations for all symbols...")
        
        results = []
        for symbol in self.symbols:
            success = self.fix_single_svg_normalization(symbol)
            results.append({
                'symbol': symbol,
                'success': success
            })
        
        return results
    
    def create_test_html(self) -> str:
        """Create test HTML to view the fixed SVGs"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔧 Fixed SVG Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f0f0f0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .svg-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .svg-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .svg-card h3 {{
            margin-top: 0;
            text-align: center;
            color: #333;
        }}
        
        .svg-comparison {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            gap: 20px;
        }}
        
        .svg-version {{
            text-align: center;
        }}
        
        .svg-version h4 {{
            margin: 10px 0 5px 0;
            font-size: 14px;
            color: #666;
        }}
        
        .svg-container {{
            width: 100px;
            height: 100px;
            border: 1px solid #ddd;
            background: white;
            margin: 0 auto;
        }}
        
        .svg-container svg {{
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Fixed SVG Normalization Test</h1>
        <p>Testing the fixed graph SVGs to ensure they display properly.</p>
        
        <div class="svg-grid">
"""

        for symbol in self.symbols:
            symbol_title = symbol.title()
            html_content += f"""
            <div class="svg-card">
                <h3>{symbol_title}</h3>
                <div class="svg-comparison">
                    <div class="svg-version">
                        <h4>Original B&W</h4>
                        <div class="svg-container">
                            <object data="svg_bw/{symbol}.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                    <div class="svg-version">
                        <h4>Fixed Graph</h4>
                        <div class="svg-container">
                            <object data="svg_normalized/{symbol}_graph.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                    <div class="svg-version">
                        <h4>Colored</h4>
                        <div class="svg-container">
                            <object data="svg_colored/{symbol}_colored.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                </div>
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        test_html_path = self.input_dir / "svg_test.html"
        with open(test_html_path, 'w') as f:
            f.write(html_content)
        
        print(f"📄 Test HTML created: {test_html_path}")
        return str(test_html_path)

def main():
    """Main execution"""
    print("🔧 MYTHRA GLYPHNET - SVG Normalization Fix")
    print("=" * 50)
    
    fixer = SVGNormalizationFixer()
    
    # Fix all SVG normalizations
    results = fixer.fix_all_svg_normalizations()
    
    # Create summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n📊 Fix Summary:")
    print(f"✅ Fixed: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n✅ Successfully Fixed:")
        for result in successful:
            print(f"  • {result['symbol'].title()}")
    
    if failed:
        print(f"\n❌ Failed to Fix:")
        for result in failed:
            print(f"  • {result['symbol'].title()}")
    
    # Create test HTML
    test_html = fixer.create_test_html()
    
    print(f"\n🎉 SVG normalization fix complete!")
    print(f"📄 Test your fixed SVGs: {test_html}")
    print(f"🌐 Open: http://localhost:8001/archetypal_53/svg_test.html")
    print(f"\n🔧 The graph SVGs should now display properly!")

if __name__ == "__main__":
    main() 
"""
Fix SVG Normalization - Proper ViewBox Handling
"""

import json
import sys
import os
from pathlib import Path
import re

class SVGNormalizationFixer:
    def __init__(self):
        self.input_dir = Path("results/gGlyphs_codex/archetypal_53")
        self.symbols = ["wolf", "lion", "bear", "fox"]
    
    def fix_single_svg_normalization(self, symbol_name: str) -> bool:
        """Fix normalization for a single symbol"""
        try:
            print(f"🔧 Fixing {symbol_name} graph SVG...")
            
            # Read the original B&W SVG
            bw_svg_path = self.input_dir / "svg_bw" / f"{symbol_name}.svg"
            normalized_svg_path = self.input_dir / "svg_normalized" / f"{symbol_name}_graph.svg"
            
            if not bw_svg_path.exists():
                print(f"❌ B&W SVG not found: {bw_svg_path}")
                return False
            
            with open(bw_svg_path, 'r') as f:
                svg_content = f.read()
            
            # Properly normalize by keeping the original viewBox but setting standard dimensions
            normalized_svg = re.sub(
                r'<svg[^>]*>',
                '<svg width="100" height="100" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">',
                svg_content,
                count=1
            )
            
            # Also ensure clean SVG structure by removing standalone declarations that might cause issues
            normalized_svg = re.sub(r'<\?xml[^>]*\?>\s*', '', normalized_svg)
            normalized_svg = re.sub(r'<!DOCTYPE[^>]*>\s*', '', normalized_svg)
            
            # Add clean XML declaration
            clean_svg = '<?xml version="1.0" encoding="UTF-8"?>\n' + normalized_svg
            
            with open(normalized_svg_path, 'w') as f:
                f.write(clean_svg)
            
            print(f"✅ Fixed {symbol_name} graph SVG: {normalized_svg_path}")
            return True
            
        except Exception as e:
            print(f"❌ Error fixing {symbol_name}: {e}")
            return False
    
    def fix_all_svg_normalizations(self) -> list:
        """Fix normalization for all symbols"""
        print("🔧 Fixing SVG normalizations for all symbols...")
        
        results = []
        for symbol in self.symbols:
            success = self.fix_single_svg_normalization(symbol)
            results.append({
                'symbol': symbol,
                'success': success
            })
        
        return results
    
    def create_test_html(self) -> str:
        """Create test HTML to view the fixed SVGs"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔧 Fixed SVG Test</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
            background: #f0f0f0;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .svg-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .svg-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        
        .svg-card h3 {{
            margin-top: 0;
            text-align: center;
            color: #333;
        }}
        
        .svg-comparison {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            gap: 20px;
        }}
        
        .svg-version {{
            text-align: center;
        }}
        
        .svg-version h4 {{
            margin: 10px 0 5px 0;
            font-size: 14px;
            color: #666;
        }}
        
        .svg-container {{
            width: 100px;
            height: 100px;
            border: 1px solid #ddd;
            background: white;
            margin: 0 auto;
        }}
        
        .svg-container svg {{
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Fixed SVG Normalization Test</h1>
        <p>Testing the fixed graph SVGs to ensure they display properly.</p>
        
        <div class="svg-grid">
"""

        for symbol in self.symbols:
            symbol_title = symbol.title()
            html_content += f"""
            <div class="svg-card">
                <h3>{symbol_title}</h3>
                <div class="svg-comparison">
                    <div class="svg-version">
                        <h4>Original B&W</h4>
                        <div class="svg-container">
                            <object data="svg_bw/{symbol}.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                    <div class="svg-version">
                        <h4>Fixed Graph</h4>
                        <div class="svg-container">
                            <object data="svg_normalized/{symbol}_graph.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                    <div class="svg-version">
                        <h4>Colored</h4>
                        <div class="svg-container">
                            <object data="svg_colored/{symbol}_colored.svg" type="image/svg+xml"></object>
                        </div>
                    </div>
                </div>
            </div>
"""

        html_content += """
        </div>
    </div>
</body>
</html>
"""
        
        test_html_path = self.input_dir / "svg_test.html"
        with open(test_html_path, 'w') as f:
            f.write(html_content)
        
        print(f"📄 Test HTML created: {test_html_path}")
        return str(test_html_path)

def main():
    """Main execution"""
    print("🔧 MYTHRA GLYPHNET - SVG Normalization Fix")
    print("=" * 50)
    
    fixer = SVGNormalizationFixer()
    
    # Fix all SVG normalizations
    results = fixer.fix_all_svg_normalizations()
    
    # Create summary
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n📊 Fix Summary:")
    print(f"✅ Fixed: {len(successful)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n✅ Successfully Fixed:")
        for result in successful:
            print(f"  • {result['symbol'].title()}")
    
    if failed:
        print(f"\n❌ Failed to Fix:")
        for result in failed:
            print(f"  • {result['symbol'].title()}")
    
    # Create test HTML
    test_html = fixer.create_test_html()
    
    print(f"\n🎉 SVG normalization fix complete!")
    print(f"📄 Test your fixed SVGs: {test_html}")
    print(f"🌐 Open: http://localhost:8001/archetypal_53/svg_test.html")
    print(f"\n🔧 The graph SVGs should now display properly!")

if __name__ == "__main__":
    main() 