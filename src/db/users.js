import { Low } from 'lowdb';
import { JSONFile } from 'lowdb/node';
const adapter = new JSONFile('data/users.json');
const db      = new Low(adapter, { users: [] });

export async function initUserDB() { await db.read(); await db.write(); }
export async function getUser(id) { await db.read(); return db.data.users.find(u => u.id === id); }
export async function saveUser(u) { await db.read(); const i = db.data.users.findIndex(x => x.id===u.id); if(i>-1) db.data.users[i]=u; else db.data.users.push(u); await db.write(); }
export async function updateUserStats(userId, gGlyphCounts, emotions) {
  let user = await getUser(userId);
  if(!user) user = { id: userId, mask:'', dreamSeeds:[], gGlyphFrequency:{}, emotionFrequency:{}, lastUpdated:'' };
  user.dreamSeeds.push(userId);
  Object.entries(gGlyphCounts||{}).forEach(([k,v]) => user.gGlyphFrequency[k]=(user.gGlyphFrequency[k]||0)+v);
  emotions.forEach(e => user.emotionFrequency[e]=(user.emotionFrequency[e]||0)+1);
  user.lastUpdated = new Date().toISOString();
  await saveUser(user);
  return user;
}
