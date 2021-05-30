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
curr_index = 0
while update:
    update = False
    curr = 0

    for i in range(1,len(height)):

        if results[i,3] != 1:
            pass
        else:
            if extranonce[i] > curr:# and extranonce[i] - curr < 20:
                curr = extranonce[i]
                curr_index = i
                results[i,3] = seq_counter
                update = True
    for i in range(1,len(height)-50):
        if results[i,3] == seq_counter and seq_counter > 1:
            if extranonce[i] < extranonce[i+1] and extranonce[i-1] < extranonce[i]:
                results[i+1,3] = seq_counter

#            if extranonce[i] < extranonce[i-1] and extranonce[i-1] < extranonce[i+1] and results[i-1,3] != results[i+1,3]:
#                j = i+1
#                k = results[i+1,3]
#                p = results[i-1,3]
#                while results[j,3] == k:
#                    results[j,3] = p
#                    j += 1
    seq_counter += 1


extranonce_deltas = []
timestamp_deltas = []
k = 2
while k < 17500:
    if k == 1400:
        k = 1917
    while results[k,3] == results[k+1,3]:
        e_delta = results[k+1,2]-results[k,2]
        t_delta = results[k+1,1]-results[k,1]
        if e_delta < 30 and e_delta > 0 and t_delta < 2500 and t_delta > 0:
            extranonce_deltas.append(e_delta)
            timestamp_deltas.append(t_delta)
        else:
            print(results[k-1,:],results[k,:],results[k+1,:])
        k+=1
    else:
        k+=1
print(len(extranonce_deltas))
r_value = stats.spearmanr(timestamp_deltas,extranonce_deltas)
plt.scatter(timestamp_deltas,extranonce_deltas,label = "correlation "+ str(r_value[0]))
plt.xlabel("t_deltas")
plt.ylabel("extranonce deltas")
plt.legend(loc = 'upper right')
plt.show()
print(max(extranonce_deltas))
print(stats.spearmanr(timestamp_deltas,extranonce_deltas))
'''

for i in range(2,len(height)):
    if extranonce[i] > extranonce[i-1] and extranonce[i-1] > extranonce[i-2] and results[i,3] != results[i-1,3]:
        results[i,3] = results[i-1,3]

new_results = np.array(results[np.argsort(results[:,3],kind = "stable")])
print(len(new_results))
'''



'''
index_list = []
for element in new_results[:,3]:
    index_list.append(element)
print(len(new_results))

for i in range(2,max(new_results[:,3])):
    start = index_list.index(i)
    while new_results[start,2] < new_results[start+1,2]:
        #print(new_results[start+1,2]-new_results[start,2],new_results[start+1,3],new_results[start,3])
        if new_results[start+1,0]-new_results[start,0] < 25 and new_results[start+1,1]-new_results[start,1] < 3000:
            extranonce_deltas.append(new_results[start+1,2]-new_results[start,2])
            timestamp_deltas.append(new_results[start+1,1]-new_results[start,1])
        start += 1
'''







