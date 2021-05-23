# created by cobra0798 on 2/20/2020.
class Mutation:
    def __init__(self, ingredients, chance):
        self.ingredients = ingredients
        self.chance = chance


class Pigment:
    def __init__(self, name):
        self.name = name
        self.mutations = []


class Path:
    def __init__(self, target, left, right):
        self.target = target
        self.left = left
        self.right = right

    def __str__(self):
        if self.left is None and self.right is None:
            return ""
        else:
            return str(self.left) + str(
                self.right) + self.target + " = " + self.right.target + " + " + self.left.target + "\n"


def get_pigments():
    pigments = {}
    with open('pigments.txt', 'r') as pf:
        lines = [l.strip() for l in pf.readlines()]
        for line in lines:
            pigments[line] = Pigment(line)
    with open('mutations.txt', 'r') as mf:
        lines = mf.readlines()
        for line in lines:
            line.strip()
            splice = line.split(',')
            mut = Mutation((splice[0].strip(), splice[1].strip()), int(splice[3].strip()))
            pigments[splice[2].strip()].mutations.append(mut)
    return pigments


def get_target():
    target = None
    print("select the target pigment:")
    target = input().strip()
    return target


def get_collection():
    collection = []
    print("select the pigments you have, separated by commas:")
    input_string = input().strip()
    collection = [l.strip() for l in input_string.split(',')]
    return collection


def get_combinations(collection):
    combinations = []
    for first_ingredient in collection:
        for second_ingredient in collection:
            if not first_ingredient == second_ingredient:
                combinations.append((first_ingredient, second_ingredient))
    return combinations


def get_possible_results(pigments, combinations, target):
    results = []
    for combination in combinations:
        for pigment in pigments.values():
            for mut in pigment.mutations:
                if combination[0] == mut.ingredients[0] and combination[1] == mut.ingredients[1]:
                    if pigment.name == target:
                        return [pigment.name, combination[0], combination[1]]
                    else:
                        results.append(pigment.name)
    return list(set(results))


def find_path(collection, target, pigments):
    tiers = [collection]
    found = False
    unobtainable = False
    results = []
    path_to_target = None
    if target in collection:
        found = True
        path_to_target = Path(target, None, None)
    while not found and not unobtainable:
        tiers_flattened = list(set([j for sub in tiers for j in sub]))
        combinations = get_combinations(tiers_flattened)
        results = get_possible_results(pigments, combinations, target)
        tiers.append(results)
        found = target in results
        unobtainable = len(tiers_flattened) == len(list(set([j for sub in tiers for j in sub])))
    if path_to_target is None and not unobtainable:
        path_to_target = Path(target, find_path(collection, results[1], pigments),
                              find_path(collection, results[2], pigments))
    if unobtainable:
        print("target pigment is unobtainable with the provided pigments.")
    return path_to_target


def main():
    pigments = get_pigments()
    target = get_target()
    collection = get_collection()
    path = find_path(collection, target, pigments)

    if path is not None:
        print(path)
    print("press any key to continue.")
    finish = input()


if __name__ == "__main__":
    main()
