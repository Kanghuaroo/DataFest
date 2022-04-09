class NPC():
    def __init__(self, model, args):
        self.model = model
        #from dataSheet
        self.unique_id = args.get('id')
        self.args = args

        self.connections = set()
        self.sentiment = 0
        self.rank = "Not Sure"
    
    def printout(self):
        print(self.unique_id)
        print("Connections: ", self.connections)
        print("Sentiment: ", self.sentiment)
        print("Rank: ", self.rank)

    def getID(self):
        return self.unique_id

    def getData(self):
        output = list()
        vals = ['data0Text', 
                'data1Text', 
                'data2text', 
                'data3Text']

        for i in vals:
            if self.args.get(i):
                if type(self.args.get(i)) == type('str'):
                    output.append(self.args.get(i))
        
        return output

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

    def getInvolved(self):
        return self.args.get('peopleInvolved')
    
    def getInvite(self):
        return self.args.get("inviteText")
