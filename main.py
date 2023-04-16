import random
import math
import matplotlib.pyplot as plt

SEED = "TESTING"

def sci_not(x, n_digits=10):
    
    if x <= 10**n_digits and x >= -10**n_digits:
        return str(x)
    
    sign = ""
    if x < 0:
        sign = "-"
        x *= -1
    
    e = math.ceil(math.log10(x)) - n_digits
    
    return f"{sign}{x//(10**(e))}E{e}"
    
    



class Farm:
    
    def __init__(self, n_worms:int=20, worm_len:int = 19, min:int = 0, max:int = 10, \
        mutation_rate = .01, punishment=-99, death_rate = -1, avg_lifespan = -1):
        self.n_generation = 0
        self.n_worms = n_worms 
        self.worm_len = worm_len
        self.min = min
        self.max = max
        self.mutation_rate = mutation_rate
        self.punishment = punishment
        self.death_rate = death_rate
        self.avg_lifespan = avg_lifespan
        self.worms = []
        self.n_div_0 = 0
        self.deaths = 0
        
        
        if n_worms % 2 or n_worms < 4:
            raise Exception("ERROR: Number of worms must be even and >= 4")
        
        if not worm_len % 2 or worm_len < 3:
            raise Exception("Worm length must be odd and >= 3")
        
        for i in range(n_worms):
            self.worms.append(Worm(self, worm_len))

    def __str__(self):
        self.worms.sort(key=lambda x: x.get_total(), reverse=True)
        out = ["\\"*40]
        out.append(f"Generation: {self.n_generation} Total: {sci_not(self.get_total())} \n\n")
        out.append(f"Deaths: {self.deaths} Divisions By 0: {self.n_div_0} \n\n")
        out.append('\n'.join([str(i) for i in self.worms]))
        out.append("\n\n")
        out.append("\\"*40)  
        return '\n'.join(out)
    
    __repr__ = __str__
            
    def run_generation(self):
    
        
        if self.death_rate != -1:
            last_gen = self.worms
            
            # Handle death
            self.worms = []
            for worm in last_gen:
                
                total = worm.get_total()
                if not total:
                    total += 1
                
                if self.avg_lifespan != -1:
                    old_age = (self.n_generation - worm.gen) / (self.avg_lifespan*2)
                else:
                    old_age = 0
                    
                if random.random() - old_age > self.death_rate:
                    self.worms.append(worm)
                else:
                    self.deaths += 1
            
        
        # Sort worms by total
        self.worms.sort(key=lambda x: x.get_total(), reverse=True)
        
        
            
        
        # Breed the worms together
        for i in range(1, len(self.worms), 2):
               
            self.worms.append(self.breed_worms(self.worms[i-1],self.worms[i]))

        # Sort again an cull population down to n_worms
        self.worms.sort(key=lambda x: x.get_total(), reverse=True)
        self.worms = self.worms[:self.n_worms]
        
        self.n_generation += 1
        
    def breed_worms(self, a, b):
        
        child = []
        muts = max(a.n_muts,b.n_muts)
        
        # Randomly select which jeans to pass down
        for i in range(len(a.jeans)):
            
            if random.random() < self.mutation_rate:
                muts += 1
                if not i % 2: #Odd
                        child.append(random.randint(self.min, self.max))
                else: # Even
                    child.append(random.randint(0,4))
                    
            elif random.getrandbits(1):
                child.append(a[i])
            else:
                child.append(b[i])
        
        
        
        
        return Worm(self, self.worm_len, child, self.n_generation, muts)
    
    def get_total(self):
        total = 0
        for worm in self.worms:
            total +=  worm.get_total()
        return total
        
        

class Worm:
    
    def __init__(self, farm:Farm, length:int, jeans:list = None, gen = 0, muts=0):
        self.farm = farm
        self.gen = gen
        self.n_muts = muts
        
        if jeans is None:
            self.jeans = []
            
            if len(self.jeans) == 0:
                for i in range(length):
                    if not i % 2: #Odd
                        self.jeans.append(random.randint(self.farm.min, self.farm.max))
                    else: # Even
                        self.jeans.append(random.randint(0,4))
        else:
            self.jeans = jeans
                    

    
    def __str__(self):
        return "(Gen: {} Muts: {}) {} | Total: {}" \
                .format(self.gen, self.n_muts, self.jeans, sci_not(self.get_total()))
    
    __repr__ = __str__
    
    def __getitem__(self, key):
        return self.jeans[key]
                
    def get_total(self):
        total = self.jeans[0]
        
        for i in range(1, len(self.jeans) - 1, 2):
            operation = self.jeans[i]
            jean = self.jeans[i+1]
            
            match operation:
                case 0:
                    total += jean
                case 1:
                    total -= jean
                case 2:
                    total *= jean
                case 3:
                    #Punish invalid mutation (div by 0)
                    if jean == 0: 
                        total = self.farm.punishment
                        self.farm.n_div_0 += 1
                        break
                    else:
                        total //= jean
                    
        return total
 
 
 
   
random.seed()
farm = Farm(min=-1000000,max=1000000, n_worms=10000, mutation_rate=.1)

print(farm)   

totals = [farm.get_total()]
for i in range(5000):
    farm.run_generation()
    
    total = farm.get_total()
    print("Generation: ",farm.n_generation, " Total:", sci_not(total))
       
    totals.append(total)
        

        
# print([sci_not(i) for i in totals])

plt.plot(totals)     
                
plt.show()
