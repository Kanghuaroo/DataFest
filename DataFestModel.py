import time
import numpy as np
import pandas as pd
from NPC import *

def buildNPCs(f):
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make NPC
        npc = NPC(df.iloc[i].to_dict())
        output.append(npc)

    return output


def buildInvites(f):
    output = list()
    df = pd.read_excel(f)

    for i in range(df.shape[0]):
        #make Invite
        invite = Invitation(df.iloc[i].to_dict())
        output.append(invite)

    return output
