#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TreeCalls — page builder.

The page is a sibling of PestCalls: same structure and layout, different trade and
palette. Rather than maintain two near-identical HTML files by hand, this takes the
PestCalls page as the base and applies the TreeCalls brand and copy to it.

Brand values come from the brand sheet artifact and are not negotiable here:
  Evergreen      #123B33  handset, trunk text, dark grounds
  Leaf           #92BC12  the leaf; accent on DARK only, never body text on light
  Leaf highlight #DBECAE  the vein — part of the mark only
  Deep leaf      #2E8B6B  "Calls" in the wordmark on light
  Mint           #5FC08D  "Calls" in the wordmark on dark
  Cream          #F4F2EC  reversed handset, page text on dark
  Safety orange  #FF6B1A  buttons and CTAs only — never in the logo

Run:  python build.py
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "_base.html")
LOCK = os.path.join(HERE, "_lockup.svg")
OUT  = os.path.join(HERE, "index.html")

s = io.open(BASE, encoding="utf-8").read()
lockup = io.open(LOCK, encoding="utf-8").read().strip()


def sub(old, new, count=1, label=""):
    """Replace and fail loudly — a silent no-op here ships the wrong trade's copy."""
    global s
    if s.count(old) < count:
        sys.exit("FAILED to find (%s): %r" % (label or "?", old[:90]))
    s = s.replace(old, new, count)


# ---------------------------------------------------------------- palette
# Leaf is chartreuse and illegible as body text on cream, so the light-ground
# accent is Deep leaf. That split is the whole reason --accent-light exists.
sub("--ink:#0E2730;        /* deep slate-teal base */",
    "--ink:#123B33;        /* Evergreen — dark grounds */", label="ink")
sub("--ink-2:#0A1A21;      /* darker slab */",
    "--ink-2:#0D2B25;      /* deeper Evergreen slab */", label="ink2")
sub("--teal:#14A3B8;       /* primary accent */",
    "--leaf:#92BC12;       /* Leaf — accent on DARK only */\n"
    "    --mint:#5FC08D;       /* wordmark 'Calls' on dark */\n"
    "    --deep-leaf:#2E8B6B;  /* accent on LIGHT grounds */", label="accent")
sub("--teal-pale:#CFE9EE;  /* pale wash on dark */",
    "--leaf-hi:#DBECAE;    /* the vein — mark only */", label="pale")

# Every accent usage inherited from PestCalls now resolves to Leaf; the ones that
# sit on cream get corrected to Deep leaf immediately below.
s = s.replace("var(--teal)", "var(--leaf)")
s = s.replace("rgba(20,163,184,", "rgba(146,188,18,")
s = s.replace("#04222A", "#10231D")          # text on accent fills
s = s.replace("--body:#33454C;", "--body:#38493F;")
s = s.replace("--muted:#7C8D94;", "--muted:#7E8F82;")
s = s.replace("--line-dark:rgba(14,39,48,.14);", "--line-dark:rgba(18,59,51,.14);")
s = s.replace("background:rgba(14,39,48,.94)", "background:rgba(18,59,51,.94)")

# Light-ground accents: Deep leaf, per the brand sheet.
sub("""  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--leaf);margin:0 0 .9em
  }""",
    """  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--deep-leaf);margin:0 0 .9em
  }
  .dark .label,.hero .label{color:var(--leaf)}""", label="label split")

sub("""  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--leaf);border-bottom:2.5px solid var(--leaf);
    transform:rotate(-45deg)
  }""",
    """  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--deep-leaf);border-bottom:2.5px solid var(--deep-leaf);
    transform:rotate(-45deg)
  }
  .dark ul.ticks li::before{border-color:var(--leaf)}""", label="ticks split")

sub("summary::after{content:\"+\";margin-left:auto;color:var(--leaf);",
    "summary::after{content:\"+\";margin-left:auto;color:var(--deep-leaf);", label="summary marker")

# ---------------------------------------------------------------- logo
# The real lockup replaces whatever mark the base is carrying. Matched by regex
# rather than by literal: the PestCalls mark has already changed once (improvised
# handset -> handset and shield) and a literal match rots silently when it does.
_head = re.search(r'    <a class="logo" href="/">.*?    </a>', s, re.S)
if not _head:
    sys.exit("header logo block not found")
s = s.replace(_head.group(0), """    <a class="logo lockup" href="/" aria-label="TreeCalls">
      """ + lockup + """
    </a>""", 1)

_foot = re.search(r'      <a class="logo" href="/" style="font-size:1rem">.*?      </a>', s, re.S)
if not _foot:
    sys.exit("footer logo block not found")
