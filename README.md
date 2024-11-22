# Paperboy Game

A side-scrolling arcade game where you play as a paperboy delivering newspapers while dodging various obstacles. Built with Python and Pygame.

## Game Description

In this retro-style game, you control a paperboy who must deliver newspapers to houses while avoiding obstacles like cars, police, dogs, and barriers. The game features:

- Side-scrolling gameplay
- Newspaper throwing mechanics
- Multiple obstacle types
- Scoring system
- Lives system

## Installation

1. Ensure you have Python 3.7+ installed
2. Clone the repository:
   ```bash
   git clone https://github.com/ekzwixoe/paperboy-game.git
   cd paperboy-game
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Controls

- ⬆️ Up Arrow: Move paperboy up
- ⬇️ Down Arrow: Move paperboy down
- Spacebar: Throw newspaper

## Game Mechanics

- **Player**: Control the paperboy moving up and down
- **Newspapers**: Throw them at houses to score points
- **Houses**: Hit them with newspapers to score
- **Obstacles**: Avoid various moving obstacles
- **Lives**: Start with 3 lives, lose one when hitting obstacles
- **Score**: Earn points for successful deliveries

## Project Structure

```
paperboy-game/
├── paperboy_game.py    # Main game file
├── requirements.txt    # Python dependencies
├── assets/            # Game assets directory
│   └── README.md      # Asset requirements
└── README.md          # This file
```

## Development Log

### Version 0.1 (Current)
- Initial game setup with Pygame
- Basic game mechanics implemented:
  - Player movement
  - Newspaper throwing
  - Obstacle generation
  - Collision detection
  - Score tracking
  - Lives system
- Placeholder graphics using colored rectangles
- Basic game loop and physics

### Planned Features
- Custom sprite graphics:
  - Paperboy character (50x50px)
  - Newspaper projectile (20x20px)
  - House variations (60x60px)
  - Various obstacles (40x40px)
- Sound effects
- Background music
- High score system
- Level progression
- Animation systems

## Technical Details

### Current Implementation
- **Player Class**: Handles paperboy movement and state
- **Newspaper Class**: Manages projectile physics
- **Obstacle Class**: Controls various moving obstacles
- **House Class**: Manages target buildings
- **Collision System**: Pygame sprite collision detection
- **Scoring System**: Points for successful deliveries

### Dependencies
- Python 3.7+
- Pygame 2.4.0

## Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/new-feature`
3. Commit your changes: `git commit -am 'Add new feature'`
4. Push to the branch: `git push origin feature/new-feature`
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Development Notes

### Current Status
- Basic game mechanics implemented
- Placeholder graphics in use
- Core gameplay loop functioning
- Need to add custom sprites and assets

### Next Steps
1. Create and implement custom sprite assets
2. Add sound effects and background music
3. Implement scoring system improvements
4. Add game start/end screens
5. Enhance obstacle variety and behavior

### Known Issues
- None currently reported

## Contact

Project maintained by ekzwixoe (ekz.wi.xoe@gmail.com)
