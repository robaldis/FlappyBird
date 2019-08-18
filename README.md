# Flappy bird
This project is a flappy bids style game that I can add an AI to that will play the game for me.

The game is made with the pygame library with a bird class and a pipe class so I can easily have a lot of birds once I've made the genetic algorithm to tech the birds

# To Run
To run the game. It will run the genetic algorithm from the beginning picking random weights to all the weights and will automatically go to the next generation
```
python main.py
```


## Adding in the brain
To add in the brain I didn't have to do a lot just in the bird class adding in a neural network object that has the 4 inputs 4 hidden layers and one output. The output will be between 1 and 0. if it is 1 then it should flap, if it is 0 it shouldn't.

### Inputs
The next thing to do is make the inputs for the brain so that it can have the most accurate information possible. For this I needed to get the pipe that was up next and get the information like distance from the pipe, distance to the top of the pipe and distance to the bottom of the pipe as well as the birds velocity.

## Genetic algorithm
To train the bird to actually do a good job you need a few things like fitness and loads of birds. The next thing to do is add the genetic algorithm to pick the birds to go into the next generation. This is done by having a random number and taking the fitness away until it equals 0 and choosing that bird to go in the next generation.
The next thing is to setup a new bird with the last birds brain. Then mutating the brains weights a little bit to hopefully making it improve.

## Results
The Birds do very well with just 200 in each generation it takes roughly 16 generations to make a perfect bird that can get through almost any gap.
