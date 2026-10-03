# anime.js v4 — API reference cheat-sheet

Concise, copy-pasteable snippets for each module. All examples assume ESM
imports from `'animejs'`. Package version: **4.x**. License: MIT.

```js
import {
  animate, createTimeline, createTimer, createAnimatable,
  createDraggable, createScope, onScroll, stagger,
  svg, text, utils, eases, createSpring, engine, waapi,
} from 'animejs';
```

---

## animate(targets, params)

```js
const anim = animate('.box', {
  x: 250,                    // translateX (px)
  y: '2rem',                 // units allowed
  rotate: { from: -90, to: 0 },
  scale: [0.5, 1],          // [from, to]
  opacity: 1,
  backgroundColor: '#FF4B4B',
  duration: 800,             // ms (or engine.timeUnit)
  delay: stagger(60),
  ease: 'outElastic(1, .5)',
  loop: 2,                   // number | true
  alternate: true,
  autoplay: true,            // false | onScroll(...)
  onBegin:  self => {},
  onUpdate: self => {},
  onComplete: self => {},
});

anim.pause(); anim.play(); anim.restart();
anim.reverse(); anim.seek(400); anim.seek(anim.duration * 0.5);
anim.then(() => console.log('finished')); // promise
```

Target types: CSS selector string, Element, NodeList/array, or a plain JS object
(`animate(state, { value: 100 })`). Function-based values:
`x: (el, i, total) => i * 50`.

---

## createTimeline(params)

```js
const tl = createTimeline({
  defaults: { duration: 500, ease: 'inOutQuad' },
  loop: true,
});

tl.add('.a', { x: 100 })            // appended after previous
  .add('.b', { y: 100 }, '-=200')   // start 200ms before prev end (overlap)
  .add('.c', { opacity: 1 }, '+=100')// 100ms gap
  .add('.d', { scale: 2 }, 1000)     // absolute time 1000ms
  .label('mid', 800)                 // named position
  .add('.e', { rotate: 90 }, 'mid');

tl.play(); tl.seek('mid');
```

You can also add timers and call `.set(targets, props, pos)` for instant value
changes within the sequence.

---

## createTimer(params)

No targets — a controllable clock. Good for counters, sync, game loops.

```js
createTimer({
  duration: 1000,
  loop: true,
  frameRate: 30,
  onUpdate: self => { el.textContent = utils.round(self.progress * 100, 0); },
  onLoop: self => {},
});
```

---

## createAnimatable(target, params)

A reusable handle for cheap, frequent updates (no re-instantiation per frame).

```js
const ball = createAnimatable('.ball', {
  x: 0, y: 0,
  ease: 'out(3)',
  duration: 400,
});

window.addEventListener('pointermove', e => {
  ball.x(e.clientX);   // setter animates toward the value
  ball.y(e.clientY);
});
// ball.x() with no arg reads the current value
```

---

## createDraggable(target, params)

```js
const drag = createDraggable('.card', {
  container: '.bounds',          // bounds element or [t,r,b,l]
  x: true, y: true,              // axes (or false to lock)
  snap: 50,                      // grid snap
  releaseStiffness: 40,          // spring on release
  releaseEase: 'out(4)',
  onGrab:    self => {},
  onDrag:    self => {},
  onRelease: self => {},
});
drag.disable(); drag.enable();
```

---

## createScope({ root, mediaQueries })

Group animations, add responsive behavior, and revert everything at once —
ideal for component frameworks.

```js
const scope = createScope({
  root: containerEl,
  mediaQueries: { reduced: '(prefers-reduced-motion: reduce)' },
}).add(self => {
  if (self.matches.reduced) return;        // skip motion
  animate('.item', { y: [20, 0], opacity: [0, 1], delay: stagger(50) });
});

// React/Vue cleanup:
scope.revert();   // stops + resets all animations created in the scope
```

---

## onScroll(params)

Tie playback to scroll. Returns a value usable as `autoplay` (or standalone).

