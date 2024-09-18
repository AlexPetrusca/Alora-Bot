from abc import abstractmethod


class Action:
    tick_counter = 0

    @abstractmethod
    def first_tick(self):
        ...

    @abstractmethod
    def tick(self, t):
        ...

    def reset(self):
        self.tick_counter = 0

    def run(self, t):
        if self.tick_counter == 0:
            self.first_tick()
        self.tick_counter += 1
        return self.tick(t)
