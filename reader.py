import numpy as np

with open("/home/rihandsilva/Academic/CS747/Programming Assignment 2/data/mdp/episodic-mdp-2-2.txt") as f:
    content_list = f.readlines()
# remove new line characters
content_list = [x.strip() for x in content_list]
for line in content_list:
    line_lst=line.split()
    if line_lst[0]=='numStates':
        n=int(line_lst[1])
    elif line_lst[0]=='numActions':
        m=int(line_lst[1])
        T=np.zeros([n,m,n])
        R=np.zeros([n,m,n])
    elif line_lst[0]=='transition':
        s=int(line_lst[1])
        a=int(line_lst[2])
        snxt=int(line_lst[3])
        r=float(line_lst[4])
        p=float(line_lst[5])
        T[s,a,snxt]=p
        R[s,a,snxt]=r


print(T[1,1,0])
print(R[0,1,0])
print(np.arange(0,10))