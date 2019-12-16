import os

pc = 500
rc = 500
fc = 150

mv = 10.0
mh = 0.5
ms = 2.0

sens = 300

try:
    while True:
        print 'lo'
except Exception as e:
    print e
finally:
    os.system('echo "' + str(pc) + ' '+str(rc)+' '+str(fc)+' '+str(mv)+' '+str(mh)+' '+str(ms)+' '+str(sens)+'" >> long-term-output.txt')
    print pc
    print rc
    print fc
    print mv
    print mh
    print ms
    print sens
    input('enter')