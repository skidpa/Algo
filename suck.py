#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import timeit
import copy


class PANoob:
    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size
        self.count = 0
        self.collision = 0
        self.collisionLongest = 0
        self.collisionTotal = 0
        self.probes = 0
        self.l_down = 0
        self.l_up = 0
        self.loadfactor = 0
        self.collicount = 0
        self.collisionchain = 0
        self.hasCollided = False
        self.collisionLongestSofar = 0
        self.collisionTest = 0

    def hashFunct(self, key):
        return hash(key) % self.size

    def insertSlot(self, key):
        slot = self.hashFunct(key)

        while self.slots[slot] is not None:

            self.hasCollided = True

            self.probes += 1

            slot = (slot + 1) % self.size
        return slot

    def insert(self, key):
        slot = self.insertSlot(key)

        if self.hasCollided:
            self.collisionTotal += 1
            self.collision +=1
            if self.collision > self.collisionLongestSofar:
                self.collisionLongestSofar = self.collision
        else:
            if self.collision > self.collisionLongestSofar:
                self.collisionLongestSofar = self.collision
                print "wtf am i doing here"
            self.collision = 0

        if self.slots[slot] != key:
            self.slots[slot] = key
            self.count += 1
            self.hasCollided = False



# --------- class 2 -------------


class StahlJohanUpDown:

    def __init__(self, size):
        self.size = size
        self.slots = [None] * self.size
        self.count = 0
        self.collision = 0
        self.collisionTotal = 0
        self.collisionLongest = 0
        self.l_down = 0
        self.l_up = 0
        self.probes = 0
        self.inserts = 0
        self.loadfactor = 0
        self.collicount = 0
        self.collisionchain = 0
        self.hasCollided = False
        self.collisionLongestSofar = 0
        self.collisionTest = 0
        self.hasCollidedup = False
        self.hasCollideddown = False

    def hashFunct(self, key):
        return hash(key) % self.size  # returnerar X mod M som positionsplats.

    def insertSlot(self, key):
        slot = self.hashFunct(key)  # har tilldelas svaret fran X mod M till variabel

        #if self.slots[slot] is not None:
            #self.collision += 1
         #   print "first if ", self.collision

        if self.l_down <= self.l_up:

            while self.slots[slot] is not None:
                self.l_down += 1
                self.hasCollidedup = True
                self.hasCollided = True
                slot = (slot + 1) % self.size

            # self.collision += 1
            # self.collisionTotal += 1
        if self.l_down >self.l_up:

            while self.slots[slot] is not None:
                self.l_up += 1
                self.hasCollideddown = True
                self.hasCollided = True
                slot = (slot - 1) % self.size

            # self.collision += 1
            # self.collisionTotal += 1

        return slot

    def insert(self, key):

        if self.l_down < self.l_up:
            slot = self.insertSlot(key)
            #self.l_down += 1
        else:
            slot = self.insertSlot(key)
            #self.l_up += 1

        if self.slots[slot] != key:
            self.slots[slot] = key
            self.inserts += 1
            self.hasCollided = False
            #self.collisionreset()

# --------- class 3 -------------

