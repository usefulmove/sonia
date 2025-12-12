# SQLite Migration Plan

## Executive Summary

Migrate Sonia from DuckDB to SQLite to reduce dependencies, simplify deployment, and better match the application's use case as a simple note-taking CLI tool.

**Status**: Planning Phase  
**Target Version**: 0.4.0 (breaking change)  
**Estimated Effort**: 4-6 hours  
**Risk Level**: Medium (requires careful testing)

---

## 1. Rationale

### Why SQLite is Better for Sonia

| Aspect | DuckDB (Current) | SQLite (Proposed) |
|--------|------------------|-------------------|
| **Use Case** | OLAP/Analytics | OLTP/Transactions |
| **Dependencies** | External package | Python stdlib |
| **File Size** | Larger | Smaller |
| **Complexity** | Higher (schemas, sequences) | Lower (simpler model) |
| **Fit for Notes** | Overkill | Perfect match |

### Benefits
- ✅ Zero external dependencies (part of Python stdlib)
- ✅ Smaller database files
- ✅ Better suited for transactional workload
- ✅ More universal compatibility
- ✅ Simpler codebase maintenance

### Trade-offs
- ❌ Loss of DuckDB's analytical features (not used)
- ❌ Breaking change for existing users
- ⚠️ Requires data migration path for users

---

## 2. Technical Changes Required

### 2.1 Dependencies (`pyproject.toml`)

**Remove:**
```toml
dependencies = [
    "duckdb",
    "rich>=14.2.0",
]
```

**Update to:**
```toml
dependencies = [
    "rich>=14.2.0",
]
# Note: SQLite3 is included in Python standard library
```

### 2.2 Database Module (`src/sonia/notedb.py`)

#### Import Changes (Line 6)
```python
# Before:
import duckdb

# After:
import sqlite3
```

#### Connection Function (Lines 71-93)
```python
# Before:
def get_connection() -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(Path(db_path).expanduser())
    con.begin()
    con.execute(f"create schema if not exists {SCHEMA};")
    con.execute(f"set schema = {SCHEMA};")
    con.execute("create sequence if not exists nid_sequence start 1;")
    con.execute(f"""
        create table if not exists {TABLE} (
            {NID_COLUMN} integer primary key default nextval('nid_sequence'),
            {TIMESTAMP_COLUMN} timestamp,
            {MESSAGE_COLUMN} varchar
        );
    """)
    con.commit()
    return con

# After:
def get_connection() -> sqlite3.Connection:
    con = sqlite3.connect(
        Path(db_path).expanduser(),
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    # SQLite doesn't need schema or sequence - AUTOINCREMENT handles it
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            {NID_COLUMN} INTEGER PRIMARY KEY AUTOINCREMENT,
            {TIMESTAMP_COLUMN} TIMESTAMP,
            {MESSAGE_COLUMN} TEXT
        );
    """)
    con.commit()
    return con
```

#### Schema Constants (Lines 45-50)
```python
# Before:
SCHEMA = "coredb"
TABLE = "notes"

# After:
# SCHEMA removed - SQLite doesn't use schemas
TABLE = "notes"
```

#### Create Notes Function (Lines 285-306)
```python
# Before:
query = f"""
insert into {TABLE}
    ({TIMESTAMP_COLUMN}, {MESSAGE_COLUMN})
values
    (cast('{datetime.now()}' as timestamp), ?)
returning *;
"""

# After:
query = f"""
INSERT INTO {TABLE}
    ({TIMESTAMP_COLUMN}, {MESSAGE_COLUMN})
VALUES
    (?, ?);
"""
# Then fetch the inserted row using last_insert_rowid()
```

#### Rebase Function (Lines 309-352)
```python
# Before: Complex sequence management with DuckDB sequences

# After: Simplified - SQLite AUTOINCREMENT handles next ID automatically
def rebase() -> None:
    """Rebase note identifiers starting at 1."""
    
    with get_connection() as con:
        # Create temporary table with renumbered IDs
        con.execute(f"""
            CREATE TEMPORARY TABLE temp_notes AS
            SELECT 
                ROW_NUMBER() OVER(ORDER BY {NID_COLUMN}) as new_id,
                {TIMESTAMP_COLUMN},
                {MESSAGE_COLUMN}
            FROM {TABLE};
        """)
        
        # Clear and rebuild main table
        con.execute(f"DELETE FROM {TABLE};")
        con.execute(f"""
            INSERT INTO {TABLE} 
                ({NID_COLUMN}, {TIMESTAMP_COLUMN}, {MESSAGE_COLUMN})
            SELECT new_id, {TIMESTAMP_COLUMN}, {MESSAGE_COLUMN}
            FROM temp_notes
            ORDER BY new_id;
        """)
        
        # Clean up
        con.execute("DROP TABLE temp_notes;")
        
        # Reset AUTOINCREMENT counter
        max_id = con.execute(
            f"SELECT MAX({NID_COLUMN}) FROM {TABLE}"
        ).fetchone()[0] or 0
        
        con.execute(f"""
            UPDATE sqlite_sequence 
            SET seq = {max_id} 
            WHERE name = '{TABLE}';
        """)
        
        con.commit()
```

