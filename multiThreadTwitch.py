from threading import *
from twitchDataset import dataGraph
import twitch
import argparse

m_graph_semaphore = Semaphore()
threadCount = 0

def runner(name):
    while len(dataGraph.m_node_set)<dataGraph.node_limit:
        print('Number of nodes added = ',len(dataGraph.m_node_set))
        if len(dataGraph.m_user_queue) ==0:
            break
        id,follower_set,following_set = dataGraph.get_followers_following()

        # Acquire Semaphore
        m_graph_semaphore.acquire()
        dataGraph.add_to_graph(id,follower_set,following_set)
        m_graph_semaphore.release()
        # Released Semaphore

parser = argparse.ArgumentParser()

parser.add_argument('--followerLimit',type=int)
parser.add_argument('--followingLimit',type=int)
parser.add_argument('--nodeLimit',type=int)
parser.add_argument('--initQueue',type=str)
parser.add_argument('--numThreads',type=int)

args = parser.parse_args()

if args.followerLimit:
    dataGraph.follower_limit = args.followerLimit
else:
    dataGraph.follower_limit = 2
if args.followingLimit:
    dataGraph.following_limit = args.followingLimit
else:
    dataGraph.following_limit=2
if args.nodeLimit:
    dataGraph.node_limit = args.nodeLimit
else:
    dataGraph.node_limit=20
if args.initQueue:
    arr = args.initQueue.split(',')
    dataGraph.m_user_queue.clear()
    for id in arr:
        dataGraph.m_user_queue.append(int(id))
else:
    dataGraph.m_user_queue = [39543557,54452228, 79774729]

if args.numThreads:
    threadCount = args.numThreads
else:
    threadCount = min(3, len(dataGraph.m_user_queue))

dataGraph.helix = twitch.Helix('clientId','clientSecret')

m_thread_arr = []

for i in range(0,threadCount):
    thread_name = 'Thread-'+str(i+1)
    t = Thread(runner,args=(thread_name,))
    m_thread_arr.append(t)

for t in m_thread_arr:
    t.start()