# Your Foundvia Discovery

## A practical Google + ChatGPT discovery playbook

**For founders building their first SaaS with AI.**

Build something useful. Help people find it. Learn from the first 100 visits.

Ronaldo Paulino / @ronaldships / Ship & Grow

English community edition v1.0 / October 6, 2026

Adapted from [SEO + GEO Playbook](https://github.com/ronaldships/foundvia-discovery), by Ronaldo Paulino. Source snapshot: `92c63d26e632b8af19f538540803f8fc9a886145`.

This is an implementation guide, not a promise of rankings, recommendations, or traffic within a deadline. Google and OpenAI do not endorse this guide. The 100-visit target is a learning milestone, not a benchmark proved by the source repository.



# 01 / Define the milestone

You shipped your app. Now give the right person a reason to discover it.

This guide reduces the original playbook to a small starting system: one audience, one useful problem, three discovery pages, and a weekly review. The suggested quantities and schedule are editorial recommendations, not search-engine requirements.

## What counts as a visit?

For this guide, count **100 cumulative, measured sessions attributed to Google organic search or ChatGPT**, starting on a date you choose. A session is a visit; it is not necessarily a unique person. A returning person can create another session.

- Use one analytics platform and keep its session definition unchanged.
- Exclude your own testing, teammates, paid campaigns, and known bots where your platform supports it.
- Assign each session to one channel. Do not count the same session twice.
- Keep direct, social, other search engines, and other AI sources separate.
- Report the two channels separately, even when using a combined total.

**Illustration only:** 72 Google organic sessions + 28 ChatGPT sessions = 100 target sessions. This is not a prediction or a reported result.

## Keep the stages separate

**Discovered > Crawled > Indexed or retrieved > Shown or cited > Clicked > Used > Paid**

A sitemap helps with discovery. An impression means visibility. A citation means your link appeared in an answer. None of those is a visit. A visit is not activation, retention, or payment.

Search Console clicks are a useful Google diagnostic, but do not add them to analytics sessions. They measure different things. [9]

**Before you start:** record your domain, start date, analytics tool, and one meaningful product action, such as creating a first page or completing a calculation.



# 02 / Pick a problem worth finding

Start with a task your product already helps someone complete. Choose the audience you understand best.

## Write one sentence

> My product helps [specific person] do [specific task] without [specific friction].

**Example, not a claim about an existing product:** My product helps independent musicians put their songs, shows, and contact links on one page without building a website.

## Collect five real questions

Look at your own support messages, conversations, and relevant public discussions. Read Google results for the task. Notice what people still struggle to understand. These are research activities; do not copy other people's content.

Possible questions for the musician example:

- How do I put all my music links in one Instagram bio?
- What should I include on a musician's link page?
- How can fans find my next show from my profile?
- Can I create a music link page without coding?
- How can I track which links people click?

## Choose one question first

Score each candidate from 1 to 3 for audience fit, product fit, and your ability to show a useful example. Start with the strongest combined fit. This is a planning heuristic, not a ranking score.

Do not start with a broad target like "best SaaS." A concrete task gives you a clearer page to build. You do not need an expensive keyword tool for this first pass.

**Done when:** you have one audience, one task, one chosen question, and one page URL that will answer it. The reader should be able to tell whether your page is for them.



# 03 / Make the public site discoverable

Before writing more pages, check that the pages you already have can be reached.

## A small technical check

- Open the page in a signed-out browser. Its useful content should not require an account.
- Confirm the live page loads successfully rather than returning an error or a permanent loading screen.
- Check that the main answer is readable on mobile, including buttons and examples.
- Link to the page from another public page using descriptive link text.
- Check for accidental `noindex` directives in HTML or response headers. [5]
- Check `robots.txt` for rules that block the intended public page or resources needed to render it. [4]
- Use a consistent preferred URL and list that version in your sitemap. [6]

Robots rules manage crawling; they do not secure a dashboard or private customer data. Use authentication for private areas. If you need a search engine to see a `noindex` directive, it must be able to crawl the page. [4, 5]

## Connect Google Search Console

Verify your site using a method you can maintain. Submit the sitemap, then inspect the homepage and your main discovery page with URL Inspection. Check the reported issue before requesting indexing. [1, 7]

A sitemap is a discovery aid, not an indexing guarantee. Use actual canonical URLs. If you supply `lastmod`, use the real date of a significant update; do not set every page to today's date on every build. Google ignores sitemap `priority` and `changefreq`. [6]

**Done when:** your priority page is reachable, linked, represented correctly in the sitemap, and has no accidental indexing block.

Crawling can take days to weeks. Requesting the same URL repeatedly does not speed it up, and a request does not guarantee inclusion. [7]



# 04 / Give ChatGPT search access

Search access and model training are different decisions.

## Know the three names

- **OAI-SearchBot:** used for ChatGPT search discovery and results.
- **GPTBot:** crawls content that may be used for model training.
- **ChatGPT-User:** handles some user-triggered visits. It does not decide search eligibility; robots rules may not apply to those visits. [2]

To support discovery in ChatGPT search, allow OAI-SearchBot to reach the public content you want included. Check your hosting or firewall too: an allowed robots rule cannot fix a blocked request. Validate access using the current published IP ranges when configuring your infrastructure. [2]

## Illustrative robots.txt

```text
User-agent: *
Allow: /
Disallow: /admin/
Disallow: /dashboard/

User-agent: OAI-SearchBot
Allow: /
Disallow: /admin/
Disallow: /dashboard/

Sitemap: https://example.com/sitemap.xml
```

Replace the domain and review your real routes. This is a starting example, not a safe replacement for every site's existing rules. Specific bot groups need their own exclusions. Do not block assets required to render public pages.

Allowing OAI-SearchBot does not require allowing GPTBot. Make the training choice separately. [2]

**Done when:** public discovery pages are accessible and the search crawler is not blocked. This makes discovery possible; it does not force a recommendation.



# 05 / Build three useful pages

The original playbook combines niche pages, free tools, comparisons, and guides. Start with a smaller version you can actually maintain. [R]

## Page 1 / A focused product page

Explain who the product helps, what they can do, and what it costs. Show a real screenshot or working example. Give one clear next step.

**Example title:** A link page for independent musicians

**Example URL:** `/for-musicians`

The page should solve a distinct audience need. Swapping profession names in otherwise identical pages is not a useful content strategy.

## Page 2 / A guide that answers the chosen question

Show how to complete the task, including steps, an example, and limitations. Explain where your product fits without turning every paragraph into a pitch.

**Example title:** How to put your music links in one Instagram bio

**Example URL:** `/guides/music-links-instagram-bio`

## Page 3 / A small tool or reusable template

Offer something useful before asking for a signup: a checklist, calculator, template, or another small resource connected to the task. Avoid building a generic tool just because it has search volume.

**Example:** A musician's link-page checklist

**Example URL:** `/tools/musician-link-checklist`

## Connect them naturally

Link the guide to the template where the reader needs it. Link both to the product page where the product helps. Link the product page back to helpful instructions. Links should explain the destination. [1]

An honest comparison can replace the tool if you can verify both products' current features and prices. Include situations where the alternative is the better fit.

**Done when:** each page offers a different kind of value and the reader can move from learning to trying.



# 06 / Make the answer useful and believable

Use AI to organize your knowledge. Add the details that only someone who built or used the product can provide.

## A page structure you can reuse

1. A clear title that describes the task.
2. A short answer that helps the reader immediately.
3. Steps with real examples or screenshots.
4. Limits, tradeoffs, or common mistakes.
5. A relevant next action.
6. An author and genuine update date where appropriate.

This structure is an editorial choice for readability, not a special format required by Google or ChatGPT.

## Example opening

> To put your music links in one Instagram bio, create a public link page, add your streaming and show links, and paste its URL into your profile. Check it on your phone before sharing it. The steps below show a simple setup and what to include.

Follow this with the actual steps. If you have not tested the workflow, test it before presenting it as your own experience.

## Before publishing, ask

- Does this answer the question without making the reader sign up first?
- Is there an example beyond generic advice?
- Are product features, prices, and limitations accurate?
- Are any testimonials and numbers real and supportable?
- Can a reader understand it on a phone?

Write descriptive page titles and unique summaries. Google can generate or rewrite title links and snippets; character targets are editing aids, not hard ranking rules. [10, 11]

Google's AI features use established search foundations. No special AI schema or `llms.txt` file is required for Google visibility. Keep useful public answers first; treat extra machine-readable files as optional experiments for other systems, not a traffic shortcut. [8]



# 07 / Measure what actually happened

Configure measurement before you call the first visits a win.

## Keep one simple dashboard

- **Google organic sessions:** visits attributed to Google's unpaid search channel by your analytics tool.
- **ChatGPT sessions:** visits attributed to ChatGPT using a recognized referral or source signal.
- **Combined target sessions:** those two mutually exclusive session counts added together.
- **Useful product actions:** users completing the action you chose on page 2.
- **Signups and payments:** separate outcomes; do not infer them from traffic.

OpenAI says ChatGPT referral URLs include `utm_source=chatgpt.com`. Check that parameter alongside the referring domain and the analytics platform's channel classification. [3]

If implementing attribution yourself, parse URLs and compare exact hostnames such as `chatgpt.com` and the legacy `chat.openai.com`. Avoid loose substring matching. Preserve first-arrival attribution for the session instead of counting an event on every page view.

**Limits:** UTMs can be copied or altered, and referrers can disappear. Your observed attribution is useful, but incomplete. Do not relabel all direct traffic as ChatGPT or classify every Bing visit as an AI referral.

## Use Search Console to diagnose Google

Review impressions, clicks, queries, and pages for the same date range. Impressions show visibility; clicks show traffic from search results. Search Console and analytics can disagree because of different collection and measurement rules. [9]

## Check ChatGPT citations separately

Try a few realistic, unbranded questions with search enabled. Record the question, date, answer, and cited URL. Avoid asking the model to recommend your brand as the test. A single answer is a snapshot, not stable visibility or a traffic count.

**Done when:** the two channels are separated, the date range is recorded, and your tracker distinguishes visits from product outcomes.



# 08 / Ship, review, improve

Use this as a manageable work schedule. It is not a promise of 100 visits in two weeks.

## A two-week setup sprint

- **Days 1-2:** define the audience, choose the question, configure analytics, and fix access problems.
- **Days 3-5:** publish the focused product page with a real example.
- **Days 6-8:** publish the guide and connect it to the product page.
- **Days 9-11:** publish one useful tool or template and connect the three pages.
- **Days 12-14:** inspect the pages, submit the sitemap if needed, and record the first measurement snapshot.

After setup, review once a week. Search discovery can take longer than the sprint. Keep other channels visible in analytics rather than mixing them into this milestone.

## Find the bottleneck before adding pages

- **Page cannot be reached:** fix errors, login barriers, loading failures, or firewall blocks.
- **Google page is not indexed:** use URL Inspection; check the reason, canonical, `noindex`, and crawl access. [5, 7]
- **Indexed with little visibility:** revisit the question and whether the page provides enough distinct value.
- **Impressions with few clicks:** inspect the actual queries and title relevance. Do not chase one universal CTR target.
- **Visits with no useful action:** test the product flow and the fit between the page's promise and the experience.
- **No ChatGPT referrals yet:** confirm access, keep improving useful content, and continue measuring. Manual citation checks do not replace traffic evidence.

## Avoid shortcuts that weaken trust

Do not create dozens of near-identical AI pages just to target variations of a phrase. Google identifies large-scale, low-value content created to manipulate rankings as scaled content abuse. [12]

Do not fabricate publication dates, testimonials, usage figures, or recommendations. Publish when the work is ready and update dates when you make meaningful changes.



# 09 / Your launch checklist

- [ ] One specific audience and one useful task selected.
- [ ] One clear question mapped to a page.
- [ ] Public pages work without signing in.
- [ ] No accidental crawl or indexing blocks.
- [ ] OAI-SearchBot can access intended public content.
- [ ] Search access and training preferences reviewed separately.
- [ ] Sitemap uses the correct preferred URLs and truthful dates.
- [ ] Search Console ownership verified and priority pages inspected.
- [ ] Three distinct pages published and linked naturally.
- [ ] Examples, claims, product features, and prices checked.
- [ ] Titles, summaries, and mobile reading experience reviewed.
- [ ] Analytics excludes testing where supported.
- [ ] Google organic and ChatGPT sessions counted separately.
- [ ] One useful product action tracked independently.
- [ ] Baseline date and weekly review recorded.

## Copy this prompt into your coding assistant

```text
Audit this project for its first Google and ChatGPT visits.
Inspect the actual public routes, rendered content, metadata,
canonicals, sitemap, robots rules, and existing analytics.
Keep private areas protected. Separate OAI-SearchBot search
access from GPTBot training preferences.
List the three biggest verified blockers with file paths
and evidence. Do not invent rankings, traffic, or results.
Suggest one audience page, one useful guide, and one small
tool or template based on what the product really does.
Prioritize a small maintainable implementation.
Explain proposed changes in plain language before applying
them. Ask before changing training preferences or publishing.
End with live checks and a plan for measuring attributed
sessions, useful actions, signups, and payments separately.
```

Use the prompt as a starting point, not a substitute for reviewing the changes and checking the deployed site.



# 10 / Sources and editorial notes

Official guidance checked October 6, 2026. Provider behavior can change; follow the linked documents for current details.

- **[R] Original playbook:** [ronaldships/foundvia-discovery](https://github.com/ronaldships/foundvia-discovery/tree/92c63d26e632b8af19f538540803f8fc9a886145). Adapted technical, on-page, content, analytics, AI search, and growth chapters.
- **[1] Google:** [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide).
- **[2] OpenAI:** [Overview of OpenAI Crawlers](https://developers.openai.com/api/docs/bots).
- **[3] OpenAI:** [Publishers and Developers FAQ](https://help.openai.com/en/articles/12627856).
- **[4] Google:** [Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro).
- **[5] Google:** [Block indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing).
- **[6] Google:** [Build and submit a sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- **[7] Google:** [Ask Google to recrawl URLs](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl).
- **[8] Google:** [Optimizing for generative AI features](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
- **[9] Google:** [Search Console performance report](https://support.google.com/webmasters/answer/7576553).
- **[10] Google:** [Title links](https://developers.google.com/search/docs/appearance/title-link).
- **[11] Google:** [Snippets and meta descriptions](https://developers.google.com/search/docs/appearance/snippet).
- **[12] Google:** [Spam policies](https://developers.google.com/search/docs/essentials/spam-policies).
- **[13] Google:** [Documentation updates](https://developers.google.com/search/updates).

## What changed from the original

This edition narrows the scope to the first 100 measured visits. It replaces a large initial page batch with a small maintainable plan, separates search crawlers from training crawlers, and makes `llms.txt` optional rather than essential. It removes unverified traffic and conversion statistics, fixed traction deadlines, unsupported top-20 prerequisites for AI citations, and fake date staggering.

FAQs can still help readers, but this edition does not present FAQ schema as required for AI visibility. Google's changelog says FAQ rich results stopped appearing in May 2026. [13]

This is an adaptation, not a complete translation of the repository or an independent validation of its case-study results. No live SaaS audit or traffic experiment was performed for this document.



# 11 / Build this with the community

The first 100 visits are a reason to listen, not just a number to screenshot.

Bring one real finding back to other builders:

- The question people searched for.
- The page that helped them.
- The step they struggled with.
- The change you made after seeing it.

Share public examples and aggregate results. Keep visitor identities, customer information, and credentials private. When reporting results, include the date range and channel definition so other people can understand what happened.

**Share the resource, suggest a correction, or contribute a tested example.** Start with the [source repository](https://github.com/ronaldships/foundvia-discovery). Follow [@ronaldships](https://x.com/ronaldships) for the ongoing journey.

## MIT License

Copyright (c) 2026 Ronaldo Paulino

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