class superkasra:
    def __init__(self, size, c):
        self.c = c
        self.size = size
        self.slots = [None] * self.size
        self.count = 0
        self.collision = 0
        self.collisionLongest = 0
        self.collisionTotal = 0
        self.probes = 0
        self.rehashed = 0
        self.l_down = 0
        self.l_up = 0
        self.inserts = 0
        self.loadfactor = 1.0
        self.fail = 0
        self.hasCollided = False
        self.collisionTest = 0
        self.collisionLongestSofar = 0 # collision chain

    def hashfunct(self, key):
        return hash(key) % self.size

    def findinsert(self, key):
        checks = 0

        j = self.hashfunct(key) # This is the index its want to try first
        hx = j

        while(True):

            self.probes += 1  #Make this larger because we are probing

            if self.slots[j] is None : #whithout altering J, if the first place is empty, insert it

                if self.collisionTest > 0:
                    self.hasCollided = True
                    self.collisionTest = 0

                    return j
                else:
                    self.hasCollided = False
                    self.collisionLongest = 0


                    #   print "we return in first" , j
                    return j

            self.collision += 1 # Since the code made it here, there has been a collission  maybe total
            self.collisionTest += 1

            j = (j+1) % self.size # We check the the next spot

            checks += 1
            #print "this is checks", checks

            if checks > self.c: # since there is no empty spot on j or j + 3 we check the next conditional
                #print "checks were overridden lets look for y"
                while True:

                    if self.slots[j] == None: #if we are here, the c next steps are pccupaid, therefore j = h(x) + c
                                              #Therefore we can use this loop to check the next empty slot
                        break
                    j = (j + 1) % self.size

                boo = True
                i = self.hashfunct(key)   # let i start on h(x)

                checklimit = self.c + 1    # this should be the ammount of times we can check the second definition
                nextChecker = 0          # we count this to see if we reach it, if we do we rehash
              #  print " i should be 13", i
                while(boo == True):

                   # print "we look for y solution"

                    self.collision += 1

                    if abs(j - self.hashfunct(self.slots[i])) <= self.c:     # checks if "next free slot" - h(y) <= c

                         self.slots[j] = self.slots[i]

                         #print self.slots

                         #print "this is i" , i
                         #print " we return", self.slots[i] % self.size
                         #return self.hashfunct(self.slots[i])
                         return i

                    i = (i + 1) % self.size
                 #   print "this is i after if", i

                    nextChecker += 1

                    if nextChecker > checklimit:

                        if self.rehashed < 50:
                            #print self.slots
                            #print "we rehash"
                            self.rehash()
                           # print "we come out of rehash but we have to return"
                            self.rehashed +=1
                           # print self.slots
                            self.insert(key)

                        else:
                            print "We exit here, no possible solution?"
                            self.loadfactor = 0.0
                            load = 0.0
                            for e in self.slots:
                                if e is not None:
                                    load += 1
                                    #print load
                            self.loadfactor = load/self.size

                            print "lf: ",self.loadfactor
                            self.exitsave()
                            #exit(1)
                            self.fail = 1
                            return -1
                        #return -1

                        #return -1
                       # print "we need to hash"

    def insert(self, key):
        #print "this is key", key
        slot = self.findinsert(key)
        if slot == -1:
            print " maybe this is the hash forever"
            return -1

        if self.hasCollided == True:
            self.collisionLongest += 1
            if self.collisionLongest >= self.collisionLongestSofar:
                self.collisionLongestSofar = self.collisionLongest
        if self.slots[slot] != key:

                self.slots[slot] = key
                #print "this is slot," ,slot
                #print self.slots
                self.count += 1
                self.inserts +=1
       # self.collisionreset()

    def rehash(self):

        self.rehashed += 1
        newtable = copy.deepcopy(self.slots)


        self.slots = [None] * self.size
        #print self.slots
        for i in range(0, self.size):

            holdkey = newtable[i]
            if(holdkey is not None):

              #  print "we hash holdkey", holdkey
                self.insert(holdkey)

    def exitsave(self):
     print "\nopen file: "
     f = open("exit_on.txt", "w")
     print "file open ", "Saving shit"
     f.write("\n--------- Exit on Test nr: " + str(self.c) + " ---------" + "\nFinal L_down: " + str(self.l_down) + "\nFinal L_up: " + str(self.l_up) +
                "\ncollisions: " + str(self.collision) + "\ncollision chain: " +str(self.collisionLongestSofar) +
                "\ntotal collision: " + str(self.collisionTotal) + "\nprobes: " + str(self.probes) + "\n Inserts: " + str(self.inserts) + "\nrehash: " + str(self.rehashed) + "\nfor m: " + str(m) + " c: " + str(self.c) + " Run time: " +#  str((stoptime - starttime)) + " sekunder" +
                "\nloadfactor: " + str(self.loadfactor) + "\n" +str(self.slots) + "\n--------- Exit on  nr: " + str(self.c) + " klar ---------" + "\n")
     f.close()


def randomgen(length, intstart, intstop, lst, filename):
    print "file open: ", filename, "\ngenerating random numbers"

    # generate the random numbers
    for i in range(length):
        lst.append(random.randint(intstart,intstop)) #för temp random lista

    # save the random numbers to file for later use
    f = open(filename, "w")
    for item in range(len(lst)):
        f.write(str(lst[item]) + "\n")

    f.close()

    print "done\n",filename, "closed."

    print "random numbers done.\n"


