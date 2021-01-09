import twitch
import networkx as nx

class dataGraph :
    m_graph = nx.DiGraph()
    m_node_set = set()
    following_limit = 2
    follower_limit = 2
    node_limit = 20
    m_user_queue = []
    m_user_queue_set = set()
    helix = None

    def get_followers_following():
        if(len(dataGraph.m_user_queue)==0):
            print('queue is empty')
            exit()
        id = dataGraph.m_user_queue.pop()
        print("In get_followers_following() for id = ",id)
        user = dataGraph.helix.user(id)
        follower_count = user.followers().total
        following_count = user.following().total
        folwrs = user.followers()
        folwing = user.following()

        follower_set = set()
        following_set = set()

        while len(follower_set)<follower_count:
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
        
        while len(following_set)<following_count:
            try :
                uu = folwing.users
            except Exception as e:
                try:
                    uu = folwing.users
                    # print('second time')
                except Exception as e:
                    print("did not work")
                    break
            for u in uu:
                if(len(following_set)>=following_count):
                    break
                following_set.add(int(u.id))
        return id, follower_set, following_set
    

    def add_to_graph(id, follower_set, following_set):
        print('In add_to_graph() for id =',id)
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

def runner() :
    while len(dataGraph.m_node_set)<dataGraph.node_limit:
        print('Number of nodes added = ',len(dataGraph.m_node_set))
        if len(dataGraph.m_user_queue) ==0:
            break
        id,follower_set,following_set = dataGraph.get_followers_following()
        dataGraph.add_to_graph(id,follower_set,following_set)


#replace 'client_id' and 'client_secret' with actual values and also find one 'user_id' to start the task
dataGraph.helix = twitch.Helix('client_id','client_secret')
dataGraph.m_user_queue.append(int('user_id'))
dataGraph.m_user_queue_set.add(int('user_id'))
runner()
print(nx.adjacency_matrix(dataGraph.m_graph))

