# animal_chess
"Jungle" also known as "Animal Chess" is a simple game for two players, played on a 7×9 board containing 4 types of squares: meadows (.), traps (#), dens (*) and ponds (~). The board looks as follows:

`.` `.` `#` `*` `#` `.` `.`  
`.` `.` `.` `#` `.` `.` `.`  
`.` `.` `.` `.` `.` `.` `.`  
`.` `~` `~` `.` `~` `~` `.`  
`.` `~` `~` `.` `~` `~` `.`  
`.` `~` `~` `.` `~` `~` `.`  
`.` `.` `.` `.` `.` `.` `.`  
`.` `.` `.` `#` `.` `.` `.`  
`.` `.` `#` `*` `#` `.` `.`  

Each player initially has a set of 8 pieces: rat (R), cat (C), dog (D), wolf (W), leopard (J), tiger (T), lion (L), elephant (E). The order in the previous sentence also defines the ranking of the pieces.

Initially, the pieces are arranged as follows:

`L` `.` `.` `.` `.` `.` `T`  
`.` `D` `.` `.` `.` `C` `.`  
`R` `.` `J` `.` `W` `.` `E`  
`.` `.` `.` `.` `.` `.` `.`  
`.` `.` `.` `.` `.` `.` `.`  
`.` `.` `.` `.` `.` `.` `.`  
`e` `.` `w` `.` `j` `.` `r`  
`.` `c` `.` `.` `.` `d` `.`  
`t` `.` `.` `.` `.` `.` `l`  

The following rules apply:

• A player cannot enter their own den.
• Only the rat can enter the water.
• A normal move involves moving a piece to an adjacent empty square in any direction (up, down, left or right).
• The tiger and lion can jump over ponds (to make a jump, the piece must enter the pond and then move in the same direction until reaching a square that is not a pond). It is not allowed to jump over an enemy rat.
• Moving a piece onto a square occupied by another piece is equivalent to capturing it. A piece can capture another piece of equal or lower rank. Contrary to the ranking, a rat is stronger than an elephant. Otherwise, the ranking corresponds to the strength of the pieces.
• A rat cannot capture while moving from a pond to land.
• A piece in a trap (one of the squares surrounding the den) loses all its strength and can be captured by any piece.
• The objective of the game is to enter the opponent's den. After such a move, the game ends and the player entering the den wins.

These traditional rules require a slight complication to prevent trivial draws by blocking one's den with "impassable" barriers. A new rule is as follows: If there is no capture or entering of a den within the next 30 moves, the game ends and the winner is determined:
a) by comparing the ranks of the pieces: the player with the highest-ranked piece not possessed by the other player wins,
b) if the players have exactly the same pieces, then the player who moved second wins.

This program will simulate an agent that plays Jungle. It will choose a move in the following way:

1) At any given time, it will generate all possible moves, make each of them, and run a board evaluation procedure. I will call the set of resulting situations S.
2) Of course, It will choose the move that gives the most advantageous situation.
3) The agent evaluates the situation s ∈ S by conducting fully random games starting from s (let's assume that the i-th game has K_{i} moves).
4) During the entire analysis, the agent will be allowed to simulate N = sum of K_{i} for all i moves. 

To compile: ``python main.py``
