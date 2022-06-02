import random
from functools import reduce
from operator import mul
from unicodedata import name
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Global settings - will become more relevant later as the intention is to cater to all cpu-performances
# And provide some user discretion as to whether they want a saved file or not
global_settings = {"cpu_setting" : 0, "save_file" : True}
global_items = {}
def dropRates():
    print("This calculator will tell you how many runs on average it will take to find the items you are looking for.")
    print("Note: choosing the high performance setting may cause performance issues if your drop rates are particularly low.")
    print("!!! \nRead README.md for examples and further advice.\n!!!\n\n")
    
    global_settings["cpu_setting"] = [1000, 10000, 50000][int(input("CPU-Usage: '1' - (low - only for very low probability tests), '2' - (medium), '3' - (high - freaky are ya?): "))-1]
    
    #Setting up user input - perhaps a easier to understand input is necessary
    item_num = int(input("How many items are you trying to find (must be from the same source)? "))
    items = {"name" : [], "p" : [], "total_prob" : 0, "cumulative_prob" : 0}
    for i in range(item_num):
        items["name"].append(input(f"What is the name of item {i+1}? "))
        try:
            items["p"].append(float(input(f"What is the drop rate (0 < p <= 1) of {items['name'][i]}? ")))
        except ValueError as e:
            #If the user doesn't input a float value between 0 and 1, make them re-enter
            print("That is not a valid integer between 0 and 1")
            items["p"].append(float(input(f"What is the drop rate (0 < p <= 1) of {items['name'][i]}? ")))

    #Some data for optimising repetitions to cater to cpu performance
    items["total_prob"] = sum(items["p"])
    items["cumulative_prob"] = reduce(mul, items["p"])
    items["iterations_required"] = round((1/items["cumulative_prob"]) * 10)

    global global_items
    global_items = items


    return (items)


def numerical_dist(items):
    #All loops is a list variable which will contain all the drop-data from all repetitions as listed in 'item_drops' below
    all_loops = []
    #Repetition List is a list variable which will contain the amount of clears it took in each repetition to find all items
    repetition_list = []
    for i in range(global_settings["cpu_setting"]):
        #Sets up a dictionary for all items that the user is seeking, also creates an 'umbrella' item at the end to contain all the other items that the user may get
        item_drops = [{"item_name" : name, "drops" : 0, "p" : prob, "index" : i, "found" : False} for i, (name, prob) in enumerate(zip(items["name"], items["p"]))] + [{"item_name" : "other", "drops" : 0, "p" : 1-items["total_prob"], "index" : len(items["name"])}]
        #Creates a distribution axis to numerically describe the probability density function after repetitions
        distribution_space = [(sum(items["p"][0: i]), prob+sum(items["p"][0: i])) for i, prob in enumerate(items["p"])] + [(sum(items["p"]), 1)]
        #Tuple (Bool, repetitions) - if all items are found, current repetition ends
        all_items_found = [False, 0]
        #Number of clears this current iteration has taken
        repetitions = 0
        while all_items_found[0] == False:
            #Using random.random() to produce a random float value (high precision)
            random_prob = random.random()
            repetitions += 1
            
            #Checks where on the distribution axis, the current random float drops - uses a brute force solution
            for i in range(len(item_drops)):
                if random_prob >= distribution_space[i][0] and random_prob <= distribution_space[i][1]:
                    item_drops[i]["drops"] += 1
                    item_drops[i]["found"] = True
                    #Once the corresponding item is found on the distribution-axis, continue the current iteration
                    continue
            for item in item_drops[0:-1]:
                    #Checks if all items have been found yet - if so break
                    all_items_found[0] = True
                    if item["found"] == False:
                        all_items_found[0] = False
                        break
                    all_items_found[1] = repetitions
        #Once current iteration is over - append the amount of clears it took to find all items in this current iteration
        repetition_list.append(repetitions)
        #Append 'item_drops' to 'all_loops'
        all_loops.append(item_drops)
    
    #Test variable - meaningless
    average_repetitions = sum(repetition_list)/global_settings["cpu_setting"]
    
    return (average_repetitions, repetition_list)
        
def describe_probability():

    #ONLY FOR PLOTTING FOR NO OVERFILL - DOES NOT AFFECT SUMMARY STATISTICS
    def reject_outliers(data, m = 5.16):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return data[s<m]

    #Call both numerical_dist() and drop_rates()
    values = numerical_dist(dropRates())

    global global_items
    
    #Key values to show on the plot figure
    key_values = {"items" : global_items["name"], "p" : global_items["p"]}
    
    #All items being sought and their corresponding probabilities
    figure_df = pd.DataFrame(key_values)
    print(figure_df)
    
    #Turn repepetition_list into a pandas dataframe for easy data analysis
    df = pd.DataFrame(values[1])
    
    #User can send the repetition_list to a csv file if they wish to do their own analysis
    #df.to_csv("probabilityDistribution.csv")
    
    #538 style looks cool
    plt.style.use('fivethirtyeight')
    
    #Plot a cumulative probability density function
    plt.hist(df, bins=np.linspace(0, max(values[1]), num=10000), cumulative=True, density=True, histtype='bar')
    
    #Plot a line down the mean of the probability density function
    plt.axvline(df.mean()[0], color='k', linestyle='dashed', linewidth=1)
    
    #Two figures explaining the key data involved in the simulation
    plt.figtext(0.1, -0.05, str(df.describe(percentiles=[0.01, 0.05, .25, .5, .75, 0.95, 0.99]))[20::], va="top", ha="left")
    plt.figtext(0.9, -0.05, figure_df.to_string(index=False), va='top', ha='right')
    
    #Axis labels and setting an x_lim, otherwise on large simulations outliers will stretch the plot far to wide
    plt.xlabel("Amount of attemps required")
    plt.xlim((len(global_items["name"]), reject_outliers(df).dropna().max()[0]))
    plt.ylabel("Probability of drop by this attempt")
    
    #Saving the probability density function as an svg file, file_size is around 2MB
    plt.savefig("distribution.svg", bbox_inches = "tight")
    plt.tight_layout()
    """
    Unless you have a supercomputer don't uncomment the plt.show, saving as an svg or png is faster, easier and better! 
    """
    #plt.show()
if __name__ == '__main__':
    describe_probability()
    pass
