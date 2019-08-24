
###############################################################
#Downloads all mods (names/author/URL/description)
#Page count needs to be updated as mods get added to CurseForge
###############################################################

from bs4 import BeautifulSoup
import requests
import sqlite3

print('Downloading all CurseForge Mods for Minecraft\n' + '-' * 20 + '\n')

class MCMod:
    def __init__(self, modName, modAuthor, modURL, modDesc):
        self.modName = modName
        self.modAuthor = modAuthor
        self.modURL = 'https://www.curseforge.com' + modURL
        self.modDesc = modDesc
    

def main():
    modResults = []
    for i in range(1,600): #Page number in curseforge
        results = getSoup(i)
        modResults = modResults + getModsFromSearchPage(results)
        print(f'========Page {i}/599 Saved========')
    writeSQL(modResults)


def writeSQL(modResults):
    sql_create_table = """ CREATE TABLE IF NOT EXISTS Mods (
                                        name text PRIMARY KEY,
                                        author text,
                                        url text,
                                        desc text
                                    ); """  
    
    conn = sqlite3.connect('CurseForgeMods.db')
    c = conn.cursor()
    c.execute(sql_create_table)
    for mod in modResults:
        c.execute('INSERT OR IGNORE INTO Mods VALUES (?,?,?,?)', [mod.modName, mod.modAuthor, mod.modURL, mod.modDesc])
    conn.commit()
    conn.close() 


def getSoup(page):
    result = requests.get(f'https://www.curseforge.com/minecraft/mc-mods?filter-sort=3&page={page}')
    src = result.content
    soup = BeautifulSoup(src, 'html.parser')
    results = soup.find_all('div', class_='project-listing-row box py-3 px-4 flex flex-col lg:flex-row lg:items-center')
    return results

def getModsFromSearchPage(results):
    modResults = []
    for modReturn in results:      
        modName = modReturn.find('h3')
        if not modName == None:     
            modName = modName.text
            modURL = modReturn.find('a').attrs['href']
            modDesc = modReturn.find('p', class_='text-sm leading-snug').text.strip()
            modAuthor = modReturn.find('a', class_='text-base leading-normal font-bold hover:no-underline my-auto').text
            ModObject = MCMod(modName, modAuthor, modURL, modDesc)
            modResults.append(ModObject)   
    return modResults
 
   
if __name__ == "__main__":
    main()