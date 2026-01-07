import time
import random

class LifeofApple:
    def __init__(self):
        #initial = seed stage
        self.stage = "Seed"
        self.age_years = 0
        self.has_fruit = False
        self.is_alive = True
    
    #make it grow~
    def grow(self):
        self.age_years += 1
        print(f"---Year {self.age_years} ---")

        #move onto sapling stage (over 1 year)
        if self.stage == "Seed" and self.age_years >= 1:
            self.stage = "Sapling"
            print("You've gotten an apple sapling, please take good care of it")
        elif self.stage == "Sapling" and self.age_years >= 3:
            self.stage = "Mature"
            print("You now have a mature apple tree")
        elif self.stage == "Mature" and self.age_years >= 5:
            self.produce_fruit()
        
        #Late stage
        if self.age_years > 40:
            if random.random() > 0.8:
                self.is_alive = False
                print("The apple tree has reached the end of its life, please grow a new one")
    
    def produce_fruit(self):
        #based on seasons
        print("Spring: There are blossoms covering the apple tree")
        time.sleep(0.5)
        self.has_fruit = True
        print("Late Summer: The apple tree has produced apples")

    def harvest(self):
        if self.has_fruit:
            print("Action: Harvested apples")
            self.has_fruit = False
        else:
            print("Action: No apples yet")
    
#run program
my_tree = LifeofApple()
while my_tree.is_alive and my_tree.age_years < 10:
    my_tree.grow()
    if my_tree.has_fruit:
        my_tree.harvest()
    time.sleep(1) #Simualate a year passing