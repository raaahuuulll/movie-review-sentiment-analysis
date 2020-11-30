# Movie review sentiment analysis
## About the project
This project is a simple sentiment analysis model that classifies the review into positive or negative. The model is trained on the [Imdb dataset](http://ai.stanford.edu/~amaas/data/sentiment/).
For usage, the project has been deployed on to the web using [Heroku](https://www.heroku.com/) on (https://moviereview-analyser.herokuapp.com/).
Please do check it out :smiley: and drop a star :star: to this repo if you like it.

### Built with
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Bootstrap](https://getbootstrap.com/)
* [jQuery](https://jquery.com/)

## Getting Started
To make a local copy of the repository and getting it up and running, follow the steps:

### Prerequisites
* Python (I've used Python v3.7.3)
* pip (The Python Package Installer)
* virtualenv package `pip install virtualenv`

### Installation
1. Clone the repo and change the working directory.
   ```sh
   git clone https://github.com/raaahuuulll/movie-review-sentiment-analysis.git
   cd movie-review-sentiment-analysis
   ```
2. Create and activate the virtual environment to avoid any conflicts with the installed packages.
   ```sh
   virtualenv env
   env\scripts\activate
   ```
3. Install the required packages.
   ```sh
   pip install -r requirements.txt
   ```
4. Download the [dataset](http://ai.stanford.edu/~amaas/data/sentiment/) and extract it in our directory in the `aclImdb` folder. Create the folder if it does not exist.
5. Processing the data before training the model.
   ```sh
   python processing.py
   ```
6. Training and saving the model for further use.
   ```sh
   python train.py
   ```
   The working directory would be looking like this up till this step
   ![woking_directory(ss)](imgs/ss1.png?raw=true "Working Directory")

7. That's it. The model is now ready to make the predictions. Start up the Flask server.
   ```sh
   python app.py
   ```
The Flask development server will be started.
![final screenshot](imgs/ss2.png?raw=true "Flask server output")
