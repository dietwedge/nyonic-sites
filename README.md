# rivalstd-landing

Marketing site for **Rivals Tournament Director**, the desktop tournament console
at `../rivals-tournament-director`.

One static file. No build step, no framework, no dependencies — open
`index.html` and it works.

## Why this exists

The original landing page was a Next.js app deployed to `rivalstd.vercel.app` on
2026-08-11 from a **second Vercel account** — not the one holding the other 38
projects. It was effectively unreachable: not in the `Jason's projects` team, not
under the `dietwedge` GitHub org, and never on this machine. It sat at
`BUILD 0.1` for a month while the app shipped online check-in, a public
scoreboard and AI features, so the product page described a version that no
longer existed.

It was found and deleted on 2026-09-10, which released the `rivalstd.vercel.app`
subdomain — `*.vercel.app` names are globally unique, so the old project had been
holding it hostage.

This is a rebuild from the live page's own markup plus the full-resolution
screenshot at `../launch-day/_asset-originals/work-rivalstd.png`. Same visual
identity, corrected copy, one static file instead of a Next.js app, and now
version-controlled so it can be updated whenever RTD ships.

## Deploying

The Vercel project is **`rivalstd`** in the `jasons-projects-b8ef8e9d` team,
linked to this repo. **Pushing to `main` deploys it** — there is no CLI step and
no build.

Note that renaming a Vercel project does not re-alias existing deployments; the
new hostname only attaches to the next deploy.

## Design notes

The palette and type are RTD's own, not the GrowTrackr design system in
`~/.claude/DESIGN.md` — that one is green/navy and belongs to a different
product. What carries over from it is the principles: one dominant action per
section, 44px minimum targets, AA contrast, reduced-motion support.

Copy follows `~/.claude/VOICE.md`.

| Token | Value | Use |
|---|---|---|
| `--paper` | `#F3F0E9` | Page ground |
| `--ink` | `#0E0E0E` | Type, buttons, status bar |
| `--coral` | `#FF5A45` | Display italic, offset block, accents |
| `--lime` | `#C6F24E` | Logo mark, marquee, feature tier CTA |
| `--shell` | `#0E141C` | App mockup surface |

Display face is **Archivo** variable (weight + width + italic) from Google
Fonts — one request. Mono labels use the system stack, so nothing else is
fetched.

The control-room mockup in the hero is **built in HTML/CSS, not a screenshot**,
so it stays accurate as the app changes and stays crisp at any size.

## What to keep in sync with the app

When RTD ships, these go stale first:

- The build number in the status strip (`BUILD 0.2.1 // DESKTOP`)
- The module count and cards in `#toolkit`
- The three columns in `#roadmap`
- The feature list in the Organizer tier

## The email form

`mailto:jason@nyonic.com`, matching the contact address already published on the
NYONIC site. It opens the visitor's mail app — no list, no tracking, no service
to maintain.

The original form had **no backend at all** (`/api/subscribe`, `/api/signup`,
`/api/waitlist`, `/api/early-access` and `/api/email` all returned 404), so
nothing was ever being collected. To capture properly later, swap the `<form>`
action for a real endpoint.

## Local preview

```
npx serve rivalstd-landing -l 5188
```

Or `preview_start` with the `rivalstd` config in `../.claude/launch.json`.
