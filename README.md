---
# 🐍 Snake Game (with AI!) 🧠

Welcome to the classic game of Snake... but turbocharged with AI brains 🧠 and a sleek modern look! Whether you're in the mood to flex your WASD fingers or just watch a digital serpent solve mazes on its own, this project has you covered.

---

## 📚 Table of Contents

- [🎮 Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🧠 How the AI Works](#-how-the-ai-works)
- [🧰 Requirements](#-requirements)
- [▶️ How to Run](#-how-to-run)
- [🛠️ File Structure](#-file-structure)
- [✨ Fun Extras](#-fun-extras)
- [🧪 Customize Me!](#-customize-me)
- [❓ FAQ](#-faq)
- [🧑‍💻 For Developers](#-for-developers)
- [📄 License](#-license)
- [🧙‍♂️ Credits](#-credits)

---

## 🎮 Features

* **Two Game Modes**:
  - 🎮 **Human Mode**: Control the snake with **WASD** keys.
  - 🤖 **AI Mode**: Watch the computer slither smartly with **A*** pathfinding.
* **Dynamic difficulty**: The snake gets faster as it grows. Gotta go fast!
* **Screen wrap-around**: Bounce off one side, appear on the other. Snake magic.
* **Stylish graphics**: Rounded corners, soft shadows, layered colors. Your eyeballs will thank you.
* **High score tracking**: Your best run is remembered! Can you beat yourself?

---

## 📸 Screenshots

Human vs AI... pick your poison 🐍

![Human playing](images/human.png)  
![AI playing](images/ai.png)

---

## 🧠 How the AI Works

The AI uses a simplified **A*** pathfinding algorithm that:

* Treats the snake’s body as obstacles,
* Uses a Manhattan distance heuristic (and accounts for screen wrap),
* Finds the shortest path to food,
* Falls back to its current direction if it’s cornered like a scared pixel.

Bonus: There's also a `decide_move_simple()` function in the code that uses a greedy approach instead. It's not enabled by default, but feel free to try it!

---

## 🧰 Requirements

* Python 3.8+
* `pygame`  
  Install it with:

```bash
pip install pygame
````

---

## ▶️ How to Run

Clone this repo and run the main file:

```bash
python snake_ai.py
```

When the menu appears:

* Press **1** to play as the snake (Human Mode).
* Press **2** to watch the AI play (AI Mode).

**Controls (Human Mode):**

* W / A / S / D to move
* ESC or close the window to quit

---

## 🛠️ File Structure

```
snake_ai.py     # The main game file with all logic inside
images/         # Screenshots used in this README
```

You don’t need any assets — everything is generated with `pygame`.

---

## ✨ Fun Extras

* 🧠 The AI makes decisions in real time every frame.
* 🍎 The food location changes, and the snake adapts instantly.
* 💥 Game over happens when you hit yourself. Just like in life, don't tailgate yourself.
* 📈 The score is shown live, and your highest score is saved between runs.

---

## 🧪 Customize Me!

Want to make it more YOU? Go wild:

* 🎨 Adjust `CELL_SIZE`, `WIDTH`, `HEIGHT` for different board sizes.
* 🤓 Swap `decide_move_astar()` with `decide_move_simple()` to see how a greedy snake performs.
* 💅 Tweak colors, fonts, snake speed, or food behavior for aesthetic chaos.

---

## ❓ FAQ

**Q: Why does the AI sometimes crash into itself?**
A: Imagine planning your route home but growing halfway there and blocking your own path. That’s what happens. The AI doesn’t predict growth after eating food, so it sometimes unknowingly traps itself.

**Q: Can the AI survive forever?**
A: Not quite. It's clever, but not clairvoyant. You can challenge it by placing food close to its tail or walls (manually or via mods).

**Q: Where is the high score saved?**
A: It’s stored in a file called `highscore.txt`. It’s automatically created and updated when you beat your previous record.

---

## 🧑‍💻 For Developers

Want to soup up the snake? Here's how the code's laid out:

* `Game` class: Handles the game loop, input, drawing, etc.
* `Snake` class: Manages position, movement, growth, and self-collision.
* `Food` class: Chooses random locations and respawns.
* `decide_move_astar()`: Main AI logic (using A\* pathfinding).
* `decide_move_simple()`: A fallback greedy AI for testing or chaos.

🧠 Try implementing:

* Hamiltonian cycle AI
* Reinforcement learning
* Multiple snakes 🐍🐍
* Boss battles (food fights?)

---

## 📄 License

MIT License.
Fork it, remix it, ship it, snake it.
Just don’t sue me if it eats your RAM. 🐍💾

---

## 🧙‍♂️ Credits

Coded with 🧠, 🎨, and probably too much ☕.
Built using [Pygame](https://www.pygame.org/).
Inspired by the eternal struggle of snake vs tail.

---