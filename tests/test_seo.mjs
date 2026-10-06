import assert from 'node:assert/strict';
import test from 'node:test';
import {
  absoluteUrl, getCanonicalUrl, generateMetadata, JsonLd,
  generateArticleJsonLd, generateProductJsonLd,
} from '../skills/seo-nextjs-implementation/scripts/seo.ts';

test('JSON-LD escapes script termination without changing the data', () => {
  const payload = { name: '</script><script>alert(1)</script>', description: '<b>test</b>' };
  const element = JsonLd({ data: payload });
  const html = element.props.dangerouslySetInnerHTML.__html;
  assert.equal(element.type, 'script');
  assert.equal(element.props.type, 'application/ld+json');
  assert.equal(html.includes('<'), false);
  assert.deepEqual(JSON.parse(html), payload);
});

test('layout defaults do not make every route canonical to the homepage', () => {
  const layout = generateMetadata();
  assert.equal(layout.alternates, undefined);
  assert.equal(layout.openGraph.url, undefined);
  const page = generateMetadata({ url: '/pricing' });
  assert.equal(page.alternates.canonical, 'https://example.com/pricing');
  assert.equal(page.openGraph.url, 'https://example.com/pricing');
  assert.equal(generateMetadata({ url: '/copy', canonical: '/original' }).alternates.canonical,
    'https://example.com/original');
});

test('canonical policy preserves content queries and removes only selected tracking', () => {
  assert.equal(getCanonicalUrl('/browse?page=2&utm_source=x#results'),
    'https://example.com/browse?page=2&utm_source=x');
  assert.equal(getCanonicalUrl('/browse?page=2&utm_source=x#results', ['utm_source']),
    'https://example.com/browse?page=2');
});

test('URL construction resolves relative assets and rejects unsafe URLs', () => {
  assert.equal(absoluteUrl('og.png'), 'https://example.com/og.png');
  assert.equal(absoluteUrl('https://cdn.example.org/image.png'), 'https://cdn.example.org/image.png');
  assert.equal(absoluteUrl('//cdn.example.org/image.png'), 'https://cdn.example.org/image.png');
  for (const value of ['javascript:alert(1)', 'data:text/html,test', 'https://user:password@example.org']) {
    assert.throws(() => absoluteUrl(value));
  }
});

test('article helper preserves actual dates and omits unknown author links', () => {
  const article = generateArticleJsonLd({ title: 'Test', description: 'Example', url: 'https://example.com/post',
    image: 'https://cdn.example.org/og.png', datePublished: '2026-10-06', authorName: 'Author' });
  assert.equal(article.image, 'https://cdn.example.org/og.png');
  assert.equal('dateModified' in article, false);
  assert.equal('url' in article.author, false);
  assert.equal(article.datePublished, '2026-10-06');
});

test('product helper does not invent availability', () => {
  const product = generateProductJsonLd({ name: 'Test', description: 'Example',
    offers: [{ price: 10, priceCurrency: 'USD' }] });
  assert.equal('availability' in product.offers[0], false);
});
