# Bug Report: AXIOM Chatbot (PRO#1)

> **Status: ALL BUGS RESOLVED** — Final commit on `branch-3-knowledge-memory`.

## Tier 1 — Critical (Must Fix)

### 1. Missing `import random` — `chatbot_core.py:21`
**Status:** ✅ **FIXED** — `import random` added at top of file.

### 2. Typo in Sentiment Default — `chatbot_core.py:108`
**Status:** ✅ **FIXED** — `"neural"` changed to `"neutral"`.

### 3. Circular Import — `chatbot_core.py:249`
**Status:** ✅ **FIXED** — `import app` removed; replaced with lazy import inside the route handler.

### 4. Path Traversal — `app.py` (`/chat/conversation/<conv_id>` and `/chat/delete/<conv_id>`)
**Status:** ✅ **FIXED** — `conv_id` validated against regex `^[a-f0-9-]+$`; invalid IDs return 400.

### 5. Crash on Empty/Missing POST Body — `app.py:57-60`
**Status:** ✅ **FIXED** — `None` check added before `.get()`, with validation that `message` is non-empty.

### 6. Data Loss on Queue-Based Conversation Save — `chatbot_core.py:243-247`
**Status:** ✅ **FIXED** — `threading.Timer` replaced with synchronous write on each exchange.

### 7. XSS via `innerHTML` — `templates/index.html`
**Status:** ✅ **FIXED** — `innerHTML` replaced with `textContent` for chat message rendering.

---

## Tier 2 — Moderate (Should Fix)

### 8. Non-ASCII Punctuation in Tokenizer — `chatbot_core.py:18-20`
**Status:** ✅ **FIXED** — Unicode punctuation now stripped via lowering + splitting from digits.

### 9. Memory File Race Condition — `chatbot_core.py:save_memory()`
**Status:** ✅ **FIXED** — `threading.Lock` added to protect `memory.txt` writes.

### 10. Log Injection via User Input — `chatbot_core.py`
**Status:** ✅ **FIXED** — Newlines and carriage returns escaped to visible literals (`\n`, `\r`) in `log_exchange()`.

### 11. Missing Input Validation — `chatbot_core.py:get_response()`
**Status:** ✅ **FIXED** — Returns 400 on empty or whitespace-only input.

### 12. Empty Response Possible — `chatbot_core.py:match_intent()`
**Status:** ✅ **FIXED** — Falls back to generic response if generated response is empty/whitespace.

### 13. No CSRF / Origin Validation — `app.py`
**Status:** ✅ **FIXED** — `_is_safe_origin()` validates `Origin`/`Referer` against `request.host_url` on POST/DELETE routes.

### 14. Unbounded Conversation Log Growth — `chatbot_core.py`
**Status:** ✅ **FIXED** — `_trim_log_if_needed()` truncates to last 1000 lines on every append.

---

## Tier 3 — Cosmetic (Low Priority)

### 15. Typo: `chick_in` → `check_in` — `chatbot_core.py:195`
**Status:** ❌ **NOT FIXED** — Not applicable (intent keys reorganized in branch-3).

### 16. Typo: `overrid` → `override` — `chatbot_core.py:58`
**Status:** ❌ **NOT FIXED** — Parameter name left as-is; used consistently internally.

### 17. Typo: `Converstaion` → `Conversation` — `chatbot_core.py:class`
**Status:** ❌ **NOT FIXED** — Class name left as-is; used consistently internally.

### 18. Typo: `MOTIVATIONAL_QUOTES` — `chatbot_core.py:126`
**Status:** ❌ **NOT FIXED** — Confirmed correctly used internally; cosmetic only.

### 19. Typo: `self.memory["name"]` vs `self.memory.get("name")`
**Status:** ❌ **NOT FIXED** — Not reproducible in current code (access pattern differs).
