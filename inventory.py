from dataclasses import dataclass
import pygame

class Inventory:
    def __init__(self, game):
        self.objet_inventory = []
        self.objet_inventory_rects = []
        self.max_quantity = 999
        self.game = game
        self.potion = Potion(any, any, game)
        self.potion.init_all_potion()
        self.weapon = Weapon(any, any, game)
        self.weapon.init_all_weapon()

# Gère l'ouverture et la gestion de l'inventaire
    def open_inventory(self, game, origin) -> bool:
        is_open = True
        object_used = False

        while is_open:
            game.screen.inventory_display.draw_inventory_display(origin)

            is_open, object_used = game.inventory.detect_object_selectionned()

            pygame.display.flip()

            if not self.game.tutorial.dic_tutorial['inventory']:
                self.game.tutorial.running('tuto_iv')
                self.game.tutorial.dic_tutorial['inventory'] = True
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.saves.save_and_quit()

        return object_used

# Vérifie si l'objet existe
    def object_existing(self, objet) -> bool:
        for existing_objet in self.objet_inventory:
            if existing_objet[0].name == objet.name:
                return True
        return False

# Regarde si la limite d'objet n'a pas été atteint
    def can_add_quantity(self, quantity , add_quantity) -> bool:
        if quantity + add_quantity < self.max_quantity:
            return True
        return False

# Ajoute une certaine quantité d'objet à l'inventaire si il existe déjà
    def update_quantity_object(self, current_objet, new_quantity):
        for i, (objet, number_object) in enumerate(self.objet_inventory):
            if objet.name == current_objet.name:
                if self.can_add_quantity(number_object, new_quantity):
                    new_number_object = self.add_quantity(number_object, new_quantity)
                    self.objet_inventory[i] = (current_objet, new_number_object)
                else:
                    self.objet_inventory[i] = (current_objet, self.max_quantity)
                break

# Vérifie si la limite d'objet est atteinte ou non et agis en conséquent
    def add_quantity(self, quantity, add_quantity):
        if quantity + add_quantity < self.max_quantity:
            return quantity + add_quantity
        elif quantity + add_quantity > self.max_quantity:
            return self.max_quantity

# Ajoute un objet a l'inventaire
    def append_object(self, objet, number=1):
        if not self.object_existing(objet):
            self.objet_inventory.append((objet, number))
        else:
            self.update_quantity_object(objet, number)

# Retire un objet de l'inventaire
    def delete_object(self, objet):
        for i, current_object in enumerate(self.objet_inventory):
            if objet.name == current_object[0].name:
                self.objet_inventory.pop(i)

        for i, (t, (current_object, a)) in enumerate(self.objet_inventory_rects):
            while any(current_object.name == objet.name for _, (current_object, _) in self.objet_inventory_rects):
                self.objet_inventory_rects.pop(i)

# Retire une certaine quantité de l'objet dans l'inventaire
    def remove_quantity(self, number_object, number, current_objet, i):
        new_number_object = number_object - number
        if new_number_object > 0:
            self.objet_inventory[i] = (current_objet, new_number_object)
        else:
            self.delete_object(current_objet)

# Supprime l'objet de l'inventaire
    def remove_object(self, objet, number=1):
        for i, (current_objet, number_object) in enumerate(self.objet_inventory):
            if objet.name == current_objet.name:
                self.remove_quantity(number_object, number, current_objet, i)
                break

# Return la liste de tout les objets
    def all_objects(self) -> list:
        return self.objet_inventory

# détecte l'objet est sékéctionner
    def detect_object_selectionned(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return False, True

            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect, objet in self.objet_inventory_rects:
                    x, y = rect
                    rect = pygame.Rect((x, y, 35, 50))
                    if rect.collidepoint(event.pos):
                        object_used = objet[0].used()
                        print(object_used)
                        if object_used:
                            message = self.game.load_txt('message_system', 'object_used') + self.game.load_txt('objects', objet[0].name)
                            self.game.add_message(message)
                            self.game.update_screen()
                        return False, object_used

                rect = self.game.screen.inventory_display.enter_zone_inventory()
                if not rect.collidepoint(event.pos):
                    return False, True

            if event.type == pygame.QUIT:
                self.game.saves.save_and_quit()
        return True, True




@dataclass
class Objet:
    name: str
    image: pygame.Surface

                                            # les potions
class Potion(Objet):
    def __init__(self, name, image, game, effect=None):
        self.effect = effect
        self.game = game
        super().__init__(name, image)

    def init_all_potion(self):
        Life_Potion(self.game)
        Big_Life_Potion(self.game)

    def used(self):
        self.effect()
        self.game.inventory.remove_object(self, 1)
        return True

class Life_Potion(Potion):
    def __init__(self, game):
        self.game = game
        path = self.game.get_path_assets("inventory\objects\potions\heal_potion.png")
        name = "Life_Potion"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (48, 48))
        super().__init__(name, image, game, self.effect)

        self.add_life = 20

    def effect(self):
        if self.game.data_player.health + self.add_life <= self.game.data_player.max_health:
            self.game.data_player.health += self.add_life
        else:
            self.game.data_player.health = self.game.data_player.max_health

class Big_Life_Potion(Potion):
    def __init__(self, game):
        self.game = game
        path = self.game.get_path_assets(r"inventory\objects\potions\big_heal_potion.png")
        name = "Big_Life_Potion"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (48, 48))
        super().__init__(name, image, game, self.effect)

        self.add_life = 40

    def effect(self):
        if self.game.data_player.health + self.add_life <= self.game.data_player.max_health:
            self.game.data_player.health += self.add_life
        else:
            self.game.data_player.health = self.game.data_player.max_health


class Weapon(Objet):
    def __init__(self, name, image, game, effect=None):
        self.effect = effect
        self.game = game
        super().__init__(name, image)

    def init_all_weapon(self):
        Bomb(self.game)

    def used(self):
        try:
            self.effect()
            self.game.inventory.remove_object(self, 1)
            return False
        except:
            pass

class Bomb(Weapon):
    def __init__(self, game):
        self.game = game
        path = self.game.get_path_assets(r"inventory\objects\weapons\Bomb.png")
        name = "Bomb"
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (48, 48))
        super().__init__(name, image, game, self.effect)

        self.dommage = 20 # de base 20

    def effect(self):
        current_enemy = self.game.fight.current_enemy
        if current_enemy.health - self.dommage > 0:
            current_enemy.health -= self.dommage
        else:
            current_enemy.health = 0