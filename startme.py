from art import tprint
from db import *
from gen import *
from process import tournament_flow
from tabulate import tabulate
tprint('T O U R N A M E N T \nM A N A G E M E N T', font = 'rounded')



def start():
    """ main funciton for the execution of the program """

    #Checks the dbs for proper functioning of the code
    check_db_setup()

    #Continues the menu selection infintely untill the user stops
    while True:
        option = menu()

        if not option:
            break #Stops the program if no input is given

        if option == 1:
            list_all_tournaments()

        elif option == 2:
            start_tournament()

        elif option == 3:
            display_all_winners()

        elif option == 4:
            tournament_info()

        elif option == 5:
            delete_tournament_info()

        elif option == 0:
            break



#Displays menu for the project
def menu():
    """ prints all data for the avaiable options """

    seperator(3)

    tprint('Menu', font = 'small')
    print('Enter the respective numbers to select the option! \nEnter 0 to quit.')
    print("""
    \t1. Show all Tournaments.
    \t2. Start new tournament.
    \t3. Check winners of all tournaments.
    \t4. Get a tournament's info
    \t5. Delete a tournament's data""")

    return get_num_input("\nSelected: ")
    seperator(n2 = 1)



#Option 1: Lists all tournaments that has been completed
def list_all_tournaments():
    """ prints tabulate form of all tournaments and it's data """

    seperator()
    tprint('DATA', font = 'rounded')
    print(tabulate(fetch('data', 'tournament_data'), ['S.No.', 'Name', 'Winner ID', 'Winner', 'Total Teams'], "pretty"))



#Option 2: Displays all the winners from every tournament
def display_all_winners():
    """ prints tabulate form of all tournaments' winners """

    seperator()
    tprint('WINNERS', font = 'rounded')
    print(tabulate(fetch('data', 'tournament_data', 'SNo, tournament_name, winner'), ['S.No.', 'Name', 'Winner'], "pretty"))



#Starts a new torunament
#Just calls the main function on process.py file.
def start_tournament():
    """ starts new tournament calls the `tournament_flow` function from `process.py` """

    seperator(2)
    tprint('NEW TOURNAMENT', font = 'rounded')
    winner, tournament_name = tournament_flow()
    seperator(2, 2)
    tprint(f'Winner of \n{tournament_name}   is...\n{winner}', font = 'small')



#Displays every info avaiable from a single tournament
#INFO: Teams, Players, Round info, Winner
def tournament_info():
    """ displays info about a given tournament """

    seperator()
    print("Avaiable tournaments")
    print(tabulate(fetch('data', 'tournament_data'), ['S.No.', 'Name', 'Winner ID', 'Winner', 'Total Teams'], "pretty"))

    while True:
        tournament_name = input('Enter the name of the tournament you want to get info.\nType "cancel" to stop! \n\nTournament: ')

        if tournament_name in show_dbs():
            break

        elif tournament_name.lower() == 'cancel':
            return print("Canceled getting tournament info! ")

        print(f"Cannot find tournament '{tournament_name}', maybe you've miss spelled it!\nTry again!")

    tprint('TOURNAMENT    INFO', font = 'rounded')
    print('\n\n')
    tprint('TEAMS', font = 'small')
    print(tabulate(fetch('teams', tournament_name), ['ID', 'NAME', 'WINS', 'LOSS'], "pretty"))

    print('\n\n')
    tprint('Players', font = 'small')
    print(tabulate(fetch('players', tournament_name), [x.upper() for x in ['ID', 'Name'] + get_member_col([], 2).split(",")[1:]], "pretty"))

    rounds = [i for i in get_all_tables(tournament_name) if i.startswith('round_')]
    for table in rounds:
        print('\n\n')
        tprint((table.upper()).replace('_', '   '), font = 'small')
        print(tabulate(fetch(table, tournament_name, 'match_id, team1_name, team2_name, win_name'), ['Match ID', 'Team 1', 'Team 2', 'Winner'], "pretty"))



#Removes a tournament's info
def delete_tournament_info():
    """ deletes all data for a tournament """

    seperator()
    print("Avaiable tournaments")
    print(tabulate(fetch('data', 'tournament_data'), ['S.No.', 'Name', 'Winner ID', 'Winner', 'Total Teams'], "pretty"))

    while True:
        tournament_name = input('Enter the name of the tournament you want to delete.\nType "cancel" to stop! \n\nTournament: ')

        if tournament_name in show_dbs():
            break

        elif tournament_name.lower() == 'cancel':
            return print("Canceled deleting tournament! ")

        print(f"Cannot find tournament '{tournament_name}', maybe you've miss spelled it!\nTry again!")

    if fetch('data', 'tournament_data', condition = f'WHERE tournament_name = "{tournament_name}"'):
        delete_row('data', 'tournament_data', condition = f'tournament_name = "{tournament_name}"')

    delete_db(tournament_name)

    print(f'Deletion successful! \nRemoved all data of "{tournament_name}" tournament!')




#-------------------------------------------
#Misc functions for checking database status
#-------------------------------------------


#Creates main DB | Setup
def create_data_tb():
    """ creates table/db for the storing all tournament's info """

    seperator()
    print('initial setup...\n')

    create_db('tournament_data')
    create_table('data',
    """SNo INT AUTO_INCREMENT PRIMARY KEY,
    tournament_name VARCHAR(60) UNIQUE NOT NULL,
    winner_id INT,
    winner VARCHAR(30),
    total_teams INT""",
    'tournament_data')

    print('Setup Completed!')
    seperator()



#Checks for DB
def check_db_setup():
    """ checks if the main db exists """

    #Checks for the data DB for storing tournament data
    if db_existance('tournament_data'):
        return

    #Checking whether any Tournaments has been conducted
    #If not it's the first time opening the pgm, so start setup process
    dbs = show_dbs()
    create_data_tb()

    if not dbs:
        return

    repair_data_tb()



#Repairs Data in the main database
def repair_data_tb():
    """ recreates the main db with it's tables """

    all_dbs = show_dbs() #Gets all tournaments as list
    all_dbs.remove('tournament_data') #Removing the db from the tournament dbs

    #Geting all the tournaments record filled in the data table
    existing_dbs = [x[0] for x in fetch('data', 'tournament_data', 'tournament_name')]

    dbs = set(all_dbs) - set(existing_dbs)

    #Adds all the old tournaments record to the tournament_data DB if the table is deleted or changed.
    for db in dbs:
        data = fetch('winner', 'x')[0][:2] + (len(fetch('teams', 'x', 'team_id')),)
        insert('data', 'tournament_data',
        "tournament_name, winner_id, winner, total_teams",
        f"'{db}', {data[0]}, '{data[1]}', {data[2]}")



start()
