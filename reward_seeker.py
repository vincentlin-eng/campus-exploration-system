from campus import Campus
from data_structures import array_max_heap
from data_structures import linked_list
from data_structures import array_list
from data_structures import hash_table_separate_chaining
from reward_structure import RewardStructure

class RewardSeeker:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.

     First, creating the Campus object reads the campus file and extracts all locations
    and connections. This takes O(N + E), where N is the number of locations and E is
    the number of connections in the campus file.

    Creating the two hash tables takes O(1), because the default table size is fixed.
    Creating the temporary LinkedList also takes O(1).

    Then, the method traverses all locations once. For each location, it appends one
    tuple into the temporary container, inserts the current reward into the hash table,
    and inserts the visited status into another hash table. These operations all take
        O(1). Therefore, this loop takes O(N).

    Finally, heapify is used to create the max heap from the temporary container.
    Heapify takes O(N), where N is the number of locations.

    sSo, the total time complexity is O(N + E) + O(N) + O(N), which simplifies to
    O(N + E).
        """
        self.campus: Campus = Campus(campus_name)
        all_locations = self.campus.get_all_locations()

             # store the currrent valid location
        self.current_valid_location_table = hash_table_separate_chaining.HashTableSeparateChaining()

        self.visited_record = hash_table_separate_chaining.HashTableSeparateChaining()

        tempt_container = linked_list.LinkedList()

        # put the locations into tempt_container and initialise hashtable
        for location in all_locations:
            tempt_container.append((location.get_reward(),location.get_name()))

            reward = location.get_reward()
            name = location.get_name()

            self.current_valid_location_table[name] = reward
            self.visited_record[name] = False


        # use heapify to create a new max heap
        self.max_heap = RewardStructure.heapify(tempt_container)
   

    def get_next_location(self):
        """
        Analyse your time complexity of this method.

        Time complexity is O(logN) for best and worst case, where N is the number of elements inside max heap
        This method is directly call extract_root in class ArrayMaxHeap, and the root is 
        always the maximum one in max_heap. Every time, it will get, delete and update the root.

        The sink operation inside takes O(logN), where N is the number of elements inside max heap.
        """
        while len(self.max_heap) != 0:
            next_top_location_tuple = self.max_heap.extract_root()

            # check if it is visited before
            if self.visited_record[next_top_location_tuple[1]] == True:
                continue

            # check if it is valid
            name = next_top_location_tuple[1]
            if next_top_location_tuple[0] != self.current_valid_location_table[name]:
                continue
            
            self.visited_record[next_top_location_tuple[1]] = True
            return next_top_location_tuple
            
            
        return None

        
    def get_top_k_locations(self, k):
        """
        Analyse your time complexity of this method.

        Time complexity is O(klogN) for best and worst case, 
        where k is the number of elements this function will return,
        and N is the number of all elements inside heap.

        Because this function need to traverse k times, each time call get_next_location once,
        check if it is None takes O(1), and append into arraylist takes O(1),
        so total is O(klogN).
        """
        result = array_list.ArrayList(k)

        for _ in range(k):
            top_location_tuple = self.get_next_location()
            # in case, get_next_location return None
            if top_location_tuple is None:
                return result
            result.append(top_location_tuple)
        
        return result


    def update_location_reward(self, location_name, new_reward):
        """
        Analyse your time complexity of this method.

        Best case is O(1), when don't need to add into heap
        Worst case is O(logN), where N is the number of locations in heap
        
        the update hashtable and get_location_by_name are both hashtable operations takes O(1)
        and if need to add into heap, add operation in heap takes O(logN) in worst case, best case is O(1)
        where N is the number of locations in heap. 
        """
        # format: heap(reward, name), hash table(name, reward)
        # update current valid location hash table
        self.current_valid_location_table[location_name] = new_reward

        # update location in campus
        location = self.campus.get_location_by_name(location_name)
        location.set_reward(new_reward)

        if self.visited_record[location_name] == False:
            # add new location into heap
            self.max_heap.add((new_reward, location_name))

           

if __name__ == '__main__':
    reward_seeker = RewardSeeker('clayton')
    # Add test code here

    # test get_next_location, get the most desirable location
    next_loc = reward_seeker.get_next_location()
    print(next_loc)

    print()

    # test get_top_k_locations
    reward_seeker = RewardSeeker('clayton')
    result = reward_seeker.get_top_k_locations(3)
    for top3 in result:
        print(top3)

    # test update_location_reward
    print()
    reward_seeker = RewardSeeker('clayton')

    reward_seeker.get_next_location()
    reward_seeker.update_location_reward('Campus Centre', 21)

    next_update = reward_seeker.get_next_location()
    print(next_update)

    print()

    reward_seeker.get_top_k_locations(2)

    reward_seeker.update_location_reward('Religious Centre', 19)
    reward_seeker.update_location_reward('Campus Centre', 21)

    top_updated = reward_seeker.get_top_k_locations(2)
    print(top_updated)

    print("All test passed!")

