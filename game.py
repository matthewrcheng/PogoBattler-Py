import pygame

def game_loop(user, opponent):
    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # time interval
    interval = 500
    last_execution_time = 0

    # window size
    width = 800
    height = 600

    # create the screen
    screen = pygame.display.set_mode((width, height))

    # title and icon
    pygame.display.set_caption("PogoBattler")
    # icon = pygame.image.load('icon.png') uncomment later when icon is added
    # pygame.display.set_icon(icon)

    # charged attack button 
    charged_button_color = (0, 0, 0)
    charged_button_highlight_color = (50, 50, 50)
    charged_button_width = 100
    charged_button_height = 100
    charged_button_coords = (350, 300)

    action = None

    # game loop
    running = True
    while running:
        # medium blue background
        screen.fill((0, 64, 255))

        mouse = pygame.mouse.get_pos()
        # print("mouse position: " + str(mouse))

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # determine first action
                # fast attack if clicked, charged attack if clicked and enough energy, otherwise do nothing
                if charged_button_coords[0] <= mouse[0] <= charged_button_coords[0] + charged_button_width and charged_button_coords[1] <= mouse[1] <= charged_button_coords[1] + charged_button_height:
                    action = "charged attack"
                else:
                    action = "fast attack"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    action = "fast attack"
                elif event.key == pygame.K_RETURN:
                    action = "charged attack"

        # check every 0.5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_execution_time >= interval:
            # make the first action that was determined in the previous step
            if action == "fast attack":
                if user.fast_attack(opponent):
                    print("User wins!")
                    running = False
            elif action == "charged attack":
                if user.charged_attack(opponent, 0):
                    print("User wins!")
                    running = False
            action = None

            # cpu action
            if opponent.can_charged_attack(0):
                if opponent.charged_attack(user, 0):
                    print("Opponent wins!")
            else:
                if opponent.fast_attack(user):
                    print("Opponent wins!")

            last_execution_time = current_time
        
        if charged_button_coords[0] <= mouse[0] <= charged_button_coords[0] + charged_button_width and charged_button_coords[1] <= mouse[1] <= charged_button_coords[1] + charged_button_height:
            pygame.draw.rect(screen, charged_button_highlight_color, (charged_button_coords[0], charged_button_coords[1], charged_button_width, charged_button_height))
        else:
            pygame.draw.rect(screen, charged_button_color, (charged_button_coords[0], charged_button_coords[1], charged_button_width, charged_button_height))

        # update the display
        pygame.display.update()
        clock.tick(60)