import json
from io import BytesIO

import requests

from serialize_data import serialize_answers


def get_marks(link: str):
    r = requests.get(link)

    my_answers = serialize_answers(BytesIO(r.content))

    with open("answerkeys.json") as fa:
        for i in json.load(fa):
            if i["date"] == my_answers["date"] and i["shift"] == my_answers["shift"]:
                answer_key = i["key"]
                break

    return raw_marks(my_answers["key"], answer_key)


def raw_marks(candidate_answers, answer_key):
    marks = 0
    for i in candidate_answers:
        if "Drop" in answer_key[str(i["id"])]:
            marks += 4
            continue

        if i["type"] == "MCQ":
            if str(i["option_id"]) in answer_key[str(i["id"])]:
                marks += 4
            else:
                marks -= 1
        else:
            if int(answer_key[str(i["id"])][0]) == int(i["answer"]):
                marks += 4
            else:
                marks -= 1

    return marks
