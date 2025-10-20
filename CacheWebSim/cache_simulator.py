import random

class Cache:
    def __init__(self, size_kb, block_size, assoc, policy, access_cycles, next_level=None):
        self.size_bytes = size_kb * 1024
        self.block_size = block_size
        self.assoc = assoc
        self.policy = policy
        self.access_cycles = access_cycles
        self.next_level = next_level
        self.num_sets = self.size_bytes // (self.block_size * self.assoc)
        self.cache = [[] for _ in range(self.num_sets)]
        self.hits = 0
        self.misses = 0
        self.accesses = 0

    def access(self, address):
        self.accesses += 1
        index = (address // self.block_size) % self.num_sets
        tag = address // (self.block_size * self.num_sets)

        if tag in self.cache[index]:
            self.hits += 1
            if self.policy == 'LRU':
                self.cache[index].remove(tag)
                self.cache[index].append(tag)
            return self.access_cycles
        else:
            self.misses += 1
            miss_penalty = self.next_level.access(address) if self.next_level else 200
            if len(self.cache[index]) >= self.assoc:
                if self.policy == 'LRU':
                    self.cache[index].pop(0)
                elif self.policy == 'Random':
                    self.cache[index].pop(random.randint(0, len(self.cache[index])-1))
                elif self.policy == 'FIFO':
                    self.cache[index].pop(0)
            self.cache[index].append(tag)
            return self.access_cycles + miss_penalty

    def reset_metrics(self):
        self.hits = self.misses = self.accesses = 0
