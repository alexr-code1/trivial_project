from typing import List

class Player:
    """
    Class for player objects in the trivial compute game. 
    """
    def __init__(self, name:str, color:str):
        """
        Initializes the player class. 
        :param name[str]: Name of the player
        :param color[str]: Color of the player
        """
        self.name = name
        self.color = color
        self.colors_won = []
        self.player_score = 0
        self.player_position = []
        self.last_position = []

    def get_name(self):
        """
        Returns the player's name. 
        """
        return self.name
    
    def get_color(self):
        """
        Returns the player's color. 
        """
        return self.color
    
    def update_colors_won(self, color:str):
        """
        Update the colors that a player has won. 
        :param color[str]: New color that the player just won. 
        :return: None
        """
        self.colors_won.append(color)

    def get_colors_won(self):
        """
        Return the colors that a player has won.
        """
        return self.colors_won

    def score_update(self, score_change: int):
        """
        Updates the player's score.
        :param score_change[int]: Amount of points to add to the player's score
        :return: None
        """
        self.player_score += score_change
    
    def get_score(self):
        """
        Returns the player's score.
        """
        return self.player_score

    def set_position(self, position: List):
        """
        Sets the player's current position. 
        :param position[List]: Coordinates of the player's current position (e.g., [1, 4])
        :return: None
        """
        self.player_position = position

    def get_position(self):
        """
        Returns the player's current position. 
        """
        return self.player_position