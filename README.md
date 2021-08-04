# Lab 8: The Game Loop

## Intro
Now we finally have a full basic game! However, there’s no real challenge or gameplay loop just yet. How are we going to keep our players engaged with the game? For our final lab, we will be completing a game loop, by adding rewards for our player, purchasable towers/upgrades, and increasing monster difficulty level.

There will be no specific coding concepts we will be teaching with this lab. Instead we want you guys to play around with the game and get a feel for balancing the game and creating an engaging game loop. There are tons of levers and pulleys you can pull to adjust the game balance between rewarding the user, and ramping up the difficulty.

Figure out what creates the most engaging game for you and have fun!


## Set Up
* Click the green 'Code' button on the top right of this section.
* Find 'Download ZIP' option and click it
* Unzip the file and move it over to your 'workspace' folder (or wherever you keep your files)

* Find the folder and open the entire folder in VSCode
    * You can find it in your Files and right click on it. Use the "Open with VSCode" option
    * You can also open VSCode, go to 'File' > 'Open' and then find the lab folder

* With VSCode open, go to the top of your window and find `Terminal`
* Click `Terminal`
* Click `New Terminal`
* Run the game with `python run.py`


## Game Explanation
This is an expanded version of tower defense with 4 tower types. The objective is to take down the monsters before they reach the destination flag.

If a monster reaches your flag, then you will lose a life. Lose all your lives, and you lose the game.

We have 4 magic towers:
* Lightning
    * Tower with weak damage but low cooldown. Good for taking down lots of targets.
* Rock
    * Tower with high damage but high cooldown. Higher DPS than lightning, but is slower and can not handle a lot of targets.
* Poison
    * Tower with weak damage that can set the poison status effect. Good against high HP monsters, but takes a while for full damage to take effect.
* Ice
    * Tower with low damage, medium cooldown, and can slow monsters down. Good against all monsters, but can not take monsters down by itself.

Each tower can be upgraded to either boost attack damage or attack speed. The left icon is to boost attack damage, while the right is to boost attack speed.

The bottom X icon is to remove the tower.



We have 4 monster types:
* Fast
    * Most common monster with high speed and low HP.
* Heavy
    * Tanky monster with high HP and low speed.
* Shield
    * Monster with average traits, but ignores first couple counts of damage
* Speed
    * Monster with high HP and very low speed. Will gain speed everytime it gets hit.

## Lab Steps
* All the code you will need to edit is in `loop.py` and the `monsters/` and `towers/` folders
* Everything inside the `engine/` folder are the inner workings of the game. Feel free to take a look, but you won't need to change anything

### Establishing the Game Loop
When you first run the game, it will just run 1 round, and then do nothing. This is because we haven't implemented the Game Loop function yet. 

* Take a look inside of `loop.py`. At the bottom of the file, we have a function called `update`. This function is called on every update loop when the game engine processes a frame (moves forward a step in time).

It should look like this:
```python

    def update(self):
        pass

```

* Right now it does nothing, so when our game encounters a change in the game loop (such as finishing a round) we don't do anything yet!

* Also notice all the helper functions we have in this class. You can use these functions to help you manage the game status (it just simply calls the game engine object)

* Let's start by having our game loop function start a new round once the current round is finished!

* Use the helper function to check if the round is over
* If the round is over, increment the current level by 1 and call the other helper function to start a new round (with the new level value)

You should get something like this
```python

    def update(self):
        if self.is_round_over():
            self.level += 1
            self.start_round(self.level)

```

* Save your file and start up the game with `python run.py`
* Now you should notice that when you finish the current wave of monsters, a new wave will start (and these monsters should be slightly tougher to beat).

* This is cool, but eventually the monsters will be too tough for the player. What we need is to start giving the player points, so that the player can buy new towers, or upgrade their current ones.

* In the update function we just edited, have the function check for any monsters that were recently defeated. For each of those monsters, use the monster's base reward value, and multiply it by the level we are currently on. That way, we can scale the rewards with the toughness of the monster.

You should get something like this
```python

    def update(self):
        if self.is_round_over():
            self.level += 1
            self.start_round(self.level)
        monsters = self.get_defeated_monsters()
        if len(monsters) > 0:
            for monster in monsters:
                reward = monster.get_reward() * self.level
                self.reward_player(reward)

```

* Notice how we iterate through each monster (since there can be multiple defeated monsters) and calculate the reward generated per each one? Then we call the helper function that will reward the player with that amount of currency
* By rewarding the player appropriately, we can allow the player to grow in strength as the game progresses. There is a balance we need to find between rewarding the player too much vs too little.

* Save your file and start up the game again with `python run.py`. You should now be able to earn money and spend it on more towers and upgrades! We have successfully established the game loop!

### Buffing the Monsters
The first thing you might notice is that the monsters are relatively easy once you build up a full tower set. Let's increase the monster's scaling between levels so that we can increase the difficulty as the game goes on.

* Take a look inside the `monsters/fast_monster.py` file
* What you'll notice is that we have the `respawn` function. This is to respawn monsters for the next wave.
* Notice how this function takes in a level and uses it to scale up the monsters hp and speed.
    * The level argument in this method is taken from the game engine. As the level goes up, the difficulty goes up.
