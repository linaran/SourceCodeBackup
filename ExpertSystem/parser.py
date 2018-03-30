__author__ = 'spidey'


def get_input():
    """
    Function parses input data and returns a tuple\n
    containing two dicts. First dict contains variables,\n
    second dict contains rules for the expert system.\n
    :return: tuple which contains two dicts\n
    :rtype: tuple
    """
    inp = open('input.txt', 'r')

    variables = {}
    rules = {}
    reading = "variables"
    counter = 0

    for line in inp:
        if reading == "variables":
            if line != "\n":
                equal_split = line.strip().replace(' ', '').split('=')
                if len(equal_split) == 2:
                    variables[equal_split[0]] = tuple(equal_split[1].split('|'))
                    last_key = equal_split[0]
                else:
                    variables[last_key] = variables.get(last_key) + tuple(equal_split[0][1:].split('|'))
                # print last_key, variables.get(last_key)
            elif line == "\n":
                reading = "rules"
                continue
        elif reading == "rules":
            if line != "\n":
                if line[0] == "I":
                    attribute_list = line[2:].strip().replace(' ', '').split('&')
                    left_side = []
                    for attribute in attribute_list:
                        at_equal_split = attribute.split('=')
                        left_side_element = [at_equal_split[0]]
                        for value in at_equal_split[1].split('|'):
                            left_side_element.append(value)
                        left_side_element = tuple(left_side_element)
                        left_side.append(left_side_element)
                    left_side = tuple(left_side)
                elif line[0] == "T":
                    counter += 1
                    right_list = line[4:].strip().replace(' ', '')
                    right_attr_list = right_list.split('&')
                    right_side = []
                    for attribute in right_attr_list:
                        right_side.append(tuple(attribute.split('=')))
                    right_side.append(counter)
                    right_side = tuple(right_side)
                    # Bound to be silent killer
                    # noinspection PyUnboundLocalVariable
                    rules[right_side] = left_side
    inp.close()
    return variables, rules