#### Clear Database Function (Lines 159-166)
```python
# Before:
con.execute(f"delete from {TABLE};")
con.execute("create or replace sequence nid_sequence start 1")

# After:
con.execute(f"DELETE FROM {TABLE};")
con.execute(f"DELETE FROM sqlite_sequence WHERE name = '{TABLE}';")
```

#### Query Adjustments
Most queries should work as-is since the code already uses `?` parameter placeholders. Key changes:
- Remove schema prefixes (no `{SCHEMA}.{TABLE}`, just `{TABLE}`)
- `varchar` → `TEXT`
- `timestamp` → `TIMESTAMP` (with proper type detection)
- `ILIKE` → Need case-insensitive collation or use `LIKE` with `LOWER()`

---

## 3. Data Migration Strategy

### Option A: Simple Approach (Recommended)
**Breaking change with manual migration**

**Documentation approach:**
1. Add migration notes to README
2. Provide export command example
3. User manually exports from old version, upgrades, re-imports

**Pros:** Simple, no complex migration code  
**Cons:** Users must manually migrate

### Option B: Automated Migration Script
**Create `scripts/migrate_duckdb_to_sqlite.py`**

```python
#!/usr/bin/env python3
"""Migrate Sonia notes from DuckDB to SQLite."""

import sys
from pathlib import Path
import duckdb
import sqlite3
from datetime import datetime

def migrate(duckdb_path: str, sqlite_path: str) -> None:
    """Read from DuckDB, write to SQLite."""
    # Connect to DuckDB
    duck_con = duckdb.connect(duckdb_path)
    
    # Read all notes
    notes = duck_con.execute("""
        SELECT nid, date, message 
        FROM coredb.notes 
        ORDER BY nid
    """).fetchall()
    
    duck_con.close()
    
    # Write to SQLite
    sqlite_con = sqlite3.connect(sqlite_path)
    sqlite_con.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            nid INTEGER PRIMARY KEY,
            date TIMESTAMP,
            message TEXT
        )
    """)
    
    sqlite_con.executemany(
        "INSERT INTO notes (nid, date, message) VALUES (?, ?, ?)",
        notes
    )
    
    sqlite_con.commit()
    sqlite_con.close()
    
    print(f"✓ Migrated {len(notes)} notes from DuckDB to SQLite")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: migrate_duckdb_to_sqlite.py <duckdb_file> <sqlite_file>")
        sys.exit(1)
    
    migrate(sys.argv[1], sys.argv[2])
```

**Pros:** Seamless user experience  
**Cons:** More complex, requires maintaining DuckDB as dev dependency

**Recommendation:** Start with Option A, add Option B if user demand is high

---

## 4. Open Questions

Before implementation, need decisions on:

### Q1: Datetime Storage Format
SQLite doesn't have native datetime. Choose one:

- **A. ISO 8601 Text** (e.g., "2025-12-12 10:30:45.123456")
  - ✅ Human-readable in raw database
  - ✅ Standard format
  - ❌ Slightly larger storage
  - **Recommended for this use case**

- **B. Unix Timestamp** (seconds since epoch)
  - ✅ Efficient storage
  - ❌ Not human-readable
  
- **C. Julian Day** (SQLite native)
  - ✅ Optimal for SQLite
  - ❌ Obscure format

**Recommendation:** Option A (ISO 8601)

### Q2: Case-Insensitive Search
DuckDB's `ILIKE` not available in SQLite. Options:

- **A.** Use `LIKE` with `LOWER()`: `LOWER(message) LIKE LOWER(?)`
- **B.** Use `COLLATE NOCASE`: `message LIKE ? COLLATE NOCASE`
- **C.** Create custom collation function

**Recommendation:** Option B (COLLATE NOCASE) - cleaner syntax

### Q3: Database Filename
- Keep: `~/.sonia.db`
- Change to: `~/.sonia.sqlite` or `~/.sonia.sqlite3`

**Recommendation:** Keep `~/.sonia.db` (simpler for users)

### Q4: Migration Support
- Include automated migration script?
- Or document manual process only?

**Recommendation:** Start with documented manual process

### Q5: Version Number
- Breaking change: Bump to 0.4.0?
- Or maintain 0.3.x series?

**Recommendation:** 0.4.0 (semantic versioning for breaking change)

---

## 5. Implementation Phases

