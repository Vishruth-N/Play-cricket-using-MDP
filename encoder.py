import random,argparse,sys
parser = argparse.ArgumentParser()
import numpy as np
import sys

class encoder():
    def __init__(self,playp,states,q):
        #Reading Player parameters
        with open(playp) as f:
            plines = f.readlines()
        #removing new line characters
        plines = [x.strip() for x in plines]
        self.q = float(q)
        self.p = float((1-self.q)/2)
        self.aA = [0,1,2,4,6] #List of actions the batsman A can take
        self.aB = [1] #List of actions the batsman B can take
        self.oB = [-1,0,1] #List of outcomes for B
        self.pB = [self.q, self.p, self.p] #Probability matrix for B
        self.oA = [-1,0,1,2,3,4,6] #List of outcomes for A
        self.AR = np.zeros([len(self.aA),len(self.oA)]) #Action Outcome Matrix
        for pline in plines:
            pline_lst = pline.split()
            if pline_lst[0] != "action":
                prob = pline_lst[1:]
                for i in range(len(prob)):
                    self.AR[self.aA.index(int(pline_lst[0])),i] = prob[i]
        #Reading list of states
        with open(states) as s:
            self.slines = s.readlines()
        #removing new line characters
        self.s_listAN = [(x.strip()+' A'+' N').split() for x in self.slines]   
        self.s_listBN = [(x.strip()+' B'+' N').split() for x in self.slines]
        self.s_listAO = [(x.strip()+' A'+' O').split() for x in self.slines]   
        self.s_listBO = [(x.strip()+' B'+' O').split() for x in self.slines]        
        self.s_list = self.s_listAN+self.s_listBN+self.s_listAO+self.s_listBO
        self.n = len(self.s_list)
        self.m = len(self.aA)
        self.T=np.zeros([self.n,self.m,self.n])          #probability matrix for transitions
        self.R=np.zeros([self.n,self.m,self.n])          #reward matrix for transitions
        self.endstates = []         
        self.escalc()
        self.transit()
        #self.prints()
            # for s2 in self.slines:
            #     bb2 = int(s2[0:2])
            #     rr2 = int(s2[2:4])
            #     diff = rr1 - rr2
            #     diffb = bb1 - bb2
            #     if(diff in o[1:] and rr1 > 0):
            #         if(diffb == 1):
            #             for i in a:
            #                 if(diff in ss):
            #                     self.T[self.slines.index(s1),a.index(i),self.slines.index(s2)] = self.AR[a.index(i),o.index(diff)]
            #                     if(rr2 == 0):
            #                         self.R[self.slines.index(s1),a.index(i),self.slines.index(s2)] = 1
        self.writefile()

    def prints(self):
        for x in self.endstates:
            print(self.s_list[x])
    def escalc(self):
        for s1 in self.s_list:
            bb1 = int(s1[0][0:2])
            rr1 = int(s1[0][2:4])
            if(rr1 == 0 or bb1 == 0 or s1[2] == 'O'):
                self.endstates.append(self.s_list.index(s1))
                continue
    
    
    def transit(self):
        for state in self.s_list:
            if(self.s_list.index(state) not in self.endstates):
                if(state[1] == 'A'):
                    for ac in self.aA:
                        for ouc in self.oA:
                            snxt = self.nxts(state, ouc)
                            self.T[self.s_list.index(state),self.aA.index(ac),self.s_list.index(snxt)] = self.AR[self.aA.index(ac),self.oA.index(ouc)]
                            if(int(snxt[0][2:4]) == 0):
                                self.R[self.s_list.index(state),self.aA.index(ac),self.s_list.index(snxt)] = 1
                elif(state[1] == 'B'):
                    for ouc in self.oB:
                        snxt = self.nxts(state, ouc)
                        if(ouc == -1):
                            self.T[self.s_list.index(state),1,self.s_list.index(snxt)] = self.q
                        elif(ouc in [0,1]):
                            self.T[self.s_list.index(state),1,self.s_list.index(snxt)] = self.p
                            if(int(snxt[0][2:4]) == 0):
                                self.R[self.s_list.index(state),1,self.s_list.index(snxt)] = 1




    def nxts(self, curs, ou):
        bbi = int(curs[0][0:2])
        bbf = bbi - 1
        rri = int(curs[0][2:4])
        strikei= curs[1]
        onout = curs[2]
        if(ou != -1):
            rrf = rri - ou
            if(rrf<0):
                rrf = 0
        elif(ou == -1):
            onout = 'O'
            rrf = rri
        strikef = strikei
        if((ou in [1,3] and bbi not in [6,12]) or (ou in [0,2,4,6] and bbi in [6,12])):
            if(strikei == 'A'):
                strikef = 'B'
            elif(strikei == 'B'):
                strikef = 'A'
        return(self.stategen(bbf,rrf,onout,strikef))


    def stategen(self, bb, rr, o, st):
        return [str(bb).zfill(2)+  str(rr).zfill(2), st, o]


    def writefile(self):
        with open("/host/code/data/cricket/cricketmdp.txt",'a') as cm:
            cm.write("numStates "+str(self.n)+"\n"+"numActions "+str(self.m)+"\n"+"end ")
            for i in self.endstates:
                cm.write(str(i) + " ")
            cm.write("\n")
            for i in range(self.n):
                for j in range(self.m):
                    for k in range(self.n):
                        if(self.T[i,j,k] != 0):
                            cm.write("transition " + str(i) + " " + str(j) + " " + str(k) + " " + str(self.R[i,j,k]) + " " + str(self.T[i,j,k]))
                            cm.write("\n")
            cm.write("mdptype episodic\ndiscount 1")





if __name__ == "__main__":
    parser.add_argument("--parameters",type=str,default="/host/code/data/cricket/sample-p2.txt")
    parser.add_argument("--states",type=str,default="/host/code/data/cricket/states.txt")
    parser.add_argument("--q",type=float,default=0.25)
    args = parser.parse_args()  
    param = encoder(args.parameters,args.states,args.q)
    sys.exit()