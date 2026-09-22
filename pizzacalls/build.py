#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PizzaCalls — page builder.

Third in the [Trade]Calls family. Takes the PestCalls page as `_base.html` and applies
the PizzaCalls brand and copy. Same discipline as treecalls/build.py: every `sub()`
fails loudly, and the file refuses to write if any pest-control wording survives.

Palette note — this one deliberately breaks the family CTA rule. TreeCalls and PestCalls
both use safety orange #FF6B1A for actions. Orange next to Italian red reads as a
mistake, so here the CTA is the flag's red. Cream #F4F2EC still carries across, and the
base hue moves to a wood-fired near-black rather than green: a green ground would have
collided with TreeCalls' evergreen on the NYONIC card row.

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
    "--ink:#171009;        /* wood-fired near-black */", label="ink")
sub("--ink-2:#0A1A21;      /* darker slab */",
    "--ink-2:#100B06;      /* deeper oven slab */", label="ink2")
sub("--teal:#14A3B8;       /* primary accent */",
    "--green:#008C45;      /* Italian green */\n"
    "    --green-lt:#39B36B;   /* accent on DARK grounds */\n"
    "    --green-dk:#00703A;   /* accent on LIGHT grounds — contrast-checked */\n"
    "    --red:#CD212A;        /* Italian red — actions */", label="accent")
sub("--teal-pale:#CFE9EE;  /* pale wash on dark */",
    "--cream-2b:#E6E2D8;   /* pale wash */", label="pale")
sub("--orange:#FF6B1A;     /* shared with TreeCalls — action only */",
    "--orange:#CD212A;     /* the family's action slot, filled with flag red here */",
    label="cta")

s = s.replace("var(--teal)", "var(--green-lt)")
s = s.replace("rgba(20,163,184,", "rgba(57,179,107,")
s = s.replace("#04222A", "#14100D")
s = s.replace("--body:#33454C;", "--body:#4A4036;")
s = s.replace("--muted:#7C8D94;", "--muted:#948676;")
s = s.replace("--line-dark:rgba(14,39,48,.14);", "--line-dark:rgba(23,16,9,.14);")
s = s.replace("background:rgba(14,39,48,.94)", "background:rgba(23,16,9,.94)")

# Light-ground accents need the darker green.
sub("""  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--green-lt);margin:0 0 .9em
  }""",
    """  .label{
    font-size:.735rem;letter-spacing:.17em;text-transform:uppercase;
    font-weight:700;color:var(--green-dk);margin:0 0 .9em
  }
  .dark .label,.hero .label{color:var(--green-lt)}""", label="label split")

sub("""  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--green-lt);border-bottom:2.5px solid var(--green-lt);
    transform:rotate(-45deg)
  }""",
    """  ul.ticks li::before{
    content:"";position:absolute;left:0;top:.42em;width:17px;height:9px;
    border-left:2.5px solid var(--green-dk);border-bottom:2.5px solid var(--green-dk);
    transform:rotate(-45deg)
  }
  .dark ul.ticks li::before{border-color:var(--green-lt)}""", label="ticks split")

sub("summary::after{content:\"+\";margin-left:auto;color:var(--green-lt);",
    "summary::after{content:\"+\";margin-left:auto;color:var(--green-dk);", label="summary marker")

# ---------------------------------------------------------------- mark
SLICE = ('      <path d="M45 39.5 L31.5 12 Q45 5.4 58.5 12 Z" fill="#CD212A"/>\n'
         '      <path d="M31.5 12 Q45 5.4 58.5 12" fill="none" stroke="#F4F2EC" stroke-width="5.2" stroke-linecap="round"/>\n'
         '      <circle cx="41" cy="18.5" r="2.7" fill="#F4F2EC"/>\n'
         '      <circle cx="49.5" cy="21.5" r="2.4" fill="#F4F2EC"/>')