* Change this function to increase the fast monster's HP by level * 20. This way, the fast monster will be much more tougher each round

You should get something like this
```python

    def respawn(self, level):
        super().respawn(level)
        # Update hp and speed when the wave gets respawned and difficulty increases
        self.hp = self.BASE_STARTING_HP + level * 20
        self.speed = self.BASE_STARTING_SPEED + level * 4

```

* Save your file.
* Now do the same with `HeavyMonster`, `SpeedMonster`, and `ShieldMonster` (with ShieldMonster, increase it to 40)

* Save your file, and run the game with `python run.py`

* You should now have a much harder challenge each time the level increases!


### Buffing the Towers
Now that our monsters are getting tougher, we should address this by buffing our towers a bit more. Specifically let's increase the attack damage upgrades, so we can handle the monsters' higher HP.

* Take a look inside the `towers/lightning.py` file
* Notice how we have these new functions
    * get_attack_upgrade_price
    * get_speed_upgrade_price
    * upgrade_attack
    * upgrade_speed
* There are two ways for us to buff the lightning tower's attack growth.
* We can either:
    * Increase the amount of attack damage each time it gets upgraded
    * Make the upgrade cheaper, so the player can upgrade more often
* For experiment's sake, let's go with the second option

* Take a look at the `get_attack_upgrade_price` method
* Right now it takes a base cost of 50 and scales it with the `self.attack_level` variable (and divides that in half)
* Notice how the `self.attack_level` increments by 1 every time we upgrade our attack. This is how we scale our cost and values when we grow our tower.
* Let's change this to scale a bit slower (so the player can upgrade the tower more often)
* Change the method to return 50 * self.attack_level * 0.1
* This won't be a big change in the first round, but it'll allow us to cheaply upgrade the tower as the game goes on.

```python

    def get_attack_upgrade_price(self):
        return 50 * self.attack_level * 0.1

```

* Save your file and run the game with `python run.py`


### Buff our Player
You might notice that this isn't a big improvement though. Another way we can buff our player is to increase the amount of rewards we give out. By giving the player more money, we empower the player to make more moves and increase power scale more quickly.

Right now the game is set up to give the player rewards when defeating a monster. Now let's give some rewards out when the player completes a round.

* Go into `loop.py` and find the `update` function again.
* Inside the update function, let's use the `is_round_over` conditional block to also attach a new behavior to the game: Every time a round completes, reward the player a certain amount of money multiplied by the current level.
* Inside the `is_round_over` conditional, create a variable called `round_reward` that will be calculated by multiplying 100 with the current level. 
* Call the `reward_player` method with the `round_reward` variable as an argument.

You should get something like:
```python

    def update(self):
         if self.is_round_over():
            round_reward = 100 * self.level
            self.reward_player(round_reward)
            self.level += 1
            self.start_round(self.level)
         monsters = self.get_defeated_monsters()
         if len(monsters) > 0:
            for monster in monsters:
                reward = monster.get_reward() * self.level
                self.reward_player(reward)

```

* Save your file and run the game with `python run.py`
* You should see your money increase with each score


### Buff the Horde
One issue now is that our money scales faster than the monster health. Let's throw in a new twist by adding new monsters each round.

* Go into `loop.py` and find the `update` function again.
* Notice how we have a ton of helper functions and examples on how to add more monsters to the game. Take note of these for your own purposes.

* Inside the conditional checking if the round is over, add some new code right after you increment the level and right before you call the next round to start
* Use iteration to add (1 * level) new fast monsters and heavy monsters

Your update function should finally look like
```python

    def update(self):
        if self.is_round_over():
            round_reward = 100 * self.level
            self.reward_player(round_reward)
            self.level += 1
            i = 0
            while i < self.level:
                fast_monster = FastMonster(path_1, 8)
                heavy_monster = HeavyMonster(path_1, 10)
                self.add_new_monsters([fast_monster, heavy_monster])
                i += 1
            self.start_round(self.level)
        monsters = self.get_defeated_monsters()
        if len(monsters) > 0:
            for monster in monsters:
                reward = monster.get_reward() * self.level
                self.reward_player(reward)

```

* Now with each level, you will start spawning more and even more monsters! This will definitely ramp up the difficulty.
    * IMPORTANT: Be careful since spawning new monsters can be intensive on your computer. If you try to scale up too fast, you might get a laggy game.
* Save your file and run `python run.py` to play the game!


## On Your Own
Now that we've had some experience adjusting the game balance and scaling up the power on either side, I want you to go ahead and see what you can do to create an engaging game.

* Will you buff both the player and monsters and create some large power scales?
* Will you nerf certain towers and buff certain ones to create an optimal playstyle?
* Will you change up the monster composition and make monsters such as Heavy or Speed become like boss characters?

From here on out it's up to you. Hope you have fun with this and I hope you enjoyed this course!


This code is yours to keep, modify, and play as much as you want. If you ever have any questions or need any help, feel free to reach out to me! `kevin.koh.dev@gmail.com`


Happy Playing!
