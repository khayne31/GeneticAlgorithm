import sys
from random import randint
from random import random
import time
global pop
global target

count = 0
w, h = 3,3

game = 0
corner = randint(0,3
)win = 0
level = 1
remaining = 9


#This is what you want to eventually print out. Change this to what you want to say
target = "hjko9uhnmlpo9iujm,lo"*90
alphabet = [(x + 65) for x in range(26)]
for i in range(26):
    alphabet.append(i+97)
alphabet.append(32)
alphabet.append(63)
alphabet.append(44)

global letters
#this basically loads up the letters array with all the ascii characters a-z, A-Z, ? and " "
letters = [(chr(x)) for x in alphabet]
#this creates the individual strings basically. Don't change anything in this.
class individual():
    def __init__(self, instantiation = False, item = "", newTarget):
        self.size = len(newTarget)
        self.newTarget = newTarget
        self.size = size_of_string
        self.string = item
        self.fitness = 0
        if instantiation:
            for i in range(self.size):
                self.string = self.string + letters[randint(0, len(letters) - 1)]

    def value(self):
        print(self.string)

    def calc_fitness(self):
        self.fitness = 0
        target_iter = 0
        for i in self.string:
            #converts target_iter and i into numbers
            self.fitness += abs(ord(self.newTarget[target_iter]) - ord(i))
            target_iter += 1
    def return_fitness(self):
        self.calc_fitness()
        return self.fitness

    def print_fitness(self):
        print(self.fitness)

#this creates the population. it requries the size of the population when initilized
class population():
    def __init__(self, sizeOfPop, pop_target):
        self.size = sizeOfPop
        self.pop_target = pop_target
        self.population = [individual(True, newTarget = self.pop_target) for x in range(self.size)]
        self.cutoff = 100
        

    #this is where eveything happenes. 1) it takes a switch variable which does not turn on unless the greatest fitness is less than self.cutoff more on that later,
    #2) it takes a mutation variable that determines the frequency of mutations
    #3 it takes a selection variable that selects that percentage of the best individuals in the population
    #4 this takes a random_select variable that gives each individual in the remaing "unfit" population that chance of joing the parents
    #KEEP THE MUTATION RATE AT 1% IT IS SO MUCH BETTER
    def evolve(self, switch = False, mutation = .01, selection = .2, random_select = .05):
        length = len(self.population)
        graded = [(x.return_fitness(), x.string) for x in self.population]
        #this basically sorts the array based on fitness from least to greatest
        graded = [x[1] for x in sorted(graded)]
        if switch:
            immune = 5
            graded = [graded[0] for i in range(length)]
            #so basically this little section is for when the highest fitness is below the self.cutoff threshold
            #when this happens the entire population is filed with the most fit individual, and the only way any evolution happens is through mutations
            #the most fit, as determined by immune, will be exempt from any mutation

            for i in range(len(graded) - immune):
                for j  in range(len(graded[i + immune])):
                    if random() < mutation:
                        graded[i + immune] = graded[i + immune][:j] + (letters[randint(0, len(letters) - 1)]) + graded[i + immune][j + 1:]
            self.population = [individual(item = graded[j]) for j in range(len(graded))]
        else:
            #this is the array of the fittest
            parents = [graded[i] for i in range(int(len(graded) * selection))]
            #this the the array of "unfit"
            graded = graded[len(parents):]
            #this goes through the population and runs each percentage, through random_select, to decide if they will be chosen for the parents array
            for item in graded:
                if random() < random_select:
                    parents.append(item)
            #this puts all but the top 5 parents through mutation
            for i in range(len(parents) - 5):
                for j  in range(len(parents[i + 5])):
                    if random() < mutation:
                        parents[i + 5] = parents[i + 5][:j] + (letters[randint(0, len(letters) - 1)]) + parents[i + 5][j + 1:]
            #this determines how many children need to be created
            children_needed = length - len(parents)
            children = []
            iter = 0
            restart = False
            #basically run this lop until enough children have been made
            while len(children) < children_needed and restart == False:
                #this if loop will basically exit thi generation if the while loop get stuck infinitly. DON'T CHANGE
                if iter == length * 2:
                    restart = True
                #this basically creates a male and a female from  random parents in the parent array
                male = parents[randint(0, len(parents) - 1)]
                female = parents[randint(0, len(parents) - 1)]
                #this checks to see the parents are not the same
                if(male != female):
                    #this whole section is the reproduction aspect of the algorithm. I have  create two diffrent types
                    #1) this is where the child is the resultant of the first 25& of either parent, the middle 50% of the other, and the last 25% of the first
                    #2) this is where the child is the resultant of crossover, or half or one parent plus half of the other
                    if random() < .5:
                        breakpoint1 = int(.25 * len(male)) -1
                        breakpoint2 = int(.75 * len(male)) -1
                        child = male[:breakpoint1] + female[breakpoint1:breakpoint2] +  male[breakpoint2:] if random() < .5 else female[:breakpoint1] + male[breakpoint1:breakpoint2] +  female[breakpoint2:]
                    else:
                        half = int(len(male) * .5)
                        if random() < .25:
                            child = male[:half] + female[half:]
                        elif random() < .5:
                            child = male[half:] + female[:half]
                        elif random() < .75:
                            child = female[:half] + male[half:]
                        else:
                            child = female[half:] + male[:half]
                    #this is where the mutation for the child occurs
                    for i  in range(len(child)):
                        if random() < mutation:
                            child = child[:i] + (letters[randint(0, len(letters) - 1)]) + child[i + 1:]
                    children.append(child)
                iter += 1

            if not restart:
                #adds the children to the parents
                parents.extend(children)
                #becasue what we are mutation and changing are strings, and self.population is a list of Individuals() we must convert  each member of the parents list into Individuals()
                for i in range(len(parents)):
                    parents[i] = individual(item = parents[i])
                #the population is updated after evolution
                self.population = parents


    #this function basically calls evloution until one stands victorious
    def evolution(self):
        #just ignore this, it basically is a quick way to initilize graded
        graded = [(1,"this is just for initilization purposes")]
        iter = 0
        #basically while the target has not been achived
        while graded[0][0] != 0:
            graded = [(x.return_fitness(), x.string) for x in self.population]
            graded = sorted(graded)
            sum = 0
            for item in graded:
                sum += item[0]
            average = sum/len(graded)

            if graded[0][0] == 0:
                #self.ask()
                print(graded[0][1])
            elif graded[0][0] <= self.cutoff:
                self.evolve(True)
                #print("\niteration: ", iter)
                print(graded[0][1],graded[0][0])
                sys.stdout.flush()
            else:
                self.evolve()
                #print("\niteration: ", iter)
                print(graded[0][1], graded[0][0], average)
                sys.stdout.flush()
                #time.sleep(.3)
            iter += 1

    def printPop(self):
        for x in self.population:
            x.value()

    def ask(self):
        while(True):
            print(self.pop_target)

class species():
    def __init(self, size_of_string, size_of_pop):
        self.size_of_string = size_of_string
        self.target_array = []
        self.size = size_of_species
        self.members = []
        self.sizeOfPop = size_of_pop

    def define_target(self):
        while(len(target) > 0):
            if(len(target) - size_of_string < 0):
                self.append(target)
            else:
                self.target_array.append(target[0:size_of_string])
                target = [size_of_string:]

    def species_evolution(self):
        self.members = [population(sizeOfPop, self.target[i]) for i in range(len(self.target_array))]


pop = population(500)
start = time.time()
pop.evolution()
end = time.time()
print(end-start)
