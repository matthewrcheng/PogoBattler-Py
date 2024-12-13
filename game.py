import pygame

from move_animation import *

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
    charged_button_coords = (350, 450)


    bar_outline_color = (0, 0, 0)
    # user health bar
    user_health_bar_color = (0, 255, 0)
    user_health_bar_width = 200
    user_health_bar_height = 20
    user_health_bar_coords = (50, 50)

    # opponent health bar
    opponent_health_bar_color = (255, 0, 0)
    opponent_health_bar_width = 200
    opponent_health_bar_height = 20
    opponent_health_bar_coords = (50, 100)

    # user energy bar
    user_energy_bar_color = (0, 0, 255)
    user_energy_bar_width = 200
    user_energy_bar_height = 20
    user_energy_bar_coords = (300, 50)

    # user image
    user_image = pygame.image.load(user.image)
    user_image_coords = (150, 300)

    # opponent image
    opponent_image = pygame.image.load(opponent.image)
    opponent_image_coords = (550, 300)

    # shadow images
    shadow0 = pygame.image.load("graphics/shadow/shadow0.png")
    shadow1 = pygame.image.load("graphics/shadow/shadow1.png")
    shadow2 = pygame.image.load("graphics/shadow/shadow2.png")
    shadow3 = pygame.image.load("graphics/shadow/shadow3.png")
    shadow4 = pygame.image.load("graphics/shadow/shadow4.png")
    shadow5 = pygame.image.load("graphics/shadow/shadow5.png")
    shadow6 = pygame.image.load("graphics/shadow/shadow6.png")
    shadow7 = pygame.image.load("graphics/shadow/shadow7.png")
    shadow_images = [shadow0, shadow1, shadow2, shadow3, shadow4, shadow5, shadow6, shadow7]
    shadow_idx = 0
    last_shadow_time = 0

    # moves
    move_animation_queue = []

    action = None
    user_charged_idx = 0
    opponent_charged_idx = opponent.get_better_charged_attack(user)

    # game loop
    running = True
    while running:
        # medium blue background
        screen.fill((220, 224, 255))

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
                    if user.can_charged_attack(0):
                        action = "charged attack"
                else:
                    action = "fast attack"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    action = "fast attack"
                elif event.key == pygame.K_RETURN:
                    if user.can_charged_attack(0):
                        action = "charged attack"
                        user_charged_idx = 0
                elif event.key == pygame.K_RSHIFT:
                    if user.can_charged_attack(1):
                        action = "charged attack"
                        user_charged_idx = 1

        # check every 0.5 seconds
        current_time = pygame.time.get_ticks()
        if current_time - last_execution_time >= interval:
            if user.attack >= opponent.attack:
                # make the first action that was determined in the previous step
                if action == "fast attack":
                    move_animation_queue.append(MoveAnimationHandler(screen, user.fast_move, (user_image_coords[0] + 96, user_image_coords[1] + 48), (opponent_image_coords[0], opponent_image_coords[1] + 48)))
                    if user.fast_attack(opponent):
                        print("User wins!")
                        running = False
                elif action == "charged attack":
                    move_animation_queue.append(MoveAnimationHandler(screen, user.charged_moves[user_charged_idx], (user_image_coords[0] + 96, user_image_coords[1] + 48), (opponent_image_coords[0], opponent_image_coords[1] + 48), radius=20))
                    if user.charged_attack(opponent, user_charged_idx):
                        print("User wins!")
                        running = False
                action = None

                # cpu action
                if opponent.can_charged_attack(0):
                    move_animation_queue.append(MoveAnimationHandler(screen, opponent.charged_moves[opponent_charged_idx], (opponent_image_coords[0], opponent_image_coords[1] + 48), (user_image_coords[0] + 96, user_image_coords[1] + 48), radius=20, direction='right'))
                    if opponent.charged_attack(user, opponent_charged_idx):
                        print("Opponent wins!")
                        running = False
                else:
                    move_animation_queue.append(MoveAnimationHandler(screen, opponent.fast_move, (opponent_image_coords[0], opponent_image_coords[1] + 48), (user_image_coords[0] + 96, user_image_coords[1] + 48), direction='right'))
                    if opponent.fast_attack(user):
                        print("Opponent wins!")
                        running = False
                
            else:
                # cpu action
                if opponent.can_charged_attack(0):
                    move_animation_queue.append(MoveAnimationHandler(screen, opponent.charged_moves[opponent_charged_idx], (opponent_image_coords[0], opponent_image_coords[1] + 48), (user_image_coords[0] + 96, user_image_coords[1] + 48), radius=20, direction='right'))
                    if opponent.charged_attack(user, opponent_charged_idx):
                        print("Opponent wins!")
                else:
                    move_animation_queue.append(MoveAnimationHandler(screen, opponent.fast_move, (opponent_image_coords[0], opponent_image_coords[1] + 48), (user_image_coords[0] + 96, user_image_coords[1] + 48), direction='right'))
                    if opponent.fast_attack(user):
                        print("Opponent wins!")

                # make the first action that was determined in the previous step
                if action == "fast attack":
                    move_animation_queue.append(MoveAnimationHandler(screen, user.fast_move, (user_image_coords[0] + 96, user_image_coords[1] + 48), (opponent_image_coords[0], opponent_image_coords[1] + 48)))
                    if user.fast_attack(opponent):
                        print("User wins!")
                        running = False
                elif action == "charged attack":
                    move_animation_queue.append(MoveAnimationHandler(screen, user.charged_moves[user_charged_idx], (user_image_coords[0] + 96, user_image_coords[1] + 48), (opponent_image_coords[0], opponent_image_coords[1] + 48), radius=20))
                    if user.charged_attack(opponent, user_charged_idx):
                        print("User wins!")
                        running = False
                action = None

            last_execution_time = current_time
        
        if charged_button_coords[0] <= mouse[0] <= charged_button_coords[0] + charged_button_width and charged_button_coords[1] <= mouse[1] <= charged_button_coords[1] + charged_button_height:
            pygame.draw.rect(screen, charged_button_highlight_color, (charged_button_coords[0], charged_button_coords[1], charged_button_width, charged_button_height))
        else:
            pygame.draw.rect(screen, charged_button_color, (charged_button_coords[0], charged_button_coords[1], charged_button_width, charged_button_height))

        # draw health bars
        pygame.draw.rect(screen, bar_outline_color, (user_health_bar_coords[0], user_health_bar_coords[1], user_health_bar_width, user_health_bar_height))
        pygame.draw.rect(screen, bar_outline_color, (opponent_health_bar_coords[0], opponent_health_bar_coords[1], opponent_health_bar_width, opponent_health_bar_height))
        pygame.draw.rect(screen, user_health_bar_color, (user_health_bar_coords[0], user_health_bar_coords[1], user_health_bar_width * (user.remaining_hp / user.hp), user_health_bar_height))
        pygame.draw.rect(screen, opponent_health_bar_color, (opponent_health_bar_coords[0], opponent_health_bar_coords[1], opponent_health_bar_width * (opponent.remaining_hp / opponent.hp), opponent_health_bar_height))

        # draw user energy bar
        pygame.draw.rect(screen, bar_outline_color, (user_energy_bar_coords[0], user_energy_bar_coords[1], user_energy_bar_width, user_energy_bar_height))   
        pygame.draw.rect(screen, user_energy_bar_color, (user_energy_bar_coords[0], user_energy_bar_coords[1], user_energy_bar_width * (user.energy / 100), user_energy_bar_height))

        # draw pokemon
        screen.blit(user_image, (user_image_coords[0], user_image_coords[1]))
        if user.shadow:
            screen.blit(shadow_images[shadow_idx], (user_image_coords[0], user_image_coords[1]))
            current_shadow_time = pygame.time.get_ticks()
            if current_shadow_time - last_shadow_time >= 100:
                shadow_idx = (shadow_idx + 1) % 8
                last_shadow_time = current_shadow_time
        screen.blit(opponent_image, (opponent_image_coords[0], opponent_image_coords[1]))
        if opponent.shadow:
            screen.blit(shadow_images[shadow_idx], (opponent_image_coords[0], opponent_image_coords[1]))
            current_shadow_time = pygame.time.get_ticks()
            if current_shadow_time - last_shadow_time >= 100:
                shadow_idx = (shadow_idx + 1) % 8
                last_shadow_time = current_shadow_time

        # draw moves
        to_remove = []
        for i,move in enumerate(move_animation_queue):
            if move.get_image() is None:
                to_remove.append(i)

        for i in reversed(to_remove):
            move_animation_queue.pop(i)


        # update the display
        pygame.display.update()
        clock.tick(60)