# import pygame
# global waters
# waters = []
# dsize = (1850, 990)
# pygame.init()
# win = pygame.display.set_mode(dsize)
# for water in waters:
#     pygame.draw.rect(win, (0, 0, 255), (water[0][0], water[0][1], water[1][0], water[1][1]))

# def water():
#     waters.append([[120, 70], [80, 60]])
#     waters.append([[1200, 700], [80, 60]])
#     waters.append([[520, 870], [100, 40]])
#     waters.append([[720, 200], [400, 700]])

# running = True

# while running:
#     #check for break
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 running = False
    
#     water()
#     pygame.draw.rect(win, (0, 0, 0), (120 + 80, 70, 20, 20))
#     pygame.display.update()
#     win.fill((0, 255, 0))
