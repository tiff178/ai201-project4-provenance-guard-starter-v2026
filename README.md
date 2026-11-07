# Provenance Guard

# Unit 7

## What This Does

Provenance Guard is a web service that estimates whether a piece of writing was written by a person or by AI. It never gives a verdict. It gives a label, and a writer who disagrees can appeal. When a submission arrives at `POST /submit`, the service does these steps:

1. **Receive and validate.** The route reads `text` and `creator_id` from the JSON body. If `text` is missing or empty, it logs a rejection and returns a 400 instead of crashing. A missing `creator_id` becomes `"unknown"`.
2. **Assign a `content_id`.** Each accepted submission gets a unique ID, which `/appeal` and the audit log use later.
3. **Score with the model signal.** `detector.py:model_signal` uses a local language model to measure how predictable the text is. Predictable text scores closer to 1 (more likely AI). 
4. **Score with the style signal.** `stylometry.py:style_signal` measures sentence-length variation, vocabulary diversity and punctuation density. This is a different kind of evidence from the first signal.
5. **Combine the signals.** `scoring.py:combine_signals` averages the two scores with equal weight. If they disagree by more than 0.3, the result stays in the `unsure` band, so neither signal alone can accuse a writer.
6. **Map the score to a label.** `scoring.py:score_to_label` turns the combined score into one of three labels: high-confidence human (below 0.35), unsure (0.35 to 0.70), or high-confidence AI (0.70 and above). Each label has fixed wording for the reader.
7. **Log and respond.** `audit.py:log_decision` records the content ID, creator, guess, both signal scores, the combined score and the label. The response returns `content_id`, `guess`, `confidence`, `label`, `model_score` and `style_score`.

If a writer thinks the label is wrong, they send the `content_id` and their reasoning to `POST /appeal`. The service checks that the ID exists and that it hasn't already been appealed. It then logs the appeal and sets the status to `under_review`, so a person can look at it. `GET /log` shows every decision and appeal.

---

## Signals and Scoring

### Signal one — the model signal (`detector.py`)

**What it measures:** Text predictability and token sequence likelihood using a local language model.

**Why that might differ between human and AI writing:** AI models naturally select statistically common tokens, producing predictable patterns (words in sequence), whereas human writers often use unexpected phrasing or unique word choices. 

**What it can't see:** Plain, direct writing. Simple vocabulary and short, straightforward sentences (common in plain prose or non-native writing) score as highly predictable and get falsely flagged as AI, while dense or ornate AI prose can fool it into reading as human.

### Signal two — the style signal (`stylometry.py`)

**What it measures:** Surface-level structural features like sentence length variation, unique word ratio (vocabulary diversity), and punctuation density.

**Why that might differ between human and AI writing:** Human writing naturally varies in rhythm, sentence length, and structural shape, while AI writing tends to maintain uniform structural patterns.

**What it can't see:** Content meaning or intent. Minor surface edits like adding typos, breaking up long sentences, or pasting quotations alter the metrics without changing the text's substance, and it breaks down on short submissions where there isn't enough text for statistical measurement.

### The combining rule

**The rule:** Average the two signals with equal weight. If they disagree by more than 0.3, don't let the result leave the `unsure` band. Two methods splitting that far is uncertainty, and neither signal alone should be able to accuse a writer. 

**The numbers:** 
- WEIGHT_MODEL_SIGNAL = 0.5
- WEIGHT_STYLE_SIGNAL = 0.5
- DISAGREEMENT_LIMIT = 0.3 
- HUMAN_THRESHOLD = 0.35
- AI_THRESHOLD = 0.7
- `Unsure` = 0.35 to 0.7

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**

A famous quote from Marilyn Monroe: 

``` 
I'm selfish, impatient and a little insecure. I make mistakes, I am out of control and at times hard to handle. But if you can't handle me at my worst, then you sure as hell don't deserve me at my best.
```