### Phase 1: Code Updates (2-3 hours)
- [ ] Update `pyproject.toml` dependencies
- [ ] Rewrite `src/sonia/notedb.py`
  - [ ] Change imports
  - [ ] Update `get_connection()`
  - [ ] Remove schema/sequence logic
  - [ ] Update `create_notes()`
  - [ ] Simplify `rebase()`
  - [ ] Update `clear_database()`
  - [ ] Fix case-insensitive searches
  - [ ] Update all SQL queries
- [ ] Update type hints
- [ ] Run linter: `ruff check --fix`
- [ ] Run formatter: `ruff format`

### Phase 2: Testing (1-2 hours)
- [ ] Run full test suite: `pytest test/`
- [ ] Fix any failing tests
- [ ] Add SQLite-specific edge case tests if needed
- [ ] Manual testing of all commands:
  - [ ] `sonia add "test note"`
  - [ ] `sonia list`
  - [ ] `sonia search "test"`
  - [ ] `sonia remove 1`
  - [ ] `sonia clear`
- [ ] Test on fresh database
- [ ] Test rebase functionality
- [ ] Verify database file size reduction

### Phase 3: Documentation (1 hour)
- [ ] Update `README.md`
  - [ ] Change DuckDB → SQLite in description
  - [ ] Update Technologies section
  - [ ] Add migration notes for existing users
- [ ] Update `CHANGELOG.md` (create if doesn't exist)
- [ ] Add migration guide if providing script
- [ ] Update version to 0.4.0

### Phase 4: Optional Migration Tool (1-2 hours)
Only if decided to provide automated migration:
- [ ] Create `scripts/migrate_duckdb_to_sqlite.py`
- [ ] Test migration script
- [ ] Document usage in README
- [ ] Keep duckdb in dev dependencies temporarily

### Phase 5: Release (30 min)
- [ ] Final test run
- [ ] Commit changes
- [ ] Tag release: `v0.4.0`
- [ ] Update PyPI if published
- [ ] Announce breaking change

---

## 6. Testing Checklist

### Functional Tests
- [ ] All existing pytest tests pass
- [ ] Create notes (single and multiple)
- [ ] List all notes
- [ ] Search with text matching
- [ ] Search with tag matching
- [ ] Update note text
- [ ] Delete specific notes
- [ ] Rebase note IDs
- [ ] Change text in notes
- [ ] Clear database
- [ ] Verify timestamps are correct
- [ ] Test with empty database

### Edge Cases
- [ ] Database doesn't exist (first run)
- [ ] Database is empty
- [ ] Special characters in notes
- [ ] Very long notes
- [ ] Unicode/emoji in notes
- [ ] Concurrent access (if applicable)

### Platform Testing
- [ ] Linux
- [ ] macOS
- [ ] Windows (if supported)

---

## 7. Rollback Plan

If issues arise:

1. **Immediate:** Revert to previous version (0.3.8)
2. **Git:** Use `git revert` on migration commit
3. **Users:** Provide clear rollback instructions
4. **Data:** If migration script provided, document reverse process

---

## 8. Success Criteria

Migration is successful when:

- [ ] All tests pass
- [ ] No DuckDB dependency in `pyproject.toml`
- [ ] Application works exactly as before
- [ ] Database files are smaller
- [ ] Installation is simpler (no external DB dependency)
- [ ] Documentation is updated
- [ ] Migration path exists for users

---

## 9. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Data loss during migration | Low | High | Backup instructions, migration script testing |
| Test failures | Medium | Medium | Comprehensive test suite already exists |
| Performance regression | Low | Low | SQLite should be faster for this use case |
| User confusion | Medium | Medium | Clear documentation and migration guide |
| Subtle SQL differences | Medium | Medium | Thorough testing of all queries |

---

## 10. Timeline

**Estimated Total: 4-6 hours**

- Code updates: 2-3 hours
- Testing: 1-2 hours  
- Documentation: 1 hour
- Migration tool (optional): +1-2 hours

Can be completed in single session or split across 2 days.

---

## 11. Next Steps

**Before Implementation:**
1. ✅ Review this plan
2. ⏳ Answer open questions (Section 4)
3. ⏳ Get approval to proceed
4. ⏳ Decide on migration approach

**After Approval:**
1. Create feature branch: `git checkout -b feature/sqlite-migration`
2. Begin Phase 1 implementation
3. Iterate through phases 2-5
4. Merge and release

---

## Notes

- SQLite version in Python 3.13+: 3.45.3 (verified via stdlib)
- No breaking changes to CLI interface (commands stay same)
- Database file format changes (binary incompatible with DuckDB)
- Consider this a good opportunity to bump to 0.4.0

---

**Document Version:** 1.0  
**Created:** 2025-12-12  
**Author:** OpenCode Assistant  
**Status:** Awaiting Review
