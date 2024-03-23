import threading
import random

LOWER_NUM = 1
UPPER_NUM = 10000
BUFFER_SIZE = 100
MAX_COUNT = 10000

# Global variables
buffer = []
buffer_lock = threading.Lock()
producer_done = threading.Event()
even_file = open("even.txt", "w")
odd_file = open("odd.txt", "w")
all_file = open("all.txt", "w")

# Producer function
def producer():
    for _ in range(MAX_COUNT):
        num = random.randint(LOWER_NUM, UPPER_NUM)
        with buffer_lock:
            buffer.append(num)
            all_file.write(str(num) + "\n")
            if len(buffer) > BUFFER_SIZE:
                buffer.pop(0)
        if producer_done.is_set():
            break
    producer_done.set()

# Consumer function for even numbers
def consumer_even():
    while not producer_done.is_set() or buffer:
        with buffer_lock:
            if buffer and buffer[-1] % 2 == 0:
                num = buffer.pop()
                even_file.write(str(num) + "\n")

# Consumer function for odd numbers
def consumer_odd():
    while not producer_done.is_set() or buffer:
        with buffer_lock:
            if buffer and buffer[-1] % 2 != 0:
                num = buffer.pop()
                odd_file.write(str(num) + "\n")

# Start threads
producer_thread = threading.Thread(target=producer)
even_consumer_thread = threading.Thread(target=consumer_even)
odd_consumer_thread = threading.Thread(target=consumer_odd)

producer_thread.start()
even_consumer_thread.start()
odd_consumer_thread.start()

# Join threads
producer_thread.join()
even_consumer_thread.join()
odd_consumer_thread.join()

# Close files
even_file.close()
odd_file.close()
all_file.close()