The model signal (`detector.py:model_signal`) scores it as 0.8389, whereas the style signal (`stylometry.py:style_signal`) scores it as 0.4511. The model signal believes this text is most likely AI, whereas the style signal does not believe it is likely to be AI. The two combined signal scores average to 0.645, which is under the 0.7 line to be indicated as AI. The signals also disagree by 0.39, which is more than my 0.3 limit, so the rule holds the result inside the `unsure` band instead of letting one signal decide. As this is a famous quote, a LLM finds this text very easy to predict (more likely to be AI), whereas the style signal looks at rhythm, sentence length, and structural shape (not as likely to be AI). Both signals have little to work with given the short text. 

This rule protects real writers from false accusations whenever signals disagree with each other, keeping texts safely inside the `unsure` band.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 - 0.35 | We think this was probably written by a person. |
| unsure | 0.35 - 0.70 | We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work. |
| high-confidence AI | 0.70 - 1.00 | This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it. |

**Why I worded the "unsure" one this way:** The `unsure` label is the hardest of the three. It has to admit uncertainty without sounding like an accusation, because the writer could have written every word themselves. 

"Nothing is being assumed about you or your work." prevents false accusations to writers and attributes uncertainty in the system rather than to the writer. 

---

## Sample Run

**A submission**

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "No way! You did an amazing job presenting your speech.", "creator_id": "tiff"}'
```

```json
{
  "confidence": 0.3406,
  "content_id": "8d8feb34-7bf5-42ba-9740-664d66bd5f9c",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.2756,
  "style_score": 0.3838239541920477
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c01e5c56-f341-4e2b-9309-21b3c55d3f1c", "reasoning": "I wrote this myself for a class assignment."}'
```

```json
{
  "content_id": "c01e5c56-f341-4e2b-9309-21b3c55d3f1c",
  "message": "Your appeal has been recorded and the decision is now under review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.628892329365344,
      "content_id": "e8ab9851-7152-40fb-9386-f5652252ee67",
      "creator_id": "tiff",
      "guess": "unsure",
      "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
      "model_score": 0.8567,
      "status": "decided",
      "style_score": 0.401084658730688,
      "timestamp": "2026-11-01T04:41:07+00:00"
    },
    {
      "combined_score": 0.8404485657136469,
      "content_id": "c01e5c56-f341-4e2b-9309-21b3c55d3f1c",
      "creator_id": "tiff",
      "guess": "ai",
      "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
      "model_score": 0.9426,
      "status": "decided",
      "style_score": 0.7382971314272938,
      "timestamp": "2026-11-01T04:47:44+00:00"
    },
    {
      "content_id": "c01e5c56-f341-4e2b-9309-21b3c55d3f1c",
      "creator_id": "tiff",
      "event": "appeal",
      "reasoning": "I wrote this myself for a class assignment.",
      "status": "under_review",
      "timestamp": "2026-11-01T04:49:02+00:00"
    }
  ]
}
```

---

## Stretch Features - Unit 7
`GET /content/<id>`: endpoint that returns one item's current status (`app.py:get_content`)

**An item's current status**
```bash
$ curl "http://127.0.0.1:5000/content/c01e5c56-f341-4e2b-9309-21b3c55d3f1c"
```

```json
{
  "appeal": {
    "appealed_at": "2026-11-01T04:49:02+00:00",
    "reasoning": "I wrote this myself for a class assignment."
  },
  "combined_score": 0.8404485657136469,
  "content_id": "c01e5c56-f341-4e2b-9309-21b3c55d3f1c",
  "creator_id": "tiff",
  "decided_at": "2026-11-01T04:47:44+00:00",
  "guess": "ai",
  "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
  "model_score": 0.9426,
  "status": "under_review",
  "style_score": 0.7382971314272938
}
```

## How I Used AI

**Moment 1**

- *What I asked for:* Brainstorming session for the criterion into Claude - "My system allows this rate of wrongly flagging human writing as AI-generated. Write the message a real writer would send me if they were one of the people that rate allows. Don't tell me whether my number is right." 
- *What came back:* An appeal from a wrongly flagged writer as an email format asking for a human review of submission or way to submit evidence, correction to the label on record, and explanation of what tool looks at. The writer suggests to think aout how a "high-confidence" label affects people like her, who has no way to prove a negative once it's stamped onto their work. 
- *What I changed:* My criterion for false positives only allows at most 1 with a `high-confidence AI` label already, so this already ensures that real writers are rarely misflagged. No changes were needed, it confirmed that my criterion does minimize false positives. 

**Moment 2**

- *What I asked for:* A clearly-AI text from Claude that will then be used for appeal.
- *What came back:* A clearly-AI text to be used on submission and appeal. 
- *What I changed:* Had to test a few different prompts with Claude to get a stronger clearly-AI text as the ones I was trying to generate fell under `unsure` more often. 

**Moment 3**

- *What I asked for:* More clearly-AI text from Claude/ChatGPT for `scenarios.py`.
- *What came back:* More clearly-AI text.
- *What I changed:* Tested different prompts with Claude and ChatGPT for clearly-AI text for `scenarios.py`. The clearly-AI text is used in score spread and label coverage. 

---

# Unit 8

## Rate Limiting

**My limits:** 8 per minute, 150 per day

**Why those numbers and not others:** A limit of 8 requests per minute provides real writers ample headroom to edit and resubmit their work in quick succession. The limit of 150 requests per day protects backend resources against low/slow scraping over a 24-hour window without restricting real writers who iterate on their work throughout the day. 

**What a caller counts as:** per-address (`get_remote_address`)

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15`

