__author__ = 'spidey'

import parser
from operator import itemgetter


def get_rules(goal, rules):
    """
    Function returns all the rules that can be applied to the given goal.\n
    Rules are immediately sorted by importance. Notice: returned list
    should be treated as a stack so the most important element can be popped first.\n
    :param goal: string\n
    :param rules: dict\n
    :return: list\n
    :rtype: list\n
    """
    ret_value = []
    for key in rules.keys():
        for i in range(0, len(key) - 1):
            if key[i][0].lower() == goal.strip().lower():
                ret_value.append(key)
                break
    if not ret_value:
        return None
    return sorted(ret_value, key=itemgetter(1), reverse=True)


def is_provable(goal, rules):
    for key in rules.keys():
        for i in range(0, len(key) - 1):
            if key[i][0].lower() == goal.lower():
                return True
    return False


def compute_rules(conflict_rules, ram, rules):
    breaker = False
    if not conflict_rules:
        raise IndexError("List is empty!")
    for i in range(len(conflict_rules) - 1, -1, -1):
        rule = conflict_rules[i]
        left_side = rules.get(rule)
        for attribute in left_side:
            if attribute[0] not in ram:
                if is_provable(attribute[0], rules):
                    return attribute[0], "prove"
                else:
                    print
                    inp = raw_input("Give me more information about " + str(attribute[0]) + ": ")
                    print
                    return (attribute[0], inp), "input"
            elif ram.get(attribute[0]) not in attribute[1:]:
                print "I HAPPENED"
                conflict_rules.pop()
                breaker = True
                break
        if breaker:
            breaker = False
            continue
        else:
            print "Ignited rule", rules.get(rule), rule
            return rule[:-1], "proof"


def dict_output(dict, msg):
    print "///////////", msg
    for key in dict.keys():
        print key, dict.get(key)
    print "----------", msg


def rule_stack_ouput(right_list, rules):
    for element in right_list:
        print rules.get(element), "=>" ,element


def ender(ram):
    print
    dict_output(ram, "Finish")
    exit(0)


def main():
    map_tuple = parser.get_input()
    variables = map_tuple[0]
    rules = map_tuple[1]
    ram = {}
    goal_stack = []
    rules_stack = []
    new_goal = True

    dict_output(variables, "Knowledge base")
    inp = raw_input("What did you imagine: ")
    print
    goal_stack.append(inp)

    while True:
        if not goal_stack:
            ender(ram)

        # [[(('Zivotinja', 'patka'), ('RodZivotinje', 'pero'), 15), (('Zivotinja', 'albatros'), 14), ...], [...]]
        if new_goal:
            rules_stack.append(get_rules(goal_stack[-1], rules))
            new_goal = False
        dict_output(ram, "RAM")
        print "Conflict rules...", goal_stack[-1]
        rule_stack_ouput(rules_stack[-1], rules)

        decision = compute_rules(rules_stack[-1], ram, rules)
        if decision is None:
            ram[goal_stack[-1]] = "Nope"
            goal_stack.pop()
            rules_stack.pop()
            continue

        if decision[1] == "prove":
            goal_stack.append(decision[0])
            new_goal = True
        elif decision[1] == "input":
            # (('ToplaKrv', 'da'), True)
            ram[decision[0][0]] = decision[0][1]
        elif decision[1] == "proof":
            # (('RodZivotinje', 'sisavac'),)
            for element in decision[0]:
                ram[element[0]] = element[1]
            goal_stack.pop()
            rules_stack.pop()
            if not goal_stack:
                ender(ram)
        print

main()
