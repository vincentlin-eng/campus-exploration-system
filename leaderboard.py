from campus import LeaderboardReader
from algorithms import merge_sort
from data_structures import array_list

class Leaderboard:
    def __init__(self, campus_name):
        """
        Analyse your time complexity of this method.

        Best and Worst case: O(NlogN), where N is the number of players in leaderboard file.
        Create arraylist takes O(N), reading the leaderboard file takes O(N)
        then merge_sort takes O(NlogN) in both best and worst case. So total is O(NlogN).
        """
        self.players = array_list.ArrayList()
        list_of_players = LeaderboardReader.read(campus_name)
        # sort 
        self.players = merge_sort.merge_sort(list_of_players, key = lambda player : (- player.score, - player.stamina))


    def combine(self, other_leaderboard):
        """
        Analyse your time complexity of this method.

        The best and worst case of this function is O(N+M), where N is the number of players from current leaderboard object which is self_players,
        and M is the number of players in other_leaderboard.players.

        The main while loop appends one player each iteration, and compare and append operation both takes O(1),
        so this step takes O(M) or O(N), depends on which one is end earlier.
        Then the two remaining while loops append the leftover players. So all in all, the algorithm will process every player inside,
        so the total time complexity is O(N+M).
        """
        new_container = array_list.ArrayList(len(self.players) + len(other_leaderboard.players))

        pointer_self = 0
        pointer_other = 0

        
        while pointer_self < len(self.players) and pointer_other < len(other_leaderboard.players):
            
            self_player = self.players[pointer_self]   # prevent self_player not change
            other_player = other_leaderboard.players[pointer_other]
            
            if self_player.score > other_player.score:
                new_container.append(self_player)
                pointer_self += 1
               

            elif self_player.score == other_player.score and self_player.stamina >= other_player.stamina:
                new_container.append(self_player)
                pointer_self += 1
              
            else:
                new_container.append(other_player)
                pointer_other += 1
               

        while pointer_self < len(self.players):
            self_player = self.players[pointer_self]
            
            new_container.append(self_player)
            pointer_self += 1
            

        while pointer_other < len(other_leaderboard.players):
            other_player = other_leaderboard.players[pointer_other]
            
            new_container.append(other_player)
            pointer_other += 1
           

        self.players = new_container
        
    

    def __str__(self):
        """
        Optional: For debugging purposes only
        """
        pass


if __name__ == "__main__":
    leaderboard = Leaderboard("clayton")
    # Add test code here

    # check the initialisation
    for player in leaderboard.players:
        print(player)

    # test the first player is sorted correctly
    assert leaderboard.players[0].name == "Dana"
    assert leaderboard.players[0].id == 4
    assert leaderboard.players[0].score == 150
    assert leaderboard.players[0].stamina == 14
    print("the first player is correct!")


    # leave a space
    print()

    # check the combination
    malaysia = Leaderboard("malaysia")

    leaderboard.combine(malaysia)
    for player in leaderboard.players:
        print(player)

    print("All test passed!")