#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SnowCalls — page builder.

Fourth in the [Trade]Calls family. Takes the PestCalls page as `_base.html` and applies
the SnowCalls brand and copy. Every `sub()` fails loudly; the file refuses to write if
any pest-control wording survives.

Palette: midnight navy base, deliberately bluer than PestCalls' slate-teal so the two do
not read as the same card in the NYONIC row. Ice blue splits by ground (#8FD8F2 on dark,
#0E6B96 on light — the pale ice fails contrast on cream). Cream and safety orange carry
across from the family; orange happens to read as a plow beacon here, so unlike
PizzaCalls there was no reason to break the CTA rule.

Run:  python build.py
"""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "_base.html")
OUT  = os.path.join(HERE, "index.html")

s = io.open(BASE, encoding="utf-8").read()


def sub(old, new, count=1, label=""):
    global s
    if s.count(old) < count:
        sys.exit("FAILED to find (%s): %r" % (label or "?", old[:90]))
    s = s.replace(old, new, count)


# ---------------------------------------------------------------- palette
sub("--ink:#0E2730;        /* deep slate-teal base */",
    "--ink:#0D1830;        /* midnight navy */", label="ink")
sub("--ink-2:#0A1A21;      /* darker slab */",
    "--ink-2:#08101F;      /* deeper night slab */", label="ink2")
sub("--teal:#14A3B8;       /* primary accent */",
    "--ice:#8FD8F2;        /* pale ice — accent on DARK grounds */\n"
    "    --ice-mid:#5FC0E4;    /* fills and wordmark on dark */\n"
    "    --ice-dk:#0E6B96;     /* accent on LIGHT grounds — contrast-checked */",
    label="accent")
sub("--teal-pale:#CFE9EE;  /* pale wash on dark */",
    "--frost:#DCEEF8;      /* frost wash */", label="pale")

s = s.replace("var(--teal)", "var(--ice-mid)")
s = s.replace("rgba(20,163,184,", "rgba(95,192,228,")
s = s.replace("#04222A", "#08182B")
s = s.replace("--body:#33454C;", "--body:#3A4455;")
s = s.replace("--muted:#7C8D94;", "--muted:#7C8BA6;")
s = s.replace("--line-dark:rgba(14,39,48,.14);", "--line-dark:rgba(13,24,48,.14);")
s = s.replace("background:rgba(14,39,48,.94)", "background:rgba(13,24,48,.94)")

# Light-ground accents need the darker ice.
sub("""  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--ice-mid);margin:0 0 .9em
  }""",
    """  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--ice-dk);margin:0 0 .9em
  }
  .dark .label,.hero .label{color:var(--ice)}""", label="label split")

sub("""  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--ice-mid);border-bottom:2.5px solid var(--ice-mid);
    transform:rotate(-45deg)
  }""",
    """  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--ice-dk);border-bottom:2.5px solid var(--ice-dk);
    transform:rotate(-45deg)
  }
  .dark ul.ticks li::before{border-color:var(--ice)}""", label="ticks split")

sub("summary::after{content:\"+\";margin-left:auto;color:var(--ice-mid);",
    "summary::after{content:\"+\";margin-left:auto;color:var(--ice-dk);", label="summary marker")

# ---------------------------------------------------------------- mark
FLAKE_G = ('      <g stroke="#8FD8F2" stroke-width="3.7" stroke-linecap="round" fill="none">\n'
           '        <path d="M44 4.5 v31 M30.6 12.25 L57.4 27.75 M30.6 27.75 L57.4 12.25"/>\n'
           '        <path d="M40 8.6 L44 12 L48 8.6 M40 31.4 L44 28 L48 31.4"/>\n'
           '        <path d="M33.2 16.6 L34.9 21.5 L30 22.3 M54.8 23.4 L53.1 18.5 L58 17.7"/>\n'
           '        <path d="M30 17.7 L34.9 18.5 L33.2 23.4 M58 22.3 L53.1 21.5 L54.8 16.6"/>\n'
           '      </g>')
FLAKE_INLINE = ('<g stroke="#8FD8F2" stroke-width="3.7" stroke-linecap="round" fill="none">'
                '<path d="M44 4.5 v31 M30.6 12.25 L57.4 27.75 M30.6 27.75 L57.4 12.25"/>'
                '<path d="M40 8.6 L44 12 L48 8.6 M40 31.4 L44 28 L48 31.4"/>'
                '<path d="M33.2 16.6 L34.9 21.5 L30 22.3 M54.8 23.4 L53.1 18.5 L58 17.7"/>'
                '<path d="M30 17.7 L34.9 18.5 L33.2 23.4 M58 22.3 L53.1 21.5 L54.8 16.6"/></g>')
PHONE = ('M16.5 20c-2.4 0-4.6 2.2-4.6 4.6 0 15.6 13.4 29 29 29 2.4 0 4.6-2.2 4.6-4.6'
         'v-5.6l-10.1-3.4-4.5 4.5c-5.6-3.4-10.1-7.9-13.5-13.5l4.5-4.5z')

# Located structurally, not by literal — the base mark has changed before.
_head = re.search(r'      <svg viewBox="0 0 64 64" aria-hidden="true">.*?      </svg>', s, re.S)
if not _head:
    sys.exit("header mark not found")
s = s.replace(_head.group(0),
    '      <svg viewBox="0 0 64 64" aria-hidden="true">\n' + FLAKE_G +
    '\n      <path d="' + PHONE + '" fill="#F4F2EC"/>\n      </svg>', 1)

_foot = re.search(r'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M44 5.*?</svg>', s, re.S)
if not _foot:
    sys.exit("footer mark not found")
s = s.replace(_foot.group(0),
    '<svg viewBox="0 0 64 64" aria-hidden="true">' + FLAKE_INLINE +
    '<path d="' + PHONE + '" fill="#F4F2EC"/></svg>', 1)

_fav_i = s.find('<link rel="icon"')
if _fav_i < 0:
    sys.exit("favicon link not found")
_fav = s[_fav_i:s.find('>', _fav_i) + 1]
s = s.replace(_fav,
  "<link rel=\"icon\" href=\"data:image/svg+xml,"
  "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
  "%3Crect width='64' height='64' rx='14' fill='%230D1830'/%3E"
  "%3Cg transform='translate(32,32) scale(.78) translate(-32,-32)'%3E"
  "%3Cg stroke='%238FD8F2' stroke-width='3.7' stroke-linecap='round' fill='none'%3E"
  "%3Cpath d='M44 4.5 v31 M30.6 12.25 L57.4 27.75 M30.6 27.75 L57.4 12.25'/%3E"
  "%3Cpath d='M40 8.6 L44 12 L48 8.6 M40 31.4 L44 28 L48 31.4'/%3E%3C/g%3E"
  "%3Cpath d='" + PHONE + "' fill='%23F4F2EC'/%3E%3C/g%3E%3C/svg%3E\">", 1)

# ---------------------------------------------------------------- wordmark
sub("<span>Pest<b>Calls</b></span>", "<span>Snow<b>Calls</b></span>", count=2, label="wordmark")

# ---------------------------------------------------------------- head
sub("<title>PestCalls — Every missed call, answered | NYONIC</title>",
    "<title>SnowCalls — Every missed call, answered | NYONIC</title>", label="title")
sub('content="24/7 call answering and booking for pest control companies. Every after-hours call answered, qualified, and booked into your calendar before the caller dials the next company."',
    'content="24/7 storm line for snow removal contractors. Every 3am plow call answered, qualified and dispatched while you are still in the truck."',
    label="meta desc")
sub('<meta name="theme-color" content="#0E2730">',
    '<meta name="theme-color" content="#0D1830">', label="theme colour")
sub('<meta property="og:title" content="PestCalls — Every missed call, answered">',
    '<meta property="og:title" content="SnowCalls — Every missed call, answered">', label="og title")
sub('<meta property="og:description" content="The 9pm call doesn\'t wait until Monday. PestCalls answers it, qualifies it, and books it.">',
    '<meta property="og:description" content="It starts snowing at 2am. The phone starts at 2:15. SnowCalls answers every one of them.">',
    label="og desc")

# ---------------------------------------------------------------- hero
sub('<p class="label">24/7 call answering for pest control</p>',
    '<p class="label">24/7 storm line for snow removal</p>', label="hero label")
sub("<h1>The 9pm call doesn't wait until Monday.</h1>",
    "<h1>It starts snowing at 2am. The phone starts at 2:15.</h1>", label="h1")
sub('<p class="lede">Wasps in a kid\'s bedroom wall. Mice in the kitchen the night before a party. Those callers are not leaving a voicemail — they are dialing the next company on the list about ninety seconds later.</p>',
    '<p class="lede">A property manager needs a lot bare before the doors open at seven. Somebody is buried in and has a six o\'clock shift. None of them are leaving a voicemail at three in the morning — they are working down the list until a person picks up.</p>',
    label="hero lede 1")
sub('<p class="lede">PestCalls answers every one of those calls, around the clock, asks what your estimator would ask, and puts the job on your calendar before you have picked up the phone.</p>',
    '<p class="lede">SnowCalls answers every one of those calls through the whole storm, asks what you would ask, and puts the address on the route while you are still in the truck with the plow down.</p>',
    label="hero lede 2")

# ---------------------------------------------------------------- transcript
sub('<div class="phone-top"><span class="dot"></span> Saturday · 9:14 PM · inbound</div>',
    '<div class="phone-top"><span class="dot"></span> Tuesday · 4:52 AM · inbound</div>', label="time")
sub('<span class="who">PestCalls</span>', '<span class="who">SnowCalls</span>', count=2, label="speaker labels")
sub('<span class="bub">Hi — we\'ve got bees or wasps or something going in and out of the siding by our back door. There\'s a lot of them. We\'ve got a two-year-old.</span>',
    '<span class="bub">Hi — I manage the building on Ridge Road. We got hammered overnight and the lot hasn\'t been touched. We open at seven thirty and staff start pulling in before seven.</span>',
    label="msg 1")
sub('<span class="bub">That sounds like it needs looking at quickly. I\'m the automated line for <span class="co">Northside Pest Control</span> — I\'ll take the details and get you on the schedule. Are they going into the siding itself, or a hole in the trim?</span>',
    '<span class="bub">Understood, that\'s a tight window. I\'m the automated line for <span class="co">Northside Snow Removal</span> — I\'ll get the details down and onto the route. Roughly how many spaces is the lot, and are there cars left in it overnight?</span>',
    label="msg 2")
sub('<span class="bub">Into the siding, right at the corner. Been getting worse for about a week.</span>',
    '<span class="bub">About forty spaces. There should be two or three cars along the back fence.</span>', label="msg 3")
sub('<span class="bub">Got it. Anyone in the house allergic to stings? And is a technician able to get to the back of the property without going through a locked gate?</span>',
    '<span class="bub">Got it. Where do you want the snow piled, and do you want the walks and entrances salted while we\'re there?</span>',
    label="msg 4")
sub('<span class="bub">No allergies. Gate\'s unlocked, it\'s the grey house on Elm.</span>',
    '<span class="bub">Far corner past the dumpster. Yes to salt — the front entrance especially.</span>', label="msg 5")
sub('<div class="h"><span class="dot"></span> Booked · sent to the crew at 9:17 PM</div>',
    '<div class="h"><span class="dot"></span> On the route · sent to the truck at 4:54 AM</div>', label="booked h")
sub("""          <dt>Job</dt><dd>Stinging insect — nest in siding, rear corner</dd>
          <dt>Urgency</dt><dd>High — young child on site</dd>
          <dt>Access</dt><dd>Unlocked gate, rear of property</dd>
          <dt>Slot</dt><dd>Monday 8:00–10:00 AM</dd>""",
    """          <dt>Site</dt><dd>Ridge Road lot — approx. 40 spaces</dd>
          <dt>Deadline</dt><dd>Clear and salted before 7:00 AM</dd>
          <dt>On site</dt><dd>2–3 cars along the back fence</dd>
          <dt>Notes</dt><dd>Pile past the dumpster · salt walks and front entrance</dd>""",
    label="job card")

# ---------------------------------------------------------------- problem
sub("<h2 style=\"max-width:20ch\">You don't lose those jobs on price. You lose them on silence.</h2>",
    "<h2 style=\"max-width:22ch\">A season's worth of customers is decided on about nine nights.</h2>",
    label="problem h2")
sub("<p>Pest work is different from most trades. Nobody books it a month out. Something appears in a wall or a bedroom, the caller wants it gone tonight, and they will keep dialing until a human answers.</p>",
    "<p>Snow is the most compressed trade there is. The work does not trickle in — it lands on a handful of nights a winter, all at once, on everybody at the same time. Every plow contractor in the county gets the same calls in the same two hours.</p>",
    label="problem p1")
sub("<p>Meanwhile you are on a roofline, under a crawlspace, driving, or asleep — all of which are the correct places to be. The call does not go unanswered because you stopped caring. It goes unanswered because you were doing the job.</p>",
    "<p>And you are the one person who cannot pick up, because you are in the truck at four in the morning with the plow down and a route to finish. The call does not go unanswered because you stopped caring. It goes unanswered because you were plowing.</p>",
    label="problem p2")
sub("<p>By the time you clear the voicemail on Monday, somebody else has already treated the nest and picked up the quarterly contract that came with it.</p>",
    "<p>By the time the route is done and you get to the voicemail, it is nine in the morning, the sun is out, and somebody else plowed that lot at five. You did not lose one push. You lost the seasonal contract that came with it, and next winter's too.</p>",
    label="problem p3")
sub("<h3>What one missed Saturday costs</h3>", "<h3>What one missed storm costs</h3>", label="cost h3")
sub('<p style="margin-top:10px">A single stinging-insect callout is a few hundred dollars. The customer who liked how fast you answered is worth a recurring plan, and every neighbor they tell.</p>',
    '<p style="margin-top:10px">One commercial lot is a season-long agreement, not a single push. The property manager who got a real answer at five in the morning does not shop the following year, and tells the other buildings they manage.</p>',
    label="cost p")
sub("<p>You are not being outsold. You are being out-answered.</p>",
    "<p>Nobody is undercutting you at 4am. They are just picking up.</p>", label="cost p2")

# ---------------------------------------------------------------- how it works
sub("<p>Keep your number. Calls ring you first — after hours, or after a set number of rings, they come to PestCalls instead of voicemail. Nothing on your phone changes.</p>",
    "<p>Keep your number. Calls ring you first — during a storm, or after a set number of rings, they come to SnowCalls instead of voicemail. Nothing on your phone changes.</p>",
    label="step 1")
sub("<p>Pest and location, how long it's been going on, allergies and pets, access to the property, whether it's a rental. We write those questions with you, in your first week.</p>",
    "<p>Address, driveway or lot, rough size, when it has to be clear by, where the snow gets piled, cars left on site, salt or no salt. We write those questions with you before the first flake falls.</p>",
    label="step 2")
sub("<h3>The job lands booked</h3>", "<h3>The address lands on the route</h3>", label="step 3 h3")
sub("<p>An available slot goes on your calendar and the details hit your phone as a text. No new dashboard, no app to remember to open.</p>",
    "<p>The site and its notes text through to whoever is running the route, ordered by when each one has to be clear. No new dashboard, no app to open with gloves on.</p>",
    label="step 3 p")

# ---------------------------------------------------------------- included
sub("<li>Answered 24/7 — nights, weekends, holidays, and the middle of a treatment</li>",
    "<li>Answered right through the storm — 3am, weekends, holidays, mid-route</li>", label="inc 1")
sub("<li>Qualified with your questions, not a generic script</li>",
    "<li>Qualified with your questions, not a generic script</li>", label="inc 2")
sub("<li>Booked into the calendar you already use</li>",
    "<li>Contract customers recognised and flagged ahead of one-off callers</li>", label="inc 3")
sub("<li>Job details texted to whoever is on call</li>",
    "<li>Site details and deadlines texted to whoever is running the route</li>", label="inc 4")
sub("<li>Overflow cover during the day, so a busy signal never happens</li>",
    "<li>Storm surge cover — two hundred calls in two hours is the same to it as one</li>", label="inc 5")
sub("<li>A weekly summary of what came in and what got booked</li>",
    "<li>A summary after every storm: who called, who got served, who you had to turn down</li>",
    label="inc 6")

# ---------------------------------------------------------------- what it isn't
sub("<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. Your customers are not typing at 9pm. They are calling.</p>",
    "<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. Nobody types out a web form at 4am with a foot of snow in the driveway. They call.</p>",
    label="isnt p1")
sub("<p><strong style=\"color:var(--ink)\">It never quotes a price.</strong> It gathers, it books, it hands over. Anything that commits you to a number or a promise routes to a human first.</p>",
    "<p><strong style=\"color:var(--ink)\">It never quotes a price, and it never promises a time.</strong> Snow pricing depends on the site and the season, and the one thing you cannot do at 4am is promise an arrival you might miss by three hours. It gathers and it hands over.</p>",
    label="isnt p2")

# ---------------------------------------------------------------- terms + faq
sub("<li>Priced on call volume and how many trucks it books for. Told to you before you commit, not after.</li>",
    "<li>Priced on call volume and how many trucks it routes for, and it can be paused out of season. Told to you before you commit, not after.</li>",
    label="terms")
sub("<p>It hands off. Anything unusual, angry, or outside what we set up gets routed to a real person or flagged for a callback first thing, with the recording attached. It is built to know its edges.</p>",
    "<p>It hands off. Anything unusual, angry, or outside what we set up — a damage claim, a dispute about a contract — goes to a real person or gets flagged with the recording attached. It is built to know its edges.</p>",
    label="faq handoff")
sub("<p>About a week. Most of that is the two of us writing the questions it asks, which is the part that decides whether the bookings are any good.</p>",
    "<p>About a week, and the time to do it is October. Most of it is the two of us writing the questions and loading your contract list, which is what decides whether the routing is any good once it actually snows.</p>",
    label="faq timing")
sub("<p>We agree the number before anything is built — after-hours calls answered, jobs booked without a human, callbacks avoided. If that number hasn't moved in the first month, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    "<p>We agree the number before anything is built — storm calls answered, sites routed without a human, contract customers reached first. If that number hasn't moved after the first real storm, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    label="faq measure")
sub("<p>No. You keep your number and your calendar. This sits behind what you already have as an overflow destination — the same slot voicemail occupies now.</p>",
    "<p>No. You keep your number and however you run your routes. This sits behind the line as the overflow destination — the same slot voicemail occupies now — and it can sit idle from April to October without costing you the setup again.</p>",
    label="faq software")

# ---------------------------------------------------------------- CTA + footer
sub("<h2>Tell me what happens to a 9pm call today.</h2>",
    "<h2>Tell me what happens to the 4am call today.</h2>", label="cta h2")
sub("<p class=\"lede center\" style=\"margin-top:14px\">Walk me through it — where it rings, who hears it, when it gets returned. Fifteen minutes is usually enough to see whether this is worth doing, and I will tell you straight if it isn't.</p>",
    "<p class=\"lede center\" style=\"margin-top:14px\">Walk me through the last big storm — how many calls came in, how many you got to, and what happened to the rest. Fifteen minutes is usually enough to see whether this is worth doing, and I will tell you straight if it isn't.</p>",
    label="cta sub")

s = s.replace("subject=PestCalls", "subject=SnowCalls")
s = s.replace('<p class="fnote center" style="margin-inline:auto">PestCalls is a NYONIC product.',
              '<p class="fnote center" style="margin-inline:auto">SnowCalls is a NYONIC product.')
s = s.replace('"PestCalls for "', '"SnowCalls for "')
s = s.replace('"PestCalls — "', '"SnowCalls — "')
s = s.replace("// Personalized banner: /?for=Some%20Pest%20Control",
              "// Personalized banner: /?for=Some%20Snow%20Removal")

leftover = re.findall(r"PestCalls|pest control|pest technician|stinging|Northside Pest", s, re.I)
if leftover:
    sys.exit("Untranslated PestCalls copy remains: %r" % (set(leftover),))

io.open(OUT, "w", encoding="utf-8", newline="").write(s)
print("wrote %s (%d bytes)" % (OUT, len(s.encode("utf-8"))))
