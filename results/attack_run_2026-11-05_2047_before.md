# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-05 20:47
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **55**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `773b992e-b76b-405e-8d1f-6b1e52f178ba` | unsure | 0.259 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `2dc73af3-d739-4917-9060-cbb78b8fdecb` | unsure | 0.037 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `b951cdba-4816-4862-9178-31c600266fa7` | unsure | 0.153 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `ea1139f9-ad54-490a-8e93-2b4666db8ab0` | unsure | 0.166 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `3a10277c-0426-49df-a398-dd4943e6076f` | human | 0.302 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `bec0dcac-8205-4b2a-ab13-30ae229c4356` | unsure | 0.065 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `84bf77f1-258f-4085-be80-efbaf5f89f3a` | unsure | 0.005 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `e727644b-845b-49fe-9862-18c2913e0571` | unsure | 0.182 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `1c5cc5c7-730d-4e46-ba5b-70a8c5c0e563` | unsure | 0.165 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `458f9b1a-e73d-4cf9-ba9c-171b8954b16b` | ai | 0.741 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `5a0ec27f-ae4e-429d-9005-24d3cfa698d3` | unsure | 0.199 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `3b2b611a-0585-4465-80ca-f8a020d4adfb` | unsure | 0.400 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `a3b14e53-c6df-430d-aa7c-f20ee8998f5f` | ai | 0.455 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `3c276dde-8f8a-4a4a-800b-b00d9b1b3430` | ai | 0.417 | BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `9fc1d82f-3da3-4675-8e2c-7d9f815b456a` | ai | 0.465 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `a38d43ba-b359-482a-b1ca-431a785bf817` | unsure | 0.380 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b584e435-a053-43ae-bcd3-649aa764acb1` | unsure | 0.380 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `907b69a8-364f-4399-b10c-fa182b277c25` | unsure | 0.155 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6004d4c5-05f1-4181-86d3-2296e3905598` | unsure | 0.070 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `692ded33-91a0-4e2f-b279-0341c1811c03` | human | 0.406 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `b12358f3-f817-410a-a237-a8dc9e32d14d` | unsure | 0.086 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f0d67daf-3dc4-422b-82f8-80b0874089cd` | unsure | 0.051 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `87eb1b9c-6be3-431a-bd78-75fb16fc4cb7` | unsure | 0.173 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `4777d5e6-2250-45ec-b4bc-090520bc91cc` | unsure | 0.137 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 500 | `—` | — | — | BROKE |
| MF03 | malformed | text is control characters | 200 | `1c32771e-2432-4f72-bb5c-899984c82d31` | unsure | 0.280 | HELD |
| MF04 | malformed | text is only punctuation | 200 | `65bd6003-be08-4744-b881-e51c99b4c25a` | unsure | 0.011 | HELD  |
| MF05 | malformed | text is a very long single word | 200 | `5793a466-07bb-4dfe-984d-1cba376f431d` | unsure | 0.380 | HELD |
| MF06 | malformed | text is emoji only | 200 | `1bd130cd-e267-4ff0-9d9a-ca531935bba8` | ai | 0.997 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `4df24544-a879-4544-974a-c3af3ca01c27` | ai | 0.906 | BROKE |
| MF08 | malformed | text is 60,000 characters | 200 | `a2923b1f-20c4-413c-9bb8-5eadd0e6901c` | unsure | 0.380 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `f345e9c4-d740-4267-8c5d-5f8ea661bd04` | unsure | 0.094 | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 200 | `f187d507-ee14-424f-b91f-e323095f7199` | unsure | 0.280 | BROKE |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `41202e3c-3c98-4bfa-8333-97d43404da88` | unsure | 0.280 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c05ee837-eb63-4cfd-b502-f99e23b54949` | unsure | 0.280 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `688a6a5a-850d-4550-9c26-187afb5dc6cb` | unsure | 0.280 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `47c53093-00dc-4dcb-a46e-78c56e879895` | unsure | 0.280 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `af0e152e-e502-44fe-8bee-63fc93cdda8b` | unsure | 0.280 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `40387ad7-8dc8-4fb3-8b59-e7c512caf328` | unsure | 0.280 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1014f1e1-1db5-41f3-aeda-5ef17c627859` | unsure | 0.280 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `759d6c52-5e57-4e7b-9898-0da10cfe1038` | unsure | 0.280 | HELD |
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
| `malformed` | 20 | 1 | 19 |
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
  "content_id": "773b992e-b76b-405e-8d1f-6b1e52f178ba",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.2587,
  "model_score": 0.1635,
  "style_score": 0.5777937214851786,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "2dc73af3-d739-4917-9060-cbb78b8fdecb",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.0367,
  "model_score": 0.5943,
  "style_score": 0.36895823137771533,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "b951cdba-4816-4862-9178-31c600266fa7",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.1531,
  "model_score": 0.6662,
  "style_score": 0.48692492989853936,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "ea1139f9-ad54-490a-8e93-2b4666db8ab0",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.1658,
  "model_score": 0.6114,
  "style_score": 0.5543929087321869,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "3a10277c-0426-49df-a398-dd4943e6076f",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3023,
  "model_score": 0.3212,
  "style_score": 0.37653872845679465,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "bec0dcac-8205-4b2a-ab13-30ae229c4356",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.065,
  "model_score": 0.5727,
  "style_score": 0.36231884057971014,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "84bf77f1-258f-4085-be80-efbaf5f89f3a",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0049,
  "model_score": 0.5862,
  "style_score": 0.4089347079037801,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "e727644b-845b-49fe-9862-18c2913e0571",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.1824,
  "model_score": 0.2452,
  "style_score": 0.5723857625084604,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "1c5cc5c7-730d-4e46-ba5b-70a8c5c0e563",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.1649,
  "model_score": 0.7042,
  "style_score": 0.46073113610805233,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "458f9b1a-e73d-4cf9-ba9c-171b8954b16b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7411,
  "model_score": 0.9792,
  "style_score": 0.7618607564466905,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "5a0ec27f-ae4e-429d-9005-24d3cfa698d3",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.1993,
  "model_score": 0.6175,
  "style_score": 0.581802784739827,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "3b2b611a-0585-4465-80ca-f8a020d4adfb",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.3998,
  "model_score": 0.7387,
  "style_score": 0.6611116446852616,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "a3b14e53-c6df-430d-aa7c-f20ee8998f5f",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.4547,
  "model_score": 0.8051,
  "style_score": 0.6496398516315162,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "3c276dde-8f8a-4a4a-800b-b00d9b1b3430",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.4166,
  "model_score": 0.8329,
  "style_score": 0.5836558866707483,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "9fc1d82f-3da3-4675-8e2c-7d9f815b456a",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.4653,
  "model_score": 0.8005,
  "style_score": 0.6648470364437674,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "a38d43ba-b359-482a-b1ca-431a785bf817",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8814,
  "style_score": 0.5561120028558734,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "b584e435-a053-43ae-bcd3-649aa764acb1",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8816,
  "style_score": 0.5473228664308369,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "907b69a8-364f-4399-b10c-fa182b277c25",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.1554,
  "model_score": 0.3223,
  "style_score": 0.5223290993692603,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6004d4c5-05f1-4181-86d3-2296e3905598",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.0695,
  "model_score": 0.4625,
  "style_score": 0.46800402418152576,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "692ded33-91a0-4e2f-b279-0341c1811c03",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.4055,
  "model_score": 0.2044,
  "style_score": 0.3901290685348684,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "b12358f3-f817-410a-a237-a8dc9e32d14d",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.086,
  "model_score": 0.5943,
  "style_score": 0.4917093196114351,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "f0d67daf-3dc4-422b-82f8-80b0874089cd",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0507,
  "model_score": 0.4998,
  "style_score": 0.4494641315425401,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "87eb1b9c-6be3-431a-bd78-75fb16fc4cb7",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1726,
  "model_score": 0.6401,
  "style_score": 0.18730960418076723,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "4777d5e6-2250-45ec-b4bc-090520bc91cc",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.137,
  "model_score": 0.5583,
  "style_score": 0.5786906041100662,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 500,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>ValueError: Text is too short to score \u2014 a few sentences at least.\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes&a",
  "verdict": "BROKE"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "1c32771e-2432-4f72-bb5c-899984c82d31",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "65bd6003-be08-4744-b881-e51c99b4c25a",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0112,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "5793a466-07bb-4dfe-984d-1cba376f431d",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.9976,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "1bd130cd-e267-4ff0-9d9a-ca531935bba8",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.9969,
  "model_score": 0.9969,
  "style_score": 1.0,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "4df24544-a879-4544-974a-c3af3ca01c27",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9064,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "a2923b1f-20c4-413c-9bb8-5eadd0e6901c",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.9876,
  "style_score": 0.5915710673071022,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "f345e9c4-d740-4267-8c5d-5f8ea661bd04",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.0938,
  "model_score": 0.2395,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "f187d507-ee14-424f-b91f-e323095f7199",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0492,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "41202e3c-3c98-4bfa-8333-97d43404da88",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c05ee837-eb63-4cfd-b502-f99e23b54949",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "688a6a5a-850d-4550-9c26-187afb5dc6cb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "47c53093-00dc-4dcb-a46e-78c56e879895",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "af0e152e-e502-44fe-8bee-63fc93cdda8b",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "40387ad7-8dc8-4fb3-8b59-e7c512caf328",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "1014f1e1-1db5-41f3-aeda-5ef17c627859",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "759d6c52-5e57-4e7b-9898-0da10cfe1038",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.28,
  "model_score": 0.0287,
  "style_score": 0.6666666666666666,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
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
  "verdict": ""
}
```
