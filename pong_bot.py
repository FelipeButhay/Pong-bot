import math
import pygame

def get_inter(pos, vx, vy, screen_y, limit):
    y_movement = ((limit - pos[0])/vx)*vy
    if y_movement == 0:
        return pos[1]
    
    #bajando
    elif y_movement > 0:
        y_movement -= screen_y - pos[1]
        rest = y_movement % screen_y
        n_bounce = y_movement // screen_y
        if n_bounce%2 == 0:#arriba
            return screen_y - rest
        else: # abajo
            return rest
    
    #subiendo    
    elif y_movement < 0:
        y_movement += pos[1]
        rest = y_movement % screen_y
        n_bounce = y_movement // screen_y
        if n_bounce%2 == 0:#arriba
            return rest
        else: # abajo
            return screen_y - rest