PHONE = ('M16.5 20c-2.4 0-4.6 2.2-4.6 4.6 0 15.6 13.4 29 29 29 2.4 0 4.6-2.2 4.6-4.6'
         'v-5.6l-10.1-3.4-4.5 4.5c-5.6-3.4-10.1-7.9-13.5-13.5l4.5-4.5z')

old_head = re.search(r'      <svg viewBox="0 0 64 64" aria-hidden="true">\n.*?      </svg>', s, re.S)
if not old_head:
    sys.exit("header mark not found")
s = s.replace(old_head.group(0),
    '      <svg viewBox="0 0 64 64" aria-hidden="true">\n' + SLICE +
    '\n      <path d="' + PHONE + '" fill="#F4F2EC"/>\n      </svg>', 1)

old_foot = re.search(r'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="M44 5.*?</svg>', s, re.S)
if not old_foot:
    sys.exit("footer mark not found")
s = s.replace(old_foot.group(0),
    '<svg viewBox="0 0 64 64" aria-hidden="true">'
    '<path d="M45 39.5 L31.5 12 Q45 5.4 58.5 12 Z" fill="#CD212A"/>'
    '<path d="M31.5 12 Q45 5.4 58.5 12" fill="none" stroke="#F4F2EC" stroke-width="5.2" stroke-linecap="round"/>'
    '<circle cx="41" cy="18.5" r="2.7" fill="#F4F2EC"/>'
    '<circle cx="49.5" cy="21.5" r="2.4" fill="#F4F2EC"/>'
    '<path d="' + PHONE + '" fill="#F4F2EC"/></svg>', 1)

old_fav = s[s.find('<link rel="icon"'):s.find('>', s.find('<link rel="icon"')) + 1]
s = s.replace(old_fav,
  "<link rel=\"icon\" href=\"data:image/svg+xml,"
  "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
  "%3Crect width='64' height='64' rx='14' fill='%23171009'/%3E"
  "%3Cg transform='translate(32,32) scale(.78) translate(-32,-32)'%3E"
  "%3Cpath d='M45 39.5 L31.5 12 Q45 5.4 58.5 12 Z' fill='%23CD212A'/%3E"
  "%3Cpath d='M31.5 12 Q45 5.4 58.5 12' fill='none' stroke='%23F4F2EC' stroke-width='5.2' stroke-linecap='round'/%3E"
  "%3Cpath d='" + PHONE + "' fill='%23F4F2EC'/%3E%3C/g%3E%3C/svg%3E\">", 1)

# ---------------------------------------------------------------- wordmark
sub("<span>Pest<b>Calls</b></span>", "<span>Pizza<b>Calls</b></span>", count=2, label="wordmark")

# ---------------------------------------------------------------- head
sub("<title>PestCalls — Every missed call, answered | NYONIC</title>",
    "<title>PizzaCalls — Every missed call, answered | NYONIC</title>", label="title")
sub('content="24/7 call answering and booking for pest control companies. Every after-hours call answered, qualified, and booked into your calendar before the caller dials the next company."',
    'content="24/7 call answering for pizzerias. Every call answered through the Friday rush — hours, delivery zone, wait times and large orders, without pulling anyone off the line."',
    label="meta desc")
sub('<meta name="theme-color" content="#0E2730">',
    '<meta name="theme-color" content="#171009">', label="theme colour")
sub('<meta property="og:title" content="PestCalls — Every missed call, answered">',
    '<meta property="og:title" content="PizzaCalls — Every missed call, answered">', label="og title")
sub('<meta property="og:description" content="The 9pm call doesn\'t wait until Monday. PestCalls answers it, qualifies it, and books it.">',
    '<meta property="og:description" content="Friday at 6:40 the phone does not stop. PizzaCalls answers every one, so nobody comes off the line.">',
    label="og desc")

# ---------------------------------------------------------------- hero
sub('<p class="label">24/7 call answering for pest control</p>',
    '<p class="label">24/7 call answering for pizzerias</p>', label="hero label")
sub("<h1>The 9pm call doesn't wait until Monday.</h1>",
    "<h1>Friday at 6:40. The phone hasn't stopped in an hour.</h1>", label="h1")
