#Main

import telebot 
from random import randint
from logic import Pokemon, Wizard, Fighter

bot = telebot.TeleBot("7974971011:AAEZGKHDhWFH2Por9DR98N1xs8u-28xr0BI") 

@bot.message_handler(commands=['go'])
def go(message):
    if message.from_user.username not in Pokemon.pokemons.keys():
        chance = randint(1,3)
        if chance == 1:
            pokemon = Pokemon(message.from_user.username)
        elif chance == 2:
            pokemon = Wizard(message.from_user.username)
        elif chance == 3:
            pokemon = Fighter(message.from_user.username)  
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_photo(message.chat.id, pokemon.show_img())
        
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")

@bot.message_handler(commands=['attack'])

@bot.message_handler(commands=['feed'])
def feed_pok(message):
    if message.from_user.username in Pokemon.pokemons.keys():
        pok = Pokemon.pokemons[message.from_user.username]
        response = pok.feed()
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "You dont have a Pokemon")



bot.infinity_polling(none_stop=True)

#Logic

from random import randint
import requests
from datetime import datetime, timedelta

class Pokemon:
    pokemons = {}
    # Инициализация объекта (конструктор)
    def __init__(self, pokemon_trainer):
        self.last_feed_time = datetime.now()


        self.pokemon_trainer = pokemon_trainer   

        self.pokemon_number = randint(1,1000)
        self.img = self.get_img()
        self.name = self.get_name()
        self.hp = randint(30,60)
        self.power = randint(30,60)
        


        Pokemon.pokemons[pokemon_trainer] = self

    # Метод для получения картинки покемона через API
    def get_img(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['sprites']['other']['official-artwork']['front_default'])
        else:
            return "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/home/shiny/1.png"
    
    # Метод для получения имени покемона через API
    def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return (data['forms'][0]['name'])
        else:
            return "Pikachu"

    def feed(self, feed_interval = 20, hp_increase = 10 ):
        current_time = datetime.now()  
        delta_time = timedelta(seconds=feed_interval)  
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Здоровье покемона увеличено. Текущее здоровье: {self.hp}"
        else:
            return f"Следующее время кормления покемона: {self.last_feed_time+delta_time}"


    # Метод класса для получения информации
    def info(self):
        return f"Имя твоего покеомона: {self.name} pokemons power: {self.power} pokemons health: {self.hp}"

    # Метод класса для получения картинки покемона
    def show_img(self):
        return self.img

    def attack(self, enemy):
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return f"Сражение @{self.pokemon_trainer} с @{enemy.pokemon_trainer}"
        else:
            enemy.hp = 0
            return f"Победа @{self.pokemon_trainer} над @{enemy.pokemon_trainer}! "

class Wizard(Pokemon):
    def attack(self, enemy):
        if isinstance(enemy, Wizard): # Проверка на то, что enemy является типом данных Wizard (является экземпляром класса Волшебник)
            chance = randint(1,5)
            if chance == 1:
                return "Pokemon the Wizard used his shield in the fight"
    def info(self):
        return "Your pokemon is wizard"+super().info()
    def feed(self):
        return super().feed(hp_increase=20)


class Fighter(Pokemon):
    def attack(self, enemy):
        super_power = randint(5,15)
        self.power += super_power
        result = super().attack(enemy)
        self.power -= super_power
        return result + f"\nThe fighter used his superpower:{super_power} "
    def info(self):
        return "Your pokemon is fighter"+super().info()
    
    def feed(self):
        return super().feed(hp_increase=10)

