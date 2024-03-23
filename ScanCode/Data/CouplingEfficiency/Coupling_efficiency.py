data = [
    [1724666, 1843451, 11663],
    [482531, 611641, 1015],
    [710880, 2403986, 5001],
    [1691005, 2495838, 7480],
    [114465, 153563, 18],
    [25185, 30133, 130],
    [43000,34000,200]
]
for item in data:
    print("Coupling efficiency of 1st coupler", item[2] / item[0] * 100)
    print("Coupling efficiency of 2st coupler", item[2] / item[1] * 100)
