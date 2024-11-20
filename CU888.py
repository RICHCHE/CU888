import pygame
import random
import os
from collections import Counter
import cv2

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GRAY = (200, 200, 200)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GOLD = (255, 215, 0)
BLUE = (70, 130, 180)
HOVER_HIGHLIGHT = (220, 220, 255)
SHADOW_COLOR = (50, 50, 50)
DARK_GREEN = (34, 139, 34)
DARK_RED = (139, 0, 0)

# Set up screen
screen_width, screen_height = 1024, 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("CU888")

# Load background images
background_image_path = "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Backgroud/Backgroud.jpg"
battle_background_image_path = "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Backgroud/Backgroud.jpg"

if os.path.exists(background_image_path):
    background_image = pygame.image.load(background_image_path)
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
else:
    print("Background image not found. Please check the file path.")
    background_image = None

if os.path.exists(battle_background_image_path):
    battle_background_image = pygame.image.load(battle_background_image_path)
    battle_background_image = pygame.transform.scale(battle_background_image, (screen_width, screen_height))
else:
    print("Battle background image not found. Please check the file path.")
    battle_background_image = None

# Function to convert an image to grayscale
def convert_to_grayscale(image):
    grayscale_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            r, g, b, *a = image.get_at((x, y))
            gray = int(0.3 * r + 0.59 * g + 0.11 * b)
            grayscale_image.set_at((x, y), (gray, gray, gray, *a))
    return grayscale_image

# Define card sizes for different contexts
normal_card_size = (100, 150)  # Normal card size for all other pages
gacha_card_size = (150, 225)   # Larger card size for Gacha page

# Load card images and define their properties
cards = [
    {"name": "Ploy", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/AjPloy_9star.png", "stars": 9, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/AjPloy.MP4"},
    {"name": "Rain", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Rain_2star.png", "stars": 2, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Rain.MOV"},
    {"name": "Earth", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Earth_2star.png", "stars": 2, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Earth_new.MOV"},
    {"name": "Richche", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Richche_1star.png", "stars": 2, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Richche.MOV"},
    {"name": "Pee", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Pee_1star.png", "stars": 1, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Pee.MOV"},
    {"name": "Su", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Su_4star.png", "stars": 4, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Su.MOV"},
    {"name": "TangMo", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/TM_3star.png", "stars": 3, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/TM.mov"},
    {"name": "Film", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Film_3star.png", "stars": 3, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Film.MOV"},
    {"name": "Monk", "image_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Picture/Charecter/Monk_10star.png", "stars": 10, "video_path": "/Users/bhurichchankasem/Desktop/Chula_Game/Video/Film.MOV"}
]

# Load card images with normal size initially
for card in cards:
    if os.path.exists(card["image_path"]):
        card["image"] = pygame.image.load(card["image_path"])
        card["image"] = pygame.transform.scale(card["image"], normal_card_size)  # Normal card size
        card["grayscale_image"] = convert_to_grayscale(card["image"])  # Create a grayscale version
    else:
        print(f"Card image for {card['name']} not found. Please check the file path.")
        card["image"] = pygame.Surface(normal_card_size)  # Create a blank surface as placeholder
        card["image"].fill(WHITE)
        card["grayscale_image"] = card["image"].copy()

# Define Drop Rates for Normal and Premium Gacha
normal_gacha_drop_rates = {
    "Ploy": 0.01,   # 1%
    "Rain": 0.2,   
    "Earth": 0.3, 
    "Richche": 0.3, 
    "Pee": 0.5,   
    "Su": 0.15,
    "TangMo": 0.17,
    "Film": 0.17
}

premium_gacha_drop_rates = {
    "Ploy": 0.2,    
    "Rain": 0.4,    
    "Earth": 0.3,   
    "Richche": 0.15, 
    "Pee": 0.05,     
    "Su": 0.3,
    "TangMo": 0.4,
    "Film": 0.4,
    "Monk": 0.1
}

# Function to draw a card based on drop rate
def draw_card_based_on_drop_rate(drop_rates):
    total_rate = sum(drop_rates.values())
    pick = random.uniform(0, total_rate)
    current = 0
    for card in cards:
        current += drop_rates[card["name"]]
        if current >= pick:
            return card

# Initialize player inventory
player_inventory = []

# Define fonts
font = pygame.font.Font(None, 36)
header_font = pygame.font.Font(None, 64)  # Larger header font for modern look
result_font = pygame.font.Font(None, 80)  # Font for result text

# Define button properties
button_width = 220
button_height = 60
button_color = (70, 130, 180)  # Steel blue color
hover_color = (100, 149, 237)  # Lighter blue for hover effect
button_border_radius = 15

