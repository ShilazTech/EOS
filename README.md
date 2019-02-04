I have strange interests and inquisitiveness. After seeing so many gambling games on various blockchains e.g. magicdice on Steem, Tronbet on Tron, BetDice on EOS and many more - I developed interest to study if there is possibility to predict next roll/s using Artificial Intelligence.

I know it is stretching the limits of AI. There is already so much written about this subject and more or less the conclusion is that it is not possible. I also tend to conclude that but ....I think that these games have two components - random rolling and players behaviour. And both need to be used for predicting next roll.

There are doubts about the fairness of the house from conventional rolling websites as well as data for players is not available so easily.

The best possible dataset that captures above issues, without any malpractices, could be now obtained from one of the above dice dApps. It is because they have implemented provably fair practices that can be proved with the capabilities of blockchain. So the data would represent true gambling behaviour of participants against a truly random mechanism.

It is this observation and conclusion that motivated me to try my AI expertise onto this elusive problem.

As usual first step is always to get data. So I spent a week to learn technicalities of EOS blockchain. Fortunately, a python API on github is now available which can be used to interact with EOS blockchain. And I used that with help from the developers of this API.

I successfully created a python script that collects all the necessary data ["index","roll_blocknumber","from_account","roll_predicted", "user_betvalue","user_currency", "user_seed", "Gameseed", "roll_result", "roll_reward", "roll_value"] from EOS blockchain and writes it into a csv file.

This script does exactly that.
