import os
from time import sleep
import random

pc = 500
rc = 500
fc = 150

mv = 10.0
mh = 0.5
ms = 2.0

sens = 300

try:
    while True:
        print str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)
        active = True
        while active:
            try:
                f1 = open("training1/info.txt")
                f2 = open("training2/info.txt")
                f3 = open("training3/info.txt")
                f4 = open("training4/info.txt")
                f5 = open("training5/info.txt")
                f1.close()
                f2.close()
                f3.close()
                f4.close()
                f5.close()
                dtag = 0
                drabbit = 0
                dfox = 0
                for i in range(1, 6):
                    with open('training' + str(i) + '/info.txt') as f:
                        tag = 0
                        rabbit = 0
                        fox = 0
                        for line in f:
                            if 'neuerTag' in line:
                                line = line.split(' ')
                                tag = lin[1]
                                if line[2] > fox:
                                    fox = line[2]
                                if line[3] > rabbit:
                                    rabbit = line[3]
                        dtag += float(tag) / float(5)
                        dfox += float(fox) / float(5)
                        drabbit += float(rabbit) / float(5)
                fittness = dtag
                if drabbit > 2000:
                    fittness -= abs(drabbit - 2000)
                if dfox > 2000:
                    fittness -= abs(dfox - 2000)
                
                abweichung = float(4000 - fittness) / float(10000)

                mv += mv *float((random.random() - 0.5) * 2) * float(abweichung)
                mh += mh*float((random.random() - 0.5) * 2) * float(abweichung)
                ms += ms*float((random.random() - 0.5) * 2) * float(abweichung)

                sens += sens*float((random.random() - 0.5) * 2) * float(abweichung)

                for i in range(5):
                    print('python2.7 ecosimulation.py -o training -c 10000 -pc 500 -rc 500 -fc 150 -mv '+str(mv)+' -mh '+str(mh)+' -ms '+str(ms)+' -sens '+str(sens))
                # Do something with the file
            except IOError:
                print("File not accessible")
            except KeyboardInterrupt:
                active = False
                pass
            else:
                f1.close()
                f2.close()
                f3.close()
                f4.close()
                f5.close()
            sleep(1)
except Exception as e:
    print e
finally:
    print str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)
    os.system('echo "' + str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)+'" >> long-term-output.txt')