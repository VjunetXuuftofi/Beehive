class Forager:
    MAX_NECTAR_CAPACITY = 5
    MAX_HUNGER = 200
    HONEY_HUNGER_DECREASE = 5
    FORAGE = 0
    EAT = 1
    DEPOSIT_NECTAR = 2
    MOVE = 3
    REDUCE_INTO_HONEY = 4

    def __init__(self, environment, loc):
        self.environment = environment
        self.pos = loc
        self.hunger = 0
        self.nectar = 0
        self.action_taken = False

    def submit_action(self, action):
        if self.action_taken:
            #raise Exception("This Forager has already taken an action!")
            print("This forager has already taken an action.")
        elif action[0] == Forager.FORAGE:
            self._forage()
        elif action[0] == Forager.EAT:
            self._eat()
        elif action[0] == Forager.DEPOSIT_NECTAR:
            self._deposit_nectar()
        elif action[0] == Forager.MOVE:
            self._move(action[1])
        elif action[0] == Forager.REDUCE_INTO_HONEY:
            self._reduce_into_honey()
        self.action_taken = True

    def _forage(self):
        if self.pos in self.environment.flowers:
            self.nectar += 1
        else:
            raise Exception("You tried to get a Forager to forage, "
                            "but it was not on a flower. ")

    def _eat(self):
        if self.pos in self.environment.cells:
            this_cell = self.environment.cells[self.pos]
            if this_cell["honey"] > 0:
                this_cell["honey"] -= 1
                self.hunger -= Forager.HONEY_HUNGER_DECREASE
                if self.hunger < 0:
                    self.hunger = 0
            else:
                raise Exception("You tried to eat in a cell with no honey.")
        else:
            raise Exception("You tried to eat, but you weren't in a cell.")

    def _deposit_nectar(self):
        if self.pos in self.environment.cells:
            amount_deposited = self.environment.deposit_nectar(self.pos,
                                                               self.nectar)
            self.nectar -= amount_deposited
        else:
            raise Exception("You must deposit nectar into a cell")

    def _move(self, pos):
        if pos[0] < 0 or pos[0] > self.environment.X_SIZE or pos[1] < 0 \
                or pos[1] > self.environment.Y_SIZE:
            raise Exception("You can't go off of the screen!")
        if pos in self.environment.foragers:
            raise Exception("You cannot move a forager into a position with "
                            "another forager.")
        elif abs(pos[0] - self.pos[0]) > 1 or abs(pos[1]-self.pos[1]) > 1:
            raise Exception("You can only move one square at a time.")
        else:
            self.environment.foragers.pop(self.pos) # pop off the old position
            self.pos = pos # change the data member
            self.environment.foragers[pos] = self # put this into the new
            # location

    def _reduce_into_honey(self):
        if self.pos in self.environment.cells:
            this_cell = self.environment.cells[self.pos]
            if this_cell["nectar"] > 0:
                this_cell["nectar"] -= 1
                this_cell["honey"] += 1
            else:
                raise Exception("Cell must have nectar to be reduced.")
        else:
            raise Exception("You must be in a cell to reduce nectar into honey.")


    def __str__(self):
        return str(self.action_taken)
