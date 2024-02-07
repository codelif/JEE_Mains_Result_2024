import json
from serialize_data import serialize_answers
import requests
import sys
from io import BytesIO

LINK = sys.argv[1]

def get_marks(link: str)
    r = requests.get(link)

    my_answers = serialize_answers(BytesIO(r.content))

    with open("answer_key.json") as fa:
        answer_key = json.load(fa)


    marks = 0
    for i in my_answers:
        if int(answer_key[str(i["id"])][0]) == int(i["answer"]):
            marks += 4
        else:
            marks -= 1

    return marks
