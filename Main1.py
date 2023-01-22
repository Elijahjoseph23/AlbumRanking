
import tkinter
import json
import math
import pandas as pd
import gspread
import df2gspread as d2g
import customtkinter as tk
AR={} #"""Albums Ranking List"""
AA={} #Albums corresponding artist
Discog={}
with open("AlbumRanking.json","r") as f:
    source1=f.read()
with open("AlbumArtist.json", "r") as f2:
    source2=f2.read()
AR=json.loads(source1)
AA=json.loads(source2)
for album in AA.keys():
    for x in range(len(AA[album])):
        if AA[album][x].strip().title() in Discog:
           Discog[AA[album][x].strip().title()]=tuple(list(Discog[AA[album][x].strip().title()])+[album])
        else:
            Discog[AA[album][x].strip().title()]=tuple([album])
#Methods
#-------------------------------------------------------------------------------------------------------------------
def totalAverage():
    a=0
    for score in AR.values():
        a+=int(score)
    a=a/len(AR.values())
    print("The average album rating is: "+str(round(a,2)))

def preAddAlbum():
    def submit_album():
        album = e1.get()
        artist = e2.get()
        score = e3.get()
        print(f"{album} by {artist} is now in the database!")
        add.destroy()
        addAlbum(album, artist, score)
    add=tk.CTk()
    add.title("Enter an Album")
    frame=tk.CTkFrame(master=add)
    frame.pack(pady=20,padx=50,fill="both",expand=True)
    l1=tk.CTkLabel(frame,text="Album Name:")
    e1=tk.CTkEntry(frame)
    l2=tk.CTkLabel(frame,text="Artist:")
    e2=tk.CTkEntry(frame)
    l3=tk.CTkLabel(frame,text="Score:")
    e3=tk.CTkEntry(frame)
    l1.pack()
    e1.pack()
    l2.pack()
    e2.pack()
    l3.pack()
    e3.pack()
    b5=tk.CTkButton(add,text="Enter",command=submit_album)
    b5.pack(pady=10)
    add.mainloop()
    
def addAlbum(album,artist,score):
    album=album.strip()
    aList=[]
    if "and" in artist:
        for x in artist.split("and"):
            aList+=[x.strip()]
    else:
        AR[album]=(score)
        AA[album]=[artist]
    if artist in Discog:
        Discog[artist]=tuple(list(Discog[artist])+[album])
    else:
        Discog[artist]=tuple([album])
    update()

  
def averageScore(artist="%atp%"):
    def getArtist():
        a=e1.get()
        print(averageScore(a))
    if artist=="%atp%":
        avg=tk.CTk()
        avg.title("Enter an Artist")
        frame=tk.CTkFrame(master=avg)
        frame.pack(pady=20,padx=50,fill="both",expand=True)
        l1=tk.CTkLabel(frame,text="Artist Name:")
        e1=tk.CTkEntry(frame)
        l1.pack()
        e1.pack()
        b1=tk.CTkButton(avg,text="Enter",command=getArtist)
        b1.pack(pady=10)
        avg.mainloop()
    else:
        artist=artist.title()
        if artist in Discog:
            d=Discog[artist]
            total=0
            for album in d:
               total+=int(AR[album])
            return str(artist)+": "+str(round(total/len(Discog[artist]),1))
        else:
            return 0

def scoreList(artist="%atp%"):
    def getArtist():
        a=e1.get()
        print("Here are "+a+"'s scores"+":")
        avg.destroy()
        scoreList(a)
    if artist=="%atp%":
        avg=tk.CTk()
        avg.title("Enter an Artist")
        frame=tk.CTkFrame(master=avg)
        frame.pack(pady=20,padx=50,fill="both",expand=True)
        l1=tk.CTkLabel(frame,text="Artist Name:")
        e1=tk.CTkEntry(frame)
        l1.pack()
        e1.pack()
        b1=tk.CTkButton(avg,text="Enter",command=getArtist)
        b1.pack(pady=10)
        avg.mainloop() 
    else:
        sl=[]
        for album in Discog[artist]:
            sl+=[[album,AR[album]]]
        sort=sorted(sl,key= lambda x:int(x[1]),reverse=True)
        for a in sort:
            print(a[0]+":"+str(a[1]))
              
