import pygame

from pokemon import *

def render_choices(screen, color, FONT, fast_move_rects):
    for fast_move, fast_move_rect in fast_move_rects.items():
        pygame.draw.rect(screen, color, fast_move_rect)
        text = FONT.render(fast_move, True, (255, 255, 255))
        screen.blit(text, (fast_move_rect.x + 5, fast_move_rect.y + 5))


def selection_loop():
    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # window size
    width = 800
    height = 600
    BG_COLOR = (255, 255, 0)
    TEXT_COLOR = (255, 255, 255)
    HIGHLIGHT_COLOR = (100, 100, 255)
    INPUT_BOX_COLOR = (50, 50, 50)
    OPTION_BOX_COLOR = (70, 70, 70)
    FONT_SIZE = 24
    FONT = pygame.font.Font(None, FONT_SIZE)

    # create the screen
    screen = pygame.display.set_mode((width, height))

    # title and icon
    pygame.display.set_caption("PogoBattler")
    # icon = pygame.image.load('icon.png') uncomment later when icon is added
    # pygame.display.set_icon(icon)

    # dropdown
    OPTIONS = get_all_pokemon()
    input_box_rect = pygame.Rect(50, 50, 300, FONT_SIZE + 10)
    dropdown_rect = pygame.Rect(0, 0, 0, 0)
    next_rect = pygame.Rect(375, 50, 50, FONT_SIZE + 10)
    input_text = ""
    filtered_options = OPTIONS.copy()
    dropdown_visible = False
    selected_index = None
    scroll_offset = 0
    MAX_VISIBLE_OPTIONS = 10
    OPTION_HEIGHT = FONT_SIZE + 5

    def render_options(filtered_options, scroll_offset):
        dropdown_rect = pygame.Rect(input_box_rect.x, input_box_rect.bottom, input_box_rect.width, 
                                min(MAX_VISIBLE_OPTIONS, len(filtered_options)) * OPTION_HEIGHT)
        pygame.draw.rect(screen, OPTION_BOX_COLOR, dropdown_rect)
        pygame.draw.rect(screen, TEXT_COLOR, dropdown_rect, 2)

        # Draw visible options
        for i, option in enumerate(filtered_options[scroll_offset:scroll_offset + MAX_VISIBLE_OPTIONS]):
            option_rect = pygame.Rect(input_box_rect.x, input_box_rect.bottom + i * OPTION_HEIGHT, 
                                    input_box_rect.width, OPTION_HEIGHT)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR if i + scroll_offset == selected_index else OPTION_BOX_COLOR, option_rect)
            option_text = FONT.render(option, True, TEXT_COLOR)
            screen.blit(option_text, (option_rect.x + 5, option_rect.y + 5))


    selection = None
    picking_fast_move = False

    # game loop
    running = True
    while running:
        # medium blue background
        screen.fill(BG_COLOR)

        pygame.draw.rect(screen, INPUT_BOX_COLOR, input_box_rect)
        input_text_surface = FONT.render(input_text, True, TEXT_COLOR)
        screen.blit(input_text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_box_rect.collidepoint(event.pos):
                    dropdown_visible = True
                elif dropdown_rect.collidepoint(event.pos):
                    relative_y = event.pos[1] - dropdown_rect.y
                    clicked_index = relative_y // OPTION_HEIGHT + scroll_offset
                    if clicked_index < len(filtered_options):
                        input_text = filtered_options[clicked_index]
                        selection = filtered_options[clicked_index]
                        dropdown_visible = False
                elif next_rect.collidepoint(event.pos) and selection:
                    print("selected: " + selection)
                    pokemon = Pokemon(selection)

                    # create a rect for each potential fast move
                    fast_move_rects = {}
                    for i,fast_move in enumerate(pokemon.fast_moves):
                        fast_move_rects[fast_move] = pygame.Rect(50+i*75, 150, 50, 50)

                    # create a rect for each potential charged move
                    charged_move_rects = {}
                    for charged_move in pokemon.charged_moves:
                        charged_move_rects[charged_move] = pygame.Rect(50+i*75, 250, 50, 50)

                    # create a rect for each IV set
                    iv_rects = {}
                    for iv in pokemon.default_ivs:
                        iv_rects[iv] = pygame.Rect(50+i*75, 350, 50, 50)

                    picking_fast_move = True
                else:
                    dropdown_visible = False

                if dropdown_visible:
                    dropdown_rect = pygame.Rect(input_box_rect.x, input_box_rect.bottom, input_box_rect.width, 
                                                min(MAX_VISIBLE_OPTIONS, len(filtered_options)) * OPTION_HEIGHT)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    dropdown_visible = False
                else:
                    input_text += event.unicode

                # Update filtered options
                filtered_options = [opt for opt in OPTIONS if input_text.lower() in opt.lower()]
                scroll_offset = 0  # Reset scroll offset
            elif event.type == pygame.MOUSEWHEEL:
                if dropdown_visible:
                    if event.y > 0:  # Scroll up
                        scroll_offset = max(0, scroll_offset - 1)
                    elif event.y < 0:  # Scroll down
                        scroll_offset = min(len(filtered_options) - MAX_VISIBLE_OPTIONS, scroll_offset + 1)

        if dropdown_visible:
            render_options(filtered_options, scroll_offset)
        if picking_fast_move:
            render_choices(screen, OPTION_BOX_COLOR, FONT, fast_move_rects)
        pygame.draw.rect(screen, OPTION_BOX_COLOR, next_rect)

        # update the display
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    selection_loop()