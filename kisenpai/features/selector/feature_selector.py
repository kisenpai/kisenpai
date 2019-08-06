import random
import pandas as pd
from deap import base, creator, tools

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


class FeatureSelector:

    def __init__(self, data: pd.DataFrame, train_eval_function, goal=1.0, max_generations=1000,
                 init_population=100, crossover=tools.cxTwoPoint, crossover_prob=0.5, attr_mutation_prob=0.05,
                 individual_mutation_prob=0.2):
        self.__original_features = data.columns
        self.__data = data
        self.__goal = goal
        self.__max_generations = max_generations
        self.__population_size = init_population
        self.__crossover_prob = crossover_prob
        self.__individual_mutation_prob = individual_mutation_prob
        self.__train_eval_function = train_eval_function
        self.__toolbox = base.Toolbox()
        self.__toolbox.register("attr_bool", random.randint, 0, 1)
        self.__toolbox.register("individual", tools.initRepeat, creator.Individual, self.__toolbox.attr_bool,
                                len(self.__original_features))
        self.__toolbox.register("population", tools.initRepeat, list, self.__toolbox.individual)
        self.__toolbox.register("evaluate", self.__evaluate_individual)
        self.__toolbox.register("mate", crossover)
        self.__toolbox.register("mutate", tools.mutFlipBit, indpb=attr_mutation_prob)
        self.__toolbox.register("select", tools.selTournament, tournsize=3)

    def __evaluate_individual(self, individual) -> tuple:
        return self.__train_eval_function(individual),

    def get_selected_features(self) -> list:
        population = self.__toolbox.population(n=self.__population_size)
        fitnesses = list(map(self.__toolbox.evaluate, population))
        best_individual = []
        best_individual_fitness = 0

        for individual, fitness in zip(population, fitnesses):
            individual.fitness.values = fitness
            if fitness[0] >= best_individual_fitness:
                best_individual = individual
                best_individual_fitness = fitness[0]

        population_fitnesses = [ind.fitness.values[0] for ind in population]
        generations = 0

        # Evolution Phase
        while max(population_fitnesses) < self.__goal and generations < self.__max_generations:
            generations += 1
            print("-- Generation %i --" % generations)
            offspring = self.__toolbox.select(population, len(population))
            offspring = list(map(self.__toolbox.clone, offspring))

            # Apply crossover and mutation on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.__crossover_prob:
                    self.__toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            for mutant in offspring:
                if random.random() < self.__individual_mutation_prob:
                    self.__toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid_individuals = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(self.__toolbox.evaluate, invalid_individuals)

            for ind, fit in zip(invalid_individuals, fitnesses):
                ind.fitness.values = fit

            population[:] = offspring

            for ind in population:
                if ind.fitness.values[0] >= best_individual_fitness:
                    best_individual = ind
                    best_individual_fitness = ind.fitness.values[0]

            # Gather all the fitnesses in one list and print the stats
            fits = [ind.fitness.values[0] for ind in population]

            length = len(population)
            mean = sum(fits) / length
            sum2 = sum(x * x for x in fits)
            std = abs(sum2 / length - mean ** 2) ** 0.5

            print("   Min %s" % min(fits))
            print("   Max %s" % max(fits))
            print("   Avg %s" % mean)
            print("   Std %s" % std)
            print("   Best Individual [:>] ", best_individual)

        return best_individual


data0 = pd.read_csv("wine.csv", encoding="utf-8", delimiter=";")
label = data0["quality"]
data0.drop(columns=["quality"], inplace=True)

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import numpy as np


def fake(individual):
    selected_features = []
    for activation, feature in zip(individual, data0.columns):
        if activation == 1:
            selected_features.append(feature)
    new_data = data0[selected_features]
    X_train, X_valid, y_train, y_valid = train_test_split(new_data, label, test_size=0.20, random_state=42)
    classifier = GaussianNB().fit(X_train, y_train)
    labels_predicted = classifier.predict(X_valid)
    return np.mean(labels_predicted == y_valid)


fs = FeatureSelector(data0, fake)
fs.get_selected_features()
