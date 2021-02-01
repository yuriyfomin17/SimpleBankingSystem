hero_damage = 100


def double_damage():
    global hero_damage
    hero_damage = 2 * hero_damage


def disarmed():
    global hero_damage
    hero_damage = 0.1 * hero_damage


def power_potion():
    global hero_damage
    hero_damage += 100


x = 10
if x > 100:
    print(x)
elif x == 10:
    print(x)
