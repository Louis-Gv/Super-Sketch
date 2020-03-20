import client
from multiprocessing import Process, Queue, Value
if __name__ == '__main__':
    client.client(1, Process())