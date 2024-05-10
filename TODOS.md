# TODOS of Molkovich Game Development

This document outlines the current state of the Molkovich game development, highlighting completed functionalities, features in progress, and aspects yet to be implemented.

## Completed Use Cases

- **Star-like dots:** The Dot class creates elements that move from right to left, resembling stars in the background.
- **Spaceship:** The Player class defines the spaceship sprite with movement controls.
- **Enemies:** The Enemy class creates enemy sprites, currently stationary.
- **Bullet firing:** The Player.fire_bullet() function allows the player to shoot bullets (blue rectangles) moving right.
- **Big bullet firing:** The Player.fire_big_bullet() function enables firing larger white bullets that move right.
- **Dots:** The Dots class represents green dots appearing on the screen.
- **Point collision:** The GameWindow.update() function detects collisions between the player and points.
- **Sounds:**
  - SoundManager.play_bullet_sound() plays a sound when firing bullets.
  - SoundManager.play_big_bullet_sound() plays a sound when firing big bullets.

## Uncompleted Use Cases

- **Enemy movement:** Enemy sprites are not moving yet. Implement logic in the Enemy class to make them move from right to left.
- **Hit detection:**
  - Enemy hit detection is missing.
  - Player hit detection needs to be implemented.
- **Enemy destruction:** Enemies should be destroyed upon being hit by a player's bullet or big bullet. This logic needs to be incorporated.
- **Explosion effects:** Visual effects for enemy and player explosions are not implemented.
- **Molkovich (Boss):**
  - The boss logic for Molkovich's appearance is not yet defined.
  - Molkovich's sprite and sounds (appear, hit, attack, roar, etc.) are missing.
- **Start page:** The game lacks a start menu with a logo, credits, and playing instructions.
- **Timer for Molkovich:** A timer that triggers Molkovich's appearance at a random point in the game is not implemented.
- **Background music:** While mentioned in the notes, the code doesn't include background music functionality. Implement SoundManager.play_background_music() to add it.

## Suggestions

Here is some other things that I would like to maybe add to the game.

- **Power-Ups:** Introduce power-ups that enhance the player's abilities or grant temporary advantages such as increased firepower, shield protection, or temporary invincibility.
- **Dynamic Level Design:** Create diverse and challenging levels with unique obstacles, enemy formations, and environmental hazards that require strategic maneuvering and timing.
- **Boss Battles:** Design epic boss encounters inspired by iconic bosses from Sinistar and R-Type, each with distinct attack patterns, phases, and weaknesses for the player to exploit.
- **Upgrade System:** Implement an upgrade system where players can customize and improve their spaceship's attributes, weapons, and defenses between levels or by collecting specific items during gameplay.
- **Multiplayer Mode:** Add a cooperative or competitive multiplayer mode where players can team up to tackle challenges together or compete against each other in intense space battles.
- **Visual Effects Overhaul:** Enhance the game's visual effects with stunning particle effects, dynamic lighting, and immersive animations to create a more immersive and visually appealing experience.
- **Storyline and Narrative:** Develop a compelling storyline with engaging characters, plot twists, and narrative-driven missions that unfold as players progress through the game.
- **Alternate Endings:** Introduce multiple endings based on the player's choices and performance throughout the game, providing replay value and encouraging different playstyles.
- **Achievements and Challenges:** Incorporate achievements, challenges, and leaderboards to incentivize players to explore every aspect of the game and compete for high scores and bragging rights.
- **Easter Eggs and References:** Include hidden Easter eggs, references to delight players and add an extra layer of charm to the game.
