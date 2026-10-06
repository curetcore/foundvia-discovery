/** Explicit, truthful dates. Synthetic slug-based date generators were removed. */
export interface ContentDateRecord {
  publishedAt?: string;
  updatedAt?: string;
}

function validated(value: string | undefined, label: string, now: Date): string | undefined {
  if (value === undefined) return undefined;
  // Accept an ISO calendar day or an explicit ISO timestamp with timezone.
  if (!/^\d{4}-\d{2}-\d{2}(?:T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?(?:Z|[+-]\d{2}:\d{2}))?$/.test(value)) {
    throw new Error(`${label} must be an ISO date or timezone-qualified timestamp`);
  }
  const parsed = new Date(value);
  const calendarDay = value.slice(0, 10);
  if (!Number.isFinite(parsed.getTime()) || new Date(calendarDay).toISOString().slice(0, 10) !== calendarDay) {
    throw new Error(`${label} is not a valid calendar date`);
  }
  if (parsed.getTime() > now.getTime()) throw new Error(`${label} cannot be in the future`);
  return value;
}

export function contentDates(record: ContentDateRecord, now = new Date()) {
  if (!Number.isFinite(now.getTime())) throw new Error("now must be a valid Date");
  const datePublished = validated(record.publishedAt, "publishedAt", now);
  const dateModified = validated(record.updatedAt, "updatedAt", now);
  if (datePublished && dateModified && new Date(dateModified) < new Date(datePublished)) {
    throw new Error("updatedAt cannot precede publishedAt");
  }
  return { datePublished, dateModified };
}
