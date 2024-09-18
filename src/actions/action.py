from abc import abstractmethod

INTERVAL = 0.1

class Action:
    tick_counter = 0

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, t):
        ...

    @abstractmethod
    def last_tick(self):
        ...

    def run(self, t):
        if self.tick_counter == -1:
            self.first_tick()
            self.tick_counter = 0
        if t / INTERVAL > self.tick_counter:
            self.tick_counter += 1
            if self.tick(t):
                print(self.tick_counter)
                self.last_tick()
                self.tick_counter = -1
                return True
        return False