```
15 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/15] 200
  [ 2/15] 200
  [ 3/15] 200
  [ 4/15] 200
  [ 5/15] 200
  [ 6/15] 200
  [ 7/15] 200
  [ 8/15] 200
  [ 9/15] 429
  [10/15] 429
  [11/15] 429
  [12/15] 429
  [13/15] 429
  [14/15] 429
  [15/15] 429

============================================================
200 200 200 200 200 200 200 200 429 429 429 429 429 429 429
============================================================
```

---

## Attack Run — Before

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

**Ten audit log entries from the run** (`EV05`, `EV09`, `FP03`, `FP04`, `FP05`, `PI02`, `MF06`, `M07`, `RQ06`, `FL01_09`)

```json
{"timestamp": "2026-11-06T04:47:48+00:00", "content_id": "3a10277c-0426-49df-a398-dd4943e6076f", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.37653872845679465, "combined_score": 0.3488693642283973, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:49+00:00", "content_id": "1c5cc5c7-730d-4e46-ba5b-70a8c5c0e563", "creator_id": "attacker_EV09", "guess": "unsure", "model_score": 0.7042, "style_score": 0.46073113610805233, "combined_score": 0.5824655680540262, "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:50+00:00", "content_id": "a3b14e53-c6df-430d-aa7c-f20ee8998f5f", "creator_id": "attacker_FP03", "guess": "ai", "model_score": 0.8051, "style_score": 0.6496398516315162, "combined_score": 0.7273699258157581, "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:50+00:00", "content_id": "3c276dde-8f8a-4a4a-800b-b00d9b1b3430", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.5836558866707483, "combined_score": 0.7082779433353741, "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:50+00:00", "content_id": "9fc1d82f-3da3-4675-8e2c-7d9f815b456a", "creator_id": "attacker_FP05", "guess": "ai", "model_score": 0.8005, "style_score": 0.6648470364437674, "combined_score": 0.7326735182218838, "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:51+00:00", "content_id": "692ded33-91a0-4e2f-b279-0341c1811c03", "creator_id": "attacker_PI02", "guess": "human", "model_score": 0.2044, "style_score": 0.3901290685348684, "combined_score": 0.2972645342674342, "label": "We think this was probably written by a person.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:53+00:00", "content_id": "1bd130cd-e267-4ff0-9d9a-ca531935bba8", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 1.0, "combined_score": 0.9984500000000001, "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:53+00:00", "content_id": "4df24544-a879-4544-974a-c3af3ca01c27", "creator_id": "attacker_MF07", "guess": "ai", "model_score": 0.9064, "style_score": 1.0, "combined_score": 0.9532, "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:54+00:00", "content_id": "f187d507-ee14-424f-b91f-e323095f7199", "creator_id": "unknown", "guess": "unsure", "model_score": 0.0492, "style_score": 0.6666666666666666, "combined_score": 0.36, "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.", "status": "decided"}
{"timestamp": "2026-11-06T04:47:55+00:00", "creator_id": "attacker_flood", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "8 per 1 minute"}
```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it: 
- The single worst outcome in this attack is FP03 (false_positive), where a non-native English speaker writing carefully was falsely classified as AI with a model score of `0.8051` and assigned a label of *"This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it."* Explaining this outcome to a writer would be devastating because falsely accusing a real writer, especially a non-native English speaker who took extra care to write carefully, inflicts immediate personal and professional harm. Automated false accusations penalize real writers' effort, erode trust in the platform, and unfairly force the writers to need to appeal. 

