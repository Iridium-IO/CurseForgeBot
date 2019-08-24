
###############################################################
#Debug console outputs for CurseForgeBot
#Not necessary for normal function
###############################################################

def Version(version_Numeral):
    print(f'CurseForgeBot v{version_Numeral}\n' + '-' * 10)

def Authenticated(username):
    print(bcolors.HEADER + f"Authenticated as {username}\n" + bcolors.ENDC)

def BuildingResponse(number_mods, comment_id):
     print(bcolors.OKGREEN + f'Building Response for {number_mods} mod(s) on comment {comment_id}:' + bcolors.ENDC)

def AlreadyCommented(comment_id):
    print(bcolors.WARNING + f'Already Commented on {comment_id}' + bcolors.ENDC)

def ResponseSubmitted():
    print(bcolors.OKGREEN + 'Response Submitted\n' + bcolors.ENDC)

def ResponseFailed():
    print(bcolors.FAIL + 'Failed to submit response\n' + bcolors.ENDC)

def ModFound(searchName, foundName):
    print(bcolors.OKGREEN + '| ' + bcolors.ENDC + f'- {searchName}: {foundName}')  

def ModNotFound(searchName):
    print(bcolors.FAIL + '| '  + f'- {searchName}: No result found' + bcolors.ENDC)    

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
