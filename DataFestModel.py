import time
import re
import numpy as np
import pandas as pd
from NPC import *

def buildNPCs(model, f):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make NPC
        npc = NPC(model, df.iloc[i].to_dict())
        output.append(npc)

    return output


def buildInvites(model, f):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make Invite
        invite = Invitation(model, df.iloc[i].to_dict())
        output.append(invite)

    return output

class Model():
    def __init__(self, npc_file, invite_file):
        self.npcs = buildNPCs(self, npc_file)
        self.invites = buildInvites(self, invite_file)
        self.bannedWords = ["beer", 'drinking', 'wasted',
                'drunk', 'trashed', 'smoking', 'smoke',
                'weed', 'alcohol', 'bullying', 'pot',
                'cigs', 'cigarettes', 'green']

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
    
    def formASentiment(self, i):
        #TODO add better sentiment analysis
        #check to see how "good" a person is based on 
        #their messages
        
        #currently only checks to see if banned words are said

        msg = i.getData()
        flag = True
        for m in msg:
            for word in self.bannedWords:
                if m.find(word) != -1:
                #say bad word == you bad person
                    flag = False
        if flag:
            i.setSentiment(1)
        else:
            i.setSentiment(0)

    def formSentiment(self):
        for i in self.npcs:
            self.formASentiment(i)
            
    def formRank(self):
        #if I am a bad person or know a bad person
        # I am "Bad News"
        connections_weight = 1
        sentiment_weight = 1
        threshold = .50

        for i in self.npcs:
            mean = (i.getConnectionValue() * connections_weight)
            mean += (i.sentiment * sentiment_weight)
            mean = mean / 2
            if mean < threshold:
                i.rank = 0
            else:
                i.rank = 4
    
    def analyzeInvite(self, invite):
        msg = invite.getInvite()
        flag = True
        for word in self.bannedWords:
            if msg.find(word) != -1:
                #bad word == bad event
                flag = False
        if flag:
            invite.setSentiment(1)
        else:
            invite.setSentiment(0)
    
    def analyzeInvites(self):
        for i in self.invites:
            self.analyzeInvite(i)

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
    m.analyzeInvites():

    return m

if __name__ == "__main__":
    main()