# Function to draw button with shadow and hover effect
def draw_button(screen, button, hover=False):
    shadow_offset = 5
    shadow_rect = button["rect"].move(shadow_offset, shadow_offset)
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=button_border_radius)
    color = hover_color if hover else button_color
    if button["label"] == "Premium Gacha":
        color = GOLD  # Set Premium Gacha button to gold color
    pygame.draw.rect(screen, color, button["rect"], border_radius=button_border_radius)
    text_surface = font.render(button["label"], True, WHITE)
    text_rect = text_surface.get_rect(center=button["rect"].center)
    screen.blit(text_surface, text_rect)

# Button positions
buttons_main_menu = [
    {"label": "Gacha Menu", "rect": pygame.Rect(screen_width // 2 - button_width - 150, 500, button_width, button_height)},
    {"label": "Start Game", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 500, button_width, button_height)},
    {"label": "Album", "rect": pygame.Rect(screen_width // 2 + 150, 500, button_width, button_height)}
]

buttons_gacha_menu = [
    {"label": "Add Money", "rect": pygame.Rect(50, 150, button_width, button_height)},
    {"label": "Normal Gacha", "rect": pygame.Rect(screen_width // 2 - button_width - 50, 600, button_width, button_height)},
    {"label": "Premium Gacha", "rect": pygame.Rect(screen_width // 2 + 50, 600, button_width, button_height)},
    {"label": "Back to Main Menu", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 700, button_width, button_height)},
]

buttons_battle = [
    {"label": "Hit", "rect": pygame.Rect(screen_width // 2 - button_width - 50, 600, button_width, button_height)},
    {"label": "Stand", "rect": pygame.Rect(screen_width // 2 + 50, 600, button_width, button_height)},
    {"label": "Back to Main Menu", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 700, button_width, button_height)},
]

button_back_to_gacha = {"label": "Back to Gacha Menu", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 650, button_width, button_height)}
button_back_to_menu = {"label": "Back to Main Menu", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 700, button_width, button_height)}
button_back_to_menu_battle = {"label": "Back to Main Menu", "rect": pygame.Rect(screen_width // 2 - button_width // 2, 700, button_width, button_height)}

# Game state
state = "main_menu"  # Initial state
player_money = 8888  # Example initial amount of money
normal_price = 88  # Cost for normal gacha
premium_price = 888  # Cost for premium gacha

# Input state
input_active = False
input_text = ""

# Function to handle money addition based on input code
def add_money(code):
    if code == "CU888":
        return 888
    elif code == "COMSCI888":
        return 8888
    else:
        return 0

# Function for battle between two card sets (Blackjack style)
def battle(player_cards, ai_cards):
    player_score = sum(card["stars"] for card in player_cards)
    ai_score = sum(card["stars"] for card in ai_cards)

    if player_score > 21:
        return "Player busts!"
    elif ai_score > 21:
        return "AI busts!"
    elif player_score > ai_score:
        return "Player wins!"
    elif player_score < ai_score:
        return "AI wins!"
    else:
        return "It's a draw!"

import cv2
import pygame

# Function to play video within Pygame
def play_video(video_path):
    # Check if the video file exists
    if not os.path.exists(video_path):
        print("Video file not found.")
        return

    # Load the video using OpenCV
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    clock = pygame.time.Clock()

    # Get video properties
    video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    aspect_ratio = video_width / video_height

    # Set desired width while maintaining aspect ratio
    desired_width = min(video_width, 480)
    desired_height = int(desired_width / aspect_ratio)
    
    back_button = {
        "label": "Back to Album",
        "rect": pygame.Rect(screen_width // 2 - 100, screen_height - 80, 200, 50),
        "color": BLUE,
        "hover_color": LIGHT_GRAY
    }

    # Play the video frame by frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to a format suitable for Pygame
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame_surface = pygame.surfarray.make_surface(frame)
        frame_surface = pygame.transform.scale(frame_surface, (desired_width, desired_height))

        # Display the frame in the Pygame window with background
        if background_image:
            screen.blit(background_image, (0, 0))  # Draw background before the video
        else:
            screen.fill(BLACK)  # Fill screen with black before drawing video
        
        video_rect = frame_surface.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(frame_surface, video_rect.topleft)

        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        draw_button(screen, back_button, hover=back_button["rect"].collidepoint(mouse_pos))

        pygame.display.update()

        # Limit frame rate
        clock.tick(30)

        # Handle quit and button events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cap.release()
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Press 'q' to quit video playback
                    cap.release()
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and back_button["rect"].collidepoint(mouse_pos):
                    cap.release()
                    return

    # Release the video capture object
    cap.release()

# Main game loop
running = True
battle_result = ""
player_cards = []
ai_cards = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if state == "main_menu":
                    for button in buttons_main_menu:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["label"] == "Gacha Menu":
                                state = "gacha_menu"
                            elif button["label"] == "Album":
                                state = "album_page"
                            elif button["label"] == "Start Game":
                                if len(player_inventory) >= 2:  # Ensure player has at least 2 cards from gacha
                                    state = "battle"  # Start the battle directly
                                    player_cards = random.sample(player_inventory, 2)  # Draw 2 cards for the player initially
                                    ai_cards = random.sample(cards, 2)  # Draw 2 cards for the AI initially
                                    battle_result = ""
                elif state == "gacha_menu":
                    for button in buttons_gacha_menu:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["label"] == "Normal Gacha" and player_money >= normal_price:
                                selected_card = draw_card_based_on_drop_rate(normal_gacha_drop_rates)
                                player_inventory.append(selected_card)
                                player_money -= normal_price
                                state = "gacha_page"
                            elif button["label"] == "Premium Gacha" and player_money >= premium_price:
                                selected_card = draw_card_based_on_drop_rate(premium_gacha_drop_rates)
                                player_inventory.append(selected_card)
                                player_money -= premium_price
                                state = "gacha_page"
                            elif button["label"] == "Add Money":
                                input_active = True
                                input_text = ""
                            elif button["label"] == "Back to Main Menu":
                                state = "main_menu"
                elif state == "gacha_page":
                    if button_back_to_gacha["rect"].collidepoint(mouse_pos):
                        state = "gacha_menu"
                elif state == "album_page":
                    x_offset = 50
                    y_offset = 100
                    card_width = 100
                    card_height = 150
                    card_spacing_x = 20
                    card_spacing_y = 15
                    for card in cards:
                        card_rect = pygame.Rect(x_offset, y_offset, card_width, card_height)
                        if card_rect.collidepoint(mouse_pos):
                            if os.path.exists(card["video_path"]):
                                play_video(card["video_path"])
                        x_offset += card_width + card_spacing_x
                        if x_offset + card_width > screen_width:
                            x_offset = 50
                            y_offset += card_height + card_spacing_y
                    if button_back_to_menu["rect"].collidepoint(mouse_pos):
                        state = "main_menu"
                elif state == "battle":
                    for button in buttons_battle:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["label"] == "Hit" and len(player_inventory) > len(player_cards):
                                player_cards.append(random.choice(player_inventory))  # Player draws a card from their inventory
                                if sum(card["stars"] for card in player_cards) > 21:
                                    battle_result = "Player busts!"
                                    state = "battle"
                            elif button["label"] == "Stand":
                                while sum(card["stars"] for card in ai_cards) < 17:
                                    ai_cards.append(random.choice(cards))  # AI draws until it reaches 17 or higher
                                battle_result = battle(player_cards, ai_cards)
                                state = "battle"
                            elif button["label"] == "Back to Main Menu":
                                state = "main_menu"
                elif state == "battle_result":
                    if button_back_to_menu_battle["rect"].collidepoint(mouse_pos):
                        state = "main_menu"

        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    added_amount = add_money(input_text)
                    if added_amount > 0:
                        player_money += added_amount
                        print(f"Added {added_amount} money!")
                    else:
                        print("Invalid code.")
                    input_active = False
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

    # Drawing logic
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)

    if state == "main_menu":
        title_text = header_font.render("CU888 Casino", True, GOLD)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        
        for button in buttons_main_menu:
            draw_button(screen, button, hover=button["rect"].collidepoint(pygame.mouse.get_pos()))

        money_text = font.render(f"Money: {player_money}", True, GOLD)
        screen.blit(money_text, (50, 50))  # Display money in the top left corner
        
        if input_active:
            pygame.draw.rect(screen, LIGHT_GRAY, (screen_width // 2 - 150, 300, 300, 50), border_radius=button_border_radius)
            input_surface = font.render(input_text, True, BLACK)
            screen.blit(input_surface, (screen_width // 2 - 140, 310))

    elif state == "gacha_menu":
        gacha_menu_text = header_font.render("Gacha888", True, GOLD)
        screen.blit(gacha_menu_text, (screen_width // 2 - gacha_menu_text.get_width() // 2, 50))
        money_text = font.render(f"Money: {player_money}", True, GOLD)
        screen.blit(money_text, (50, 50))
        
                
        for button in buttons_gacha_menu:
            draw_button(screen, button, hover=button["rect"].collidepoint(pygame.mouse.get_pos()))

        if input_active:
            pygame.draw.rect(screen, LIGHT_GRAY, (screen_width // 2 - 150, 400, 300, 50), border_radius=button_border_radius)
            input_surface = font.render(input_text, True, BLACK)
            screen.blit(input_surface, (screen_width // 2 - 140, 410))

    elif state == "gacha_page":
        gacha_text = header_font.render("Your card888!", True, GOLD)
        screen.blit(gacha_text, (screen_width // 2 - gacha_text.get_width() // 2, 50))
        if selected_card:
            # Resize the card to gacha size for displaying in Gacha page
            gacha_card_image = pygame.transform.scale(selected_card["image"], gacha_card_size)
            card_rect = gacha_card_image.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(gacha_card_image, card_rect)
        draw_button(screen, button_back_to_gacha)

    elif state == "album_page":
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill(WHITE)

        album_text = header_font.render("Your Album888", True, GOLD)
        screen.blit(album_text, (screen_width // 2 - album_text.get_width() // 2, 20))

        inventory_count = Counter([card["name"] for card in player_inventory])
        x_offset = 50
        y_offset = 100
        card_width = 100
        card_height = 150
        card_spacing_x = 20
        card_spacing_y = 15

        for card in cards:
            card_rect = pygame.Rect(x_offset, y_offset, card_width, card_height)
            shadow_rect = card_rect.inflate(10, 10)
            pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=10)

            if card["name"] in inventory_count:
                screen.blit(card["image"], card_rect.topleft)
                if inventory_count[card["name"]] > 1:
                    count_text = font.render(f"x{inventory_count[card['name']]}", True, GOLD)
                    screen.blit(count_text, (x_offset + 70, y_offset + 120))
            else:
                screen.blit(card["grayscale_image"], card_rect.topleft)

            if card_rect.collidepoint(pygame.mouse.get_pos()):
                hover_overlay = pygame.Surface((card_width, card_height), pygame.SRCALPHA)
                hover_overlay.fill((255, 255, 255, 60))
                screen.blit(hover_overlay, card_rect.topleft)
                tooltip_text = font.render(card["name"], True, BLACK)
                tooltip_rect = tooltip_text.get_rect(center=(card_rect.centerx, card_rect.top - 20))
                pygame.draw.rect(screen, LIGHT_GRAY, tooltip_rect.inflate(10, 5), border_radius=5)
                screen.blit(tooltip_text, tooltip_rect)

            x_offset += card_width + card_spacing_x
            if x_offset + card_width > screen_width:
                x_offset = 50
                y_offset += card_height + card_spacing_y

        draw_button(screen, button_back_to_menu)

    elif state == "battle":
        if battle_background_image:
            screen.blit(battle_background_image, (0, 0))
        else:
            screen.fill(WHITE)
        battle_text = header_font.render("Battle", True, GOLD)
        screen.blit(battle_text, (screen_width // 2 - battle_text.get_width() // 2, 50))
        player_text = font.render("Player Cards:", True, GOLD)
        ai_text = font.render("AI Cards:", True, GOLD)
        screen.blit(player_text, (50, 150))
        screen.blit(ai_text, (screen_width - 250, 150))

        # Display player cards with better spacing to prevent overlap
        x_offset_player = 50
        y_offset_player = 200
        for card in player_cards:
            screen.blit(card["image"], (x_offset_player, y_offset_player))
            x_offset_player += 120  # Adjust spacing for cards
            if x_offset_player + 100 > screen_width - 400:  # Move to next row if out of horizontal space
                x_offset_player = 50
                y_offset_player += 170

        # Display AI cards with better spacing
        x_offset_ai = screen_width - 400
        y_offset_ai = 200
        for card in ai_cards:
            screen.blit(card["image"], (x_offset_ai, y_offset_ai))
            x_offset_ai += 120  # Adjust spacing for cards
            if x_offset_ai + 100 > screen_width:
                x_offset_ai = screen_width - 400
                y_offset_ai += 170

        # Display the battle result if available
        if battle_result:
            result_box = pygame.Rect(screen_width // 2 - 200, 470, 400, 100)
            pygame.draw.rect(screen, DARK_GRAY, result_box, border_radius=15)
            pygame.draw.rect(screen, GOLD, result_box, 5, border_radius=15)
            result_color = GREEN if "Player wins" in battle_result else RED if "busts" in battle_result or "AI wins" in battle_result else BLACK
            result_text = result_font.render(battle_result, True, result_color)
            screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 500))

        for button in buttons_battle:
            draw_button(screen, button, hover=button["rect"].collidepoint(pygame.mouse.get_pos()))

    elif state == "battle_result":
        if battle_background_image:
            screen.blit(battle_background_image, (0, 0))
        else:
            screen.fill(WHITE)
        result_text = header_font.render("Battle Result", True, GOLD)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 50))
        result_color = GREEN if "Player wins" in battle_result else RED if "busts" in battle_result or "AI wins" in battle_result else BLACK
        result_text = result_font.render(battle_result, True, result_color)
        screen.blit(result_text, (screen_width // 2 - result_text.get_width() // 2, 150))
        draw_button(screen, button_back_to_menu_battle)

    pygame.display.flip()

pygame.quit()