def listRank(n=-600):
    def getRank():
        a=e1.get()
        listRank(int(a))
    if n==-600:
        avg=tk.CTk()
        avg.title("Get All Scores")
        frame=tk.CTkFrame(master=avg)
        frame.pack(pady=20,padx=50,fill="both",expand=True)
        l1=tk.CTkLabel(frame,text="Score:")
        e1=tk.CTkEntry(frame)
        l1.pack()
        e1.pack()
        b1=tk.CTkButton(avg,text="Enter",command=getRank)
        b1.pack(pady=10)
        avg.mainloop() 
    else:
        print("Here are all the albums that have a score of "+str(n)+":")
        for album in AR.keys():
            if AR[album]==n:
                print(album+":", end=" ")
                for artist in AA[album]:
                    print(artist, end=" ")
                print()
            
def maxScore():
    def avg(artist):
        if artist in Discog:
            d=Discog[artist]
            total=0
            for album in d:
               total+=int(AR[album])
        return total/len(Discog[artist])
    m=0
    maxArtist=""
    for artist in Discog.keys():
        if avg(artist)>m:
            m=avg(artist)
            maxArtist=artist
    print("The artist with the highest average score is", maxArtist,"("+str(m)+")")

def stats():
    rank=[0,0,0,0,0,0,0,0,0,0,0]
    for s in AR.values():
        rank[int(s)]+=1
    print("Album Score Distribution: ")
    print("___________________________________")
    scores=0
    for r in rank:
        if scores<10:
            print(str(scores)+": ",(round(r/len(AR.values())*100))*"■",str(round(r/len(AR.values())*100,2))+"%")
        else:
            print(str(scores)+":",(round(r/len(AR.values())*100))*"■",str(round(r/len(AR.values())*100,2))+"%")
        scores+=1

def changeRank(album="%none%",n=-1):
    def albumEntered():
        a=e1.get()
        b=e2.get()
        changeRank(a,b)
    if album=="%none%":
        q=tk.CTk()
        q.title("Update")
        frame=tk.CTkFrame(master=q)
        frame.pack(pady=20,padx=50,fill="both",expand=True)
        l1=tk.CTkLabel(frame,text="Enter the album name:")
        l1.pack()
        e1=tk.CTkEntry(frame)
        e1.pack()
        l2=tk.CTkLabel(frame,text="Enter the new album score:")
        l2.pack()
        e2=tk.CTkEntry(frame)
        e2.pack()
        b1=tk.CTkButton(q,text="Enter",command=albumEntered)
        b1.pack(pady=10)
        q.mainloop()
    else:
        if not album in AR.keys():
            print("No album exists in the database")
        else:
            AR[album]=n
            print(f"Done! {album} by {AA[album]} is now a {n} out of 10!")
        
def update():
    with open("AlbumRanking.json", "w") as f:
        json.dump(AR, f, indent=4)
    with open("AlbumArtist.json", "w") as f:
        json.dump(AA,f,indent=4)
    with open("Discography.json","w") as f:
        json.dump(Discog,f,indent=4)

def createPanda():
    dataset={"Artist":AA.values(),"Score":AR.values()}
    chart=pd.DataFrame(dataset,index=AA.keys())
    print(chart)
#----------------------------------------------------------------------------------------------------------------------
#Gui
def closeWindow():
    window.destroy()
    quit()
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
window=tk.CTk()
window.geometry("400x425")
frame=tk.CTkFrame(master=window)
frame.pack(pady=20,padx=50,fill="both",expand=True)
window.title("Menu")
TAbutton = tk.CTkButton(frame, text="Find the total average",command=totalAverage)
ADDbutton=tk.CTkButton(frame, text="Add an album",command=preAddAlbum)
ArtistAveragebutton=tk.CTkButton(frame, text="Find an artist's average score",command=averageScore)
SLbutton=tk.CTkButton(frame, text="Find an artist's album scores",command=scoreList)
LRbutton=tk.CTkButton(frame, text="List all albums of a certain score",command=listRank)
MSbutton=tk.CTkButton(frame, text="Find the artist with the highest average score",command=maxScore)
Sbutton=tk.CTkButton(frame, text="Statistics",command=stats)
EditAlbumbutton=tk.CTkButton(frame,text="Change an Album's Score",command=changeRank)
label = tk.CTkLabel(frame, text="What do you want to do?")
label.pack(pady=5,padx=8)
Sbutton.pack(pady=5,padx=8)
ADDbutton.pack(pady=5,padx=8)
ArtistAveragebutton.pack(pady=5,padx=8)
SLbutton.pack(pady=5,padx=8)
LRbutton.pack(pady=5,padx=8)
MSbutton.pack(pady=5,padx=8)
TAbutton.pack(pady=5,padx=8)
EditAlbumbutton.pack(pady=5,padx=8)
close=tk.CTkButton(window,text="Exit",command=closeWindow)
close.pack(pady=5)
window.mainloop()








