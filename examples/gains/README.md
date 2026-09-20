# Example gain submissions

What a student's submission looks like, and the fixtures `scripts/gains.py` is
tested against. **No student work is here, and none ever should be.**

Real submissions arrive in a MATLAB Drive folder that syncs to the lecturer's
machine. Point the tool at that folder directly:

```bash
python scripts/gains.py check ~/MATLAB\ Drive/cade30008-gains
```

| File | What it exercises |
|---|---|
| `reference.json`, `good.csv` | Designs inside the envelope, which should be accepted. |
| `alice.json`, `bob.csv` | Stable but too slow — rejected on settling time. |
| `team.csv` | One per failure mode: unstable, negative gain, no derivative, over-voltage. |
| `broken.json` | Not valid JSON. Must be reported by name, not skipped silently. |
| `nogains.csv` | Readable, but no `kp`/`ki`/`kd` columns. |

Either format works, and the reader is deliberately forgiving about shape — key
case, column order, stray whitespace — and unforgiving about values:

```json
{"name": "Kestrel", "kp": 6.0, "ki": 0.18, "kd": 14.0}
```

```csv
alias,kp,ki,kd
Kestrel,6.0,0.18,14.0
```

`name` or `alias`, whichever a student gives. **The drop folder is shared, so
everyone can see everyone's submission** — which is why an alias is offered, and
why students are told that before they upload, not after.
