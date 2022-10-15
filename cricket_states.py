import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--balls",required=False,type=str,help="Number of balls", default=15)
parser.add_argument("--runs",required=False,type=str,help="Runs to score", default=30)
args = parser.parse_args()
total_balls = int(args.balls)
score = int(args.runs)
for balls in range(total_balls+1):
    for runs in range(score+1):
        for player in range(1):
            #print(str(total_balls-balls).zfill(2)+  str(score-runs).zfill(2))
            with open('host/code/data/cricket/states.txt', 'a') as f:
                f.writelines(str(total_balls-balls).zfill(2)+  str(score-runs).zfill(2))
                f.write('\n')
