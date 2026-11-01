# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

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

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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
