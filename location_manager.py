from campus import Campus
from data_structures import binary_search_tree
from data_structures import hash_table_separate_chaining
from data_structures import array_list

class LocationManager:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.
        First, read the campus file and extract locations and connections takes O(E), 
        where E is total connections in campus.

        create an empty BST takes O(1), creating a default hashtable depends on the size of hashtable,
        but the default size is 17, so it is O(1).

        Calculating the desirability of every location will base on the number of current connections difficulty of location.
        It traverse that all connections that location has
        so this part is O(E), where E is total connections in campus.

        Traversing all_locations takes O(N), where N is the number of locations in campus, and every location
        will be inserted into hashtable, which takes O(1). 
        And inserting into BST, which takes O(log N), where N is the number of locations in campus

        So, the total time complexity is O(E + NlogN), for both best and worst case. 
        """
        self.campus: Campus = Campus(campus_name)
        all_locations = self.campus.get_all_locations()

        self.binary_tree = binary_search_tree.BinarySearchTree()
        self.hash_table = hash_table_separate_chaining.HashTableSeparateChaining()

        for location in all_locations:
            desirability = self.get_desirability(location)
            self.hash_table[location.get_name()] = desirability
            self.binary_tree[desirability] = location

    # helper function to calculate desirability
    def get_desirability(self, location):
        reward = location.get_reward()
        avg_difficulty = self.get_avg_connection_difficulty(location)

        desirability = round(reward / (1 + avg_difficulty), 2)
        return desirability

    # helper function to get average_connection_difficulty
    def get_avg_connection_difficulty(self, location):
        # get linkedlist storing connections
        all_connections_for_location = location.get_connections()
        # calculate average connection difficulty
        total_difficulty = 0

        if len(all_connections_for_location) == 0:
            return 0
        
        for connection in all_connections_for_location:
            total_difficulty += connection.get_difficulty()
        
        avg_difficulty = total_difficulty / len(all_connections_for_location)
        return avg_difficulty
            

    # can access the internals of data structure
    def get_locations_in_range(self, min_score, max_score):
        """
        Analyse your time complexity of this method.

        Because for better best case time efficiency, so I do not use the InorderIterator in binary_search_tree.
        I do the search on my own.

        The best case is O(logN), where N is the number of nodes in binary search tree. 
        It happens when the search excludes most of the tree and only focus on one path of the tree
        And this equals to the depth of the tree.

        The worst case is O(N), where N is the number of nodes in binary search tree. 
        It happens when it need to search all nodes of tree.

        """
        result = array_list.ArrayList()

        self.get_locations_in_range_aux(self.binary_tree._root, min_score, max_score, result)

        return result

    # helper function
    def get_locations_in_range_aux(self, current_node, min_score, max_score, result):

        # base case
        if current_node is None:
            return
        
        # recursion
        if current_node.key > min_score:
            self.get_locations_in_range_aux(current_node.left, min_score, max_score, result)
        
        if min_score <= current_node.key <= max_score:
            result.append((current_node.key, current_node.item.get_name()))
        
        if max_score > current_node.key:
            self.get_locations_in_range_aux(current_node.right, min_score, max_score, result)
        


    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.

        The best and worst case is O(logN + k), where N is the number of nodes in BST,
        and k is the length of result.
        The logic is stopping when k nodes has been added into result. It does not require to 
        traverse the entire BST.
        Reaching the rightmost(biggest) node takes O(logN), logN is the depth of BST.
        And, append into result takes O(1), at most k locations appended. So this step is O(k).
        """
        result = array_list.ArrayList()
        self.get_top_k_locations_aux(k, self.binary_tree._root, result)

        return result

    def get_top_k_locations_aux(self, k, current_node, result):
        # base case
        if current_node == None:
            return
        
        if len(result) == k:
            return

        # recursion 
        self.get_top_k_locations_aux(k, current_node.right, result)

        if len(result) < k:
            result.append((current_node.key, current_node.item.get_name()))
        else:
            return

        self.get_top_k_locations_aux(k, current_node.left, result)


    def update_location(self, name, new_reward):
        """
        Analyse your time complexity of this method.

        get desirability from hash table takes O(1), 
        
        for worst case,delete from binary tree takes O(logN), where N is the number of nodes in BST
        for best case, it is O(1), the deleting node is root node
        because need to find the deleting node first, which need to traverse a path of BST.

        update reward takes O(1), but recalculating the desirability takes O(E), where E is the number of 
        connections of current location

        for worst case, insert into BST and put the node into right position takes O(logN) , 
        where N is the number of nodes in BST
        
        for best case is O(1), 
        update hash table takes O(1)
        """

        # get the old desirability
        old_desirability = self.hash_table[name]
        
        # find the accoresonding node and delete the location info
        del self.binary_tree[old_desirability]

        # update the new_reward
        location = self.campus.get_location_by_name(name)
        location.set_reward(new_reward)

        # recalculate the desirability
        new_desirability = self.get_desirability(location) 

        # insert new updated new binary node
        self.binary_tree[new_desirability] = location

        # update hash table values
        self.hash_table[location.get_name()] = new_desirability

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == '__main__':
    location_manager = LocationManager('clayton')

    # Add test code here
    # test get_locations_in_range function
    result = location_manager.get_locations_in_range(2.00, 7.00)

    for i in result:
        print(i)

    assert len(result) == 7

    print()
    # test get_top_k_locations function
    result2 = location_manager.get_top_k_locations(3)

    for i in result2:
        print(i)

    # test update_location
    location_manager.update_location('Robert Blackwood Hall', 20)
    # assert the desirability result
    assert location_manager.hash_table['Robert Blackwood Hall'] == 4.0

    print("All test passed!")

   

