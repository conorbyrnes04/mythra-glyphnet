import { Low } from 'lowdb';
import { JSONFile } from 'lowdb/node';

// Use a JSON file in the project’s data folder
const adapter = new JSONFile('data/genericGlyphs.json');
// Initialize with an empty array if the file is missing or empty
const db = new Low(adapter, { gGlyphs: [] });

export async function initGlyphDB() {
  await db.read();
  await db.write();
}

export async function addGlyph(glyph) {
  await db.read();
  // generate an ASCII-only ID string
  const entry = {
    id: 'gGlyph_' + Date.now().toString(),
    ...glyph
  };
  db.data.gGlyphs.push(entry);
  await db.write();
  return entry;
}

export async function listGlyphs() {
  await db.read();
  return db.data.gGlyphs;
}
