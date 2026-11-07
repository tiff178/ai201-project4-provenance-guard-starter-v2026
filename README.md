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

## Stretch Features
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

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
