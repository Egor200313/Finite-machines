from src.Tree import create_machine_with_regex
import webbrowser
import os
rules = []


def setup():

    print("Enter regex in reverse polish form and color")
    while True:
        try:
            regex, color = input().split()
        except ValueError:
            break

        rules.append(list((regex + " " + color).split()))


def indicateWord(word: str, machines) -> int:
    for i, machine in enumerate(machines):
        if machine.has_word(word):
            return i
    return -1


def ParseText(filename: str):
    setup()
    text = []
    with open(filename) as input_file:
        for line in input_file.readlines():
            text.append(line.split())

    machines = [create_machine_with_regex(reg[0]) for reg in rules]

    with open("output.html", "w", encoding="utf-8") as output_file:
        for line in text:
            for word in line:
                word_group = indicateWord(word, machines)
                color = rules[word_group][1]
                if word_group == -1:
                    color = 'black'
                output_file.write('<font color="{}">{} </font>'.format(color, word))
            output_file.write('<br>\n')

    new = 2  # open in a new tab, if possible

    webbrowser.open('file://' + os.path.realpath("output.html"), new=new)

