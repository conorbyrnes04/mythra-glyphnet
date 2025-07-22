#!/usr/bin/env node
import { listGlyphs } from './db/genericGlyphs.js';
(async()=>console.table(await listGlyphs()))();
