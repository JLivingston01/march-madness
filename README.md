# MARCH MADNESS

This is an ML approach to pick winners in the NCAA men's basketball tournament. The strategy applied here is to predict how deep into the tournament each team will go. This strategy took second place in my 2022 Tourney, aka I'm the first loser. Let's do it again in 2023, but better.

## The Strategy

Tournament progress is encoded as:

Champs: 1  
Finals: 2  
Final Four: 4  
Elite Eight: 8  
Sweet 16: 16  
...  
Not in tourney: 128

Efficiency and Percentage statistics for each team since 2008, along with end-of-tourney finish are obtained from:  
https://barttorvik.com/#  

Most features are taken from E&P stats, along with conference membership info.  

For a particular match-up in the tournament the team with the lower predicted tournement progress is naively selected as the winner (e.g. team 1 predicition: 8.5, team 2 prediction: 10.25 - team 1 is chosen as the game's predicted winner).

