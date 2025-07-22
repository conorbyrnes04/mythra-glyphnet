import { Low } from 'lowdb';
import { JSONFile } from 'lowdb/node';
import { updateUserStats } from './users.js';
const adapter = new JSONFile('data/dreamSeeds.json');
const db      = new Low(adapter, { dGlyphs: [] });

export async function initDreamDB() { await db.read(); await db.write(); }
export async function addDream(s)   { await db.read(); const entry = { id: \`dream_\${Date.now()}\`, ...s }; db.data.dGlyphs.push(entry); await db.write(); await updateUserStats(entry.userId, entry.gGlyphCounts, entry.extractedEmotions); return entry; }
export async function listDreams()  { await db.read(); return db.data.dGlyphs; }
