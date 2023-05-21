#Valorant Instalock Tool created by Curtis Buckingham (https://github.com/CurtisBuckyy)
from tkinter import *
import ttkbootstrap as tb
from valclient.client import Client
import threading
import json

root = tb.Window(themename="main")
root.title("Valorant Instalock Tool") 
root.geometry("550x800+685+140") 
root.resizable(False, False) 
root.iconbitmap("logo.ico") 

agent_names = []
runningFlag = True
instaLockComplete = False

with open('agents.json', 'r') as data:
    agents = json.load(data)
    agents = agents['agents']
    
sorted_dict = {key: value for key, value in sorted(agents.items())}

for key in sorted_dict:
    agent_names.append(key.capitalize())
    
def enableComboBoxes():
    agentSelectorCboBox['state'] = 'readonly'
    selectRegion['state'] = 'readonly'
    
def loadRegionDataFile():
    with open('region.txt', 'r') as f:
        region = f.read()
        
    return region
    
def removeLabels():
    infoMessage2.pack_forget()
    
def writeRegion(regionChoice):
    regionChoice = selectRegion.get()
    
    msg = f"Region ({regionChoice}) saved"
    infoMessage2.config(text=msg)
    infoMessage2.config(anchor="center")
    infoMessage2.pack(pady=20)
    infoMessage2.after(2000, removeLabels)

    with open('region.txt', 'w') as f:
        f.write(regionChoice.lower())
        
    return regionChoice

def cancelInstaLock():
    global instaLockComplete
    instaLockComplete = True
    
    enableComboBoxes()
    
    cancelLockBtn.pack_forget()
    infoMessage.config(text="")
    
def executeInstaLock(agentChoice):
    
    region = loadRegionDataFile()
    agentChoiceCapitalized = agentChoice.capitalize()
    
    cancelLockBtn.pack(pady=40)
    
    try:
        client = Client(region=region)
        client.activate()
        
        infoMessage3.pack_forget()
        
        matchFoundFlag = client.fetch_presence(client.puuid)['sessionLoopState']
        
        while instaLockComplete == False:
            
            agentSelectorCboBox['state'] = 'disabled'
            selectRegion['state'] = 'disabled'
            
            matchFoundFlag = client.fetch_presence(client.puuid)['sessionLoopState']
        
            message = f"You have picked Agent ({agentChoiceCapitalized}): Status: Ready for Queue!"
            infoMessage.pack_forget()
            infoMessage.config(text=message)
            infoMessage.pack()
            
            if (matchFoundFlag == "PREGAME"):
                try:
                    client.pregame_select_character(agents[agentChoice])
                    client.pregame_lock_character(agents[agentChoice])
                    
                    enableComboBoxes()
                    
                    cancelLockBtn.pack_forget()

                    infoMessage.pack_forget()
                    infoMessage.pack(pady=40)
                    infoMessage.config(text= "Agent Locked Successfully!")
                    root.mainloop()
                    
                except:
                    pass
                
            root.update()
    except:
        infoMessage3.pack(pady=40)
        cancelLockBtn.pack_forget()

def selectAgent(agentChoice):
    global runningFlag
    runningFlag = True
    
    infoMessage.pack_forget()
    infoMessage2.pack_forget()
    
    if runningFlag == True:
        global instaLockComplete
        instaLockComplete = False
        agentChoice = agentSelectorCboBox.get().lower()
        thread = threading.Thread(target=executeInstaLock(agentChoice))
        thread.daemon = True 
        thread.start()
        
frame = tb.Frame(master=root)
frame2 = tb.Frame(master=root)
frame2.pack(pady=40)

softwareLogo = PhotoImage(file = "logo.png")
softwareLogoLabel = Label(frame2, image=softwareLogo)
softwareLogoLabel.pack()

cancelLockBtn = tb.Button(master=frame2, text="Stop Instalock Execution", command=cancelInstaLock, style="danger", cursor="hand2", padding=15)
infoMessage = tb.Label(frame2, text = "", width=400, anchor="center")
infoMessage.pack()

agentSelectorCboBox = tb.Combobox(frame2, textvariable="Select an Agent", font=("Arial", -18), state='readonly', values=agent_names, 
                                  bootstyle="primary", )
agentSelectorCboBox.set("Select an agent")
agentSelectorCboBox.pack(pady=40)
agentSelectorCboBox.bind("<<ComboboxSelected>>", selectAgent)

region = loadRegionDataFile()

selectRegion = tb.Combobox(frame2, font=("Arial", -18), state='readonly', values=['EU', 'NA', 'LATAM', 'AP', 'BR', 'KR', 'PBE'], 
                           width=10, bootstyle="primary")
selectRegion.set(region.upper())
selectRegion.pack(pady=10)
selectRegion.bind("<<ComboboxSelected>>", writeRegion)

infoMessage2 = tb.Label(frame2, text = "", width=400, anchor="center")
infoMessage2.pack()

infoMessage3 = tb.Label(frame2, text = "Please launch Valorant and try again at main menu!", width=400, font=("Arial", -18), 
                        anchor="center", foreground="red")

root.mainloop()