from campus import Campus

class Exploration:
    def __init__(self, campus_name):
        self.campus = Campus(campus_name)

    def greedy_student(self, location, stamina):
        """
        Analyse your time complexity of this method.

        Best case is O(1), when stamina is 0 or there is no connections for the location.

        Worst case is O(N * E), where E is value of the stamina, and N is number of all connections for the location

        The logic is for each recursive call, the function traverse all connections of the location, which takes O(N)
        and then, when call recursion again, it will reduce stamina by 1 every time, so there are E times recursion call

        So, total is O(N * E)
        """
        
        current_location = location
        current_reward = current_location.get_reward()
        all_connections = current_location.get_connections()
        
        # base case
        if len(all_connections) == 0 or stamina == 0:
            return current_reward
        
        # find the best connection
        best_connection = None
       
        for connection in all_connections:
            if best_connection is None:
                best_connection = connection
                continue

            if connection.get_difficulty() < best_connection.get_difficulty():
                best_connection = connection
                continue

            if connection.get_difficulty() == best_connection.get_difficulty():
                if connection.get_location().get_reward() > best_connection.get_location().get_reward():
                    best_connection = connection
                    continue
        
        # recursion 
        return self.greedy_student(best_connection.get_location(), stamina - 1) + current_reward
       

    def total_difficulty(self, location):
        """
        Time complexity analysis not required for this method.
        """
        (total_paths, total_difficulty) = self.child_difficulty(location)
        return total_difficulty
    

    # return child paths and child total difficulty
    def child_difficulty(self, location):

        connections = location.get_connections()

        # base case
        if len(connections) == 0:
            return 1, 0
        
        total_paths = 0
        total_difficulty = 0

        # loop and recursion
        for connection in connections:
            edge_difficulty = connection.get_difficulty()
            next_location = connection.get_location()

            child_paths, child_difficulty = self.child_difficulty(next_location)

            total_paths += child_paths
            total_difficulty += edge_difficulty * child_paths + child_difficulty
        
        return total_paths, total_difficulty


    def total_reward_for_longest_path(self, location):
        """
        Time complexity analysis not required for this method.
        """
        (best_max_length, best_total_reward) = self.total_reward_for_longest_path_aux(location)
        return best_total_reward

    # helper function
    def total_reward_for_longest_path_aux(self, location):
        connections = location.get_connections()
        current_reward = location.get_reward()
        
        # base case
        if len(connections) == 0:
            return 1, current_reward
        

        best_max_length = 0
        best_total_reward = 0
        
        # loop and recursion
        for connection in connections:
            next_location = connection.get_location()
            child_length, child_reward = self.total_reward_for_longest_path_aux(next_location)

            candidate_length = child_length + 1
            candidate_reward = child_reward + current_reward

            if candidate_length > best_max_length:
                best_max_length = candidate_length
                best_total_reward = candidate_reward
            
            elif candidate_length == best_max_length:
                if candidate_reward > best_total_reward:
                    best_total_reward = candidate_reward
        
        return best_max_length, best_total_reward


    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass

if __name__ == '__main__':
    print("Clayton")
    clayton = Exploration("clayton")
    for campus_location in clayton.campus.get_all_locations():
        print(campus_location)
    print()

    print("Malaysia")
    malaysia = Exploration("malaysia")
    for campus_location in malaysia.campus.get_all_locations():
        print(campus_location)

    # Sample test cases
    assert clayton.greedy_student(clayton.campus.get_location_by_name('Menzies Building'), 1) == 22, "Greedy student should collect 22 reward"
    assert clayton.total_difficulty(clayton.campus.get_start_location()) == 190, "Total difficulty should be 190"
    assert clayton.total_reward_for_longest_path(clayton.campus.get_start_location()) == 86, "Longest path should be 86"

    # Add test code here
    end_location = clayton.campus.get_location_by_name("New Horizons")
    assert clayton.greedy_student(end_location, 5)  == end_location.get_reward()
    assert clayton.total_difficulty(end_location) == 0
    assert clayton.total_reward_for_longest_path(end_location) == end_location.get_reward()

    print("All test passed!")