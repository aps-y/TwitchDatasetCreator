import twitch
import networkx as nx
from threading import Semaphore
import time

class dataGraph :
    m_graph = nx.DiGraph()
    m_node_set = set()
    following_limit = 2
    follower_limit = 2
    node_limit = 20
    m_user_queue = []
    m_user_queue_set = set()
    helix = None
    m_user_queue_semaphore = Semaphore()

    def get_followers_following(name):
        # Acquire Semaphore
        dataGraph.m_user_queue_semaphore.acquire()
        if(len(dataGraph.m_user_queue)==0):
            print('queue is empty')
            exit()
        id = dataGraph.m_user_queue.pop()
        dataGraph.m_user_queue_semaphore.release()
        # Released Semaphore
        print(name,"In get_followers_following() for id = ",id)
        user = dataGraph.helix.user(id)
        follower_count = user.followers().total
        following_count = user.following().total
        folwrs = user.followers()
        folwing = user.following()

        follower_set = set()
        following_set = set()

        prev_count = -1
        while len(follower_set)<follower_count and len(follower_set)>prev_count:
            prev_count=len(follower_set)
            try :
                uu = folwrs.users
            except Exception as e:
                try:
                    uu = folwrs.users
                    # print('second time')
                except Exception as e:
                    print("did not work")
                    break
            for u in uu:
                if(len(follower_set)>=follower_count):
                    break
                follower_set.add(int(u.id))
        print(name,'Total Followers = ',follower_count,'; ','Followers Obtained = ',len(follower_set),'for id = ',id)


        prev_count= -1
        while len(following_set)<following_count and len(following_set)>prev_count :
            prev_count = len(following_set)
            try :
                uu = folwing.users
            except Exception as e:
                try:
                    uu = folwing.users
                    # print('second time')
                except Exception as e:
                    print(name,"did not work")
                    break
            for u in uu:
                if(len(following_set)>=following_count):
                    break
                following_set.add(int(u.id))
        print(name,'Total Following = ',following_count,'; ','Following Obtained = ',len(following_set),'for id = ',id)

        return id, follower_set, following_set
    

    def add_to_graph(id, follower_set, following_set,name):
        print(name,'In add_to_graph() for id =',id)
        dataGraph.m_node_set.add(id)
        existing_followers = set()
        for f_id in follower_set:
            if f_id in dataGraph.m_node_set:
                dataGraph.m_graph.add_edge(f_id,id)
                existing_followers.add(f_id)
        follower_set = follower_set.difference(existing_followers)

        existing_following = set()
        for f_id in following_set:
            if f_id in dataGraph.m_node_set:
                dataGraph.m_graph.add_edge(id,f_id)
                existing_following.add(f_id)
        following_set = following_set.difference(existing_following)

        count =0
        for f_id in follower_set:
            if count >= dataGraph.follower_limit :
                break
            if f_id not in dataGraph.m_user_queue_set:
                dataGraph.m_user_queue.append(f_id)
                dataGraph.m_user_queue_set.add(f_id)
                count+=1
        
        count=0
        for f_id in following_set:
            if count >= dataGraph.follower_limit :
                break
            if f_id not in dataGraph.m_user_queue_set:
                dataGraph.m_user_queue.append(f_id)
                dataGraph.m_user_queue_set.add(f_id)
                count+=1
