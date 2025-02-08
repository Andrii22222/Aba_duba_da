import random
import pymorphy2
import time

start_time = time.time()

lower_vowels = "аеєиіїоуюя"
upper_vowels = "АЕЄИІЇОУЮЯ"
lower_not_vowels = "бвгджзйклмнпрстфхцчшщ"
upper_not_vowels = "БВГДЖЗЙКЛМНПРСТФХЦЧШЩ"
alphabet = list("аеєиіїоуюябвгджзйклмнпрстфхцчшщ")

morph = pymorphy2.MorphAnalyzer(lang='uk')

cnt_shlack = 0
cnt_norm = 0
while True:
    length = 5  # random.randint(4,10)
    result = (str(random.choice(alphabet))).upper()
    # result = np.random.choice(alphabet).upper()
    for i in range(1, length):
        # result += np.random.choice(alphabet)
        result += str(random.choice(alphabet))

    parsed = morph.parse(result)
    if any(p.is_known for p in parsed):
        cnt_norm += 1
        end_time = time.time()
        all_time = end_time - start_time
        if int(all_time + 1) % 30 == 0:
            print(f"Знайдено шлаку: {cnt_shlack}\nЗнайдено слів: {cnt_norm}")
            print(f"Пройшло: {all_time} секунд!")

        if result == "Артем":
            print("Ура! Слово *Артем* знайдено! На це нам знадобилось: ", all_time)
            print(f"Знайдено шлаку: {cnt_shlack}\nЗнайдено слів: {cnt_norm}")
            break
    else:
        cnt_shlack += 1
# Знайдено шлаку: 91439
# Знайдено слів: 856

# Знайдено шлаку: 57361
# Знайдено слів: 527
