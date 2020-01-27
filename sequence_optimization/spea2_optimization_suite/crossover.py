def crossover(parents, probability_crossover):
    """number_of_crossovers = len(parents) * probability_crossover
    if number_of_crossovers is 0 or len(parents) < 2 or parents[0] is not SequenceContainer:
        return
    for current_num_crossovers in range(number_of_crossovers):
        parent2 = parent1 = random.randint(1, len(parents))
        while parent1 is parent2:
            parent2 = random.randint(1, len(parents))
        crossover_point = random.randint(1, len(parents-1))
        parents.extend(getattr(parents[parent1], "sequence").tomutable()[:crossover_point].extend(getattr(parents[parent2], "sequence").tomutable()[crossover_point-1:]))
    """
    return parents