---

## Run Log and Verdicts

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | 
|---|---|---|---|---|---|
| 1. Real writers are almost never falsely flagged as AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET | 
| 2. Clearly-AI and clearly-human text score clearly apart | gap ≥ 0.3 | 0.099 | 0.099 | 0.099 | MISSED |
| 3. Every label (`high-confidence AI`, `high-confidence human`, `unsure`) is reachable | each label ≥ 2 of 15 | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | MET |
| 4. Appeals always change status and are recorded | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Missing, empty, or enormous texts are handled explicitly | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

**Real output from one trial**

Criterion 1, Trial 1: false positives (`run_eval.py::main`)

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.2756,
    "style_score": 0.3838239541920477,
    "label": "We think this was probably written by a person.",
    "sent": "No way! You did an amazing job presenting your speech."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2163,
    "model_score": 0.7242,
    "style_score": 0.4920634920634921,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "What is your favorite artist/group to listen to on a daily basis? Mine"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4258,
    "model_score": 0.2122,
    "style_score": 0.3620460048460248,
    "label": "We think this was probably written by a person.",
    "sent": "guess what? I passed my Microsoft Azure AI Fundamentals exam recently!"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.116,
    "model_score": 0.685,
    "style_score": 0.43096440627115085,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "I'm not ready for this midterm coming up... I still have a lot to stud"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4204,
    "model_score": 0.2257,
    "style_score": 0.3539132127639541,
    "label": "We think this was probably written by a person.",
    "sent": "What classes are you planning to take next semester? I'm thinking to t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3143,
    "model_score": 0.7214,
    "style_score": 0.5928744485996313,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Have you tried this new cafe/matcha spot? I seen it all over my Instag"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2796,
    "model_score": 0.855,
    "style_score": 0.4246214726356949,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Congrats! Can't wait to see what's in store for you in the future! I k"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.1847,
    "model_score": 0.8543,
    "style_score": 0.3303721745056052,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "AI and Machine Learning is such a huge topic in the industry right now"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0784,
    "model_score": 0.6528,
    "style_score": 0.4256027539194693,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "made some cantonese style egg tarts today, turned out really good! it'"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2118,
    "model_score": 0.7157,
    "style_score": 0.49613833857367334,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "I need some advice on what certification to study next that will be be"
  }
]
```

Criterion 2, Trial 1: score spread (`run_eval.py::main`)

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6809,
    "model_score": 0.9426,
    "style_score": 0.7382971314272938,
    "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Artificial intelligence is a powerful technology that is changing the "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2662,
    "model_score": 0.8093,
    "style_score": 0.4568809791713669,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Many people see failure as something to avoid, but it is often one of "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2478,
    "model_score": 0.7766,
    "style_score": 0.4712197736877021,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Choosing to be patient when things don't go our way, learning from mis"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.479,
    "model_score": 0.8492,
    "style_score": 0.6297771471740042,
    "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "This product is a great choice for anyone who wants a reliable and aff"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.38,
    "model_score": 0.8709,
    "style_score": 0.5243186680009541,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "As we grow older, we begin to realize that friendship isn't about how "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.2756,
    "style_score": 0.3838239541920477,
    "label": "We think this was probably written by a person.",
    "sent": "No way! You did an amazing job presenting your speech."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2163,
    "model_score": 0.7242,
    "style_score": 0.4920634920634921,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "What is your favorite artist/group to listen to on a daily basis? Mine"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4678,
    "model_score": 0.1702,
    "style_score": 0.3620460048460248,
    "label": "We think this was probably written by a person.",
    "sent": "guess what? I passed my Microsoft Azure AI Fundamentals exam recently!"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.116,
    "model_score": 0.685,
    "style_score": 0.43096440627115085,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "I'm not ready for this midterm coming up... I still have a lot to stud"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4204,
    "model_score": 0.2257,
    "style_score": 0.3539132127639541,
    "label": "We think this was probably written by a person.",
    "sent": "What classes are you planning to take next semester? I'm thinking to t"
  }
]
```

