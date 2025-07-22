#!/usr/bin/env node
import { Command } from 'commander';
import seedSimple   from './seedSimple.js';
import { listGlyphs }   from './db/genericGlyphs.js';
import { listDreams }   from './db/dreamSeeds.js';
import startServer  from './server.js';

const program = new Command();
program.name('glyph-db').description('Manage gGlyphs & dGlyphs');
program.command('seed-g').action(()=>seedSimple());
program.command('list-g').action(async()=>console.table(await listGlyphs()));
program.command('list-d').action(async()=>console.table(await listDreams()));
program.command('serve').action(()=>startServer());
program.parse(process.argv);
