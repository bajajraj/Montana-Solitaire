
###############################################################################
#This assignment focuses on the design, implementation and testing of a \     #
#Python program which uses control structures to solve the problem described\ # 
#for the assignment. The project tests the ability to lists, manipulation of \# 
#classes, use of while, if, and for loop.                                      #
#                                                                             #
###############################################################################

#DO NOT DELETE THESE LINES
import cards, random
random.seed(100) #random number generator will always generate 
                 #the same random number (needed to replicate tests)


def initialize():
    '''
        This function creates, initializes, and returns the tableau. 
        Tableau is a list of 4 lists, each list containing 13 cards.
        
        parameters:
            None
            
        return: 
            Tableau: data structure representing the tableau 
    '''
    mydeck = cards.Deck() #calling Deck class
    mydeck.shuffle()      #shuffling the deck
    tableau = [[],[],[],[]]
    row = 0
    for index in range(52):
        mydeal = mydeck.deal() #dealing the deck
        tableau[row].append(mydeal)
        if len(tableau[row]) == 13: #length of each row not to exceed 13
            row += 1
    return tableau    
        

def display(tableau):
    '''
        This function displays the current state of the game.
        It display four rows of 13 cards with row and column labels.
        Ace is displayed with a blank.
        
        parameters: 
            tableau: data structure representing the tableau 
        
        Returns: None
    '''

    print("{:3s} ".format(' '), end = '')
    for col in range(1,14):
        print("{:3d} ".format(col), end = '')
    print()
        
    for r,row_list in enumerate(tableau):
        print("{:3d}:".format(r+1), end = '')
        for c in row_list:
            if c.rank() == 1:
                print("  {}{}".format(' ',' '), end = '')
            else:
                print("{:>4s}".format(str(c)),end = '')
        print()

def validate_move(tableau, source_row, source_col, dest_row, dest_col):
    '''
        The function returns True, if the move is valid; and False, otherwise.
        
        parameter:
            Tableau: data structure representing the tableau 
            source_row, source_col, dest_row, dest_col = integers
            
        return: Boolean
    '''
    
    #checking that the parameters are coorect
    if source_row < 0 or source_row > 3:
        return False
    if dest_row < 0 or dest_row > 3:
        return False
    if source_col < 0 or source_col > 12:
        return False
    if dest_col < 0 or dest_col > 12:
        return False
    
    source = tableau[source_row][source_col] #cards source location
    destination = tableau[dest_row][dest_col] #cards destination location
    if destination.rank() != 1: #if destination is not empty
        return False
    
    if dest_col == 0 and source.rank() == 2: #if the source cards is not 2 for leftmost column
        return True
    
    destination_2 = tableau[dest_row][dest_col - 1]
    if destination_2.rank() == 1:
        return False
    #to check that the left card is of the same suit and one less than source card
    if destination_2.suit() == source.suit() and source.rank() - destination_2.rank() == 1: 
        return True
    
    return False
    
def move(tableau,source_row,source_col,dest_row,dest_col):
    '''
       If the move is valid, this function will update the tableau.
       It will return True; otherwise, it will do nothing to it and return False.
       
       parameter:
           tableau: data structure representing the tableau 
           source_row, source_col, dest_row, dest_col = integers
           
       return: Boolean
    '''
    #if move is validate
    if validate_move(tableau,source_row,source_col,dest_row,dest_col): 
        source = tableau[source_row][source_col]
        destination = tableau[dest_row][dest_col]
        #updating the tableau
        tableau[dest_row][dest_col] = source
        tableau[source_row][source_col] = destination
        return True
    return False
  
