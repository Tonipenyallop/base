# base — a database storage engine from scratch

A disk-backed storage engine built in Python from first principles to explore
how databases manage memory and disk: **slotted pages**, a **bitmap free-space
map**, and a **buffer-pool manager with CLOCK (second-chance) page replacement**.

No frameworks — every layer, down to byte-level page layout and raw `seek`/
`read`/`write`, is hand-written. The goal was to *measure* why a buffer pool
matters, not just to read about it.

## Result

On the bundled test workload (`testcase.txt`, starting from the committed data
file), routing page access through the buffer pool instead of hitting disk
directly cut disk **reads ~5× (74 → 14)** while roughly halving seeks and writes.
Every file operation is instrumented (`fileLogger.py`), so the trade-offs between
strategies are observable rather than assumed.

| Page accessor                 | reads | seeks | writes |
| ----------------------------- | :---: | :---: | :----: |
| Direct disk I/O               |  74   |  142  |   68   |
| Single-frame buffer (`pageBuffer`) |  14 |  35   |   21   |
| **Buffer pool, CLOCK (`clockBuffer`)** | **14** | **26** | **12** |

The 6-frame buffer pool with CLOCK eviction does the least disk work of the
three and is the default accessor.

## Architecture

Requests flow top-down; each layer is independently testable.

```
main.py (REPL: write / read / delete)
   │
   ▼
ClockBuffer  ── 6-frame pool, CLOCK eviction (default) ┐
PageBuffer   ── single-frame buffer                    │  swap to compare
FileManager  ── direct disk I/O (no cache)             ┘
   │
   ▼
FileManager  → maps pageIndex → byte offset
   │
   ▼
FileLogger   → wraps the file, counts read/seek/write
   │
   ▼
data/data-0.bin  (fixed-size 41-byte pages on disk)
```

### Components

| File              | Responsibility                                                                 |
| ----------------- | ------------------------------------------------------------------------------ |
| `bitmap.py`       | 1-byte free-space bitmap; bitwise set/unset/scan over 8 record slots           |
| `page.py`         | Slotted page: 1-byte bitmap header + 8 fixed-width 5-byte records (41 B total) |
| `fileManager.py`  | Translates a page index to a byte offset and performs raw page I/O             |
| `fileLogger.py`   | Instruments the underlying file to count read/seek/write operations            |
| `pageBuffer.py`   | Minimal single-frame buffer with a dirty bit and flush-on-eviction (baseline)  |
| `clockBuffer.py`  | Buffer pool holding up to 6 pages, backed by the CLOCK replacement policy       |
| `clock.py`        | CLOCK / second-chance algorithm: reference bits + a rotating clock hand        |
| `node.py`         | A buffer frame: page, page index, reference bit, dirty bit                     |
| `main.py`         | Interactive REPL; swap the page accessor to A/B the three strategies           |

## Page layout

Each page is exactly 41 bytes:

```
byte 0           bytes 1..40
┌──────────┬───────────────────────────────────────────┐
│ bitmap   │ slot0 │ slot1 │ ... │ slot7                │
│ (8 bits) │ 5 B   │ 5 B   │     │ 5 B                  │
└──────────┴───────────────────────────────────────────┘
```

Bit *i* of the header marks whether slot *i* is occupied, so inserts find the
next free slot in O(1)-per-byte and deletes just clear a bit — no compaction.

## Running it

```bash
# initialize a fresh data file and replay the sample workload
bash db_init.bash

# or start the interactive REPL
python3 main.py
```

REPL commands:

```
write <5-char value>     # insert a record into the next free slot
read <pageIndex>:<row>   # read slot <row> of page <pageIndex>
delete <pageIndex>:<row> # free a slot
fini                     # flush dirty pages and exit
```

Switch the active strategy in `main.py` by changing `pageAccessor` to
`fileManager` (direct), `pageBuffer`, or `clockBuffer`.

## Tests

```bash
python3 testBitmap.py
python3 testPage.py
python3 testClock.py
python3 testClockBuffer.py
```

## What I learned

- How caching pages in memory turns repeated page access into cache hits, and
  how to quantify it by instrumenting disk I/O.
- Slotted-page design and bitmap-based free-space management at the byte level.
- The CLOCK / second-chance algorithm as a cheap approximation of LRU, using a
  reference bit per frame instead of full access ordering.

## Background

Inspired by UC Berkeley's [CS186](https://cs186berkeley.net/) database internals
course ([lectures](https://www.youtube.com/@CS186Berkeley/playlists)).
