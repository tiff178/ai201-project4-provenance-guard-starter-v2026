# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 22:37
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `50740b38-e4ed-48a6-9b5b-067c5199e0a2` | unsure | 0.259 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `92d2614e-a8fc-4ff2-b81b-adfdcd71eb43` | unsure | 0.037 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `e662b798-3fac-46c2-a099-570af59680bd` | unsure | 0.153 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `9bd753a1-14f1-4f91-b991-5f1c03012d64` | unsure | 0.166 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `6334f7cc-df61-4658-a525-fbe4781109f0` | human | 0.302 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `649a8e0d-45d7-4ce4-aec1-585142614a0e` | unsure | 0.065 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `06458628-25e1-474b-8839-db00b5a570f8` | unsure | 0.005 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `ed5ff4bd-667e-4f14-9337-1ab80ba48adb` | unsure | 0.182 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `608d3f9b-f5d4-4b99-943d-6ecc84f55901` | unsure | 0.165 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `68f392eb-cb4a-495a-8cc9-ead48580eb46` | ai | 0.741 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `56fa7d26-ae41-4177-8d4f-8ba8577879b7` | unsure | 0.199 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `fcaed47f-699e-4e55-9c16-98c9fd03377e` | unsure | 0.400 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `461f88af-a295-4f6d-9a28-6e8bf051f212` | ai | 0.455 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `a2d851b7-9e91-441d-937f-7974d9ba1a4c` | ai | 0.417 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `8facc0d3-ab07-4129-805f-b3c5bb8e385e` | ai | 0.465 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `92d0f448-17e4-4b73-90ab-2a51da274604` | unsure | 0.380 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `75e74e06-d36a-49d0-98e5-c60f1b5ba431` | unsure | 0.380 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `5dd97ad6-433a-4b43-b249-99934d073b7a` | unsure | 0.155 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `40ca9759-1977-4531-a5ef-906feab965c8` | unsure | 0.070 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `ad24f4a3-f300-465d-917b-041812e33407` | human | 0.406 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7ace099f-4a2c-45c5-8208-95c22eb30501` | unsure | 0.086 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `34820925-afc0-41ca-8ecb-af7fddb7bbcb` | unsure | 0.051 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `985f2252-4584-42cc-ae66-c7271b88f4b7` | unsure | 0.173 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `dce0ec58-dcae-4855-a8c7-98ef12785f47` | unsure | 0.137 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `e014b6b8-6d2a-40d5-9535-26d02c23030c` | unsure | 0.280 | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `5737206b-8f62-4fa2-b18c-5d58012b562b` | unsure | 0.380 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `62174e15-89c7-4e06-8dd3-1218308d3ffb` | unsure | 0.094 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0c88752b-48d0-4483-af03-c4dec205d46c` | unsure | 0.280 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `cf9debbe-3941-40f0-9224-8951a0651a47` | unsure | 0.280 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `445047af-7c40-4d5f-a63f-55d435c02af0` | unsure | 0.280 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `282d9ed4-7422-4483-8fd8-3596c847d475` | unsure | 0.280 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2c7f13a8-34a0-4b88-9b22-e5ea125b30ca` | unsure | 0.280 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c36ecb14-26cb-443a-b94a-7d7ee236d8c5` | unsure | 0.280 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `7f81ddb5-1e14-4cb1-af89-0f5f63a1bc24` | unsure | 0.280 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `aea4f842-66f0-4b27-98c4-7d775698675c` | unsure | 0.280 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "50740b38-e4ed-48a6-9b5b-067c5199e0a2",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.2587,
  "model_score": 0.1635,
  "style_score": 0.5777937214851786,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "92d2614e-a8fc-4ff2-b81b-adfdcd71eb43",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0367,
  "model_score": 0.5943,
  "style_score": 0.36895823137771533,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "e662b798-3fac-46c2-a099-570af59680bd",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.1531,
  "model_score": 0.6662,
  "style_score": 0.48692492989853936,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "9bd753a1-14f1-4f91-b991-5f1c03012d64",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.1658,
  "model_score": 0.6114,
  "style_score": 0.5543929087321869,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "6334f7cc-df61-4658-a525-fbe4781109f0",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3023,
  "model_score": 0.3212,
  "style_score": 0.37653872845679465,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "649a8e0d-45d7-4ce4-aec1-585142614a0e",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.065,
  "model_score": 0.5727,
  "style_score": 0.36231884057971014,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "06458628-25e1-474b-8839-db00b5a570f8",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0049,
  "model_score": 0.5862,
  "style_score": 0.4089347079037801,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "ed5ff4bd-667e-4f14-9337-1ab80ba48adb",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.1824,
  "model_score": 0.2452,
  "style_score": 0.5723857625084604,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "608d3f9b-f5d4-4b99-943d-6ecc84f55901",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.1649,
  "model_score": 0.7042,
  "style_score": 0.46073113610805233,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "68f392eb-cb4a-495a-8cc9-ead48580eb46",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7411,
  "model_score": 0.9792,
  "style_score": 0.7618607564466905,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "56fa7d26-ae41-4177-8d4f-8ba8577879b7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1993,
  "model_score": 0.6175,
  "style_score": 0.581802784739827,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "fcaed47f-699e-4e55-9c16-98c9fd03377e",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.3998,
  "model_score": 0.7387,
  "style_score": 0.6611116446852616,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "461f88af-a295-4f6d-9a28-6e8bf051f212",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.4547,
  "model_score": 0.8051,
  "style_score": 0.6496398516315162,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "a2d851b7-9e91-441d-937f-7974d9ba1a4c",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.4166,
  "model_score": 0.8329,
  "style_score": 0.5836558866707483,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "8facc0d3-ab07-4129-805f-b3c5bb8e385e",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.4653,
  "model_score": 0.8005,
  "style_score": 0.6648470364437674,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "92d0f448-17e4-4b73-90ab-2a51da274604",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8814,
  "style_score": 0.5561120028558734,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "75e74e06-d36a-49d0-98e5-c60f1b5ba431",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8816,
  "style_score": 0.5473228664308369,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "5dd97ad6-433a-4b43-b249-99934d073b7a",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.1554,
  "model_score": 0.3223,
  "style_score": 0.5223290993692603,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "40ca9759-1977-4531-a5ef-906feab965c8",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.0695,
  "model_score": 0.4625,
  "style_score": 0.46800402418152576,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "ad24f4a3-f300-465d-917b-041812e33407",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.4055,
  "model_score": 0.2044,
  "style_score": 0.3901290685348684,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "7ace099f-4a2c-45c5-8208-95c22eb30501",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.086,
  "model_score": 0.5943,
  "style_score": 0.4917093196114351,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "34820925-afc0-41ca-8ecb-af7fddb7bbcb",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0507,
  "model_score": 0.4998,
  "style_score": 0.4494641315425401,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "985f2252-4584-42cc-ae66-c7271b88f4b7",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1726,
  "model_score": 0.6401,
  "style_score": 0.18730960418076723,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "dce0ec58-dcae-4855-a8c7-98ef12785f47",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.137,
  "model_score": 0.5583,
  "style_score": 0.5786906041100662,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "e014b6b8-6d2a-40d5-9535-26d02c23030c",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "5737206b-8f62-4fa2-b18c-5d58012b562b",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.9876,
  "style_score": 0.5915710673071022,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "62174e15-89c7-4e06-8dd3-1218308d3ffb",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.0938,
  "model_score": 0.2395,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "0c88752b-48d0-4483-af03-c4dec205d46c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "cf9debbe-3941-40f0-9224-8951a0651a47",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "445047af-7c40-4d5f-a63f-55d435c02af0",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "282d9ed4-7422-4483-8fd8-3596c847d475",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "2c7f13a8-34a0-4b88-9b22-e5ea125b30ca",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c36ecb14-26cb-443a-b94a-7d7ee236d8c5",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "7f81ddb5-1e14-4cb1-af89-0f5f63a1bc24",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "aea4f842-66f0-4b27-98c4-7d775698675c",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
