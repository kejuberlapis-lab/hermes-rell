---
name: animejs
description: Build web animations with anime.js v4 — a fast, lightweight JavaScript animation library. Use this skill whenever the user wants to animate DOM elements, CSS properties, SVG (morphing, line drawing, motion paths), or plain JS objects; build timelines, staggered effects, scroll-triggered animations, draggable elements, spring physics, or animated text. Covers the v4 module API (animate, createTimeline, createTimer, createDraggable, onScroll, svg, text, stagger, utils, eases) and how to install it via npm or a CDN.
version: 1.0.0
author: Julian Garnier (upstream anime.js, MIT); skill packaged by Rinu (l3ad3r1) with Claude (Anthropic)
license: MIT
platforms:
- linux
- macos
- windows
metadata:
  hermes:
    tags:
    - Animation
    - anime.js
    - SVG
    - Web
    - Frontend
    related_skills: []
---

# anime.js (v4)

[anime.js](https://animejs.com) is a fast, lightweight JavaScript animation
library with a small, composable API. **v4** is a ground-up rewrite: it is
**modular and ESM-first** — you import named functions (`animate`,
`createTimeline`, …) rather than calling a single default `anime()` object as in
v3. Always write v4-style code unless the user explicitly pins v3.

## When to use this skill

- "Animate this element / these cards / this SVG."
- "Make a timeline that sequences several animations."
- "Add a staggered entrance / scroll-reveal / hover effect."
- "Morph this SVG path into that one" or "draw this SVG line on scroll."
- "Make this element draggable with momentum / springy motion."
- "Animate text in character by character."
- Any request to add motion to a web page, or to debug/upgrade existing anime.js.

If the user is on **v3** (default `anime({...})` syntax) and wants to upgrade,
see the [Migration](#migrating-from-v3) notes below.

## Install / import

**npm (recommended, ESM):**

```bash
npm install animejs
```

```js
import { animate, createTimeline, stagger, svg, utils } from 'animejs';
```

**CDN — ES modules (no build step):**

```html
<script type="module">
  import { animate, stagger } from 'https://esm.sh/animejs@4';
  animate('.box', { x: 200, duration: 800 });
</script>
```

**CDN — classic UMD global** (`anime` namespace; methods hang off it):

```html
<script src="https://cdn.jsdelivr.net/npm/animejs@4"></script>
<script>
  anime.animate('.box', { x: 200, rotate: '1turn', duration: 800 });
</script>
```

TypeScript types ship with the package — no `@types` needed.

## Core mental model

Every animatable thing is created by a factory function that returns an object
with **playback controls** (`.play()`, `.pause()`, `.restart()`, `.seek()`,
`.reverse()`, plus a `.then()`/`completed` promise). You target **CSS
selectors, DOM nodes, NodeLists, or plain JS objects**.

```js
animate(targets, {
  // properties to animate (CSS, transforms, attributes, or object keys)
  x: 320,                         // translateX shorthand
  rotate: { from: -180 },         // per-property keyframe object
  opacity: [0, 1],               // [from, to]
  // timing & behavior
  duration: 1250,
  delay: stagger(65, { from: 'center' }),
  ease: 'inOutQuint',
  loop: true,
  alternate: true,
  // callbacks
  onComplete: self => console.log('done', self),
});
```

Key shorthands: `x`/`y`/`z` (translate), `rotate`, `scale`, `skew`. Values can be
numbers (px assumed), units (`'50%'`, `'2rem'`, `'1turn'`), `[from, to]` arrays,
`{ from, to }` objects, function values `(el, i) => ...`, or relative strings
(`'+=100'`).

## The v4 modules

| Import | Use it for |
|---|---|
| `animate(targets, params)` | The workhorse — animate CSS, transforms, attributes, or JS object properties. |
| `createTimeline(params)` | Sequence/overlap multiple animations with precise offsets via `.add()`/`.sync()`. |
| `createTimer(params)` | A standalone clock (no targets) with `onUpdate`/`onComplete` — great for counters and game loops. |
| `createAnimatable(target, params)` | A persistent handle for high-frequency updates (e.g. cursor-follow) without re-creating animations. |
| `createDraggable(target, params)` | Drag interactions with inertia, snapping, and bounds. |
| `createScope({ root, mediaQueries })` | Scope animations to a root element + responsive media queries; `.revert()` cleans them all up (ideal for React/Vue effects). |
| `onScroll(params)` / scroll thresholds | Drive or trigger animations from scroll position (`enter`/`leave`, `sync`). Pass as a `delay`/`autoplay` or use directly. |
| `svg.morphTo`, `svg.createDrawable`, `svg.createMotionPath` | SVG path morphing, line-drawing (stroke dash), and motion-path following. |
| `text.split` | Split text into lines/words/chars for per-character stagger. |
| `stagger(value, opts)` | Generate incremental delays/values across targets (`from`, `grid`, `ease`, `range`). |
| `utils` | Helpers: `$` (select), `get`/`set`, `remove`, `clamp`, `mapRange`, `lerp`, `round`, `random`, `snap`. |
| `eases` / `createSpring` | Easing functions and spring physics generators. |
| `engine` | Global config: `engine.timeUnit`, `engine.fps`, `engine.speed`, pause-on-tab-blur. |
| `waapi` | Render via the native Web Animations API (`waapi.animate`) for GPU-offloaded transforms. |

For concrete, copy-pasteable snippets of each module, read
[`reference.md`](reference.md). A complete runnable demo (CDN, no build) is in
[`examples/index.html`](examples/index.html).

## Common recipes

**Timeline (sequence + overlap):**

```js
import { createTimeline, stagger } from 'animejs';

const tl = createTimeline({ defaults: { duration: 600, ease: 'outQuad' } });
tl.add('.title', { y: [40, 0], opacity: [0, 1] })
  .add('.card', { scale: [0.8, 1], opacity: [0, 1], delay: stagger(80) }, '-=200') // overlap by 200ms
  .add('.cta',  { opacity: [0, 1] });
```

**Stagger grid:**

```js
animate('.cell', {
  scale: [0, 1],
  delay: stagger(50, { grid: [10, 10], from: 'center' }),
});
```

**Scroll-triggered reveal:**

```js
import { animate, onScroll } from 'animejs';
animate('.section', {
  opacity: [0, 1], y: [50, 0],
  autoplay: onScroll({ enter: 'bottom-=100 top', sync: 0.5 }),
});
```

**SVG line drawing:**

```js
import { animate, svg } from 'animejs';
animate(svg.createDrawable('.path'), { draw: '0 1', duration: 2000, ease: 'inOutQuad' });
```

**Draggable with physics:**

```js
import { createDraggable } from 'animejs';
createDraggable('.box', { container: '.bounds', releaseStiffness: 40, snap: 50 });
```

## Migrating from v3

- v3 `anime({ targets, ... })` → v4 `animate(targets, { ... })` (targets is the
  first arg, not a param).
- v3 `easing: 'easeInOutQuad'` → v4 `ease: 'inOutQuad'` (renamed + shorter names).
- v3 `anime.timeline()` → v4 `createTimeline()`; `.add(params, offset)` →
  `.add(targets, params, offset)`.
- v3 `anime.stagger()` → v4 `stagger()` (named import).
- v3 `anime.set()` / `anime.random()` → v4 `utils.set()` / `utils.random()`.
- `loop`/`direction: 'alternate'` → `loop` + `alternate: true`.
- Full guide: <https://animejs.com/documentation/migrating-from-v3>.

## Tips & gotchas

- **Prefer transforms** (`x`, `y`, `scale`, `rotate`) and `opacity` for smooth,
  GPU-friendly motion; animating `width`/`top`/`left` triggers layout.
- Use `ease: createSpring({ stiffness, damping })` for natural motion instead of
  guessing cubic-bezier values.
- In **React/Vue/Svelte**, wrap creation in an effect and call
  `scope.revert()` (or the returned animation's `.revert()`) on cleanup so you
  don't leak timers across re-renders. `createScope` exists for exactly this.
- Respect `prefers-reduced-motion`: gate non-essential animation behind a media
  query check.
- Animations **autoplay by default**; pass `autoplay: false` and call `.play()`
  to control timing, or `autoplay: onScroll(...)` to tie it to scroll.

## Credits

Powered by [**anime.js**](https://github.com/juliangarnier/anime) (v4, MIT) by
**Julian Garnier**. This skill documents and wraps the library for the Claude
Agent Skills format; all credit for the animation engine belongs to its author
and contributors.
