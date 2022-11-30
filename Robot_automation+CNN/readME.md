# Binary Text Classification Trump VS Elon 
## Summary
First I use the Robot Framework to scrape the latest tweets of both Elon's and Trump's twitter accounts. Then I deploy a 1 dimentional convolutional neural network to the text data and predict who tweeted what tweet.

Note: the presentation used to talk about the different ways to encode text data is featured in the file.

The two parts are 

## Robot automation

In the ```project/robot_automation``` file you will find the 3 main files required to run the script these are ```keywords.robot``` ```robot.robot``` ```variables.py```.

The main robot file ```robot.robot``` contains the task the robot is going to complete when run. It references the ```variables.py``` file which contains the number of tweets to be scraped, twitter url, and the username of the account to be scraped.

The file ```keywords.robot``` contains the main instructions that do the taks.

We have two sections ```Settings``` and ```Keywords```. The ```Settings``` include the two libraries we use.

The ```Keywords``` section has all our keywords and the general approach. From a high-level overview we open chrome locate the tweets then we loop through them and create a text file put them in the ```/output/tweets``` folder.

**NOTE**: The datasets that I am using are not directly made from the twitter data that I have scraped, there are 2 reasons for that:
- Twitter allows to to scrape only 4 tweets without an account and then asks you to sign in.
- Instantaneously having 5 thousand reccords saves time and proved the data-hungry CNN algorithum with more records. After all combining text files into a dataframe column is not that big of a technical challange.



## Machine Learning

In the ```text_cnn_model``` jupyter notebook I am solving a Binary text classification with convolutional neural network.

Here are the data sourses for the two csv files for [Trump](https://data.world/briangriffey/trump-tweets) and [Elon](https://data.world/adamhelsinger/elon-musk-tweets-until-4-6-17).

There are comments explaining the code. Note that in there I use the more scientific 'we' pronoun.
