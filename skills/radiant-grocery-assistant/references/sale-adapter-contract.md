# Sale Adapter Contract (Scaffold)

Purpose: normalize weekly sale sources into a consistent item feed.

## Normalized sale item

```json
{
  "store_id": "string",
  "store_name": "string",
  "week_of": "YYYY-MM-DD",
  "item_name": "string",
  "brand": "string|null",
  "size": "string|null",
  "price": 0.0,
  "unit_price": 0.0,
  "unit": "oz|lb|ct|...",
  "category": "produce|protein|dairy|dry_goods|frozen|...",
  "valid_from": "ISO-8601",
  "valid_to": "ISO-8601",
  "source_url": "string"
}
```

## Adapter interface

- Input: raw flyer/ad data (API, scrape, manual import)
- Output: list of normalized sale items
- Hard rule: adapters must preserve `source_url` and validity windows

## Matching guidance

- Use fuzzy match to map sale items to ingredient canonical names.
- Prefer exact unit/size matches.
- If no size match, mark as `approximate_match=true` in internal scoring.