sub('<p class="lede">Wasps in a kid\'s bedroom wall. Mice in the kitchen the night before a party. Those callers are not leaving a voicemail — they are dialing the next company on the list about ninety seconds later.</p>',
    '<p class="lede">Every ring during the rush is somebody asking how long a large pepperoni takes, whether you deliver to their street, or if they can get eight pies to an office by Thursday. Nobody leaves a voicemail for a pizzeria. They call the next place.</p>',
    label="hero lede 1")
sub('<p class="lede">PestCalls answers every one of those calls, around the clock, asks what your estimator would ask, and puts the job on your calendar before you have picked up the phone.</p>',
    '<p class="lede">PizzaCalls answers every one of those calls on the first ring, handles the questions your staff answer forty times a night, and sends the real orders through to the shop — without anybody stepping away from the line.</p>',
    label="hero lede 2")

# ---------------------------------------------------------------- transcript
sub('<div class="phone-top"><span class="dot"></span> Saturday · 9:14 PM · inbound</div>',
    '<div class="phone-top"><span class="dot"></span> Friday · 6:41 PM · inbound</div>', label="time")
sub('<span class="who">PestCalls</span>', '<span class="who">PizzaCalls</span>', count=2, label="speaker labels")
sub('<span class="bub">Hi — we\'ve got bees or wasps or something going in and out of the siding by our back door. There\'s a lot of them. We\'ve got a two-year-old.</span>',
    '<span class="bub">Hi — do you deliver out to Brighton? And I need to sort out eight large pies for a team thing at the office on Thursday.</span>',
    label="msg 1")
sub('<span class="bub">That sounds like it needs looking at quickly. I\'m the automated line for <span class="co">Northside Pest Control</span> — I\'ll take the details and get you on the schedule. Are they going into the siding itself, or a hole in the trim?</span>',
    '<span class="bub">We do deliver to Brighton. I\'m the automated line for <span class="co">Northside Pizza</span> — I\'ll take the Thursday order down and someone will call you to confirm it and take payment. What time do you need them there?</span>',
    label="msg 2")
sub('<span class="bub">Into the siding, right at the corner. Been getting worse for about a week.</span>',
    '<span class="bub">Noon would be ideal. Two of them need to be gluten free.</span>', label="msg 3")
sub('<span class="bub">Got it. Anyone in the house allergic to stings? And is a technician able to get to the back of the property without going through a locked gate?</span>',
    '<span class="bub">Got it — six regular, two gluten free, Thursday at noon. Is there a suite number or a front desk the driver should ask for?</span>',
    label="msg 4")
sub('<span class="bub">No allergies. Gate\'s unlocked, it\'s the grey house on Elm.</span>',
    '<span class="bub">Suite 300, ask for Dana at the front desk.</span>', label="msg 5")
sub('<div class="h"><span class="dot"></span> Booked · sent to the crew at 9:17 PM</div>',
    '<div class="h"><span class="dot"></span> Taken · sent to the shop at 6:43 PM</div>', label="booked h")
sub("""          <dt>Job</dt><dd>Stinging insect — nest in siding, rear corner</dd>
          <dt>Urgency</dt><dd>High — young child on site</dd>
          <dt>Access</dt><dd>Unlocked gate, rear of property</dd>
          <dt>Slot</dt><dd>Monday 8:00–10:00 AM</dd>""",
    """          <dt>Order</dt><dd>8 large — 6 regular, 2 gluten free</dd>
          <dt>When</dt><dd>Thursday, delivered by 12:00 PM</dd>
          <dt>Where</dt><dd>Brighton · Suite 300, ask for Dana</dd>
          <dt>Next</dt><dd>Callback to confirm and take payment</dd>""", label="order card")

