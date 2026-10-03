# Fixing Duplicate Database Records in Laravel

## Root Cause Pattern
Multiple code paths call `Model::create()` without checking for existing records. Common when:
- Multiple controllers handle the same entity creation (registration approval, AI agent, admin panel)
- A standalone sync/migration script also creates records
- No unique database constraint exists

## Diagnosis Steps
1. Identify the duplicated entity (e.g. `schedule_sessions`)
2. Find ALL code paths that create it: `grep -rn "ModelName::create" --include="*.php" | grep -v vendor`
3. Check migrations for unique constraints on the relevant columns
4. Query DB for duplicates: `SELECT col1, col2, col3, COUNT(*) FROM table GROUP BY col1, col2, col3 HAVING COUNT(*) > 1`
5. **Check for linked records before deleting** — e.g., `attendances` table may reference `session_id`

## Fix Pattern (3 parts)

### Part 1: Migration — Cleanup + Unique Constraint
```php
// Clean up existing duplicates (keep earliest ID)
$duplicates = DB::table('table_name')
    ->select('col1', 'col2', DB::raw('COUNT(*) as count'))
    ->groupBy('col1', 'col2')
    ->having('count', '>', 1)
    ->get();

foreach ($duplicates as $dup) {
    $keepId = DB::table('table_name')
        ->where('col1', $dup->col1)->where('col2', $dup->col2)
        ->orderBy('id', 'asc')->first()->id;
    DB::table('table_name')
        ->where('col1', $dup->col1)->where('col2', $dup->col2)
        ->where('id', '!=', $keepId)->delete();
}

// Add unique constraint
Schema::table('table_name', function (Blueprint $table) {
    $table->unique(['col1', 'col2'], 'uniq_col1_col2');
});
```

### Part 2: Dedup Check Before Create (in ALL code paths)
```php
$existing = Model::where('col1', $value1)
    ->where('col2', $value2)
    ->exists();

if (!$existing) {
    Model::create([...]);
}
```

### Part 3: For Reschedule/Update Flows (use existing record)
```php
$existing = Model::where(...)->first();
$record = $existing ?? Model::create([...]);
```

## Emergency DB Cleanup (No Migration Available)
When you can't run migrations (e.g., no DDL permission via API):
```sql
-- Find duplicates
SELECT col1, col2, COUNT(*) as cnt FROM table_name
GROUP BY col1, col2 HAVING cnt > 1;

-- Check linked records before deleting
SELECT * FROM linked_table WHERE foreign_key IN (/* duplicate IDs */);

-- Delete duplicates (keep earliest ID)
DELETE FROM table_name WHERE id IN (/* duplicate IDs to remove */);
```

## Pitfalls
- Must fix ALL code paths, not just one — grep for every `::create()` call
- Unique constraint must match the actual dedup logic (same columns)
- **Check actual DB engine** — migrations may say SQLite but production could be MySQL
- When cleaning up duplicates, always keep the earliest ID (lowest `id`) to preserve referential integrity
- Don't forget standalone scripts (e.g. `scripts/sync_sessions.php`) — they often create records too
- **Check for linked records** — e.g., `attendances.session_id` references `schedule_sessions.id`. Keep the duplicate that has linked records, not just the earliest
- **DDL blocked via API** — `CREATE INDEX`, `ALTER TABLE` blocked on some query endpoints. Use migration files or `DELETE`-based cleanup instead
