import pygame as pg


pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
icon_size = 80
padding = 5
button_height = 60
button_width = 200
font = pg.font.Font(None, 40)
mini_font = pg.font.Font(None, 15)
menu_nav_xpad = 90
menu_nav_ypad = 130

def text_render(text, text_font=font):
    return text_font.render(str(text), True, pg.Color('black'))
def load_image(file, width, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width, height))
    return image


class Button:
    def __init__(self, text, x, y, width=button_width, height=button_height, text_font=font, func=None):
        self.func = func
        self.idle_image = load_image('images/button.png', width, height)
        self.pressed_image = load_image('images/button_clicked.png', width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_font = text_font

        self.is_pressed = False
        self.text = text_render(text, text_font=self.text_font)
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def update(self):

        mouse_pos = pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image = self.pressed_image

            else:
                self.image = self.idle_image

    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed = True
                self.func()
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.is_pressed = False


class Item:
    def __init__(self, name, price, file, is_bought=False, is_put_on=False):
        self.name = name
        self.price = price
        self.is_bought = is_bought
        self.is_put_on = is_put_on

        self.image = load_image(file, 310 // 1.7, 500 // 1.7)
        self.full_image = load_image(file, 310, 500)

class ClothesMenu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Item('Синяя футболка', 10, 'images/items/blue t-shirt.png'),
                      Item('Ботинки', 50, 'images/items/boots.png'),
                      Item('Шляпа', 50, 'images/items/hat.png')
                      ]
        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button('Вперёд', SCREEN_WIDTH - menu_nav_xpad - button_width, SCREEN_HEIGHT - menu_nav_ypad,
                                  width=int(button_width//1.2), height=int(button_height//1.2),
                                  func=self.to_next())
    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1

    def update(self):
        self.next_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        screen.blit(self.items[self.current_item], self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))


        self.next_button.draw(screen)

    def Buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True
class Game:

    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(")")

        self.happines = 100
        self.satiety = 100
        self.health = 100
        self.money = 0
        self.background = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.satiety_image = load_image('images/satiety.png', icon_size,icon_size)
        self.happines_image = load_image('images/happiness.png', icon_size, icon_size)
        self.health_image = load_image('images/health.png', icon_size, icon_size)
        self.dog_image = load_image('images/dog.png', 310, 500)
        self.money_image = load_image('images/money.png', icon_size, icon_size)

        button_x = SCREEN_WIDTH - button_width - padding

        self.mode = 'main'

        self.eat_button = Button('Еда', button_x, padding + icon_size)
        self.cloth_button = Button('Одежда', button_x, icon_size * 2 - 5, func=self.cloth_menu_on)
        self.play_button = Button('Игры', button_x, icon_size * 3 - 15)
        self.coins_per_second = 1
        self.upgrate_button = Button('Улучшить', SCREEN_WIDTH - icon_size, 0, width=button_width//3, text_font=mini_font, height=button_height//3, func=self.increase_money)

        self.costs_of_upgrade = {100: False, 1000: False, 5000: False, 10000: False}
        self.buttons = [self.eat_button, self.cloth_button, self.play_button, self.upgrate_button]
        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)


        self.clothes_menu = ClothesMenu(self)

        self.run()

    def cloth_menu_on(self):
        self.mode = 'Cloth menu'

    def increase_money(self):
        for cost, upgraded in self.costs_of_upgrade.items():
            if not upgraded and self.money >= cost:
                self.coins_per_second += 1

                self.money -= cost
                self.costs_of_upgrade[cost] = True

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()

    def event(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = 'main'

            if event.type == self.INCREASE_COINS:
                    self.money += self.coins_per_second

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += 1

            for button in self.buttons:
                    button.is_clicked(event)
            self.clothes_menu.is_clicked(event)

    def update(self):
        for button in self.buttons:
            button.update()
        self.clothes_menu.update()


    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.dog_rect = self.dog_image.get_rect()
        self.dog_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(self.happines_image, (padding, padding))
        self.screen.blit(self.satiety_image, (padding, padding + 90))
        self.screen.blit(self.health_image, (padding, padding + 180))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - padding - icon_size, padding))

        self.screen.blit(text_render(self.happines), (padding * 2 + icon_size, padding + 30))
        self.screen.blit(text_render(self.satiety), (padding * 2 + icon_size, padding + 120))
        self.screen.blit(text_render(self.health), (padding * 2 + icon_size, padding + 210))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - padding - icon_size * 1.4, padding + 30))

        for button in self.buttons:
            button.draw(self.screen)

        if self.mode == 'Cloth menu':
            self.clothes_menu.draw(self.screen)

        self.screen.blit(self.dog_image, self.dog_rect)
        pg.display.flip()


if __name__ == "__main__":
    Game()