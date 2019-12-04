
# global waters
# waters = []


# def water():
#     waters.append([[120, 70], [80, 60]])
#     waters.append([[1200, 700], [80, 60]])
#     waters.append([[520, 870], [100, 40]])
#     waters.append([[720, 200], [400, 700]])
#     if args.show:
#         for water in waters:
#             pygame.draw.rect(win, (0, 0, 255), (water[0][0], water[0][1], water[1][0], water[1][1]))


    # for water in waters:
    #     lbor = water[0][0]
    #     rbor = water[0][0] + water[1][0]
    #     tbor = water[0][1]
    #     bbor = water[0][1] + water[1][1]
    #     hborders = [tbor, bbor]
    #     vborders = [lbor, rbor]
    #     if ax >= water[0][0] and x <= water[0][0] + water[1][0]:
    #         if ay >= water[0][1] and y <= water[0][1] + water[1][1]:
    #             closest = [568656, None]

    #             for i in range(len(vborders)):
    #                 if abs(vborders[i] - x) < closest[0]:
    #                     closest = [abs(vborders[i] - x), i]

    #             for i in range(len(hborders)):
    #                 if abs(hborders[i] - y) < closest[0]:
    #                     closest = [abs(hborders[i] - y), i + 2]

    #             if closest[1] == 0:
    #                 x = water[0][0] -10
    #             if closest[1] == 1:
    #                 x = water[0][0] + water[1][0]
    #             if closest[1] == 2: 
    #                 y = water[0][1] - 10
    #             if closest[1] == 3:
    #                 y = water[0][1] + water[1][1]

        #self.thurst = -100


        # for water in waters:
        #     lbor = water[0][0]
        #     rbor = water[0][0] + water[1][0]
        #     tbor = water[0][1]
        #     bbor = water[0][1] + water[1][1]
        #     hborders = [tbor, bbor]
        #     vborders = [lbor, rbor]
        #     if ax >= water[0][0] and self.pos[0] <= water[0][0] + water[1][0]:
        #         if ay >= water[0][1] and self.pos[1] <= water[0][1] + water[1][1]:
        #             closest = [568656, None]

        #             for i in range(len(vborders)):
        #                 if abs(vborders[i] - self.pos[0]) < closest[0]:
        #                     closest = [abs(vborders[i] - self.pos[0]), i]

        #             for i in range(len(hborders)):
        #                 if abs(hborders[i] - self.pos[1]) < closest[0]:
        #                     closest = [abs(hborders[i] - self.pos[1]), i + 2]

        #             if closest[1] == 0:
        #                 self.pos[0] = water[0][0] -10
        #             if closest[1] == 1:
        #                 self.pos[0] = water[0][0] + water[1][0]
        #             if closest[1] == 2:
        #                 self.pos[1] = water[0][1] - 10
        #             if closest[1] == 3:
        #                 self.pos[1] = water[0][1] + water[1][1]


                #if self.target in waters:
                #   self.thurst -= 50


    '''def waterdistance(self, water):
        ax = self.pos[0]
        ay = self.pos[1]
        r = None
        if ax < water[0][0]:
            if ay < water[0][1]:
                #obere linke ecke
                r = water[0]
                d = self.distance(water[0])
            elif ay < water[0][1] + water[1][1]:
                #x ditance zur Linken Kante
                r = [water[0][0], self.pos[1]]
                d = abs(water[0][0] - self.pos[0])
            else:
                #untere linke Ecke
                corn = [water[0][0], water[1][1]]
                r = corn
                d = self.distance(corn)
        elif ax < water[0][0] + water[1][0]:
            if ay < water[0][1]:
                #yditance zur oberen Kante
                r = [self.pos[0], water[0][1]]
                d = water[0][1] - self.pos[1]
            elif ay < water[0][1] + water[1][1]:
                #im wasser
                #checken ob das passier
                print 'error'
                self.collision()
            else:
                # Ydistance zur unteren Kante
                p = water[0][1] + water[1][1]
                d = p - self.pos[1]
                r = [self.pos[0], p]
        else:
            if ay < water[0][1]:
                #clsosest point = water[0][0] + water[1][0]
                corn = [water[0][0] + water[1][0], water[0][1]]
                r = corn
                d = self.distance(corn)
            elif ay < water[0][1] + water[1][1]:
                #x ditance rechte Kante
                p = water[0][0] + water[1][0]
                d = p - self.pos[0]
                r = [p, self.pos[1]]
            else:
                #untere rechte Ecke
                corn = [water[0][0] + water[0][1], water[0][1] + water[1][1]]
                r = corn
                d = self.distance(corn)
        return d, r'''
        #needs = [[self.hung, 'hung'], [self.sexd, 'sex'], [self.thurst, 'thurst']]


            '''if need[1] == 'thurst':
                if self.targets[2] != None:
                    self.target = self.targets[2]
                    break'''
    
        # drinks = []

        # for water in waters:
        #     x = self.waterdistance(water)
        #     if x[0] <= self.sens:
        #         d = False
        #         drinks.append(water)
        # if len(drinks) != 0:
        #     self.targets[2] = self.findclosest(x[1])
        # else:
        #     self.targets[2] = None

#        animal.thurst += 3