s = s.replace(_foot.group(0), """      <a class="logo lockup sm" href="/" aria-label="TreeCalls">
        """ + lockup + """
      </a>""", 1)

sub("  .logo svg{width:29px;height:29px;flex:none}",
    "  .logo svg{width:29px;height:29px;flex:none}\n"
    "  .logo.lockup svg{width:auto;height:34px}\n"
    "  .logo.lockup.sm svg{height:26px}", label="lockup sizing")

FAVICON = ("%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%23123B33'/"
           "%3E%3Cpath d='M18 16c-2 0-4 2-4 4 0 14 12 26 26 26 2 0 4-2 4-4v-5l-9-3-4 4c-5-3-9-7-11-12l4-4-3-10z' fill='%23F4F2EC'/%3E%3Cpath d='M40 12c8 0 13 5 13 13 0 5-4 9-9 9-6 0-10-5-10-11 0-6 3-11 6-11z' fill='%2392BC12'/%3E%3C/svg%3E")
# Favicon: handset + leaf in the brand colours. Located by position, not by
# literal, for the same reason as the logo above.
_fav_i = s.find('<link rel="icon"')
if _fav_i < 0:
    sys.exit("favicon link not found")
_fav = s[_fav_i:s.find('>', _fav_i) + 1]
s = s.replace(_fav, "<link rel=\"icon\" href=\"data:image/svg+xml," + FAVICON + "\">", 1)

# ---------------------------------------------------------------- head
sub("<title>PestCalls — Every missed call, answered | NYONIC</title>",
    "<title>TreeCalls — Every missed call, answered | NYONIC</title>", label="title")
sub('content="24/7 call answering and booking for pest control companies. Every after-hours call answered, qualified, and booked into your calendar before the caller dials the next company."',
    'content="24/7 call answering and booking for tree services. Every storm call and after-hours estimate answered, qualified, and booked while the crew is still in the tree."',
    label="meta desc")
sub('<meta name="theme-color" content="#0E2730">',
    '<meta name="theme-color" content="#123B33">', label="theme colour")
sub('<meta property="og:title" content="PestCalls — Every missed call, answered">',
    '<meta property="og:title" content="TreeCalls — Every missed call, answered">', label="og title")
sub('<meta property="og:description" content="The 9pm call doesn\'t wait until Monday. PestCalls answers it, qualifies it, and books it.">',
    '<meta property="og:description" content="The limb comes down at 9pm. So does the phone call. TreeCalls answers it, qualifies it, and books the estimate.">',
    label="og desc")

# ---------------------------------------------------------------- hero
sub('<p class="label">24/7 call answering for pest control</p>',
    '<p class="label">24/7 call answering for tree services</p>', label="hero label")
sub("<h1>The 9pm call doesn't wait until Monday.</h1>",
    "<h1>The limb comes down at 9pm. So does the phone call.</h1>", label="h1")
sub('<p class="lede">Wasps in a kid\'s bedroom wall. Mice in the kitchen the night before a party. Those callers are not leaving a voicemail — they are dialing the next company on the list about ninety seconds later.</p>',
    '<p class="lede">A storm splits an oak over the driveway. A dead limb is resting on the garage roof. Nobody with a tree on their house leaves a voicemail — they work down the search results until a human picks up.</p>',
    label="hero lede 1")
sub('<p class="lede">PestCalls answers every one of those calls, around the clock, asks what your estimator would ask, and puts the job on your calendar before you have picked up the phone.</p>',
    '<p class="lede">TreeCalls answers every one of those calls, around the clock, asks what your estimator would ask, and puts the assessment on your calendar while your crew is still eighty feet up.</p>',
    label="hero lede 2")

# ---------------------------------------------------------------- transcript
sub('<div class="phone-top"><span class="dot"></span> Saturday · 9:14 PM · inbound</div>',
    '<div class="phone-top"><span class="dot"></span> Saturday · 9:06 PM · inbound</div>', label="transcript time")
sub('<span class="bub">Hi — we\'ve got bees or wasps or something going in and out of the siding by our back door. There\'s a lot of them. We\'ve got a two-year-old.</span>',
    '<span class="bub">We just had a big limb come down off the maple in the front yard. Part of it\'s still hanging up in the tree over the driveway. I don\'t want to park under it.</span>',
    label="msg 1")
