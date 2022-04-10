import time
import re
import numpy as np
import pandas as pd
from NPC import *

def buildNPCs(model, f, sheetNum):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f, sheet_name=sheetNum)

    for i in range(df.shape[0]):
        #make NPC
        npc = NPC(model, df.iloc[i].to_dict())
        output.append(npc)

    return output


def buildInvites(model, f, sheetNum):
    #make this work with all frames
    output = list()
    df = pd.read_excel(f, sheet_name=sheetNum)

    for i in range(df.shape[0]):
        #make Invite
        invite = Invitation(model, df.iloc[i].to_dict())
        output.append(invite)

    return output

class Model():
    def __init__(self, npc_file, invite_file, sheetNum):
        print("Running level {0} data".format(sheetNum))
        self.npcs = buildNPCs(self, npc_file, sheetNum)
        self.invites = buildInvites(self, invite_file, sheetNum)
        self.bannedWords = ["beer", 'drinking', 'wasted',
                'drunk', 'trashed', 'smoking', 'smoke',
                'weed', 'alcohol', 'bullying', 'pot',
                'cigs', 'cigarettes', 'green', 'high']

    def npcConnections(self):
        for i in self.npcs:
            msg = i.getData()
            for m in msg:
                match = re.findall("\[\w*\]", m)
                for npc in match:
                    unique_id = int(npc[4:-1])
                    #for bidirectional conneciton
                    i.addConnection(unique_id)
                    self.npcs[unique_id].addConnection(i.getID())
    
    def npcSingleSentiment(self, i):
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

    def npcSentiment(self):
        for i in self.npcs:
            self.npcSingleSentiment(i)
            
    def npcRank(self):
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
    
    def inviteSentiment(self, invite):
        #TODO again, add better sentiment analysis
        #currently only checks if a 'bad word' is said

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
    
    def invitesSentiment(self):
        for i in self.invites:
            self.inviteSentiment(i)

    def invitesConnections(self):
        for i in self.invites:
            self.inviteConnections(i)

    def inviteConnections(self, invite):
        total = 0
        people = invite.getInvolved()
        people = str(people)
        people = people.split(',')
        for i in people:
            unique_id = int(i)
            total += self.npcs[unique_id].rank
        avg = total / len(people)

        if avg >= 2:
            #if avg sentiment of people if "Seems OK" or better then go
            invite.setConnection(1)
        else:
            invite.setConnection(0)
        
    def inviteAnswer(self):
        connections_weight = 1
        sentiment_weight = 1
        threshold = .5

        for i in self.invites:
            avg = i.connections * connections_weight
            avg += i.sentiment * sentiment_weight
            avg = avg /2
            if avg > threshold:
                i.answer = 1
            else:
                i.answer = 0

    def getInviteAnswers(self):
        output = list()
        for invite in self.invites:
            output.append(invite.answer)
        return output

    def run(self):
        #check what friends each person has
        self.npcConnections()
        #check data for what person they are
        self.npcSentiment()
        #form an opinion based on Connection & Sentiment
        #can weight each one differently
        self.npcRank()

        #TODO Later
        #Send an Invite through the system
        self.invitesSentiment()
        self.invitesConnections()
        self.inviteAnswer()

        return self.getInviteAnswers()

    def checkResults(self):
        wrongIDs = list()
        for i in self.invites:
            flag = i.args.get('safe') == i.answer
            if not flag:
                wrongIDs.append(i.unique_id)
        return len(wrongIDs) == 0, wrongIDs


def main():
    for i in range(10):
        m = Model("files/NPCGeneration.xlsx", 
                "files/InviteGeneration.xlsx", i)
        m.run()
        ans = m.checkResults()
        print(ans)

if __name__ == "__main__":
    main()
