import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
con = sqlite3.connect("Enter database here")

mycursor = con.cursor()

mycursor.execute("select height, timestamp, nonce, extranonce from blocks where ispatoshi = 1 limit 18000;")

results = np.asarray(mycursor.fetchall())
con.close()
height = results[:,0]
timestamp = results[:,1]
nonce = results[:,2]
extranonce = results[:,3]



def hex_nonce(nonce):
    hex_distribution = np.zeros((256))
    lsb_values = []
    for s in nonce:
        lsb = int(s[0:2],16)
        lsb_values.append(lsb)
        hex_distribution[lsb] += 1

    return hex_distribution,lsb_values

hex_distribution,hist_data = hex_nonce(nonce)
hypothesis_sums = [sum(hex_distribution[0:5]),sum(hex_distribution[5:10]),sum(hex_distribution[19:24]),sum(hex_distribution[24:29]),sum(hex_distribution[29:34]),sum(hex_distribution[34:39]),sum(hex_distribution[39:44]),sum(hex_distribution[44:49]),sum(hex_distribution[49:54]),sum(hex_distribution[54:59])]
plt.hist(hist_data,bins=128)
plt.xlabel("LSB Value")
plt.ylabel("Frequency")
plt.show()

r_1 = stats.binom_test(hypothesis_sums[1],hypothesis_sums[0]+hypothesis_sums[1], alternative='greater')
r_2 = stats.binom_test(hypothesis_sums[3],hypothesis_sums[2]+hypothesis_sums[3],alternative='greater')
r_3 = stats.binom_test(hypothesis_sums[5],hypothesis_sums[4]+hypothesis_sums[5],alternative='greater')
r_4 = stats.binom_test(hypothesis_sums[7],hypothesis_sums[6]+hypothesis_sums[7],alternative='greater')
r_5 =  stats.binom_test(hypothesis_sums[9],hypothesis_sums[8]+hypothesis_sums[9],alternative='greater')
r_all = stats.binom_test(sum(hypothesis_sums[1::2]),sum(hypothesis_sums),alternative='greater')
#Yeah, I know. This is terrible practice. I wouldn't do this at work.
print(r_1,r_2,r_3,r_4,r_5,r_all)

