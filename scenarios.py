"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "false positives",
        "criterion": 1,
        "texts": [
            "No way! You did an amazing job presenting your speech.",
            "What is your favorite artist/group to listen to on a daily basis? Mine is Ateez. Ateez recently released a new song, called 'Drip.' It is really catchy! I would recommend this song to those who enjoy listening to K-pop.",
            "guess what? I passed my Microsoft Azure AI Fundamentals exam recently! so happy, it's time to celebrate! 🎉",
            "I'm not ready for this midterm coming up... I still have a lot to study for, but I will try to not think too much about it and start studying this weekend.",
            "What classes are you planning to take next semester? I'm thinking to take MGT 6201 and 6203, but heard that 6201 - foundations of business is really challenging, especially the exams. hopefully it won't be too bad though...",
            "Have you tried this new cafe/matcha spot? I seen it all over my Instagram feed and it looked pretty good with good reviews too. I think I will try it out this weekend when I get a chance. I'll let you know how it tastes! ",
            "Congrats! Can't wait to see what's in store for you in the future! I know you will do great things! ",
            "AI and Machine Learning is such a huge topic in the industry right now, it's really important for me to keep up with the latest technologies. What do you suggest I learn?",
            "made some cantonese style egg tarts today, turned out really good! it's not too sweet, but I think it could be even better if I added more vanilla extract to the custard!",
            "I need some advice on what certification to study next that will be beneficial for my career. AI is becoming more and more important in the industry, how can I set myself apart from others? Any advice would be greatly appreciated!",
        ],
    },
    {
        "name": "score spread",
        "criterion": 2,
        "texts": [ 
            # clearly AI (generated from AI)
            "Artificial intelligence is a powerful technology that is changing the world. Artificial intelligence is used in many industries to improve efficiency and productivity. Artificial intelligence can help businesses to make better decisions and to save time and money. Artificial intelligence is important for the future of technology and society. Artificial intelligence will continue to transform the way people live and work in the future.",
            "Many people see failure as something to avoid, but it is often one of the most valuable parts of learning. When things don't go as planned, we gain opportunities to reflect, improve, and discover new approaches.",
            "Choosing to be patient when things don't go our way, learning from mistakes instead of dwelling on them, and stepping outside our comfort zones are all signs of progress. We often compare ourselves to others and forget that everyone moves at their own pace.",
            "This product is a great choice for anyone who wants a reliable and affordable option. It is easy to use and easy to set up for new users. It also has along battery life and a simple design that works well every day. This product is a good value for the price and meets the needs of most customers, so it is highly recommended for families and for professionals.",
            "As we grow older, we begin to realize that friendship isn't about how many people we know, but about the quality of the relationships we build. True friends are the ones who celebrate our achievements, support us during difficult times, and make us feel comfortable being ourselves.", 

            # clearly human (same 5 as false positives - my own writing)
            "No way! You did an amazing job presenting your speech.",
            "What is your favorite artist/group to listen to on a daily basis? Mine is Ateez. Ateez recently released a new song, called 'Drip.' It is really catchy! I would recommend this song to those who enjoy listening to K-pop.",
            "guess what? I passed my Microsoft Azure AI Fundamentals exam recently! so happy, it's time to celebrate!",
            "I'm not ready for this midterm coming up... I still have a lot to study for, but I will try to not think too much about it and start studying this weekend.",
            "What classes are you planning to take next semester? I'm thinking to take MGT 6201 and 6203, but heard that 6201 - foundations of business is really challenging, especially the exams. hopefully it won't be too bad though...",
        ],
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": [
            # ai (generated from AI)
            "Artificial intelligence is a powerful technology that is changing the world. Artificial intelligence is used in many industries to improve efficiency and productivity. Artificial intelligence can help businesses to make better decisions and to save time and money. Artificial intelligence is important for the future of technology and society. Artificial intelligence will continue to transform the way people live and work in the future.",
            "Many people see failure as something to avoid, but it is often one of the most valuable parts of learning. When things don't go as planned, we gain opportunities to reflect, improve, and discover new approaches.",
            "Choosing to be patient when things don't go our way, learning from mistakes instead of dwelling on them, and stepping outside our comfort zones are all signs of progress. We often compare ourselves to others and forget that everyone moves at their own pace.",
            "This product is a great choice for anyone who wants a reliable and affordable option. It is easy to use and easy to set up for new users. It also has along battery life and a simple design that works well every day. This product is a good value for the price and meets the needs of most customers, so it is highly recommended for families and for professionals.",
            "As we grow older, we begin to realize that friendship isn't about how many people we know, but about the quality of the relationships we build. True friends are the ones who celebrate our achievements, support us during difficult times, and make us feel comfortable being ourselves.", 

            # human (my own writing)
            "No way! You did an amazing job presenting your speech.",
            "What is your favorite artist/group to listen to on a daily basis? Mine is Ateez. Ateez recently released a new song, called 'Drip.' It is really catchy! I would recommend this song to those who enjoy listening to K-pop.",
            "guess what? I passed my Microsoft Azure AI Fundamentals exam recently! so happy, it's time to celebrate!",
            "I'm not ready for this midterm coming up... I still have a lot to study for, but I will try to not think too much about it and start studying this weekend.",
            "What classes are you planning to take next semester? I'm thinking to take MGT 6201 and 6203, but heard that 6201 - foundations of business is really challenging, especially the exams. hopefully it won't be too bad though...",

            # unsure (borderline) 
            "So glad we got to work together! It's been a wonderful learning experience and I'm grateful to have been part of the team!",
            "When presenting analytical findings, it's important to consider potential biases in the data, such as demographic biases, and how they could affect the results and conclusions drawn from them.",
            "No way, you got to see them live?! They're my favorite artist! I wish I could've gone, but I was on vacation...",
            "To better understand how natural language processing works, it's helpful to explore the underlying algorithms and models that enable machines to interpret and generate human language.",
            "I sit alone in complete solitude, wising to myself that I had a little gratitude.",
        ],
    },
    # A criterion about the appeal path can't be tested by sending text alone;
    # it needs a submission first and then an appeal against the content_id
    # that came back. You'll need to test that one by hand, or extend this file
    # and run_eval.py to do it. Saying which you did is part of the write-up.
    # {
    #     "name": "the appeal path - test by hand",
    #     "criterion": 4,
    #     "texts": [
    #     ],
    # },
    {
        "name": "bad input",
        "criterion": 5,
        "texts": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"text": "   ", "creator_id": "eval_bad_whitespace"},
            {"text": None, "creator_id": "eval_bad_null"},
            {"creator_id": "eval_bad_missing"},  # no text field at all
            {"text": 12345, "creator_id": "eval_bad_number"},
            {"text": "a", "creator_id": "eval_bad_single_char"},
            {"text": "\n\t\r", "creator_id": "eval_bad_newlines"},
            {"text": ["item1", "item2"], "creator_id": "eval_bad_list"},
            {"text": {"nested": "object"}, "creator_id": "eval_bad_object"},
            {"text": "word " * 50000, "creator_id": "eval_bad_huge"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
