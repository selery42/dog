import json
import random

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
max_font = pg.font.Font(None, 200)
menu_nav_xpad = 90
menu_nav_ypad = 130
fps = 60
food_size = 200


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
        self.file = file
        self.is_bought = is_bought
        self.is_put_on = is_put_on

        self.image = load_image(self.file, 310 // 1.7, 500 // 1.7)
        self.full_image = load_image(file, 310, 500)


class ClothesMenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = []
        for item in data:
            self.items.append(Item(*item.values()))


        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button('Вперёд', SCREEN_WIDTH - menu_nav_xpad - button_width, SCREEN_HEIGHT - menu_nav_ypad,
                                  width=int(button_width // 1.2), height=int(button_height // 1.2),
                                  func=self.to_next)
        self.back_button = Button('Назад', 125, 420,
                                  width=int(button_width // 1.2), height=int(button_height // 1.2),
                                  func=self.to_back)
        self.wear_button = Button('Надеть', 125, 420 - padding - button_height,
                                  width=int(button_width // 1.2), height=int(button_height // 1.2),
                                  func=self.use_item)
        self.buy_button = Button('Купить', SCREEN_WIDTH // 2 - button_width // 2 + 35, SCREEN_HEIGHT // 2 + 95,
                                 width=int(button_width // 1.5), height=int(button_height // 1.5),
                                 func=self.buy)

    def to_next(self):
        if self.current_item != 0:
            self.current_item += 1
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)

    def to_back(self):
        if self.current_item != 1:
            self.current_item -= 1
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.prcie_text_rect = self.price_text.get_rect()
        self.prcie_text_rect.center = (SCREEN_WIDTH // 2, 180)

    def use_item(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_put_on = not self.items[self.current_item].is_put_on

    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.wear_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.wear_button.is_clicked(event)
        self.buy_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.prcie_text_rect = self.price_text.get_rect()
        self.prcie_text_rect.center = (SCREEN_WIDTH // 2, 180)

        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.wear_button.draw(screen)
        self.buy_button.draw(screen)

        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.price_text, self.prcie_text_rect)

        screen.blit(self.items[self.current_item].image, self.item_rect)
        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on, (0, 0))
        else:
            screen.blit(self.bottom_label_off, (0, 0))
        if self.items[self.current_item].is_put_on:
            screen.blit(self.top_label_on, (0, 0))
        else:
            screen.blit(self.top_label_off, (0, 0))
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.price_text, self.prcie_text_rect)

    def Buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True


class Eat:
    def __init__(self, name, price, image, satiety, medicine_power=0):
        self.name = name
        self.satiety = satiety
        self.image = load_image(image, food_size, food_size)
        self.price = price
        self.medicine_power = medicine_power


class Food_Menu:
    def __init__(self, game):
        self.game = game
        self.menu_page = load_image('images/menu/menu_page.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.bottom_label_off = load_image('images/menu/bottom_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.bottom_label_on = load_image('images/menu/bottom_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_off = load_image('images/menu/top_label_off.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.top_label_on = load_image('images/menu/top_label_on.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.items = [Eat('Мясо', 30, 'images/food/meat.png', 10),
                      Eat('Корм', 40, 'images/food/dog food.png', 15),
                      Eat('Элитный корм', 100, 'images/food/dog food elite.png', 25, medicine_power=2),
                      Eat('лекарство', 200, 'images/food/medicine.png', 0, medicine_power=10)
                      ]
        self.current_item = 0

        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        self.next_button = Button('Вперёд', SCREEN_WIDTH - menu_nav_xpad - button_width, SCREEN_HEIGHT - menu_nav_ypad,
                                  width=int(button_width // 1.2), height=int(button_height // 1.2),
                                  func=self.to_next)
        self.back_button = Button('Назад', 125, 420,
                                  width=int(button_width // 1.2), height=int(button_height // 1.2),
                                  func=self.to_back)

        self.buy_button = Button('Съесть', SCREEN_WIDTH // 2 - button_width // 2 + 35, SCREEN_HEIGHT // 2 + 95,
                                 width=int(button_width // 1.5), height=int(button_height // 1.5),
                                 func=self.buy)

    def to_next(self):
        if self.current_item != 0:
            self.current_item += 1
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.prcie_text_rect = self.price_text.get_rect()
        self.prcie_text_rect.center = (SCREEN_WIDTH // 2, 180)

    def to_back(self):
        if self.current_item != len(self.items) - 1:
            self.current_item -= 1
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.prcie_text_rect = self.price_text.get_rect()
        self.prcie_text_rect.center = (SCREEN_WIDTH // 2, 180)




    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price

            self.game.satiety += self.items[self.current_item].satiety
            if self.game.satiety > 100:
                self.game.satiety = 100
            self.game.health += self.items[self.current_item].medicine_power
            if self.game.health > 100:
                self.game.health = 100

    def update(self):
        self.next_button.update()
        self.back_button.update()
        self.buy_button.update()

    def is_clicked(self, event):
        self.next_button.is_clicked(event)
        self.back_button.is_clicked(event)
        self.buy_button.is_clicked(event)

    def draw(self, screen):
        screen.blit(self.menu_page, (0, 0))

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)

        self.price_text = text_render(self.items[self.current_item].price)
        self.prcie_text_rect = self.price_text.get_rect()
        self.prcie_text_rect.center = (SCREEN_WIDTH // 2, 180)


        self.next_button.draw(screen)
        self.back_button.draw(screen)
        self.buy_button.draw(screen)

        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.price_text, self.prcie_text_rect)

        screen.blit(self.items[self.current_item].image, self.item_rect)


class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/Собака общий вид.png')
        size = (310 // 2, 500 // 2)

        self.image = pg.transform.scale(self.image, size)


        self.rect = self.image.get_rect()
        self.rect.midbottom = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= 10
        if keys[pg.K_d]:
            self.rect.x += 10


class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('images/toys/blue bone.png')
        size = (100, 100)

        self.image = pg.transform.scale(self.image, size)

        self.rect = self.image.get_rect()
        self.rect.midbottom = self.rect.midbottom = (random.randint(0, SCREEN_WIDTH), 0)
    def update(self):
        self.rect.y += 5

class Minigame:
    def __init__(self, game):
        self.game = game

        self.background = load_image('images/game_background.png', SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dog = Dog()
        self.toys = pg.sprite.Group()

        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5



    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0, 100) == 0:
            self.toys.add(Toy())
        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)
        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score//2)
            self.game.mode = 'main'
    def new_game(self):
        self.dog = Dog()
        self.toys = pg.sprite.Group()
        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 5

    def draw(self, screen):
        screen.blit(self.background, (0, 0))


        screen.blit(text_render(self.score), (menu_nav_xpad + 20, 80))
        screen.blit(self.dog.image, self.dog.rect)
        self.toys.draw(screen)


class Game:

    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(")")
        with open('save.json', encoding='utf-8') as f:
            data = json.load(f)
        self.clock = pg.time.Clock()
        self.happiness = data['happiness']
        self.satiety = data['satiety']
        self.health = data['health']
        self.money = data['money']
        self.background = load_image('images/background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
        self.satiety_image = load_image('images/satiety.png', icon_size, icon_size)
        self.happines_image = load_image('images/happiness.png', icon_size, icon_size)
        self.health_image = load_image('images/health.png', icon_size, icon_size)
        self.dog_image = load_image('images/dog.png', 310, 500)
        self.money_image = load_image('images/money.png', icon_size, icon_size)

        button_x = SCREEN_WIDTH - button_width - padding

        self.mode = 'main'

        self.eat_button = Button('Еда', button_x, padding + icon_size, func=self.food_menu_on)
        self.cloth_button = Button('Одежда', button_x, icon_size * 2 - 5, func=self.cloth_menu_on)
        self.play_button = Button('Игры', button_x, icon_size * 3 - 15, func=self.game_on)
        self.coins_per_second = data['coins_per_second']
        self.upgrate_button = Button('Улучшить', SCREEN_WIDTH - icon_size, 0, width=button_width // 3,
                                     text_font=mini_font, height=button_height // 3, func=self.increase_money)

        self.costs_of_upgrade = {}
        for key, value in data['cost_of_upgrade'].items():
            self.costs_of_upgrade[int(key)] = value


        self.buttons = [self.eat_button, self.cloth_button, self.play_button, self.upgrate_button]
        self.INCREASE_COINS = pg.USEREVENT + 1
        self.DECREASE = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)
        pg.time.set_timer(self.DECREASE, 1000)

        self.clothes_menu = ClothesMenu(self, data['clothes'])

        self.food_menu = Food_Menu(self)
        self.mini_game = Minigame(self)
        self.run()

    def cloth_menu_on(self):
        self.mode = 'Cloth menu'
    def food_menu_on(self):
        self.mode = 'Food menu'
    def game_on(self):
        self.mode = 'Mini game'
        self.mini_game.new_game()
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
            self.clock.tick(fps)

    def event(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == 'Game over':
                    data = {
  "happiness": 100,
  "satiety": 100,
  "health": 100,
  "money": 0,
  "coins_per_second": 1,
  "cost_of_upgrade": {
    "100": False,
    "1000": False,
    "5000": False,
    "10000": False
  },
  "clothes": [
    {
      "name": "Синяя футболка",
      "price": 10,
      "image": "images/items/blue t-shirt.png",
      "is_put_on": False,
      "is_bought": False
    },
    {
      "name": "Синяя футболка",
      "price": 50,
      "image": "images/items/boots.png",
      "is_put_on": False,
      "is_bought": False
    },
    {
      "name": "Шляпа",
      "price": 50,
      "image": "images/items/hat.png",
      "is_put_on": False,
      "is_bought": False
    }
  ]
}
                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_per_second": self.coins_per_second,
                        "cost_of_upgrade": {
                            "100": self.costs_of_upgrade[100],
                            "1000": self.costs_of_upgrade[1000],
                            "5000": self.costs_of_upgrade[5000],
                            "10000": self.costs_of_upgrade[10000]
                        },
                        'clothes': []

                    }
                    for item in self.clothes_menu.items:
                        data['clothes'].append({
      "name": item.name,
      "price": item.price,
      "image": item.file,
      "is_put_on": item.is_put_on,
      "is_bought": item.is_bought
    })
                with open('save.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = 'main'

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_per_second
            if event.type == self.DECREASE:
                number = random.randint(1, 10)
                if number <= 5:
                    self.satiety -= 1
                elif 5<number<= 9:
                    self.happiness -= 1
                else:
                    self.health -= 1

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += 1
            if self.mode == 'main':
                for button in self.buttons:
                    button.is_clicked(event)

            if self.mode != 'main':
                self.clothes_menu.is_clicked(event)
                self.food_menu.is_clicked(event)


    def update(self):
        if self.mode == 'Cloth menu':
            self.clothes_menu.update()
        elif self.mode == 'Food menu':
            self.food_menu.update()
        elif self.mode == 'Mini game':
            self.mini_game.update()
        else:
            for button in self.buttons:
                button.update()
        if self.happiness <= 0 or self.satiety <= 0 or self.health <= 0:
            self.mode = 'Game over'

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.dog_rect = self.dog_image.get_rect()
        self.dog_rect.centerx = SCREEN_WIDTH // 2
        self.dog_rect.y = 100
        self.dog_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.screen.blit(self.happines_image, (padding, padding))
        self.screen.blit(self.satiety_image, (padding, padding + 90))
        self.screen.blit(self.health_image, (padding, padding + 180))

        self.screen.blit(self.money_image, (SCREEN_WIDTH - padding - icon_size, padding))

        self.screen.blit(text_render(self.happiness), (padding * 2 + icon_size, padding + 30))
        self.screen.blit(text_render(self.satiety), (padding * 2 + icon_size, padding + 120))
        self.screen.blit(text_render(self.health), (padding * 2 + icon_size, padding + 210))
        self.screen.blit(text_render(self.money), (SCREEN_WIDTH - padding - icon_size * 1.4, padding + 30))
        self.screen.blit(self.dog_image, self.dog_rect)
        for button in self.buttons:
            button.draw(self.screen)

        for item in self.clothes_menu.items:
            if item.is_put_on:
                self.screen.blit(item.full_image, self.dog_rect)
        if self.mode == 'Cloth menu':
            self.clothes_menu.draw(self.screen)
        if self.mode == 'Food menu':
            self.food_menu.draw(self.screen)
        if self.mode == 'Mini game':
            self.mini_game.draw(self.screen)
        if self.mode == "Game over":
            text = max_font.render('ПРОИГРЫШ', True, 'red')
            text_text = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_text)


        pg.display.flip()


if __name__ == "__main__":
    Game()
