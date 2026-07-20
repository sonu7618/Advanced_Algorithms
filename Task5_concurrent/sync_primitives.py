import threading


# Reusable barrier for thread synchronization
class Barrier:
    def __init__(self, n_threads):
        self.n_threads = n_threads
        self.count = 0
        self.generation = 0
        self.cond = threading.Condition()

    # Wait until all threads reach the barrier
    def wait(self):
        with self.cond:
            my_generation = self.generation
            self.count += 1

            if self.count == self.n_threads:
                # Last thread resets the barrier and wakes all threads
                self.generation += 1
                self.count = 0
                self.cond.notify_all()
            else:
                # Wait until the current generation is complete
                while my_generation == self.generation:
                    self.cond.wait()