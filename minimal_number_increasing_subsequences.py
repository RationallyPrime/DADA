import sqlite3
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy import stats
con = sqlite3.connect("/Users/RationallyPrime/Downloads/2012_10.db")

mycursor = con.cursor()

mycursor.execute("select height, timestamp, extranonce, ispatoshi from blocks where height < 22000 and ispatoshi = 1;")

results = np.asarray(mycursor.fetchall(),dtype=float)
results = results.astype((int))


height = results[:,0]
timestamp = results[:,1]
extranonce = results[:,2]
ispatoshi = results[:,3]
update = True
seq_counter = 2
while update:
    update = False
    curr = 0
    for i in range(1,len(height)):
        if results[i,3] != 1:   #These are currently part of some other increasing subsequence
            pass
        else:
            if extranonce[i] > curr:
                curr = extranonce[i]
                results[i,3] = seq_counter
                update = True
    for i in range(1,len(height)-50):   #Moves incorrectly tagged blocks to a more proper subsequence
        if results[i,3] == seq_counter and seq_counter > 1:
            if extranonce[i] < extranonce[i+1] and extranonce[i-1] < extranonce[i]:
                results[i+1,3] = seq_counter

    seq_counter += 1


extranonce_deltas = []
timestamp_deltas = []
k = 2
while k < 17500:
    if k == 1400:   #I know this looks fishy, but it's actually to cut out the period where he runs two miners
        k = 1917    #There is a huge number of timestamp deltas lower than 300 seconds because of that
    while results[k,3] == results[k+1,3]:
        e_delta = results[k+1,2]-results[k,2]
        t_delta = results[k+1,1]-results[k,1]
        if e_delta < 30 and e_delta > 0 and t_delta < 2500 and t_delta > 0: #Play with these values adjust outlier inclusion
            extranonce_deltas.append(e_delta)
            timestamp_deltas.append(t_delta)
        k+=1
    else:   #while-else to jump over those rare adjacent non-Satoshi blocks
        k+=1

r_value = stats.spearmanr(timestamp_deltas,extranonce_deltas)
plt.scatter(timestamp_deltas,extranonce_deltas,label = "correlation "+ str(r_value[0]))
plt.xlabel("t_deltas")
plt.ylabel("extranonce deltas")
plt.legend(loc = 'upper right')
plt.show()
print(stats.spearmanr(timestamp_deltas,extranonce_deltas))











