class NPC():
    def __init__(self, model, args):
        self.model = model
        #from dataSheet
        self.unique_id = args.get('id')
        self.args = args

        self.connections = set()
        self.sentiment = 0
        self.rank = 3
    
    def printout(self):
        print(self.unique_id)
        print("Connections: ", self.connections, ", ", self.getConnectionValue())
        print("Sentiment: ", self.sentiment)
        print("Rank: ", self.convertRank())

    def getID(self):
        return self.unique_id

    def getData(self):
        output = list()
        vals = ['data0Text', 
                'data1Text', 
                'data2Text', 
                'data3Text']

        for i in vals:
            if self.args.get(i):
                if type(self.args.get(i)) == type('str'):
                    output.append(self.args.get(i))
        
        return output
    
    def convertRank(self):
        #index = rank
        conversion = ["Bad News", 
                "Not Sure", "Seems OK", 
                "Good Friends", "Best Friends"]

        return conversion[self.rank]

    def setSentiment(self, s):
        self.sentiment = s

    def addConnection(self, person_id):
        self.connections.add(person_id)

    def getConnectionValue(self):
        if len(self.connections) == 0:
            return self.sentiment

        total = 0
        for i in self.connections:
            npc_score = self.model.npcs[i].sentiment
            total = total + npc_score
        avg = total / len(self.connections)
        return avg

class Invitation():
    def __init__(self, model, args):
        self.model = model
        #from dataSheet
        self.unique_id = args.get('id')
        self.args = args

        #connections = who is going
        self.connections = 0
        #sentiment = what I feel about the event
        self.sentiment = 0
        #answer = am I going? True or False
        self.answer = False

    def setSentiment(self, s):
        self.sentiment = s

    def setConnection(self, c):
        self.connections = c

    def getInvolved(self):
        return self.args.get('peopleInvolved')
    
    def getInvite(self):
        return self.args.get("inviteText")
