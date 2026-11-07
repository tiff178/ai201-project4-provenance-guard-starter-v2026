# Attack run — aftersecondimprovement

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 23:30
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `5da514b6-16a9-4103-a678-d212d999a576` | unsure | 0.259 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `0f194004-9986-4787-a1e8-ee6b5a52d960` | unsure | 0.037 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4dc7803e-0a28-4df6-a38e-ba2605bdba36` | unsure | 0.153 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `f95e83c4-b0e1-48d0-8b96-e53898bbbe98` | unsure | 0.166 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `8005d1f9-5ac4-43e3-b09b-69c7d9e7d333` | human | 0.302 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `2e0b45f5-43b7-45f3-9e3f-c80081de6bc6` | unsure | 0.065 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `f8a4456c-2758-47d3-af75-1fb2a9d42e2d` | unsure | 0.005 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `1fcd6da3-395c-49c7-a035-59c2bcbbb5ef` | unsure | 0.182 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `0c8a1267-3fa5-40b6-ab7f-ebbe993ddab7` | unsure | 0.165 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `fd95bea0-672e-4e84-850d-8b0b8ec3b823` | ai | 0.741 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `d9e7ba9d-9e56-4bc2-8a49-0e5984618f17` | unsure | 0.199 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `6f5f934b-6216-450b-beb1-687c0f8b4f6d` | unsure | 0.400 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `fcafe4f1-b62d-40fb-ab6a-7dd1668b19af` | unsure | 0.455 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `532ff9f2-a141-4999-85b0-ec93d8c9bf95` | unsure | 0.417 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `e55a4a1b-9611-42d2-bf5d-a17dd71ae573` | ai | 0.465 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `69a0ddab-7e33-40aa-bd5e-8ee9dbf2523b` | unsure | 0.438 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e79bfd66-9814-4068-9834-0596ad38df6b` | unsure | 0.429 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `43ba46d9-8d59-483c-ac23-0bf8274e3f22` | unsure | 0.155 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `91cb53eb-5341-419b-973e-ba0e1313a591` | unsure | 0.070 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `4b93aa3c-8e57-4225-93a7-3f74496cd620` | human | 0.406 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `7e7bea26-4716-452a-bb2e-da0abeb82933` | unsure | 0.086 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `22901c5c-ba50-4701-83fc-0a5de4f2847b` | unsure | 0.051 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `2a4a9a89-338b-4d98-a7c5-f98d825b08dd` | unsure | 0.173 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `11566591-16f3-4ff0-b7d7-b8a7fcb40863` | unsure | 0.137 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `36a7d1bf-5e09-4ace-a160-0956a677f1b7` | unsure | 0.280 | HELD |
| MF04 | malformed | text is only punctuation | 400 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 400 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `9552b5ed-c7a7-49ab-9b46-b5988bb6ffe3` | unsure | 0.440 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 200 | `4a53d0ec-3d4e-41ee-860e-1a398c1735c0` | unsure | 0.094 | HELD |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e4424729-6332-49d9-965b-3174773ab368` | unsure | 0.280 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d2fa97db-d116-4de8-9348-0df8e994cff1` | unsure | 0.280 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1f5f87d5-77ab-4d29-9624-f0a6b83ba407` | unsure | 0.280 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5b9ec270-8044-4676-a000-40ac3ce1f6a3` | unsure | 0.280 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `73fdc669-f632-43ee-98cc-4fdaa4b0eb60` | unsure | 0.280 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4dc2feb0-a04e-467f-bb76-190ff255aff8` | unsure | 0.280 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0fa7b451-682b-4dd1-a515-0aea0ba18103` | unsure | 0.280 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `9d8defe5-dfe4-4cc9-ba91-770db51f032c` | unsure | 0.280 | HELD |
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
  "content_id": "5da514b6-16a9-4103-a678-d212d999a576",
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
  "content_id": "0f194004-9986-4787-a1e8-ee6b5a52d960",
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
  "content_id": "4dc7803e-0a28-4df6-a38e-ba2605bdba36",
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
  "content_id": "f95e83c4-b0e1-48d0-8b96-e53898bbbe98",
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
  "content_id": "8005d1f9-5ac4-43e3-b09b-69c7d9e7d333",
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
  "content_id": "2e0b45f5-43b7-45f3-9e3f-c80081de6bc6",
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
  "content_id": "f8a4456c-2758-47d3-af75-1fb2a9d42e2d",
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
  "content_id": "1fcd6da3-395c-49c7-a035-59c2bcbbb5ef",
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
  "content_id": "0c8a1267-3fa5-40b6-ab7f-ebbe993ddab7",
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
  "content_id": "fd95bea0-672e-4e84-850d-8b0b8ec3b823",
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
  "content_id": "d9e7ba9d-9e56-4bc2-8a49-0e5984618f17",
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
  "content_id": "6f5f934b-6216-450b-beb1-687c0f8b4f6d",
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
  "content_id": "fcafe4f1-b62d-40fb-ab6a-7dd1668b19af",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.4547,
  "model_score": 0.8051,
  "style_score": 0.6496398516315162,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "532ff9f2-a141-4999-85b0-ec93d8c9bf95",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.4166,
  "model_score": 0.8329,
  "style_score": 0.5836558866707483,
  "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e55a4a1b-9611-42d2-bf5d-a17dd71ae573",
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
  "content_id": "69a0ddab-7e33-40aa-bd5e-8ee9dbf2523b",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.4375,
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
  "content_id": "e79bfd66-9814-4068-9834-0596ad38df6b",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.4289,
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
  "content_id": "43ba46d9-8d59-483c-ac23-0bf8274e3f22",
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
  "content_id": "91cb53eb-5341-419b-973e-ba0e1313a591",
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
  "content_id": "4b93aa3c-8e57-4225-93a7-3f74496cd620",
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
  "content_id": "7e7bea26-4716-452a-bb2e-da0abeb82933",
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
  "content_id": "22901c5c-ba50-4701-83fc-0a5de4f2847b",
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
  "content_id": "2a4a9a89-338b-4d98-a7c5-f98d825b08dd",
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
  "content_id": "11566591-16f3-4ff0-b7d7-b8a7fcb40863",
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
  "content_id": "36a7d1bf-5e09-4ace-a160-0956a677f1b7",
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
  "content_id": "9552b5ed-c7a7-49ab-9b46-b5988bb6ffe3",
  "creator_id": "attacker_MF08",
  "guess": "unsure",
  "confidence": 0.44,
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
  "content_id": "4a53d0ec-3d4e-41ee-860e-1a398c1735c0",
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
  "content_id": "e4424729-6332-49d9-965b-3174773ab368",
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
  "content_id": "d2fa97db-d116-4de8-9348-0df8e994cff1",
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
  "content_id": "1f5f87d5-77ab-4d29-9624-f0a6b83ba407",
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
  "content_id": "5b9ec270-8044-4676-a000-40ac3ce1f6a3",
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
  "content_id": "73fdc669-f632-43ee-98cc-4fdaa4b0eb60",
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
  "content_id": "4dc2feb0-a04e-467f-bb76-190ff255aff8",
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
  "content_id": "0fa7b451-682b-4dd1-a515-0aea0ba18103",
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
  "content_id": "9d8defe5-dfe4-4cc9-ba91-770db51f032c",
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
