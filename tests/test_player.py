from player import Player

def test():
    player = Player(name="Trevor", color="green")
    print("Player name and color:")
    print(player.get_name())
    print(player.get_color())

    print("Player colors won")
    print(player.get_colors_won())
    player.update_colors_won("blue")
    print(player.get_colors_won())

    print("Player scores")
    print(player.get_score())
    player.score_update(10)
    player.score_update(20)
    print(player.get_score())

    print("Player position")
    print(player.get_position())
    player.set_position([1,0])
    print(player.get_position())


if __name__ == '__main__':
    test()
