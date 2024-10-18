import random
import time

sukien_lists = ["skGapNhau", "skhanhphuc", "skkethon", "skSinhConDauLong", "skTuoiGia"]
sukien_lists1 = ["skngoaitinh", "skmuasam", "skmaymua", "skToTinh", "skchiatay"]
sukien_lists2 = ["skConLapGiaDinh", "skSinhConThuHai", "sknym"]
sukien_lists3 = [
    "sklyhon",
    "skmuasam",
    "skmaymua",
    "skchiatay",
    "skngoaitinh",
    "skaocuoi",
]
sukien_lists4 = ["skvohoacchongchettruoc", "skchaunoi"]


# ,'noel2','noel3','noel4','noel5','noel6','noel7','noel8','noel9','noel10'
# SkDudoancontuonglai
def skgendata():
    list_gen_sk = []
    random.seed(time.time())
    random_sk = random.sample(sukien_lists, 1)
    random_sk1 = random.sample(sukien_lists1, 1)
    random_sk2 = random.sample(sukien_lists2, 1)
    random_sk3 = random.sample(sukien_lists3, 1)
    random_sk4 = random.sample(sukien_lists4, 2)
    print("SU KIEN 1 - " + str(random_sk))
    print("SU KIEN 2 - " + str(random_sk1))
    print("SU KIEN 3 - " + str(random_sk2))
    print("SU KIEN 4 - " + str(random_sk3))
    print("SU KIEN 5 - " + str(random_sk4))
    list_gen_sk.append(random_sk[0])
    list_gen_sk.append(random_sk1[0])
    list_gen_sk.append(random_sk2[0])
    list_gen_sk.append(random_sk3[0])
    list_gen_sk.append(random_sk4[0])
    list_gen_sk.append(random_sk4[1])
    return list_gen_sk


def skgendatangam():
    list_gen_sk = []
    list_gen_sk.append(sukien_lists[3])
    random.seed(time.time())
    random_sk2 = random.choice(sukien_lists2)
    list_gen_sk.append(random_sk2)
    list_gen_sk.append(sukien_lists[4])
    random.seed(time.time())
    random_sk3 = random.choice(sukien_lists4)
    list_gen_sk.append(random_sk3)
    return list_gen_sk


def skgendatanoel():
    list_gen_sk = []
    list_gen_sk.append(sukien_lists5)
    return list_gen_sk
