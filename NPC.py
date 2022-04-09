class NPC():
    def __init__(self, args):
        #from dataSheet
        self.unique_id = args.get('id')
        self.args = args

        self.connections = list()
        self.rank = "Not Sure"

    def addConnections(self, person_id):
        self.connections.append(person_id)