```js
animate('.reveal', {
  opacity: [0, 1], y: [60, 0],
  autoplay: onScroll({
    target: '.reveal',         // observed element (defaults to animation target)
    enter: 'bottom top',       // when bottom of viewport meets top of target
    leave: 'top bottom',
    sync: true,                // scrub with scroll (0..1 = eased smoothing)
    onEnter: () => {},
  }),
});
```

Thresholds use `"<viewport-edge> <target-edge>"` syntax with `+=`/`-=` offsets,
e.g. `'bottom-=100 top'`.

---

## stagger(value, options)

```js
delay: stagger(100)                                  // 0,100,200,...
delay: stagger(100, { start: 500 })                  // 500,600,...
delay: stagger(100, { from: 'center' })              // 'first'|'last'|'center'|index
delay: stagger(100, { from: 'last', ease: 'inQuad' })
delay: stagger(50,  { grid: [cols, rows], from: 'center' })  // 2D grids
x:     stagger([10, 60])                              // value range, not just timing
delay: stagger(100, { reversed: true })
```

---

## svg helpers

```js
import { animate, svg } from 'animejs';

// Line drawing (stroke-dash): value is "start end" in 0..1
animate(svg.createDrawable('.path'), { draw: ['0 0', '0 1'], duration: 2000 });

// Morph one path into another
animate('#from', { points: svg.morphTo('#to'), duration: 1000, ease: 'inOutQuad' });

// Move an element along a path
const { translateX, translateY, rotate } = svg.createMotionPath('.track');
animate('.dot', { translateX, translateY, rotate, duration: 3000, loop: true });
```

---

## text.split

```js
import { animate, text, stagger } from 'animejs';

const { chars, words, lines } = text.split('.headline', { words: true, chars: true });
animate(chars, { y: [20, 0], opacity: [0, 1], delay: stagger(30) });
```

---

## utils

```js
utils.$('.box');                 // query → array of elements
utils.get(el, 'x');              // read current animated value
utils.set('.box', { x: 100, opacity: 0 });   // set instantly (no animation)
utils.remove('.box');            // cancel animations on targets
utils.clamp(v, 0, 1);
utils.round(v, 2);
utils.mapRange(v, 0, 100, 0, 1);
utils.lerp(a, b, t);
utils.random(0, 10, /*decimals*/ 0);
utils.snap(v, 5);
utils.shuffle(array);
```

---

## eases & createSpring

Built-in names (use bare, no `ease` prefix): `linear`, `inQuad`/`outQuad`/
`inOutQuad` (and Cubic, Quart, Quint, Sine, Expo, Circ, Back, Elastic, Bounce),
plus parameterized forms like `'out(3)'`, `'outElastic(1, .3)'`, `'inOutBack'`.

```js
import { createSpring } from 'animejs';
animate('.box', { x: 300, ease: createSpring({ stiffness: 120, damping: 12 }) });

// Custom ease function:
animate('.box', { x: 300, ease: t => t * t });
// Stepped:
animate('.box', { x: 300, ease: 'steps(5)' });
```

---

## engine (global config)

```js
import { engine } from 'animejs';
engine.timeUnit = 's';     // use seconds instead of ms
engine.fps = 60;           // cap frame rate
engine.speed = 0.5;        // global slow-mo (debugging)
engine.pauseOnDocumentHidden = true;
```

---

## waapi (Web Animations API renderer)

For GPU-offloaded transform/opacity animations that keep running off the main
thread:

```js
import { waapi } from 'animejs';
waapi.animate('.box', { transform: 'translateX(300px)', duration: 600 });
```

---

## Quick troubleshooting

- **Nothing moves** — check the selector matches and the element is in the DOM
  *before* `animate()` runs.
- **Jumpy/janky** — animate `transform`/`opacity`, not `width`/`top`/`left`.
- **Wrong easing name** — v4 dropped the `ease`/`easeInOut` prefixes
  (`easeInOutQuad` → `inOutQuad`).
- **Leaks on re-render** — use `createScope` + `.revert()`, or call the
  animation's `.revert()` in your framework's cleanup.
- **v3 code errors** — you're calling `anime({...})`; switch to the named v4
  factories. See the migration list in SKILL.md.