def shuffle_tableau(tableau):
    '''
        This function shuffles the card in the valid way and will also update \
        the tableau.
        
        parameter:
            tableau = data structure representing the tableau 
            
        return: None
    '''
    #part 1 = extract the cards from the tableau and put aces and the remaining card in different lists
    #part 2 = remove all the aces from the shuffle
    #part 3 = put all the cards back in tableau
    ace_cards = []
    rem_cards = []
    for j,row in enumerate(tableau):
        i = 0
        while i < len(row):
            card = row[i]
            if i > 0:
                previous_card = row[i-1]
                #checking the condition for having 2 in leftmost column and subsequent series
            if (i == 0 and card.rank() == 2) or (i > 0 and previous_card.rank() == card.rank() - 1 and\
                previous_card.suit() == card.suit()):
                i += 1
                continue
            else: #adding cards to the list which needs to be shuffles
                rem_cards.extend(row[i:])
                tableau[j] = row[:i]
                break
            
    random.shuffle(rem_cards) #shuffling the required cards
    
    #for adding the ace cards
    for value in rem_cards:
        if value.rank() == 1:
            ace_cards.append(value)
    for k in ace_cards:
        rem_cards.remove(k)
    
    i = 1
    
    for index in tableau:
        length = len(index)
        add_length = 13 - length - 1
        card = ace_cards[i-1]
        index.append(card)
        i += 1
        index.extend(rem_cards[:add_length])
        rem_cards = rem_cards[add_length:]
    
    
    

def check_win(tableau):
    '''
        This function checks that the game is won and all the rules are followed\
        and returns True: otherwise, False.
        
        parameter:
            tableau = data structure representing the tableau 
            
        return: Boolean
    '''
    
    for row in tableau:
        for i,m in enumerate(row):
            if i == 0 and m.rank() != 2: #if leftmost cards is not 2
                return False
            if i == 12 and m.rank() != 1: #if rightmost card is not 1
                return False
            #if the series is followed
            if 0 < i < 12 and m.rank() - row[i-1].rank() != 1:
                return False
            #if the suit is same
            if m.suit() != row[i-1].suit() and 0 < i < 12:
                return False
                
    return True
            
             
def main():
    '''
         Main function to ask for input and call other functions.
    '''
    
    choice_words = "Enter choice:\n (q)uit, (s)huffle, or space-separated: source_row,source_col,dest_row,dest_col: "
    alpha = initialize()
    print("Montana Solitaire.")
    display(alpha)
    shuffles = 2 #maximum number of shuffles
    again = 'y'
    while again == 'y':
        
        choice = input(choice_words)
        
        #Option 1 = shuffling the cards
        if choice == 's':
                if shuffles:
                    shuffle_tableau(alpha)
                    display(alpha)
                    shuffles = shuffles - 1 #1 chance of shuffling gone
                else:
                    print("No more shuffles remain.")
                    
        #Option 2 = quiting the game        
        elif choice == 'q' or choice == 'Q':
            q_choice = input("Do you want to play again (y/n)?").lower()
            if q_choice == 'y':
                print("Montana Solitaire.")
                beta = initialize()
                display(beta)
                continue
            else:
                print("Thank you for playing.")
                break
        
        #Option 3 = playing the move    
        elif choice != 'q' or choice != 'Q':
                try: #to make sure that the numbers are integers
                    s_row, s_col, d_row, d_col = [int(num) for num in choice.split()]
                
                except:
                    #If choice is not q, s, or 4 integers separated by space
                    print("Error: invalid input.  Please try again.")
                    
                else:
                    #for making compatible with python
                    s_row = s_row - 1
                    s_col = s_col - 1
                    d_row = d_row - 1
                    d_col = d_col - 1
                    #if number is incorrect
                    if not ((s_row in range(4)) and (d_row in range(4)) and \
                            (s_col in range(13)) and (d_col in range(13))):
                        print("Error: row and/or column out of range. Please Try again.")
                        continue
                    
                    if validate_move(alpha, s_row, s_col, d_row, d_col):
                        if move(alpha, s_row, s_col, d_row, d_col):
                            display(alpha)
                            if check_win(alpha):
                                print("You won!")
                                print()
                                check_input = input("Do you want to play again (y/n)?").lower()
                                if check_input == 'y':
                                    print("Montana Solitaire.")
                                    beta = initialize()
                                    display(beta)
                                    continue
                                else:
                                    print("Thank you for playing.")
                                    break
                            else:
                                continue
                        else:
                            print("Error: invalid move.  Please try again.")
                            continue
                    else:
                        print("Error: invalid move.  Please try again.")
                        continue
        
        #If incorrect option is entered                
        else:
            print("Error: invalid move.  Please try again.")
            continue
    
    
    
    

if __name__ == "__main__":
    main() 

