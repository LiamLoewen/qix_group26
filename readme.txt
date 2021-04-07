So we'll call this version 2.2: 2 being we are making the sequel to Qix, .2 being the second time it's been 'pushed' to our group.

Major areas that need work:
1. Qix
    1.1. The Qix needs a more advanced movement algorithm than just random direction
    1.2. The Qix has no wall collision, so it needs detection/rebound angle calculation
    1.3. The Qix doesn't reset the player if it hits the line being drawn
2. Sparxs
    2.1. The Sparx haven't been coded at all
3. Player   
    # New Feature: Hold SPACE to draw a line
    3.1. Everything about drawing lines is sound, besides the fact that you can draw them through already ''drawn off' areas
    3.2. The player should have 3 lives displayed on the HUD
4. Game state
    4.1. The '0%' coverage is a placeholder function that hasn't been coded yet
    4.2. A point system should also be displyed in the HUD 
    4.3. The 'RESET' button is likely only temporary and should be replaced by a pause menu
    4.4. 'Drawn off' areas should turn a different colour
    4.5. Cosmetically the HUD is pretty ugly so feel free to change fonts/colours etc.