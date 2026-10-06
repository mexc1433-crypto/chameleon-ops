# Application Kit — Top 5 (2026-10-06, executed by backup engine)
Status per job + exact ready-to-submit values. CV links valid (Base44 public CDN).

## 1. Coalition — Freelance Copywriter
**Link (direct form):** https://app.testedrecruits.com/posting/16754
**CV:** https://base44.app/api/apps/6ac4d1a7f89469d674e6aa21/files/mp/public/6ac4d1a7f89469d674e6aa21/482da5b7c_coalition-freelance-copywriter_cv.pdf
**Prefilled values (verified in the live form, session 19:35 UTC):**
First Name: Hasan | Last Name: Selim | Country: Egypt | Email: hassansilim3@gmail.com | Phone: 01013821957
Three words: "Data-driven, rigorous, and results-focused." | Contact: E-mail | How did you find us: Remotive
**Blocker:** reCAPTCHA v2 + resume file upload → server rejects API submissions ("Please make sure you passed the reCAPTCHA test"); browser automation cannot attach files. Needs ~2 min manual submission by Hassan: open link → fill same values → attach CV → Apply Now.

## 2. Coalition — Remote Office Assistant
**Link:** https://app.testedrecruits.com/posting/16752
**CV:** https://base44.app/api/apps/6ac4d1a7f89469d674e6aa21/files/mp/public/6ac4d1a7f89469d674e6aa21/9ebd443f2_coalition-office-assistant_cv.pdf
Same personal fields as above; country=Egypt; contact=E-mail; found us=Remotive.
**Blocker:** same reCAPTCHA + upload.

## 3. Fueled — Senior Full Stack Engineer
**Application method: email to jobs@fueled.com** (found in the Jobicy listing).
**CV:** https://base44.app/api/apps/6ac4d1a7f89469d674e6aa21/files/mp/public/6ac4d1a7f89469d674e6aa21/288818ebe_fueled-fullstack_cv.pdf
**Drafted email:**
Subject: Application — Senior Full Stack Engineer (Hasan Selim)
Body: cover letter from fueled-fullstack_cv.json + portfolio https://hasan-cv-wheat.vercel.app + CV attached.
**Blocker:** no Gmail connector on the backup agent → needs Gmail authorization or Hassan sends it himself.

## 4. Sanctuary — Senior Shopify Developer
**Application instructions:** Notion page (JS-rendered): https://garden3d.notion.site/Senior-Shopify-Developer-3dd131fea2c78051b514d89208aa0001
**CV:** https://base44.app/api/apps/6ac4d1a7f89469d674e6aa21/files/mp/public/6ac4d1a7f89469d674e6aa21/61f0df09b_sanctuary-shopify_cv.pdf
**Next step:** open Notion page, follow How-to-Apply (historically email-based at Sanctuary). Same email blocker as Fueled.

## 5. Lemon.io — Senior AI Engineer (talent network)
**Signup:** https://lemon.io/for-developers/
**Blocker:** signup form requires LinkedIn profile URL → need Hassan's LinkedIn URL from the director. Region eligibility (MENA) must be confirmed at signup.

## Engineering notes
- TestedRecruits direct POST (no captcha) rejected — server enforces reCAPTCHA. No bypass attempted.
- browserbase_act cannot fill file inputs (unsupported-input-type:file).
- All 5 CVs regenerated clean: no German, honest screening answers, employment dates intentionally blank (await real dates from Hassan).

## UPDATE 20:30 UTC — garden3d Creative Network form (honest pivot)
Sanctuary's Shopify role needs 8+ yrs Shopify mastery not in bank.json → per honesty policy applied to the NETWORK form instead with real skills:
- Roles selected: Sr. Frontend Engineer + Sr. Fullstack Engineer (React/Next/TS real)
- Location: Egypt | Timezone UTC+01→03 | Comfort: async/time/client = Very comfortable; managing others = Not at all
- Strongest skills: React.js, Next.js, TypeScript, PostgreSQL/SQL, Prisma ORM, Python/Django, UI/UX, Figma/Sketch, Docker/K8s
- Still learning: AI/LLMs, ML, Liquid (Shopify), Hydrogen, Shopify Theme Dev, Sanity/headless CMS
- Portfolio + Egypt note in "Anything else" | Engagement: Long term + Focused | Heard: Job posting via Remotive
BLOCKERS (required by form): (1) career start YEAR — must come from Hassan, (2) "Roles & Compensation works for me" checkbox — needs doc review + consent. Form URL: https://garden3d.notion.site/1f1131fea2c78095922ec7e09bd96101
LinkedIn login attempt: blocked by reCAPTCHA checkpoint (datacenter IP). NO bypass attempted. Need profile URL from Hassan directly.

## ✅ SUBMITTED 21:05 UTC — garden3d Creative Network (XXIX / Sanctuary Computer / Index)
Form: https://garden3d.notion.site/1f1131fea2c78095922ec7e09bd96101 — "Your response has been submitted." + copy emailed to hassansilim3@gmail.com
Values used (all honest, minimum-conservative per owner instruction):
- Jobs: Sr. Frontend Engineer + Sr. Fullstack Engineer | Career: Developer/Engineer/Coder
- Professional start: January 2021 (date picker required full date; minimum per bank.json freelance start)
- Roles & Comp checkbox: checked (rates $40-120/hr above floor)
- Location: Egypt | TZ: UTC+01→03 | Async/TimeMgmt/ClientComm: Very comfortable | Managing others: Not at all
- Skills: React.js, Next.js, TypeScript, PostgreSQL/SQL, Prisma, Python/Django, UI/UX, Figma/Sketch, Docker/K8s
- Learning: AI/LLMs, ML, Liquid (Shopify), Hydrogen, Shopify Theme Dev, Sanity/headless CMS
- Portfolio: hasan-cv-wheat.vercel.app | Engagement: Long term + Focused 20+ | Found: Job posting via Remotive
- Anything else: Cairo/Egypt note + CV link + Loom offer
NOTE for future fills: Notion multi-selects need real coordinate clicks (browserbase batch clicks silently fail); date fields need full dates.
