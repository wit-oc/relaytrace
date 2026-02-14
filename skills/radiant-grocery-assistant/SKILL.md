---
name: radiant-grocery-assistant
description: Plan household meals and shopping lists with optional sale-aware optimization and aisle/section sorting. Use when users ask for weekly meal plans, grocery lists, budget-aware substitutions, store-efficient shopping routes, or “what should we cook/buy this week.” If sale preference is unknown, ask once before proposing meals and persist that preference for future runs.
---

# Radiant Grocery Assistant

Use this skill to produce meal-plan + shopping outputs with a clear preference handshake.

## Interaction contract (required)

Before proposing meals, check whether sale optimization preference is known:
1. If known, apply stored setting.
2. If unknown, ask once:
   - "Do you want me to bias this week’s plan toward sale items?"
   - options: `yes`, `no`, `only-if-similar-quality`
3. Persist preference for next run in session/user memory.

Do not re-ask every turn once preference is known unless user changes it.

## Planning workflow

1. Collect constraints
   - household size, prep time, dietary constraints, budget signal
2. Build candidate meals
   - prioritize feasible prep and repeatable ingredients
3. Apply sale bias (optional)
   - use adapter-normalized sale items from `references/sale-adapter-contract.md`
   - apply only light bias unless user asks strong cost-optimization
4. Build shopping list
   - aggregate recipe ingredients
   - deduplicate and normalize units
5. Sort by aisle/section
   - if store map exists, use it
   - else use heuristic taxonomy from `references/aisle-taxonomy.md`
6. Output
   - meal plan
   - shopping list by aisle/section
   - substitutions + cost notes

## Output requirements

Return these sections in order:
1. `Meal Plan`
2. `Shopping List (By Aisle/Section)`
3. `Sale-Driven Swaps`
4. `Assumptions / Missing Inputs`

If store-specific aisle data is missing, state that sorting is heuristic.

## Files to consult

- `references/sale-adapter-contract.md`
- `references/aisle-taxonomy.md`
- `templates/user-preference-schema.json`
- `templates/shopping-output-schema.json`
