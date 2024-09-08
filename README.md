| Файл | Описание |
|---   |---       |
# Shooter
###### Создание прототипа игры шутер

---

| Файл | Описание |
|---   |---       |
| Супер-пупер Шутер.exe| Исполняемый файл |
| shooter_game.py | Главный файл для запуска |
| asteroid.png | Файл препятсвия |
| galaxy.jpg | Файл заднего фона |
| bullet.jpg | Файл пули |
| rocket.jpg | Файл персонажа |
| ufo.jpg | Файл врагов |
| space.ogg | Фоновый звук |
| fire.ogg | Звук выстрела |

Список задач:
- [x] ~~Создать экран~~
- [ ] Создать класс GameSprite
- [ ] Создать класс Player
- [ ] Создать игровой цикл
- [ ] Создать условия выигрыша и проигрыша
- [ ] Сделать проверку столкновений
- [ ] Сделать исполняемый файл

```python
pyinstaller --onefile -n "Shooter" ./shooter_game.py
```