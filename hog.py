"""CS 61A Presents The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.x
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    your_score = 0
    y = 0
    while num_rolls: 
        x = dice()
        if x != 1:
            your_score = your_score + x
        else: 
            y = 1
        num_rolls -= 1
    if y == 1:
        return 1 
    else:
        return your_score
    # END PROBLEM 1


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    if opponent_score < 10:
        your_score = opponent_score + 1
    else: 
        x, y = opponent_score % 10, opponent_score // 10
        y = y % 10 
        your_score = max(x, y) + 1
    return your_score

   # END PROBLEM 2


# Write your prime functions here!
def is_prime(your_score):
    if your_score == 1:
        return False
    else:
        d = 2
        while your_score > d:
            if your_score % d != 0:
                d += 1
            else:
                return False
        return True 

def next_prime(your_score):
    p = your_score + 1
    d = 2 
    while p > d:
        if p % d != 0:
            d += 1
        else: 
            p += 1
            d = 2
    return p

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    "*** REPLACE THIS LINE ***"
    if num_rolls == 0:
        your_score = free_bacon(opponent_score)
        if is_prime(your_score) == True:
            return next_prime(your_score)
        else: 
            return your_score
    else:
        your_score = roll_dice(num_rolls, dice)
        if is_prime(your_score) == True:
            return next_prime(your_score)
        else: 
            return your_score
        

    # END PROBLEM 2 


def select_dice(dice_swapped):
    """Return a six-sided dice unless four-sided dice have been swapped in due
    to Perfect Piggy. DICE_SWAPPED is True if and only if four-sided dice are in
    play.
    """
    # BEGIN PROBLEM 3
    "*** REPLACE THIS LINE ***"
    if dice_swapped == True:
        return four_sided 
    else: 
        return six_sided # Replace this statement
    # END PROBLEM 3


# Write additional helper functions here!
def perfect_square(turn_score):
    root = pow(turn_score, 1/2)
    root = int(root)
    return root*root == turn_score

def perfect_cube(turn_score):
    root = pow(turn_score, 1/3)
    root = int(root)
    return pow(root, 3) == turn_score 

def is_perfect_piggy(turn_score):
    """Returns whether the Perfect Piggy dice-swappiquitng rule should occur."""
    # BEGIN PROBLEM 4
    "*** REPLACE THIS LINE ***" 
    if turn_score == 1:
        return False 
    else: 
        return perfect_square(turn_score) == True or perfect_cube(turn_score) == True
        
    # END PROBLEM 4


def is_swap(score0, score1):
    """Returns whether one of the scores is double the other."""
    # BEGIN PROBLEM 5
    "*** REPLACE THIS LINE ***"
    if score0 != 0 and score1 != 0:
        return score0 / score1 == 2 or score1 / score0 == 2
    # END PROBLEM 5


def other(player):
    """Return the other player, for a player PlayER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0:     The starting score for Player 0
    score1:     The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    dice_swapped = False # Whether 4-sided dice have been swapped for 6-sided
    # BEGIN PROBLEM 6
    "*** REPLACE THIS LINE ***"
    while score0 < goal and score1 < goal:
        dice = select_dice(dice_swapped)
        if player == 0:
            num_rolls = strategy0(score0, score1)
            x = take_turn(num_rolls, score1, dice)
            score0 += x
            if is_swap(score0, score1) == True:
                score0, score1 = score1, score0
            if is_perfect_piggy(x) == True:
                if dice_swapped == False: 
                    dice_swapped = True
                else: 
                    dice_swapped = False
        else: 
            num_rolls = strategy1(score1, score0)
            x = take_turn(num_rolls, score0, dice)
            score1 += x
            if is_swap(score0, score1) == True:
                score0, score1 = score1, score0
            if is_perfect_piggy(x) == True:
                if dice_swapped == False: 
                    dice_swapped = True
                else:
                    dice_swapped = False
        player = other(player)
        

    # END PROBLEM 6
    return score0, score1


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert type(num_rolls) == int, msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the strategy
    returns a valid input. Use `check_strategy_roll` to raise an error with a
    helpful message if the strategy returns an invalid output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 7
    "*** REPLACE THIS LINE ***"
    score = 0
    opponent_score = 0
    y = 0 
    while y < goal:
        while score < goal and opponent_score < goal:
            num_rolls = strategy(score, opponent_score)
            check_strategy_roll(score, opponent_score, num_rolls)
            opponent_score += 1
        score += 1
        opponent_score = 0
        y += 1


    return None


    # END PROBLEM 7


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    "*** REPLACE THIS LINE ***"
    def average_value(*args): 
        total = 0
        x = 0 
        while x < num_samples:
            total += fn(*args)
            x += 1
        return total / num_samples
    return average_value

    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    "*** REPLACE THIS LINE ***"
    num_rolls = 1
    y = 0
    while num_rolls <= 10:
        x = make_averaged(roll_dice, num_samples = 1000)(num_rolls, dice)
        y = max(y, x)
        if x >= y:
            z = num_rolls
        num_rolls += 1
    return z 


    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    "*** REPLACE THIS LINE ***"
    x = free_bacon(opponent_score)
    if is_prime(x) == True:
        x = next_prime(x)
    if x >= margin: 
        return 0
    return num_rolls  # Replace this statement
    # END PROBLEM 10
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    "*** REPLACE THIS LINE ***"
    x = free_bacon(opponent_score)
    if is_prime(x) == True:
        x = next_prime(x)
    score += x
    if is_swap(score, opponent_score) == True:
        if score < opponent_score:
            return 0 
    if x >= margin:
        return 0
    return num_rolls # Replace this statement
    # END PROBLEM 11
check_strategy(swap_strategy)



def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** My strategy simply cycles through the possibilties of the swap strategy, making beneficial swaps more likely and causing unfavorable swaps to be less likely.  ***
    """
    # BEGIN PROBLEM 12
    "*** REPLACE THIS LINE *** "
    if score < opponent_score:
        if score >= 90 and opponent_score >= 90:
            x = bacon_strategy(score, opponent_score, margin = 10, num_rolls = 3)
        elif (score + 1) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 11, num_rolls = 10)
        elif (score + 2) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 10)
        elif (score + 3) * 2 == opponent_score or (score + 4) * 2 == opponent_score or (score + 5) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 1)
        elif (score + 6) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 2)
        elif (score + 7) * 2 == opponent_score or (score + 11) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 2)
        elif (score + 8) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 8, num_rolls = 2)
        elif (score + 9) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 9, num_rolls = 2)
        elif (score + 10) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 2)
        elif (score + 12) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 4)
        elif (score + 13) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 3)
        elif (score + 14) * 2 == opponent_score:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 4)
        else:
            x = swap_strategy(score, opponent_score, margin = 8, num_rolls = 4)
    else:
        y = (score / 2) - opponent_score 
        if score >= 90 and opponent_score % 10 == 9:
            x = bacon_strategy(score, opponent_score, margin = 10, num_rolls = 3)
        elif y == 1:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 1)
        elif y == 2:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 8)
        elif y == 3 or y == 4 or y == 5:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 7)
        elif y == 6:
            x = swap_strategy(score, opponent_score, margin = 10, num_rolls = 6)
        elif y == 7:
            x = swap_strategy(score, opponent_score, margin = 7, num_rolls = 4)
        elif y == 11:
            x = swap_strategy(score, opponent_score, margin = 1, num_rolls = 9)
        else:
            x = swap_strategy(score, opponent_score, margin = 6, num_rolls = 4) 
    return x
    # Replace this statement
    # END PROBLEM 12
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()