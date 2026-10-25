import { readFileSync, writeFileSync } from 'node:fs';

for(const language of ['ru','en','ka']){
  const file=new URL(`../${language}/kakheti-wine-house/index.html`,import.meta.url);
  const current=readFileSync(file,'utf8');
  const needle='<script src="/assets/kakheti-motion.js?v=2" defer></script>';
  if(!current.includes(needle))throw Error('Missing original motion script in '+language);
  const updated=current.replace('kakheti-motion.css?v=2','kakheti-motion.css?v=3')
    .replace(needle,'<script src="/assets/kakheti-webgl.js?v=1" defer></script><script src="/assets/kakheti-motion.js?v=3" defer></script>');
  writeFileSync(file,updated);
  process.stdout.write(language+': glTF renderer activated\n');
}
