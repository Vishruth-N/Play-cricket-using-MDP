import random,argparse,sys
parser = argparse.ArgumentParser()
import numpy as np
import sys
import encoder

class decoder():
    def __init__(self,opolicy,states):
        self.act = [0,1,2,4,6]
        #Reading list of states
        with open(states) as s:
            self.slines = s.readlines()
        #removing new line characters
        self.s_listAN = [(x.strip()+' A'+' N').split() for x in self.slines]   
        self.s_listBN = [(x.strip()+' B'+' N').split() for x in self.slines]
        self.s_listAO = [(x.strip()+' A'+' O').split() for x in self.slines]   
        self.s_listBO = [(x.strip()+' B'+' O').split() for x in self.slines]        
        self.s_list = self.s_listAN+self.s_listBN+self.s_listAO+self.s_listBO
        #Reading policyfile
        with open(opolicy) as f:
            self.oplines = f.readlines()
        #removing new line characters
        self.oplines = [x.strip() for x in self.oplines]
        self.values = np.zeros(len(self.oplines))
        self.policies = np.zeros(len(self.oplines))
        for x in self.oplines:
            self.values[self.oplines.index(x)],self.policies[self.oplines.index(x)] = x.split(" ")
        self.writefin()


    def writefin(self):
        with open('policyfile.txt', "a") as f:
            for i in range(len(self.s_listAN)):
                if(self.slines[i][0:2] != '00' and self.slines[i][2:4] != '00'):
                    f.write(str(self.s_listAN[i][0]) + " " + str(self.act[int(self.policies[i])]) + " " + str(self.values[i]) + "\n")



if __name__ == "__main__":
    parser.add_argument("--value-policy",type=str,default="/host/code/data/cricket/value_and_policy_file.txt")
    parser.add_argument("--states",type=str,default="/host/code/data/cricket/states.txt")
    args = parser.parse_args()  
    param = decoder(args.value_policy,args.states)
    sys.exit()