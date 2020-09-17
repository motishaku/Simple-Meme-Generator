# Simple-Meme-Generator
A meme generator made with Flask in python 3.7.

## Features
* User system
* SQLite / MYSQL database.
* Each module separated by blueprints for easy adaptations and adjustments.
* Base templates upload system.

## Database
As default, a SQLite database is being used, in order to setup MYSQL database instead, all you have to do is install pymysql driver and change the app configuration value to:
> mysql+pymysql://username:password@mysql-address/db_name

##Todo
* Add permission system with more admin functionality.
* Improve meme making system and add more text editing features.
* Add a platform for user to share their memes.
