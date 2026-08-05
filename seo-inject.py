"""Write the search-engine layer into every page: titles and descriptions aimed
at what people actually type, canonicals, link-preview cards, and the structured
data Google reads to understand what the business does.

Run from ~/portfolio: python3 seo-inject.py
Re-running replaces the block instead of stacking a second copy."""
import re, os

SITE = 'https://studiowallace.com'
OG_IMAGE = f'{SITE}/shots/film-poster.jpg'
START, END = '<!-- seo:start -->', '<!-- seo:end -->'

ORG = f'''{{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "@id": "{SITE}/#studio",
  "name": "Studio Wallace",
  "alternateName": "Wallace",
  "url": "{SITE}/",
  "image": "{OG_IMAGE}",
  "email": "wallace@studiowallace.com",
  "description": "Custom websites and software built end to end for businesses. Online booking, Stripe payments, online stores, and custom apps.",
  "founder": {{"@type": "Person", "name": "Wallace Chen"}},
  "parentOrganization": {{"@type": "Organization", "name": "Blueprint Advantage LLC"}},
  "areaServed": {{"@type": "Country", "name": "United States"}},
  "availableLanguage": "English",
  "priceRange": "$$",
  "knowsAbout": ["Web design", "Web development", "Online booking systems", "Stripe payments", "E-commerce", "SaaS development", "Mobile app development", "AI chatbots", "AI automation", "Lead follow-up automation"],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Services",
    "itemListElement": [
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "Custom website design and development",
        "description": "The entire website built for you: design, writing, build, launch, and the tools your business runs on."}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "AI automation for small business",
        "description": "A helper that answers customers around the clock and books them in, missed enquiries caught, automatic follow-up, and personalised recommendations."}}}},
      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "App and SaaS development",
        "description": "Turning a business idea into a working app, SaaS product or online store."}}}}
    ]
  }}
}}'''


def crumbs(name, url):
    return f'''{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Studio Wallace", "item": "{SITE}/"}},
    {{"@type": "ListItem", "position": 2, "name": "{name}", "item": "{url}"}}
  ]
}}'''


def service(name, desc, url):
    return f'''{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{name}",
  "description": "{desc}",
  "url": "{url}",
  "serviceType": "{name}",
  "provider": {{"@id": "{SITE}/#studio"}},
  "areaServed": {{"@type": "Country", "name": "United States"}}
}}'''


PAGES = {
  'index.html': dict(
    path='/',
    title='Custom Websites for Your Business | Studio Wallace',
    desc='Custom websites built end to end. Online booking, Stripe payments, an online store, and whatever else your business needs to bring in customers.',
    ld=[ORG],
  ),
  'services/websites.html': dict(
    path='/services/websites.html',
    title='Custom Business Websites Built End to End | Studio Wallace',
    desc='The entire website built for you: design, writing, launch. Take payments with Stripe, take bookings straight into your calendar, sell online.',
    ld=[crumbs('Websites', f'{SITE}/services/websites.html'),
        service('Custom website design and development',
                'The entire website built for you end to end, including payments, booking and online sales.',
                f'{SITE}/services/websites.html')],
  ),
  'services/ai.html': dict(
    path='/services/ai.html',
    title='AI Built Into Your Business | Studio Wallace',
    desc='Answer customers at 2am, never miss another enquiry, and follow up with everyone who almost booked. Practical AI built into the business you already run.',
    ld=[crumbs('AI for your business', f'{SITE}/services/ai.html'),
        service('AI automation for small business',
                'Customer-facing AI built into a business: a helper that answers customers around the clock and books them in, missed enquiries caught and answered, automatic follow-up, and personalised recommendations.',
                f'{SITE}/services/ai.html')],
  ),
  'services/custom.html': dict(
    path='/services/custom.html',
    title='Turn Your Idea Into an App or SaaS | Studio Wallace',
    desc='Bring your app, SaaS or online store idea and watch it get built. From the first conversation to a product your customers can actually use.',
    ld=[crumbs('Got a business idea?', f'{SITE}/services/custom.html'),
        service('App and SaaS development',
                'Turning a business idea into a working app, SaaS product or online store.',
                f'{SITE}/services/custom.html')],
  ),
  'pricing.html': dict(
    path='/pricing.html',
    title='What a Custom Website Costs | Studio Wallace',
    desc='Every website is built to order, so what you pay follows what your business actually needs. We talk it through first and you get quoted on exactly that.',
    ld=[crumbs('Pricing', f'{SITE}/pricing.html')],
  ),
  'book.html': dict(
    path='/book.html',
    title='Book a Free 30 Minute Call | Studio Wallace',
    desc='Book a free half hour on Google Meet. Tell me what your business needs and hear exactly how it gets built. Nothing to prepare.',
    ld=[crumbs('Book a meeting', f'{SITE}/book.html')],
  ),
  'pay.html': dict(
    path='/pay.html',
    title='Pay Your Invoice | Studio Wallace',
    desc='Pay your Studio Wallace invoice.',
    ld=[], noindex=True,
  ),
}


def block(p):
    url = SITE + p['path']
    tags = [START]
    if p.get('noindex'):
        tags.append('<meta name="robots" content="noindex, follow">')
    else:
        tags.append('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">')
    tags += [
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="Studio Wallace">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:title" content="{p["title"]}">',
        f'<meta property="og:description" content="{p["desc"]}">',
        f'<meta property="og:image" content="{OG_IMAGE}">',
        f'<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{p["title"]}">',
        f'<meta name="twitter:description" content="{p["desc"]}">',
        f'<meta name="twitter:image" content="{OG_IMAGE}">',
    ]
    for ld in p['ld']:
        tags.append(f'<script type="application/ld+json">\n{ld}\n</script>')
    tags.append(END)
    return '\n'.join(tags) + '\n'


for f, p in PAGES.items():
    s = open(f).read()
    s = re.sub(r'<title>.*?</title>', f'<title>{p["title"]}</title>', s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content=".*?">',
               f'<meta name="description" content="{p["desc"]}">', s, count=1, flags=re.S)
    s = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', s, flags=re.S)
    s = s.replace('</head>', block(p) + '</head>', 1)
    open(f, 'w').write(s)
    print('seo ->', f)

with open('robots.txt', 'w') as f:
    f.write(f'''User-agent: *
Allow: /
Disallow: /pay.html

Sitemap: {SITE}/sitemap.xml
''')

urls = ''.join(
    f'  <url>\n    <loc>{SITE}{p["path"]}</loc>\n'
    f'    <changefreq>{"weekly" if p["path"] == "/" else "monthly"}</changefreq>\n'
    f'    <priority>{"1.0" if p["path"] == "/" else "0.8"}</priority>\n  </url>\n'
    for p in PAGES.values() if not p.get('noindex'))
with open('sitemap.xml', 'w') as f:
    f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

print('robots.txt + sitemap.xml written')
