#!/usr/bin/env python3
from day9 import run_program
from collections import defaultdict
from multiprocessing import Process, Queue, Array
from queue import Empty
from time import sleep
import ctypes

def main():
    with open("day23.txt", "r") as fp:
        memory = dict()
        for i, s in enumerate(fp.read().split(",")):
            memory[i] = int(s)
    
    # Part 1
    receive_queues = [Queue() for i in range(50)]
    done_queue = Queue()
    def receive(index):
        yield index
        while True:
            try:
                (x, y) = receive_queues[index].get_nowait()
                yield x
                yield y
            except Empty:
                yield -1
                yield -1
    def send(index, program):
        while True:
            dest = next(program)
            x = next(program)
            y = next(program)
            if dest == 255:
                done_queue.put_nowait(y)
                break
            receive_queues[dest].put_nowait((x, y))
    
    senders = [
        Process(target=send, args=(i, run_program(defaultdict(lambda: 0, memory), receive(i))))
        for i
        in range(50)
    ]
    for sender in senders:
        sender.start()
    result = done_queue.get()
    for sender in senders:
        sender.terminate()
    print(result)

    # Part 2
    receive_queues = [Queue() for i in range(50)]
    nat_value = Array(ctypes.c_long, 2)
    waiting = Array(ctypes.c_bool, len(receive_queues))
    def receive(index):
        yield index
        while True:
            try:
                (x, y) = receive_queues[index].get_nowait()
                with waiting.get_lock():
                    waiting[index] = False
                yield x
                yield y
            except Empty:
                with waiting.get_lock():
                    waiting[index] = True
                yield -1
                yield -1
    def send(index, program):
        while True:
            dest = next(program)
            x = next(program)
            y = next(program)
            if dest == 255:
                with nat_value.get_lock():
                    nat_value[0] = x
                    nat_value[1] = y
            else:
                receive_queues[dest].put_nowait((x, y))
    
    senders = [
        Process(target=send, args=(i, run_program(defaultdict(lambda: 0, memory), receive(i))))
        for i
        in range(50)
    ]
    for sender in senders:
        sender.start()
    
    last_nat_y = None
    while True:
        sleep(0.25)
        with waiting.get_lock():
            all_waiting = True
            for w in waiting:
                all_waiting = all_waiting and waiting
            if all_waiting:
                with nat_value.get_lock():
                    receive_queues[0].put_nowait((nat_value[0], nat_value[1]))
                    if last_nat_y == nat_value[1]:
                        break
                    else:
                        last_nat_y = nat_value[1]
    for sender in senders:
        sender.terminate()
    print(last_nat_y)

if __name__ == '__main__':
    main()
