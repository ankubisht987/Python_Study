from redis import Redis
from rq import Queue


from RAG_Queue.queues.worker import process_query

queue = Queue(connection = Redis(
    host="localhost",
    port="6379"
))


# queue.enqueue(process_query)