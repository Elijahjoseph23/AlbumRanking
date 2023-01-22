import json
#----------------------------------------------------------------------------------------------------------------------
#Initialized the AR and AA json
class Initialize:
    def rtf_to_json(filename):
        """"
        converts a rich text file to a json file. 
        Proper Format for the rtf:
        <Album Name>- <score> (<Artist> and <OtherArtist>)
        *make sure each album is on a seperate line
        """
        AR={}
        AA={}
        with open(filename,"r") as file:
            c=0
            for line in file:
                if c>=8:
                    if c==8: 
                        line=line[14:]
                    album=line.strip().split("-")[0]
                    s=int(line.strip().split("-")[1].split("(")[0].strip())
                    temp=line.strip().split("-")[1].split("(")[1]
                    artist=temp[0:len(temp)-2]
                    album=album.replace("'91","'")
                    album=album.replace("\'92","'")
                    album=album.replace("'93","'")
                    album=album.replace("'94","'")
                    album=album.replace("\\","")
                    album=album.replace("'85","...")
                    album=album.replace("'85","...")
                    artist=artist.replace("'91","'")
                    artist=artist.replace("'92","'")
                    artist=artist.replace("'93","'")
                    artist=artist.replace("'94","'")
                    artist=artist.replace("\\","")
                    artist=artist.replace("'85","...")
                    artist=artist.replace("'85","...")
                    artist=artist.split("and")
                    AR[album]=s
                    AA[album]=tuple(artist)
                c+=1
        with open("AlbumRanking.json", "w") as f:
            json.dump(AR, f, indent=4)
        with open("AlbumArtist.json", "w") as f:
            json.dump(AA,f,indent=4)

    def discography(AA):
        Discog={}
        for album in AA.keys():
            for x in range(len(AA[album])):
                if AA[album][x].strip().title() in Discog:
                    Discog[AA[album][x].strip().title()]=tuple(list(Discog[AA[album][x].strip().title()])+[album])
                else:
                    Discog[AA[album][x].strip().title()]=tuple([album])
