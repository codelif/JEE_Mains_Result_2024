import json

from bs4 import BeautifulSoup as BS


def serialize_key(f):
    soup = BS(f.read(), "lxml")
    f.close()
    key_table = soup.find("table")

    answer_key = {}
    for i in key_table.find_all("tr")[1:]:
        row = i.find_all("td")
        question_id = int(row[0].text.strip())
        answer = int(row[1].text.strip())
        answer_type = "MCQ"

        if i.find(
            "input",
            attrs={"onkeypress": "return blockSpecialChar(event,'alphanumeric')"},
        ):
            answer_type = "SA"

        answer_key.update({question_id: [answer, answer_type]})

    with open("answer_key.json", "w+") as f:
        json.dump(answer_key, f, sort_keys=True, indent=1)

    return answer_key


def get_cell_text(tag):
    return tag.find_all("td")[-1].text.strip()


def serialize_answers(f):
    soup = BS(f.read(), "lxml")
    f.close()
    my_answers = []

    for i in soup.find("table").find_all("tr"):
        a = i.find_all("td")
        if a[0].text == "Test Date":
            test_date = a[1].text.strip().replace("/", "-")
        elif a[0].text == "Test Time":
            if a[1].text.strip().startswith("3:00"):
                shift = "Second"
            else:
                shift = "First"

    for question in soup.find_all("table", attrs={"class": "questionPnlTbl"}):
        question_menu = question.find("table", attrs={"class": "menu-tbl"})

        question_menu_rows = question_menu.find_all("tr")
        answer_type = get_cell_text(question_menu_rows[0])

        question_id = get_cell_text(question_menu_rows[1])

        answers = []
        a = None
        if answer_type == "MCQ":
            for i in question_menu_rows[2:6]:
                answers.append(int(get_cell_text(i)))
            my_answer = question_menu.find_all("td")[-1].text.strip()
            if my_answer == "--":
                my_answer = None
                continue
            my_answer = int(my_answer)
            a = answers[my_answer - 1]

            canonical = sorted(answers).index(a) + 1

            my_answer = canonical

        else:
            question_table = question.find("table", attrs={"class": "questionRowTbl"})
            my_answer = question_table.find_all("td")[-1].text

            if my_answer.strip() == "--":
                my_answer = None
                continue

        my_answers.append(
            {
                "id": int(question_id),
                "type": answer_type,
                "answer": int(my_answer),
                "option_id": a,
            }
        )

    my_answers = sorted(my_answers, key=lambda x: x["id"])

    return {"date": test_date, "shift": shift, "key": my_answers}


if __name__ == "__main__":
    f = open("raw_data/answer_key.html")
    serialize_key(f)
    f = open("raw_data/my_answers.html")
    serialize_answers(f)