Criterion 3, Trial 1: label coverage (`run_eval.py::main`)

```json
[
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.6809,
    "model_score": 0.9426,
    "style_score": 0.7382971314272938,
    "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "Artificial intelligence is a powerful technology that is changing the "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2662,
    "model_score": 0.8093,
    "style_score": 0.4568809791713669,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Many people see failure as something to avoid, but it is often one of "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2478,
    "model_score": 0.7766,
    "style_score": 0.4712197736877021,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "Choosing to be patient when things don't go our way, learning from mis"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.479,
    "model_score": 0.8492,
    "style_score": 0.6297771471740042,
    "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "This product is a great choice for anyone who wants a reliable and aff"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.38,
    "model_score": 0.8709,
    "style_score": 0.5243186680009541,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "As we grow older, we begin to realize that friendship isn't about how "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.3406,
    "model_score": 0.2756,
    "style_score": 0.3838239541920477,
    "label": "We think this was probably written by a person.",
    "sent": "No way! You did an amazing job presenting your speech."
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.2163,
    "model_score": 0.7242,
    "style_score": 0.4920634920634921,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "What is your favorite artist/group to listen to on a daily basis? Mine"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4678,
    "model_score": 0.1702,
    "style_score": 0.3620460048460248,
    "label": "We think this was probably written by a person.",
    "sent": "guess what? I passed my Microsoft Azure AI Fundamentals exam recently!"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.116,
    "model_score": 0.685,
    "style_score": 0.43096440627115085,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "I'm not ready for this midterm coming up... I still have a lot to stud"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.4204,
    "model_score": 0.2257,
    "style_score": 0.3539132127639541,
    "label": "We think this was probably written by a person.",
    "sent": "What classes are you planning to take next semester? I'm thinking to t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.38,
    "model_score": 0.8795,
    "style_score": 0.5111895353426398,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "So glad we got to work together! It's been a wonderful learning experi"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.3216,
    "model_score": 0.7929,
    "style_score": 0.5287356321839081,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "When presenting analytical findings, it's important to consider potent"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.0597,
    "model_score": 0.5337,
    "style_score": 0.4065886153043685,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "No way, you got to see them live?! They're my favorite artist! I wish "
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.4784,
    "model_score": 0.8246,
    "style_score": 0.6538461538461539,
    "label": "This may have been written by AI. This is an estimate, not proof. If you wrote it yourself, you can appeal and a person will review it.",
    "sent": "To better understand how natural language processing works, it's helpf"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.28,
    "model_score": 0.1398,
    "style_score": 0.5777777777777778,
    "label": "We can't tell whether this was written by a person or by AI. Nothing is being assumed about you or your work.",
    "sent": "I sit alone in complete solitude, wising to myself that I had a little"
  }
]
```

