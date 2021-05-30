import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
con = sqlite3.connect("/Users/RationallyPrime/Downloads/2012_10.db")

mycursor = con.cursor()

mycursor.execute("select height, timestamp, nonce, extranonce from blocks where ispatoshi = 1 limit 18000;")

results = np.asarray(mycursor.fetchall())
con.close()
height = results[:,0]
timestamp = results[:,1]
nonce = results[:,2]
extranonce = results[:,3]
integer_distribution = np.zeros((10,10)) #niður svo til hliðar
print(timestamp[-1])
def decimal_nonce(nonce):
    for s in nonce:
        i = int(s,16)
        rev = str(i)[::-1]
        for i in range(0,len(rev)):
            temp = int(rev[i])
            integer_distribution[i,temp] += 1 #fyrra sætið er staðsetning seinna sætið er gildið í nonce

def hex_nonce(nonce):
    hex_distribution = np.zeros((256,1))
    for s in nonce:
        lsb = int(s[0:2],16)
        hex_distribution[lsb] += 1

    return hex_distribution
numbers = [i for i in range(0,59)]
hex_distribution = hex_nonce(nonce)

hypothesis_sums = [sum(hex_distribution[0:5]),sum(hex_distribution[5:10]),sum(hex_distribution[19:24]),sum(hex_distribution[24:29]),sum(hex_distribution[29:34]),sum(hex_distribution[34:39]),sum(hex_distribution[39:44]),sum(hex_distribution[44:49]),sum(hex_distribution[49:54]),sum(hex_distribution[54:59])]
leng = [i for i in range(len(hypothesis_sums))]
r_1 = stats.binom_test(hypothesis_sums[1],hypothesis_sums[0]+hypothesis_sums[1], alternative='greater')
r_2 = stats.binom_test(hypothesis_sums[3],hypothesis_sums[2]+hypothesis_sums[3],alternative='greater')
r_3 = stats.binom_test(hypothesis_sums[5],hypothesis_sums[4]+hypothesis_sums[5],alternative='greater')
r_4 = stats.binom_test(hypothesis_sums[7],hypothesis_sums[6]+hypothesis_sums[7],alternative='greater')
r_5 =  stats.binom_test(hypothesis_sums[9],hypothesis_sums[8]+hypothesis_sums[9],alternative='greater')
r_all = stats.binom_test(sum(hypothesis_sums[1::2]),sum(hypothesis_sums),alternative='greater')
print(r_1,r_2,r_3,r_4,r_5,r_all)

for entry in hypothesis_sums:
    print(entry[0])
count = 0
restarts = 0
for i in range(1,18000):
    if int(extranonce[i])-int(extranonce[i-1]) == 1:
        count += 1
    if int(extranonce[i]) < int(extranonce[i-1]):
        restarts += 1

print("adjacent extra nonce values: ",count)
print("number of restarts: ",restarts)

'''
plt.plot(numbers,hex_distribution[0:59])
plt.show()
print_list = zip(list(hex_nonce(nonce)),numbers)
for entry in print_list:
    print(entry)
#print(integer_distribution)
#for i in range(0,100):
 #   print(extranonce[i])
'''