
###############################################################
#CurseForgeBot by ImminentFate
#Version 2.3
###############################################################

import praw, re, json, urllib, os, string
import FuzzyDBSearch
import CurseForgeBot_Debug as DebugS

DebugS.Version(2.2)

#u/ModdedPlayer's Curseforge API: https://www.reddit.com/r/feedthebeast/comments/9vj5nm/wip_curseforge_minecraft_mod_indexer_api/
APIURL = 'https://ddph1n5l22.execute-api.eu-central-1.amazonaws.com/dev/mods?mod_name='

#File to store IDs of comments that have already been replied to
commented_path = "commented.txt"


def main():
    if not os.path.exists(commented_path):
        open(commented_path, "w").close()
    reddit=authenticate()
    getComments(reddit)


def authenticate():
    reddit = praw.Reddit('curseforgebot')
    DebugS.Authenticated(reddit.user.me())
    return reddit


def getComments(reddit):
    for comment in reddit.subreddit('feedthebeast+mcmodfinder').stream.comments():
        resultsT = re.findall(r'\[\[(.*?)\]\]', comment.body.replace('\\',''))
         
        if len(resultsT) != 0:    
            file_obj_r = open(commented_path, "r")
            if comment.id not in file_obj_r.read().splitlines():

                CommentReply = ''
                DebugS.BuildingResponse(len(resultsT), comment.id)                   
                for match in resultsT:   
                    CommentReply = CommentReply + BuildCommentReply(match)
                try:
                    comment.reply(CommentReply + '*I am a bot that automatically tries to pull mod links from CurseForge.*')
                    DebugS.ResponseSubmitted
                except:
                    DebugS.ResponseFailed
                    file_obj_r.close() 
                else:
                    file_obj_r.close()
                    file_obj_w = open(commented_path, "a+")
                    file_obj_w.write(comment.id + "\n")
                    file_obj_w.close()        
            else:
                DebugS.AlreadyCommented(comment.id)
                

#Builds the reply comment for each individual mod. 
# Yeah I know I used multiple try-excepts. And they're nested. I hate myself. 
def BuildCommentReply(match):
    match = match.strip()
    match_nobracket = re.sub(r" ?\([^)]+\)", "", match)
    match_limitedpunctuation = re.sub(r'[^\w^.^-]', '',  match_nobracket)
    match_nopunctuation = match_nobracket.translate(str.maketrans('', '', string.punctuation)) 

    matchvariantList = [match, match_nobracket, match_limitedpunctuation, match_nopunctuation]  
    return TryLoop(0, matchvariantList)


#In each loop, it first starts with the raw match, then goes through
#each variant of the above matches until it succeeds or fails all.
#If it fails all, it will then try matching via Levenshtein distance  
#as a last resort, against a pre-downloaded database of all Curseforge mods. 
def TryLoop(iteration, matchType):
    if iteration == 4:
        mod_curseSearch = 'https://www.curseforge.com/minecraft/mc-mods/search?search=' + urllib.parse.quote(matchType[0])     
        
        FuzzySearch = FuzzyDBSearch.GetMatch(matchType[0])
        if not FuzzySearch is None:
            DebugS.ModFound(matchType[0], FuzzySearch[0])
            BuildResponse = f"**[{FuzzySearch[0]}]({FuzzySearch[2]})** by {FuzzySearch[1]}  \n **{FuzzySearch[3]}**  \n *Not the right mod? See search results for \'{matchType[0]}\' on [CurseForge]({mod_curseSearch})*\n\n---  \n"
            return(BuildResponse)

        DebugS.ModNotFound(matchType[0])
        BuildResponse = f"**{matchType[0]}**  \n Unable to find a match for this item.  \n*Search for this mod on [CurseForge]({mod_curseSearch}) instead*\n\n---  \n"     
        return(BuildResponse)

    try:
        with urllib.request.urlopen(APIURL + urllib.parse.quote(matchType[iteration])) as url:
            tdict = json.loads(url.read().decode())
            url.close()
            return(ParseJSON(tdict, matchType[iteration], matchType[0]))
    except:
        return TryLoop(iteration + 1, matchType)


#Builds the reply comment based on parsed JSON from the API
def ParseJSON(inputJSON, match, match_orig):
    index = 0
    for result in inputJSON['result']:
        if not result['name'].lower() == match_orig.lower():
            index = index + 1
            if len(inputJSON['result']) == index:
                index = 0
                break
        else:
            break

    moddata = inputJSON['result'][index]
    mod_name = moddata['name']
    mod_desc = moddata['blurb']
    mod_url = moddata['url']
    mod_author = moddata['owner']
    mod_curseSearch = 'https://www.curseforge.com/minecraft/mc-mods/search?search=' + urllib.parse.quote(match)

    DebugS.ModFound(match_orig, mod_name)
    BuildResponse = f"**[{mod_name}]({mod_url})** by {mod_author}  \n **{mod_desc}**  \n *Not the right mod? See search results for \'{match_orig}\' on [CurseForge]({mod_curseSearch})*\n\n---  \n"
    return(BuildResponse)


if __name__ == "__main__":
    main()
