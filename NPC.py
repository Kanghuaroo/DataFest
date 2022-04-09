class NPC():
    def __init__(self, args):
        #from dataSheet
        self.unique_id = args.get('id')
        self.args = args

        self.connections = list()
        self.rank = "Not Sure"
    
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

    def addConnections(self, person_id):
        self.connections.append(person_id)

class Invitation():
    def __init__(self, args):
        self.unique_id = args.get('id')
        self.args = args

    def getInvolved(self):
        return self.args.get('peopleInvolved')
    
    def getInvite(self):
        return self.args.get("inviteText")
