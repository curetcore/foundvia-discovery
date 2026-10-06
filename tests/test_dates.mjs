import assert from 'node:assert/strict';
import { contentDates } from '../skills/seo-slug-dates/scripts/dates.ts';
const now = new Date('2026-10-06T12:00:00Z');
assert.deepEqual(contentDates({}, now), { datePublished: undefined, dateModified: undefined });
assert.deepEqual(contentDates({ publishedAt: '2026-01-01', updatedAt: '2026-02-01' }, now), { datePublished: '2026-01-01', dateModified: '2026-02-01' });
assert.equal(contentDates({ publishedAt: '2024-02-29' }, now).datePublished, '2024-02-29');
for (const publishedAt of ['2026-02-30', '2026-13-01', '2026-10-07', 'not-a-date', '2026-01-01T00:00:00']) {
  assert.throws(() => contentDates({ publishedAt }, now));
}
assert.throws(() => contentDates({ publishedAt: '2026-02-01', updatedAt: '2026-01-01' }, now));
assert.throws(() => contentDates({}, new Date('invalid')));
assert.equal(contentDates({ updatedAt: '2026-10-06T07:00:00-04:00' }, now).dateModified, '2026-10-06T07:00:00-04:00');
console.log('Content date checks passed (11 assertions).');
