# Melvor Idle - Probability Distributions Calculator
Prob Dist Calculator

**Who is this calculator for?**

-- Anyone wondering how many clears of a certain dungeon it will take to get the specific items your after

-- Anyone wanting to see the probability distribution, check how many clears it would take for you to be among the 5% unluckiest people!

-- Anyone who invests hours in number crunching despite the game requiring very little input!

**What can I test**

An example of what you can test is below:

```python3
CPU-Usage: '1' - (low - only for very low probability tests), '2' - (medium), '3' - (high - freaky are ya?): 2

## Low (1,000 Repetitions), Medium (10,000 Repetitions), High (50,000 Repetitions)

## If you are testing a probability like (getting item A, B and C each with a 0.000001 p value):
## Then you will likely have a cpu crash before you get an answer. Make reasonable judgements based on your own computers specs.

## Probabilities are entered in decimal form where p is a number from 0 -> 1. If you have percentage values, just divide by 100.

What is the name of item 1? Ancient Helmet
What is the drop rate (0 < p <= 1) of Ancient Helmet? 0.00415
Any more items? Enter any key if yes, otherwise enter 'n': 

What is the name of item 2? Ancient Shield
What is the drop rate (0 < p <= 1) of Ancient Shield? 0.00415
Any more items? Enter any key if yes, otherwise enter 'n': 

What is the name of item 3? Ancient Leggings
What is the drop rate (0 < p <= 1) of Ancient Leggings? 0.0028
Any more items? Enter any key if yes, otherwise enter 'n': 

What is the name of item 4? Ancient Platebody
What is the drop rate (0 < p <= 1) of Ancient Platebody? 0.0028
Any more items? Enter any key if yes, otherwise enter 'n': n

#returns
"""
1. Saves an svg file into the same folder as this script - this shows all descriptive statistics as well as a histogram for the cumulative density function

2. Prints all descriptive statistics into the console - looks cooler on graph tho 

3. Average amount of runs required

"""
```
**What does the graph look like**


![distribution](https://user-images.githubusercontent.com/47137792/170841934-b9b272cf-3f36-4633-9594-b15bfce7f99b.svg)


I will make revisions and add more annotations to the graph in the future, but this gives a decent run down so far.

I've found this especially useful for figuring out how long its gonna take to grind out an entire god armour set.


If you have **any** questions, message me on discord: **Dat Boi#4596**