# ---------------------------------------------------------------- problem
sub("<p>Pest work is different from most trades. Nobody books it a month out. Something appears in a wall or a bedroom, the caller wants it gone tonight, and they will keep dialing until a human answers.</p>",
    "<p>A pizzeria's phone problem is not that the calls stop. It is that they all arrive in the same ninety minutes, on the night when every person in the building already has both hands full.</p>",
    label="problem p1")
sub("<p>Meanwhile you are on a roofline, under a crawlspace, driving, or asleep — all of which are the correct places to be. The call does not go unanswered because you stopped caring. It goes unanswered because you were doing the job.</p>",
    "<p>Somebody has to come off the make line, wipe their hands, and pick up — to answer that you close at ten, that yes you deliver to that street, that it is about thirty-five minutes right now. Then do it again. The call does not go unanswered because you stopped caring. It goes unanswered because you were making pizza.</p>",
    label="problem p2")
sub("<p>By the time you clear the voicemail on Monday, somebody else has already treated the nest and picked up the quarterly contract that came with it.</p>",
    "<p>And the one call you truly could not afford to miss — the eight-pie office order for Thursday — sounded exactly like the other forty while it was ringing.</p>",
    label="problem p3")
sub("<h3>What one missed Saturday costs</h3>", "<h3>What one missed Friday costs</h3>", label="cost h3")
sub('<p style="margin-top:10px">A single stinging-insect callout is a few hundred dollars. The customer who liked how fast you answered is worth a recurring plan, and every neighbor they tell.</p>',
    '<p style="margin-top:10px">A dropped Friday call is one order. A dropped catering call is a standing weekly order and the office that keeps ordering from whoever picked up first.</p>',
    label="cost p")
sub("<p>You are not being outsold. You are being out-answered.</p>",
    "<p>And a phone order is worth more to you than the same order through a delivery app that takes a third of it.</p>",
    label="cost p2")

# ---------------------------------------------------------------- how it works
sub("<p>Keep your number. Calls ring you first — after hours, or after a set number of rings, they come to PestCalls instead of voicemail. Nothing on your phone changes.</p>",
    "<p>Keep your number. Calls ring the shop first — when the line is busy or nobody picks up by the fourth ring, they come to PizzaCalls instead of ringing out. Nothing about your phone changes.</p>",
    label="step 1")
sub("<p>Pest and location, how long it's been going on, allergies and pets, access to the property, whether it's a rental. We write those questions with you, in your first week.</p>",
    "<p>Your hours, your delivery zone, tonight's wait time, what is on the menu and what is not. For real orders: sizes, toppings, allergies, when and where. We write all of it with you in your first week.</p>",
    label="step 2")
sub("<h3>The job lands booked</h3>", "<h3>The order lands in the shop</h3>", label="step 3 h3")
sub("<p>An available slot goes on your calendar and the details hit your phone as a text. No new dashboard, no app to remember to open.</p>",
    "<p>Order details print or text through to the shop the way you want them. No new tablet on the counter, no app anybody has to remember to open.</p>",
    label="step 3 p")

# ---------------------------------------------------------------- included
sub("<li>Answered 24/7 — nights, weekends, holidays, and the middle of a treatment</li>",
    "<li>Answered on the first ring — through the rush, after close, and all the way to last call</li>", label="inc 1")
sub("<li>Qualified with your questions, not a generic script</li>",
    "<li>Your hours, your delivery zone, your menu — not a generic script</li>", label="inc 2")
sub("<li>Booked into the calendar you already use</li>",
    "<li>Catering and large orders taken in full and routed for a callback</li>", label="inc 3")
sub("<li>Job details texted to whoever is on call</li>",
    "<li>Order details printed or texted through to the shop</li>", label="inc 4")
sub("<li>Overflow cover during the day, so a busy signal never happens</li>",
    "<li>No busy signal on a Friday, however many people call at once</li>", label="inc 5")
sub("<li>A weekly summary of what came in and what got booked</li>",
    "<li>A weekly summary of what came in, what got taken, and what people asked for</li>", label="inc 6")

