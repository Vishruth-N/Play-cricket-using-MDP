import random,argparse,sys
import sys
parser = argparse.ArgumentParser()
import pulp
import numpy as np
class plan_my_MDP():
    def __init__(self,mdp,policy_file,algorithm):
        mdpLines = open(mdp,'r').readlines()         #READING MDP FILE
        for x in range(len(mdpLines)):
            mdpLines[x] = mdpLines[x].strip()
        for line in mdpLines:
            mlines=line.split()
            if mlines[0]=='numStates':
                self.nOfStates=int(mlines[1])           #number of States
            elif mlines[0]=='transition':
                a=int(mlines[2])
                s=int(mlines[1])
                r=float(mlines[4])
                p=float(mlines[5])
                snxt=int(mlines[3])
                self.Transition[s,snxt,a]=p
                self.Reward[s,snxt,a]=r
            elif mlines[0]=='numActions':
                self.nOfActions=int(mlines[1])           #number of actions
                self.Reward=np.zeros([self.nOfStates,self.nOfStates,self.nOfActions])          #reward matrix for transitions
                self.Transition=np.zeros([self.nOfStates,self.nOfStates,self.nOfActions])          #probability matrix for transitions
            elif mlines[0]=='discount':
                self.discount=float(mlines[1])
            elif mlines[0]=='mdptype':
                self.mdptype=mlines[1]

        if policy_file==None:

            if algorithm=="vi":
                self.vi()
            elif algorithm=='hpi':
                self.hpi()
            elif algorithm=='lp':
                self.lp()
        else: 
            with open(policy_file, 'r') as f:
                read_policy = f.readlines()
            self.pi= []
            policylines=[]
            for x in read_policy:
                policylines.append(x.strip())
            for y in policylines:
                self.pi.append(int(y))
            self.PE()


    def vi(self):
        actions = np.arange(0,self.nOfActions) 
        States = np.arange(0,self.nOfStates) 
        pi = [0 for s in States]   
        V = [0 for s in States]

        delta=0.00000001
        optimal_policy_found=False

        while optimal_policy_found==False:
            psi=0
            for s in States:
                v=V[s]
                maximumValue=V[s]
                for a in actions:                        
                    value = 0
                    for s_next in States:
                        value += self.Transition[ s,s_next, a] * (self.Reward[s,s_next,a] +(self.discount * V[s_next]))  
                    if value>maximumValue :
                        maximumValue=value
                        pi[s]=a
                V[s]= maximumValue
                psi=max(psi, abs(V[s]- v))

            if psi<delta:
                
                for z in range(self.nOfStates):
                    #print(V[z],pi[z])
                    sys.stdout.write( str(V[z])+ ' ' + str(pi[z]) + "\n")
                optimal_policy_found=True
        return 0

    def hpi(self):
        actions = np.arange(0,self.nOfActions) 
        States = np.arange(0,self.nOfStates) 
        # Set policy iteration parameters
        maximumPolicyIterations = 9999  # Maximum number of policy iterations
        maxValueIterations = 9999  # Maximum number of value iterations
        delta=0.00000001
        pi = []
        V = []
        for s in States:
            V.append(0)
            pi.append(0)

        for i in range(maximumPolicyIterations):
            optimal_policy_found = True
            for j in range(maxValueIterations):
                max_diff = 0 
                for s in States:
                    value = 0
                    for s_next in States:
                        value += (0+(self.discount * V[s_next])+self.Reward[s,s_next,pi[s]]) * self.Transition[s,s_next,pi[s]] * 1 # Add discounted downstream values
                    # Update maximum difference
                    max_diff = max(abs(value - V[s]), max_diff,-1)
                    V[s] = value  # Update value with highest value
                # If diff smaller than threshold delta for all States, algorithm terminates
                if  not max_diff >= delta:
                    break

            # Policy iteration
            # With updated state values, improve policy if needed
            for s in States:
                maximumValue = V[s]
                for a in actions:
                    value = 0
                    for s_next in States:
                        value += self.Transition[s, s_next,a] * (self.Reward[s,s_next,a] +( self.discount * V[s_next])) # Add discounted downstream values
                    # Update policy if (i) action improves value and (ii) action different from current policy
                    if ( pi[s] != a ) and  value > maximumValue :
                        optimal_policy_found = False
                        maximumValue = value
                        pi[s] = a
                        
                        

            # If policy did not change, algorithm terminates
            if optimal_policy_found:
                for z in range(self.nOfStates):
                    sys.stdout.write( str(V[z])+ ' ' + str(pi[z]) + "\n")
                    with open('value_and_policy_file.txt',"a") as p:
                        p.write(str(V[z])+ ' ' + str(pi[z]) + "\n")
                break    
        


    def lp(self):
        States = np.arange(0,self.nOfStates) 
        delta=0.01
        actions = np.arange( 0,self.nOfActions) 
        pi = []
        for s in States:
            pi.append(0)
        pb=pulp.LpProblem("MDP_planning", pulp.LpMaximize)
        V=list()
        for i in range(len(States)):
            #print(i)
            V.append(pulp.LpVariable(str(i)))

        
        
        pb +=  -sum(V)
        for s in States: #looping through initial States
            for a in actions : # looping through the actions 
                value=0   #initialising value to 0
                for s_next in States: #looping through the States for the final state
                    value += 1 * ( self.Reward[ s,s_next, a] +(self.discount* V[ s_next])) *self.Transition[s,s_next,a]     # Value function calculation
                pb += V[s]>= value #update probabilty

        pb.solve( pulp.PULP_CBC_CMD( msg=False ))
        maximumValuefun=[]
        for k in V:
            maximumValuefun.append( pulp.value(k))
        for s in States: #looping through initial States
                for a in actions :  # looping through the actions 
                    value =  0 #initialising value to 0
                    for s_next in States: #looping through the States for the final state
                        value +=self.Transition[s, s_next,a] *( self.Reward[s,s_next,a]+(self.discount *maximumValuefun[s_next])) # Value function calculation
                    
                    if abs( maximumValuefun[ s ]-value)<delta :
                        pi[s]= a

                        break
        
        for z in range(self. nOfStates):  

            sys.stdout.write( str(V[z] )+ ' ' + str(pi[z]) + "\n")         
            with open('value_and_policy_file.txt',"a") as p:
                p.write(str(maximumValuefun[z])+ ' ' + str(pi[z]) + "\n")

    def PE(self):
        States = np.arange(0,self.nOfStates) 
        V = []
        for s in States:
            V.append(0)
        limitOfIterations=99999
        delta=0.000000001

        for j in range(limitOfIterations):
            max_diff = 0  
            for s in States:

                
                value = 0
                for s_next in States:
                    value += self.Transition[s,s_next,self.pi[s]] * (self.Reward[s,s_next,self.pi[s]] +(self.discount * V[s_next]))  
                # Update maximum difference
                max_diff = max(max_diff, abs(value - V[s]))

                V[s] = value  
            
            if (max_diff) < delta:
                break

        for z in range(self.nOfStates):            
            sys.stdout.write( str(V[z])+ ' ' + str(self.pi[z]) + "\n")



        return 0


parser.add_argument("--mdp",type=str,default="/host/code/data/cricket/cricketmdp.txt")
parser.add_argument("--algorithm",type=str,default="hpi")
parser.add_argument("--policy",type=str)
args = parser.parse_args()
if not (args.algorithm=="vi" or args.algorithm=="hpi" or args.algorithm=="lp"):
    print("Invalid argument for algorithm")
    sys.exit(0)
algo = plan_my_MDP(args.mdp,args.policy,args.algorithm)
sys.exit()