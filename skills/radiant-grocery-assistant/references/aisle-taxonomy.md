# Aisle/Section Taxonomy (Scaffold)

Use this when store-specific aisle maps are unavailable.

## Default section order
1. Produce
2. Bakery
3. Meat/Seafood
4. Dairy/Eggs
5. Deli/Prepared
6. Canned/Jarred
7. Dry Goods (Pasta/Rice/Beans)
8. Baking/Spices/Oils
9. Snacks
10. Beverages
11. Frozen
12. Household/Cleaning
13. Personal Care

## Mapping examples
- onions, garlic, lettuce -> Produce
- chicken breast, ground beef -> Meat/Seafood
- milk, yogurt, butter -> Dairy/Eggs
- black beans, diced tomatoes -> Canned/Jarred
- pasta, rice, flour -> Dry Goods

## Store override model

If store layout is known, override section names/order with per-store config:

```json
{
  "store_id": "string",
  "sections": [
    {"name": "Produce", "order": 1, "aliases": ["fruits", "vegetables"]}
  ]
}
```