sub('<span class="bub">That sounds like it needs looking at quickly. I\'m the automated line for <span class="co">Northside Pest Control</span> — I\'ll take the details and get you on the schedule. Are they going into the siding itself, or a hole in the trim?</span>',
    '<span class="bub">A hanger over a driveway is worth looking at quickly. I\'m the automated line for <span class="co">Northside Tree Service</span> — I\'ll take the details and get you on the schedule. Is any of it touching the house, wires, or a fence?</span>',
    label="msg 2")
sub('<span class="bub">Into the siding, right at the corner. Been getting worse for about a week.</span>',
    '<span class="bub">Not the house. It\'s maybe ten feet from the power line coming in though.</span>', label="msg 3")
sub('<span class="bub">Got it. Anyone in the house allergic to stings? And is a technician able to get to the back of the property without going through a locked gate?</span>',
    '<span class="bub">Noted — I\'ll flag the line for the estimator. Roughly how big around is the limb, and can a truck get up the driveway past it?</span>',
    label="msg 4")
sub('<span class="bub">No allergies. Gate\'s unlocked, it\'s the grey house on Elm.</span>',
    '<span class="bub">Maybe a foot thick. Truck can get up, there\'s room on the left.</span>', label="msg 5")
sub('<div class="h"><span class="dot"></span> Booked · sent to the crew at 9:17 PM</div>',
    '<div class="h"><span class="dot"></span> Booked · sent to the crew at 9:09 PM</div>', label="booked time")
sub("""          <dt>Job</dt><dd>Stinging insect — nest in siding, rear corner</dd>
          <dt>Urgency</dt><dd>High — young child on site</dd>
          <dt>Access</dt><dd>Unlocked gate, rear of property</dd>
          <dt>Slot</dt><dd>Monday 8:00–10:00 AM</dd>""",
    """          <dt>Job</dt><dd>Hanger over driveway — maple, ~12in limb</dd>
          <dt>Hazard</dt><dd>Service drop within 10ft — estimator to confirm</dd>
          <dt>Access</dt><dd>Truck can pass on the left</dd>
          <dt>Slot</dt><dd>Monday 8:00–10:00 AM assessment</dd>""", label="booked card")

# Speaker labels in the transcript.
sub('<span class="who">PestCalls</span>', '<span class="who">TreeCalls</span>',
    count=2, label="transcript speaker labels")

# ---------------------------------------------------------------- problem
sub("<h2 style=\"max-width:20ch\">You don't lose those jobs on price. You lose them on silence.</h2>",
    "<h2 style=\"max-width:21ch\">You don't lose those jobs on price. You lose them on silence.</h2>", label="problem h2")
sub("<p>Pest work is different from most trades. Nobody books it a month out. Something appears in a wall or a bedroom, the caller wants it gone tonight, and they will keep dialing until a human answers.</p>",
    "<p>Tree work is different from most trades. Nobody plans it. A storm goes through on a Friday night and by Saturday morning every company in the county is getting the same calls from the same three streets.</p>",
    label="problem p1")
sub("<p>Meanwhile you are on a roofline, under a crawlspace, driving, or asleep — all of which are the correct places to be. The call does not go unanswered because you stopped caring. It goes unanswered because you were doing the job.</p>",
    "<p>Meanwhile you are eighty feet up with a saw running, or driving a chipper, or asleep after a fourteen-hour day — all of which are the correct places to be. The call does not go unanswered because you stopped caring. It goes unanswered because you were doing the job.</p>",
    label="problem p2")
sub("<p>By the time you clear the voicemail on Monday, somebody else has already treated the nest and picked up the quarterly contract that came with it.</p>",
    "<p>By the time you clear the voicemail on Monday, somebody else has already quoted the removal, taken the deposit, and picked up the stump grinding and the two neighbours who watched them work.</p>",
    label="problem p3")
sub("<h3>What one missed Saturday costs</h3>",
    "<h3>What one missed storm weekend costs</h3>", label="cost h3")
sub('<p style="margin-top:10px">A single stinging-insect callout is a few hundred dollars. The customer who liked how fast you answered is worth a recurring plan, and every neighbor they tell.</p>',
    '<p style="margin-top:10px">A single removal runs into the thousands. The customer who liked how fast you answered is worth the stump, the pruning next spring, and every neighbour who saw the truck.</p>',
    label="cost p")

# ---------------------------------------------------------------- how it works
sub("<p>Keep your number. Calls ring you first — after hours, or after a set number of rings, they come to PestCalls instead of voicemail. Nothing on your phone changes.</p>",
    "<p>Keep your number. Calls ring you first — after hours, or after a set number of rings, they come to TreeCalls instead of voicemail. Nothing on your phone changes.</p>",
    label="step 1")
