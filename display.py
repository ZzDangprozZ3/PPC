import pygame
import socket
from multiprocessing import Array
from threading import Thread
from ctypes import c_wchar_p

def display_socket(host, port, north_left, north_right, south_left, south_right, east_left, east_right, west_left, west_right, lights):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        client_socket, address = server_socket.accept()
        with client_socket:
            while True:
                data = client_socket.recv(2048)
                if not len(data):
                    break
                cars = data.decode().split()
                for i in range(4):
                    north_left[i] = cars[i]
                    north_right[i] = cars[4+i]
                    south_left[i] = cars[8+i]
                    south_right[i] = cars[12+i]
                    east_left[i] = cars[16+i]
                    east_right[i] = cars[20+i]
                    west_left[i] = cars[24+i]
                    west_right[i] = cars[28+i]
                    lights[i] = cars[32+i]
                    print(lights[:])

    


def display(width, heigth, background, host, port):
    north_left = Array(c_wchar_p, 4)
    north_right = Array(c_wchar_p, 4)
    south_left = Array(c_wchar_p, 4)
    south_right = Array(c_wchar_p, 4)
    east_left = Array(c_wchar_p, 4)
    east_right = Array(c_wchar_p, 4)
    west_left = Array(c_wchar_p, 4)
    west_right = Array(c_wchar_p, 4)
    lights = Array(c_wchar_p, 4)
    running = True
    # north_left[0] = "red"
    # north_left[1] = "blue"
    # north_left[2] = "green"

    # south_left[0] = "red"
    # south_left[1] = "blue"
    # south_left[2] = "green"
    # south_left[3] = "purple"


    # east_left[0] = "red"
    # east_left[1] = "blue"
    # east_left[2] = "green"

    # east_right[0] = "red"
    # east_right[1] = "blue"
    # east_right[2] = "green"

    # west_left[0] = "red"
    # west_left[1] = "blue"
    # west_left[2] = "green"

    # lights[0] = 1
    socket_thread = Thread(target=display_socket, args=(host, port, north_left, north_right, south_left, south_right, east_left, east_right, west_left, west_right, lights))
    socket_thread.start()
    ##########################

    smaller_dimension = min(width, heigth) 
    ######################################
    road_width = smaller_dimension // 5
    line_width = smaller_dimension // 100
    #################################################
    car_width = (road_width - line_width) // 4
    car_length = (smaller_dimension - road_width) // 12
    ##############################################
    n_s_center = width // 2
    distance_from_center = (road_width + line_width) // 4
    n_s_left = n_s_center + distance_from_center
    n_s_right = n_s_center - distance_from_center

    e_w_center = heigth // 2
    e_w_down = e_w_center + distance_from_center
    e_w_up = e_w_center - distance_from_center
    ###############################################
    n_s_car_dist = ((heigth - road_width) // 2 - 4 * car_length) // 4

    e_w_car_dist = ((width - road_width) // 2 - 4 * car_length) // 4
    #############################################################
    ####################################################################
    light_radius = 20
    light_side = light_radius * 5 // 2
    light_padding = light_radius // 5

    north_light_x = (width - road_width - light_side) // 2 - light_padding
    north_light_y = (heigth - road_width - light_side) // 2 - light_padding

    south_light_x = (width + road_width + light_side) // 2 + light_padding
    south_light_y = (heigth + road_width + light_side) // 2 + light_padding

    east_light_x = (width + road_width + light_side) // 2 + light_padding
    east_light_y = (heigth - road_width - light_side) // 2 - light_padding

    west_light_x = (width - road_width - light_side) // 2 - light_padding
    west_light_y = (heigth + road_width + light_side) // 2 + light_padding




    pygame.init()
    screen = pygame.display.set_mode((width, heigth))
    pygame.RESIZABLE = False
    clock = pygame.time.Clock()
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(background)

        # RENDER YOUR GAME HERE
        e_w_road = pygame.draw.line(screen, "black", (0, e_w_center), (width, e_w_center), width=road_width)
        n_s_road = pygame.draw.line(screen, "black", (n_s_center, 0), (n_s_center, heigth), width=road_width)

        e_w_line = pygame.draw.line(screen, "white", (0, e_w_center), (width, e_w_center), width=line_width)
        n_s_line = pygame.draw.line(screen, "white", (n_s_center, 0), (n_s_center, heigth), width=line_width)

        for i in range(4):
            if north_left[i] != "None" and north_left[i]:
                pygame.draw.line(screen, north_left[i], (n_s_left, i * car_length + (i + 1) * n_s_car_dist), (n_s_left, (i + 1) * (car_length + n_s_car_dist)), width=car_width)

            if north_right[i] != "None" and north_right[i]:
                pygame.draw.line(screen, north_right[i], (n_s_right, i * car_length + (i + 1) * n_s_car_dist), (n_s_right, (i + 1) * (car_length + n_s_car_dist)), width=car_width)

            if south_left[i] != "None" and south_left[i]:
                pygame.draw.line(screen, south_left[i], (n_s_right, heigth - (i * car_length + (i + 1) * n_s_car_dist)), (n_s_right, heigth - (i + 1) * (car_length + n_s_car_dist)), width=car_width)

            if south_right[i] != "None" and south_right[i]:
                pygame.draw.line(screen, south_right[i], (n_s_left, heigth - (i * car_length + (i + 1) * n_s_car_dist)), (n_s_left, heigth - (i + 1) * (car_length + n_s_car_dist)), width=car_width)
 
            if east_left[i] != "None" and east_left[i]:
                pygame.draw.line(screen, east_left[i], (width - (i * car_length + (i + 1) * e_w_car_dist), e_w_down), (width - (i + 1) * (car_length + n_s_car_dist), e_w_down), width=car_width)

            if east_right[i] != "None" and east_right[i]:
                pygame.draw.line(screen, east_right[i], (width - (i * car_length + (i + 1) * e_w_car_dist), e_w_up), (width - (i + 1) * (car_length + n_s_car_dist), e_w_up), width=car_width)

            if west_left[i] != "None" and west_left[i]:
                pygame.draw.line(screen, west_left[i], (i * car_length + (i + 1) * e_w_car_dist, e_w_up), ((i + 1) * (car_length + n_s_car_dist), e_w_up), width=car_width)

            if west_right[i] != "None" and west_right[i]:
                pygame.draw.line(screen, west_right[i], (i * car_length + (i + 1) * e_w_car_dist, e_w_down), ((i + 1) * (car_length + n_s_car_dist), e_w_down), width=car_width)

        pygame.draw.rect(screen, "black", pygame.Rect(north_light_x - light_side / 2, north_light_y - light_side / 2, light_side, light_side))
        if lights[3]:
            pygame.draw.circle(screen, lights[3], (north_light_x, north_light_y), light_radius)

        #south
        pygame.draw.rect(screen, "black", pygame.Rect(south_light_x - light_side / 2, south_light_y - light_side / 2, light_side, light_side))
        if lights[1]:
            pygame.draw.circle(screen, lights[1], (south_light_x, south_light_y), light_radius)

        #east
        pygame.draw.rect(screen, "black", pygame.Rect(east_light_x - light_side / 2, east_light_y - light_side / 2, light_side, light_side))
        if lights[2]:
            pygame.draw.circle(screen, lights[2], (east_light_x, east_light_y), light_radius)
        #west
        pygame.draw.rect(screen, "black", pygame.Rect(west_light_x - light_side / 2, west_light_y - light_side / 2, light_side, light_side))
        if lights[0]:
            pygame.draw.circle(screen, lights[0], (west_light_x, west_light_y), light_radius)

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()
    socket_thread.join()

if __name__ == "__main__":
    # north_left = Array(c_wchar_p, 3)
    # north_right = Array(c_wchar_p, 3)
    # south_left = Array(c_wchar_p, 3)
    # south_right = Array(c_wchar_p, 3)
    # west_left = Array(c_wchar_p, 3)
    # west_right = Array(c_wchar_p, 3)
    # east_left = Array(c_wchar_p, 3)
    # east_right = Array(c_wchar_p, 3)
    # north_left[0] = "red"
    # north_left[1] = "blue"
    # north_left[2] = "green"

    display(500, 500, "lightblue", "localhost", 3000)