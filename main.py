import pygame as pg

pg.init()
window = pg.display.set_mode((1440,810))
pg.display.set_caption("game")

color = "red"

running = True

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        window.fill(color)

        pg.display.flip()

        if(color == "red"):
            color = "blue"
        elif(color == "blue"):
            color = "green"
        else:
            color = "red"