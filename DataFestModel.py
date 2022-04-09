import time
import re
import numpy as np
import pandas as pd
from NPC import *

def buildNPCs(f):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make NPC
        npc = NPC(df.iloc[i].to_dict())
        output.append(npc)

    return output


def buildInvites(f):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make Invite
        invite = Invitation(df.iloc[i].to_dict())
        output.append(invite)

    return output

class Model():
    def __init__(self, npc_file, invite_file):
        self.npcs = buildNPCs(npc_file)
        self.invites = buildInvites(invite_file)

    def formConnections(self):
        for i in self.npcs:
            msg = i.getData()
            for m in msg:
                match = re.findall("\[\w*\]", m)
                for npc in match:
                    unique_id = int(npc[4:-1])
                    #for bidirectional conneciton
                    i.addConnection(unique_id)
                    self.npcs[unique_id].addConnection(i.getID())

    def formSentiment(self):
        #TODO add better sentiment analysis
        #check to see how "good" a person is based on 
        #their messages
        
        #currently only checks to see if banned words are said

        bannedWords = ["beer", 'drinking', 'wasted',
                'drunk', 'trashed', 'smoking', 'smoke',
                'weed', 'alcohol', 'bullying', 'pot',
                'cigs', 'cigarettes', 'green']

        for i in self.npcs:
            msg = i.getData()
            flag = True
            for m in msg:
                for word in bannedWords:
                    if m.find(word) == -1:
                    #say bad word == you bad person
                        i.setSentiment(0)
                        flag = False
            if flag:
                i.setSentiment(1)
            

    def formRank(self):
        #if I am a bad person or know a bad person
        # I am "Bad News"
        pass

def main():
    m = Model("files/NPCGeneration.xlsx", 
            "files/InviteGeneration.xlsx")
    #check what friends each person has
    m.formConnections()
    #check data for what person they are
    m.formSentiment()
    #form an opinion based on Connection & Sentiment
    #can weight each one differently
    m.formRank()

    #TODO Later
    #Send an Invite through the system

    return m

if __name__ == "__main__":
    main()