Criterion 4: the appeal path (`app.py::appeal`) 
- The criterion for the appeal path can't be tested by sending text alone as it needs a submission first and then an appeal against `content_id` that came back. This is manually tested, 10 submitted appeals - the output below is an example. 

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "fe33d05f-e627-4207-bf0b-a8c7df1ecae2", "reasoning": "I wrote this myself for my NLP class assignment."}'
```

```json
{
  "content_id": "fe33d05f-e627-4207-bf0b-a8c7df1ecae2",
  "message": "Your appeal has been recorded and the decision is now under review.",
  "status": "under_review"
}
```

Criterion 5, Trial 1: bad input (`run_eval.py::main`)

```json
[
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": \"\", \"creator_id\": \"eval_bad_empty\"}, \"creator_id\": \"eval_bad input_1\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": \"   \", \"creator_id\": \"eval_bad_whitespace\"}, \"creator_id\": \"eval_bad input_2\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": null, \"creator_id\": \"eval_bad_null\"}, \"creator_id\": \"eval_bad input_3\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"creator_id\": \"eval_bad_missing\"}, \"creator_id\": \"eval_bad input_4\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": 12345, \"creator_id\": \"eval_bad_number\"}, \"creator_id\": \"eval_bad input_5\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": \"a\", \"creator_id\": \"eval_bad_single_char\"}, \"creator_id\": \"eval_bad input_6\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": \"\\n\\t\\r\", \"creator_id\": \"eval_bad_newlines\"}, \"creator_id\": \"eval_bad input_7\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": [\"item1\", \"item2\"], \"creator_id\": \"eval_bad_list\"}, \"creator_id\": \"eval_bad input_8\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": {\"nested\": \"object\"}, \"creator_id\": \"eval_bad_object\"}, \"creator_id\": \"eval_bad input_9\"}"
  },
  {
    "status": 400,
    "guess": null,
    "confidence": null,
    "model_score": null,
    "style_score": null,
    "label": null,
    "sent": "{\"text\": {\"text\": \"word word word word word word word word word word word word word word word word word word word word w"
  }
]
```

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Real writers are almost never falsely flagged as AI | ≤ 1 of 10 | MET | Across all 3 trials, 0 of 10 were assigned a label of `ai`. An `unsure` label does not count as false positive. This target is met as none of the 10 texts I wrote myself were assigned `ai`. |
| 2 | Clearly-AI and clearly-human text score clearly apart | gap ≥ 0.3 | MISSED | Calculated the average confidence score of the 5 clearly-AI texts (0.4108) and 5 clearly-human texts (0.3122), the resulting gap was 0.099; below the target threshold of 0.3 across all 3 trials. |
| 3 | Every label (`high-confidence AI`, `high-confidence human`, `unsure`) is reachable | each label ≥ 2 of 15 | MET | Counted the frequency of each label returned across the 15 text submissions, each trial returned 3 `ai`, 3 `human`, and 9 `unsure` labels, meeting the target of at least 2 occurrences per label. |
| 4 | Appeals always change status and are recorded | 10 of 10 | MET | All 10 of 10 (manually-tested by hand) successfully update the status to `under_review` in `logs/audit.jsonl` with a timestamp and the writer's reasoning based on `content_id`. |
| 5 | Missing, empty, or enormous texts are handled explicitly | 10 of 10 | MET | All 10 of 10 are handled explicitly as it returned HTTP 400 Bad Request status code without crashing the service across all 3 trials. |

**Diagnoses**

Criterion 2, Score Spread - Clearly-AI and clearly-human text score clearly apart (gap ≥ 0.3): 
- Criterion 2 failed to hit the target separation gap of 0.3, achieving a confidence gap of only 0.099 across all 3 trials (average AI confidence of 0.4108 and average human confidence of 0.3122). This failure is likely at two stages: *Signal Two - the style signal (`stylometry.py`) and the combining rule (`scoring.py::combine_signals`)*. Signal Two - the style signal analyzes surface-level structural features like sentence length variation, unique word ratio (vocabulary diversity), and punctuation density. Given the short-text submissions for score spread (`scenarios.py`), it lacks the length needed for variance and the style signal consistently outputs netural scores clustered around (0.35-0.55). When `scoring.py::combine_signals` averages both Signal One - the model signal and Signal Two - the style signal with equal weighting (`WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5`), the neutral `style_score` creates a bidirectional drag - pulling high AI model scores down and low human model scores up toward 0.5. Furthermore, when the signals split by more than 0.3, the disagreement limit rule forcibly holds the score inside the unsure band (0.35–0.70). Confidence measures distance from the 0.5 midpoint, this middle compression limits confidence for both categories and compresses the overall gap to just 0.099.

Broken Attacks - Evasion (`EV01-EV09`), False Positive (`FP03-FP05`), Malformed (`MF02` - HTTP 500 Internal Server Error, `MF06`, `MF07`, `RQ06`):
- Evasion Attacks (`EV01-EV09`) fails at *Signal Two - the style signal (`stylometry.py`) and the combining rule (`scoring.py::combine_signals`)*. AI-text modified with minor edits, such as adding typos, breaking up sentences, pasting quotes, etc. artificially inflates vocabulary diversity and structural variance. This causes Signal Two - the style signal to output low or neutral `style_score` values. When `scoring.py::combine_signals` averages both Signal One - the model signal and Signal Two - the style signal with equal weighting (`WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5`), this neutral `style_score` drags the overall combined score below 0.7 into `unsure` or `human`, allowing AI-text to evade detection. 
- False Positive Attacks (`FP03-FP05`) fails at *Signal One - the model signal (`detector.py`) and label mapping (`scoring.py::score_to_label`)*. Authentic human writing that is formal, structured, or written carefully by a non-native English speaker generates highly predictable token sequences. This causes Signal One - the model signal to assign an artificially high `model_score` (> 0.8), which pushes the combined score past 0.7 into a false `ai` classification, misflagging real writers. 
- Malformed Attacks (`MF02` - HTTP 500 Internal Server Error, `MF06`, `MF07`, `RQ06`) fails at *`app.py::submit`*. Input text length is not validated before passing to the next signal, causing a single character text (`MF02`) to trigger an exception and crash with a HTTP 500 Internal Server Error instead of returning a HTTP 400 Bad Request status code. Other things like emojis and RTL text distort language model token probabilities into false `ai` classifications, while passing a JSON object for `creator_id` bypasses strict type checking prior to entry. 

---

## The Improvement

**What I changed:** Validate the input; One of the malformed input crashed my route (`MF02` - HTTP 500 Internal Server Error) with text as a single character. Therefore, I want to check the input before the signals see it. In `app.py::submit`, I set a minimum word count of 3, so any text that is fewer than `MIN_WORDS` (like single character, punctuation, etc.) it would reject the request with a HTTP 400 Bad Request status code, rather than crash the route. 

A type check on `creator_id` is added as well. A `creator_id` that is present, but the wrong type should be rejected instead of quietly logged as "unknown."

**Which diagnosis pointed at it:** Broken Attacks - Malformed (`MF02` - HTTP 500 Internal Server Error); This is the main focus to fix the malformed input that crashed my route (it also fixes the other malformed issues listed as well). 

### Attack Run & Run Log — After

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


| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | 
|---|---|---|---|---|---|
| 1. Real writers are almost never falsely flagged as AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET | 
| 2. Clearly-AI and clearly-human text score clearly apart | gap ≥ 0.3 | 0.102 | 0.102 | 0.102 | MISSED |
| 3. Every label (`high-confidence AI`, `high-confidence human`, `unsure`) is reachable | each label ≥ 2 of 15 | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | MET |
| 4. Appeals always change status and are recorded | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Missing, empty, or enormous texts are handled explicitly | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

**Did it help, and how do I know:** Yes, it helped resolve the malformed attacks that were `BROKE` to now `HELD`. The malformed attack (`MF02` - text is a single character) changed from triggering a HTTP 500 Internal Server Error (Verdict: `BROKE`) to returning a HTTP 400 Bad Request (Verdict: `HELD`). This prevents the server from crashing on short texts. The other malformed attacks are also now (`HELD`) instead of trying to label it as `ai`, `human`, or `unsure` when the text only has emojis or a different language text. In addition, checking the type for `creator_id` now returns a HTTP 400 Bad Request instead of bypassing type checks. This improvement validates the input before the signals see it. 

---

## Stretch Features: Second Improvement - Unit 8 

**What I changed:** Move a threshold; Increased `AI_THRESHOLD` from 0.7 to 0.73 in `config.py`, widening the `unsure` band from 0.35-0.7 to 0.35-0.73

**Which diagnosis pointed at it:** Broken Attacks - False Positives (`FP03-FP05`) were classified as `ai` even though it was clearly written by real writers. Formal, structured, and carefully written texts by a non-native English speaker were misclassified as `ai`. Adjusting the `AI_THRESHOLD` slightly should reduce the misclassification. 

### Attack Run & Run Log — After (Second Improvement)

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

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict | 
|---|---|---|---|---|---|
| 1. Real writers are almost never falsely flagged as AI | ≤ 1 of 10 | 0/10 | 0/10 | 0/10 | MET | 
| 2. Clearly-AI and clearly-human text score clearly apart | gap ≥ 0.3 | 0.102 | 0.102 | 0.102 | MISSED |
| 3. Every label (`high-confidence AI`, `high-confidence human`, `unsure`) is reachable | each label ≥ 2 of 15 | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | 3 `ai`, 3 `human`, 9 `unsure` | MET |
| 4. Appeals always change status and are recorded | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |
| 5. Missing, empty, or enormous texts are handled explicitly | 10 of 10 | 10/10 | 10/10 | 10/10 | MET |

**Did it help, and how do I know:** Yes, it helped resolve two false positives (`FP03` - a non-native English speaker writing carefully and `FP04` - a student essay written to a rubric) to `unsure` instead of `ai`. It did not resolve one of the positives (`FP05` - technical documentation written by a person). Reducing the number of false positives is crucial because we don't want to falsely accuse real writers that their work is AI. Adjusting the threshold (widening the `unsure` gap) did help a bit. It resolved the single worst outcome, which is a non-native English speaker writing carefully. An `unsure` outcome (not a false positive) is an honest admission of the system uncertainty rather than a false accusation, so it does not penalize the author.

---

## What's Still Broken

Criterion 2, Score Spread — Clearly-AI and clearly-human text score clearly apart (MISSED, 0.102 against a 0.3 target): 
- Implementing dynamic length weighting in `scoring.py::combine_signals` or testing out the weights for the model and style signal to see any changes. 
- I prioritized eliminating server crashes first, refactoring `stylometry.py` would take more time, so I stopped here. 

Broken Attacks - Evasion (`EV01-EV09`), False Positive (`FP05`):
- For evasion attacks, I would introduce adversarial text normalization (stripping inserted typos, quotes, and artificial line breaks) prior to stylometric calculation, preventing minor edits from artificially inflating style_score. For false positives attacks, I would calibrate `detector.py` for formal, repetitive, or technical registers by introducing domain-aware perplexity scaling so structured/formal technical writing isn't misflagged. 
- Adjusting the thresholds further risks introducing false positives, so I stopped here. 


**The trade I'd make if this ran for real:** I would trade lower AI detection sensitivity in order to strictly prevent wrongful false accusations (false positives) against real human writers. Undetected AI text is a minor operational nuisance, but falsely flagging genuine human work inflicts immediate personal harm and destroys user trust, making real writers pay the price if the system leans too aggressively toward detection.

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
