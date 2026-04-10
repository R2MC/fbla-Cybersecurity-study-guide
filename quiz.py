#!/usr/bin/env python3
import random
from random import randrange

def random_insert(lst, item):
    lst.insert(randrange(len(lst) + 1), item)

def load_questions(filename):
    with open(filename, 'r') as f:
        content = f.read().strip()

    blocks = content.split('\n\n\n\n')
    pool = []
    seen = set()

    for block in blocks:
        parts = block.strip().split('\n\n')
        if len(parts) < 2:
            continue

        # Question block and answer block
        q_block, a_block = parts[0].strip(), parts[1].strip()

        # Parse correct answer letter (e.g. "C") and full text ("C. forwarding…")
        if not a_block.startswith('Answer: '):
            continue
        full = a_block[len('Answer: '):].strip()             # e.g. "C. forwarding messages…"
        correct = full.split('.', 1)[0].strip().upper()     # yields "C"

        # Split question text and its option lines
        lines = q_block.split('\n')
        question_text = lines[0]
        answer_lines = lines[1:]

        # Deduplicate questions (case-insensitive)
        key = question_text.lower()
        if key in seen:
            continue
        seen.add(key)

        pool.append({
            'question': question_text,
            'answers': answer_lines,
            'correct_answer': correct,   # letter only, e.g. "C"
            'correct_full': full,        # full answer, e.g. "C. forwarding…"
        })

    return pool

def main():
    full_pool = load_questions('questions.txt')
    print(f'Loaded pool of {len(full_pool)} questions.\n\n------------------------------\n')

    # ANSI styles
    bold       = '\033[01m'
    reset      = '\033[0m'
    red_bg     = '\033[41m'
    green      = '\033[32m'
    blue       = '\033[34m'
    lightgreen = '\033[92m'
    darkgray   = '\033[90m'

    pool = full_pool[:]
    random.shuffle(pool)

    index = 1
    while pool:
        q = pool.pop(0)
        print(f"{bold}{index}{reset}. {lightgreen}{q['question']}{reset}\n")

        for ans in q['answers']:
            # Safely split into label + text
            if '. ' in ans:
                label, text = ans.split('. ', 1)
                print(f"{bold}{label}{reset}. {text}")
            else:
                print(ans)

        try:
            reply = input('\n> ').strip().upper()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{green}{bold}Good luck!{reset}")
            break

        if reply == q['correct_answer']:
            print(f"\n{green}Correct.{reset}")
        else:
            # Show full correct option
            print(f"\n{red_bg}Incorrect. Correct answer was {bold}{q['correct_full']}{reset}")
            random_insert(pool, q)

        remaining = len(pool)
        print(f"\n{blue}------------------------------ {darkgray}[{remaining} questions remaining]{reset}\n")
        index += 1

if __name__ == '__main__':
    main()