def loadrandom(m, filename):
    global randlst
    randlst = []

    # load random numbers from 0 to m from file
    with open(filename) as randoms:
        for line in range(m):
            randlst.append(int(randoms.readline()))
    randoms.close()


def runshit(m,filename, randomnumbersfile, maxirun, c):

    b = 7  # should be same as the start value for m/c depending on class to run
    print "\nopen file: ", filename
    f = open(filename, "w")
    print "file open ", filename, "Ready to save output's"

    while b <= maxirun:
        print "\nLoading random numbers from file: ", randomnumbersfile
        loadrandom(m, randomnumbersfile)

        print "\nStart timer \n running hash shit"
        starttime = timeit.default_timer()

        # choose which class to run.
        hash1 = PANoob(m)  # uncomment to run the first class
        #hash1 = StahlJohanUpDown(m)  # uncomment to run the second class (up/down)
        #hash1 = superkasra(m, c)  # uncomment to run the third class (rehash)

        print "hash1 storlek: ", hash1.size

        i = 0
        while i < m:
            # hash1.insert(random.randint(1,stop))  # uncomment for random numbers all the time

            #hash1.insert(randlst[i])  #  insert random numbers from file in the hash table
            hash1.insert(testlst[i])

            # f.write(str(hash1.slots) + "\n") # uncomment for writing the slot output's [none, none, none, 1, none] etc to file.
            i += 1
            # print hash1.slots # uncomment for terminal print of the slot output's [None, None, 1] etc

        stoptime = timeit.default_timer()

        #  Saves the output values to a .txt file
        f.write("\n--------- Test nr: " + str(b) + " ---------" + "\nFinal L_down: " + str(hash1.l_down) + "\nFinal L_up: " + str(hash1.l_up) +
                "\nprobes: " + str(hash1.probes) + "\ncollision chain: " +str(hash1.collisionLongestSofar) +
                "\ntotal collision: " + str(hash1.collisionTotal)+ "\nprobes: " + str(hash1.probes) + "\nloadfactor: " + str(hash1.loadfactor) + "\nfor m: " + str(m) + " Run time: " + str((stoptime - starttime)) + " sekunder" +
                #"\nrehash: " + str(hash1.rehashed) + " c: " + str(hash1.c) +  # uncomment to save additional values for class 3
                "\n--------- Test nr: " + str(b) + " klar ---------" + "\n")

        # terminal print's same as what is saved to file
        print "\n--------- Test nr: ", b, " ---------", "\nFinal L_down: ", hash1.l_down, "\nFinal L_up: ", hash1.l_up, \
            "\nprobes: ", hash1.probes, "\ncollisions: ",hash1.collision ,"\ncollision chain: " ,hash1.collisionLongestSofar, \
            "\nlongest collision: ", hash1.collisionLongest, "\ntotal collision: ", hash1.collisionTotal, "\nloadfactor: ", hash1.loadfactor, \
            "\nfor m: ", m, " Run time: ", (stoptime - starttime), " sekunder", \
            #"\nrehash: ", hash1.rehashed, " c: ", hash1.c  # uncomment to save additional values for class 3
        print "\n--------- Test nr: ", b, " klar ---------", "\n"

        #c += 4  # raise c value
        m += 7  # change for stepping interval of modulu and hashtable size
        print "\nNew m after run : ", m
        b += 7  # raise b, should be same as m/c depending on which class to run
    f.close()
    print "done. ", filename, " closed."

    print hash1.slots


m = 7
last_m = 7
cvarde = 4  # not used for class 1 and 2
randlst = []
#testlst=[5,15,25,3,35]  # c=3 cc=2
#testlst = [10,1,2,3,13,23,6,7,80,9]  # c = 3 cc = 2
testlst = [7,14,21,28,4,5,38]  # c= 4 cc = 3

# run randomgen below one time first to generate random numbers to be used if not supplied then comment it out again
# randomgen(langd, 1, langd, randlst, "randomnumbers_up_down.txt")

#loadrandom(m, "randomnumbers_up_down.txt")# , randlst)

#def runshit(m,filename, randomnumbersfile, maxirun, c): starting m value, name of output file, name of random numbers file, last m value, c value
runshit(m, "lab2_rehash_test5.txt", "randomnumbers_up_down.txt", last_m, cvarde)



#  [5, 15, 25, 3, 35]