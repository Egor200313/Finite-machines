from src.Tree import create_machine_with_regex

if __name__ == "__main__":
    regex, word = input().split()
    machine = create_machine_with_regex(regex)
    print(machine.max_prefix(word))
