import random
from functools import reduce
from operator import mul
from unicodedata import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

global_settings = {"cpu_setting" : 0, "save_file" : True}
def dropRates():
    print("This calculator will tell you how many runs on average it will take to find the items you are looking for.")
    print("Note: choosing the high performance setting may cause performance issues if your drop rates are particularly low.")
    print("!!! \nRead README.md for examples and further advice.\n!!!\n\n")
    

    global_settings["cpu_setting"] = [1000, 10000, 50000][int(input("CPU-Usage: '1' - (low - only for very low probability tests), '2' - (medium), '3' - (high - freaky are ya?): "))-1]
    #item_num = int(input("How many items are you trying to find (must be from the same source)? "))
    item_num = 0
    items = {"name" : [], "p" : [], "total_prob" : 0, "cumulative_prob" : 0}
    while True:
        item_num += 1
        items["name"].append(input(f"What is the name of item {item_num}? "))
        try:
            items["p"].append(float(input(f"What is the drop rate (0 < p <= 1) of {items['name'][item_num-1]}? ")))
        except ValueError as e:
            print("That is not a valid integer between 0 and 1")
            items["p"].append(float(input(f"What is the drop rate (0 < p <= 1) of {items['name'][item_num-1]}? ")))
        if input("Any more items? Enter any key if yes, otherwise enter 'n': ").lower() == "n":
            break
    
    items["total_prob"] = sum(items["p"])
    items["cumulative_prob"] = reduce(mul, items["p"])
    items["iterations_required"] = round((1/items["cumulative_prob"]) * 10)



    return (items)


def numerical_dist(items):
    all_loops = []
    repetition_list = []
    for i in range(global_settings["cpu_setting"]):
        item_drops = [{"item_name" : name, "drops" : 0, "p" : prob, "index" : i, "found" : False} for i, (name, prob) in enumerate(zip(items["name"], items["p"]))] + [{"item_name" : "other", "drops" : 0, "p" : 1-items["total_prob"], "index" : len(items["name"])}]
        distribution_space = [(sum(items["p"][0: i]), prob+sum(items["p"][0: i])) for i, prob in enumerate(items["p"])] + [(sum(items["p"]), 1)]
        all_items_found = [False, 0]
        repetitions = 0
        while all_items_found[0] == False:
            random_prob = random.random()
            repetitions += 1
            for i in range(len(item_drops)):
                if random_prob >= distribution_space[i][0] and random_prob <= distribution_space[i][1]:
                    item_drops[i]["drops"] += 1
                    item_drops[i]["found"] = True
                    continue
            for item in item_drops[0:-1]:
                    all_items_found[0] = True
                    if item["found"] == False:
                        all_items_found[0] = False
                        break
                    all_items_found[1] = repetitions
        repetition_list.append(repetitions)
        all_loops.append(item_drops)

    average_repetitions = sum(repetition_list)/global_settings["cpu_setting"]
    return (average_repetitions, repetition_list)
        
def describe_probability():
    values = numerical_dist(dropRates())
    df = pd.DataFrame(values[1])
    #df.to_csv("probabilityDistribution.csv")
    plt.hist(df, bins=np.linspace(0, max(values[1]), num=10000), cumulative=True, density=True, histtype='bar')
    plt.axvline(df.mean()[0], color='k', linestyle='dashed', linewidth=1)
    plt.figtext(0, 0.05, str(df.describe(percentiles=[0.01, 0.05, .25, .5, .75, 0.95, 0.99])), va="top", ha="left")
    plt.xlabel("Amount of attemps required")
    plt.ylabel("Probability of drop by this attempt")
    plt.savefig("distribution.svg", bbox_inches = "tight")
    plt.tight_layout()
    """
    Unless you have a supercomputer don't uncomment the plt.show, saving as an svg or png is faster, easier and better! 
    """
    #plt.show()
if __name__ == '__main__':
    describe_probability()
