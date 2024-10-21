import random
import argparse
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def add_to_score(self, points):
        self.score += points

    def reset_score(self):
        self.score = 0

    def __str__(self):
        return f"{self.name}: {self.score} points"

    def make_decision(self, current_score, turn_total):
        """Human player decision."""
        decision = input(f"{self.name}, roll again (r) or hold (h)? ").lower()
        return decision


class ComputerPlayer(Player):
    def make_decision(self, current_score, turn_total):
        """Computer strategy: hold at the lesser of 25 or 100 - current score."""
        if turn_total + current_score >= 100 or turn_total >= min(25, 100 - current_score):
            return 'h'  # Hold
        return 'r'  # Roll


class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == 'computer':
            return ComputerPlayer(name)
        elif player_type == 'human':
            return Player(name)
        else:
            raise ValueError("Unknown player type. Use 'human' or 'computer'.")


class Die:
    def __init__(self):
        self.value = 0

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value


class Game:
    def __init__(self, player1, player2):
        self.players = [player1, player2]
        self.die = Die()
        self.turn_total = 0
        self.current_player = 0

    def switch_player(self):
        """Switch to the next player."""
        self.current_player = 1 - self.current_player

    def play_turn(self):
        """Handle a single turn for the current player."""
        player = self.players[self.current_player]
        self.turn_total = 0

        while True:
            roll = self.die.roll()
            print(f"{player.name} rolled: {roll}")

            if roll == 1:
                print(f"{player.name} rolled a 1! No points added. Turn over.")
                self.turn_total = 0
                self.switch_player()
                break
            else:
                self.turn_total += roll
                print(f"Turn total: {self.turn_total}, Total score: {player.score}")

                decision = player.make_decision(player.score, self.turn_total)
                
                if decision == 'h':
                    player.add_to_score(self.turn_total)
                    print(f"{player.name}'s total score: {player.score}")
                    self.switch_player()
                    break

    def is_winner(self):
        """Check if any player has won the game by reaching 100 or more points."""
        return any(player.score >= 100 for player in self.players)

    def start_game(self):
        """Start and run the game until one player wins."""
        print("Welcome to the game of Pig!")

        while not self.is_winner():
            self.play_turn()

        winner = max(self.players, key=lambda p: p.score)
        print(f"Congratulations {winner.name}, you won with a score of {winner.score}!")


class TimedGameProxy(Game):
    def __init__(self, player1, player2):
        super().__init__(player1, player2)
        self.start_time = time.time()  # Record the game start time

    def play_turn(self):
        """Override play_turn to include time check."""
        if time.time() - self.start_time > 60:
            print("Time's up!")
            self.declare_winner()
            return
        
        # Otherwise, play as normal
        super().play_turn()

    def declare_winner(self):
        """Declare the player with the highest score as the winner."""
        winner = max(self.players, key=lambda p: p.score)
        print(f"Time's up! The winner is {winner.name} with {winner.score} points.")


def main():
    parser = argparse.ArgumentParser(description="Play Pig Game")
    parser.add_argument('--player1', choices=['human', 'computer'], required=True, help="Type of player 1")
    parser.add_argument('--player2', choices=['human', 'computer'], required=True, help="Type of player 2")
    parser.add_argument('--timed', action='store_true', help="Play timed game (1 minute limit)")
    
    args = parser.parse_args()

    # Create players using the PlayerFactory
    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")

    # Start a timed game or a regular game based on the --timed flag
    if args.timed:
        game = TimedGameProxy(player1, player2)
    else:
        game = Game(player1, player2)
    
    game.start_game()


if __name__ == "__main__":
    random.seed(0)  # Ensures consistent random rolls for testing
    main()