sub("<p>Pest and location, how long it's been going on, allergies and pets, access to the property, whether it's a rental. We write those questions with you, in your first week.</p>",
    "<p>Species and rough size, what it's leaning over, proximity to wires and structures, whether a truck and chipper can get in, storm damage or planned work. We write those questions with you, in your first week.</p>",
    label="step 2")
sub("<h3>The job lands booked</h3>", "<h3>The assessment lands booked</h3>", label="step 3 h3")

# ---------------------------------------------------------------- included
sub("<li>Answered 24/7 — nights, weekends, holidays, and the middle of a treatment</li>",
    "<li>Answered 24/7 — nights, weekends, holidays, and the middle of a climb</li>", label="inc 1")
sub("<li>Overflow cover during the day, so a busy signal never happens</li>",
    "<li>Storm surge cover — a hundred calls in a morning is the same to it as one</li>", label="inc 2")
sub("<li>Job details texted to whoever is on call</li>",
    "<li>Job details and hazards texted to whoever is on call</li>", label="inc 3")

# ---------------------------------------------------------------- what it isn't
sub("<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. Your customers are not typing at 9pm. They are calling.</p>",
    "<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. Nobody types out a description of the tree on their roof. They call.</p>",
    label="isnt p1")
sub("<p><strong style=\"color:var(--ink)\">It never quotes a price.</strong> It gathers, it books, it hands over. Anything that commits you to a number or a promise routes to a human first.</p>",
    "<p><strong style=\"color:var(--ink)\">It never quotes a price.</strong> Tree work is priced on site, by somebody who has looked at the lean and the drop zone. It gathers, it books, it hands over — anything that commits you to a number routes to a human first.</p>",
    label="isnt p2")

# ---------------------------------------------------------------- terms + faq
sub("<li>Priced on call volume and how many trucks it books for. Told to you before you commit, not after.</li>",
    "<li>Priced on call volume and how many crews it books for. Told to you before you commit, not after.</li>", label="terms")
sub("<p>It hands off. Anything unusual, angry, or outside what we set up gets routed to a real person or flagged for a callback first thing, with the recording attached. It is built to know its edges.</p>",
    "<p>It hands off. Anything unusual, angry, or outside what we set up — an emergency with wires down, say — gets routed to a real person or flagged for a callback first thing, with the recording attached. It is built to know its edges.</p>",
    label="faq handoff")
sub("<p>They are yours. You get every call, every transcript, and the customer list, exported whenever you ask. Nothing about this is designed to make leaving difficult.</p>",
    "<p>They are yours. You get every call, every transcript, and the customer list, exported whenever you ask. Nothing about this is designed to make leaving difficult.</p>",
    label="faq recordings")
sub("<p>We agree the number before anything is built — after-hours calls answered, jobs booked without a human, callbacks avoided. If that number hasn't moved in the first month, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    "<p>We agree the number before anything is built — after-hours calls answered, assessments booked without a human, callbacks avoided. If that number hasn't moved in the first month, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    label="faq measure")

# ---------------------------------------------------------------- CTA + footer
sub("<h2>Tell me what happens to a 9pm call today.</h2>",
    "<h2>Tell me what happens to a storm call today.</h2>", label="cta h2")
sub('mailto:jason@nyonic.com?subject=PestCalls">Email me</a>',
    'mailto:jason@nyonic.com?subject=TreeCalls">Email me</a>', label="cta mail")
sub('<p class="fnote center" style="margin-inline:auto">PestCalls is a NYONIC product.',
    '<p class="fnote center" style="margin-inline:auto">TreeCalls is a NYONIC product.', label="fnote")
sub('<a href="mailto:jason@nyonic.com?subject=PestCalls">jason@nyonic.com</a>',
    '<a href="mailto:jason@nyonic.com?subject=TreeCalls">jason@nyonic.com</a>', label="footer mail")

# ---------------------------------------------------------------- script
s = s.replace('"PestCalls for "', '"TreeCalls for "')
s = s.replace('"PestCalls — "', '"TreeCalls — "')
s = s.replace("// Personalized banner: /?for=Magnum%20Pest%20Control",
              "// Personalized banner: /?for=Some%20Tree%20Service")

# Anything left mentioning the other trade is a miss in this script, not a choice.
leftover = re.findall(r"PestCalls|pest control|pest technician", s, re.I)
if leftover:
    sys.exit("Untranslated PestCalls copy remains: %r" % (set(leftover),))

io.open(OUT, "w", encoding="utf-8", newline="").write(s)
print("wrote %s (%d bytes)" % (OUT, len(s.encode("utf-8"))))
