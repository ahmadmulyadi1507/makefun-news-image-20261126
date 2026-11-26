// make.fun entry: "Sum up 26 November's world news in one image"
// (news-image-20261126). Node 22, standard library only. The image is the
// entry.png beside this file, drawn from scratch for this competition, and
// the program copies it to /output/entry.png. The gate takes a whole PNG of
// at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the
// bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
copyFileSync(new URL('./entry.png', import.meta.url), dest);

// The gate takes at most 1 MiB and 1024 by 1024 pixels: fail loudly here
// rather than submitting a file the gate would refuse.
const size = statSync(dest).size;
if (size > 1048576) throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
