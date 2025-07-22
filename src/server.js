#!/usr/bin/env node
import express from 'express';
import { initGlyphDB, addGlyph, listGlyphs }   from './db/genericGlyphs.js';
import { initDreamDB, addDream, listDreams }   from './db/dreamSeeds.js';
import { initUserDB }                         from './db/users.js';

(async()=>{
  await initGlyphDB(); await initDreamDB(); await initUserDB();
  const app = express(); app.use(express.json());
  app.post('/gGlyphs', async (req,res)=>res.json(await addGlyph(req.body)));
  app.get ('/gGlyphs', async (_ ,res)=>res.json(await listGlyphs()));
  app.post('/dGlyphs', async (req,res)=>res.json(await addDream(req.body)));
  app.get ('/dGlyphs', async (_ ,res)=>res.json(await listDreams()));
  app.listen(3000,()=>console.log('API on http://localhost:3000'));
})();