# ---------------------------------------------------------------- what it isn't
sub("<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. Your customers are not typing at 9pm. They are calling.</p>",
    "<p style=\"margin-top:22px\">A chat bubble is the most visible and least useful version of this. The person who wants a pizza in thirty minutes is not typing at you. They are calling.</p>",
    label="isnt p1")
sub("<p><strong style=\"color:var(--ink)\">It never quotes a price.</strong> It gathers, it books, it hands over. Anything that commits you to a number or a promise routes to a human first.</p>",
    "<p><strong style=\"color:var(--ink)\">It never quotes a catering price or takes payment.</strong> It gathers the order and hands it over. Anything that commits you to a number, a delivery time you cannot make, or a card on file routes to a human first.</p>",
    label="isnt p2")

# ---------------------------------------------------------------- terms + faq
sub("<li>Priced on call volume and how many trucks it books for. Told to you before you commit, not after.</li>",
    "<li>Priced on call volume and how many locations it answers for. Told to you before you commit, not after.</li>", label="terms")
sub("<p>It hands off. Anything unusual, angry, or outside what we set up gets routed to a real person or flagged for a callback first thing, with the recording attached. It is built to know its edges.</p>",
    "<p>It hands off. A complaint about an order, anything unusual, anything outside what we set up — it goes to a real person, or gets flagged for a callback with the recording attached. It is built to know its edges.</p>",
    label="faq handoff")
sub("<p>We agree the number before anything is built — after-hours calls answered, jobs booked without a human, callbacks avoided. If that number hasn't moved in the first month, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    "<p>We agree the number before anything is built — calls answered during the rush, orders taken without anybody leaving the line, catering enquiries captured. If that number hasn't moved in the first month, we change it or you switch it off. I would rather lose the work than keep invoicing for something that isn't landing.</p>",
    label="faq measure")
sub("<p>About a week. Most of that is the two of us writing the questions it asks, which is the part that decides whether the bookings are any good.</p>",
    "<p>About a week. Most of that is the two of us going through your menu, your hours and your delivery zone, which is the part that decides whether any of it is any good.</p>",
    label="faq timing")
sub("<p>No. You keep your number and your calendar. This sits behind what you already have as an overflow destination — the same slot voicemail occupies now.</p>",
    "<p>No. You keep your number, your POS and your delivery apps. This sits behind the phone line as the overflow destination — the same slot ringing out occupies now.</p>",
    label="faq software")

# ---------------------------------------------------------------- CTA + footer
sub("<h2>Tell me what happens to a 9pm call today.</h2>",
    "<h2>Tell me what happens to the 6:40 call today.</h2>", label="cta h2")
sub("<p class=\"lede center\" style=\"margin-top:14px\">Walk me through it — where it rings, who hears it, when it gets returned. Fifteen minutes is usually enough to see whether this is worth doing, and I will tell you straight if it isn't.</p>",
    "<p class=\"lede center\" style=\"margin-top:14px\">Walk me through a Friday — who picks up, what they get asked, and what happens when both lines go at once. Fifteen minutes is usually enough to see whether this is worth doing, and I will tell you straight if it isn't.</p>",
    label="cta sub")

s = s.replace("subject=PestCalls", "subject=PizzaCalls")
s = s.replace('<p class="fnote center" style="margin-inline:auto">PestCalls is a NYONIC product.',
              '<p class="fnote center" style="margin-inline:auto">PizzaCalls is a NYONIC product.')
s = s.replace('"PestCalls for "', '"PizzaCalls for "')
s = s.replace('"PestCalls — "', '"PizzaCalls — "')
s = s.replace("// Personalized banner: /?for=Magnum%20Pest%20Control",
              "// Personalized banner: /?for=Some%20Pizzeria")

leftover = re.findall(r"PestCalls|pest control|pest technician|stinging", s, re.I)
if leftover:
    sys.exit("Untranslated PestCalls copy remains: %r" % (set(leftover),))

io.open(OUT, "w", encoding="utf-8", newline="").write(s)
print("wrote %s (%d bytes)" % (OUT, len(s.encode("utf-8"))))
