#!/usr/bin/env node
import { createInterface } from 'readline';
import { initGlyphDB, addGlyph } from './db/genericGlyphs.js';
(async()=>{
  await initGlyphDB();
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const ask = q=>new Promise(res=>rl.question(q,res));
  const title = await ask('Title: ');
  const svg   = await ask('SVG markup: ');
  rl.close();
  const entry = await addGlyph({ title, svg });
  console.log('✅ Added gGlyph:', entry);
})();
