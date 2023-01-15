# hack-roll

JoDoFioFe presents.. a funeral planner for Hack & Roll 2023!

1 Project Title and Aims

The title of our project is 'Everybody Dies'. We know, this may seem like an obvious statement at face value. However, it is precisely because little thought is spared on the topic of death that we believe our project is useful in aiding individuals in much-needed late-stage life planning. Set against a gradually ageing society, we believe more thought needs to be given to death and funerals as a celebration of our lives.

2 Project Description

Our project comprises of 2 main components. The first is the 'Everybody Dies' Telegram bot, that allows users to enter their preferences with regards to their funeral planning. We have come up with a comprehensive list of questions and options that would cater even to all sorts of funeral lovers.

The second part of the project is a webpage built using Flutter for people to virtually view the funeral they designed. The link to the webpage is generated once the user has keyed in all their preferences. They are also able to update their preferences afterward, by simply retaking the assesment in the bot.

3 Project Functionalities

Through the Telegram bot, users are able to customise their e-funerals using the following characteristics:
* Name
* Photo of self
* Religion
* Preferred funeral style
* Preferred flower arrangement
* Preferred casket
* Menu of choice
* Song of choice
* Eulogy speakers
* Parting words of the to-be deceased

Users' funeral preferences are saved as fields in documents on our cloud firestore database. This allows real-time syncing between the answers keyed in by users and our database. If a user were to /cancel their funeral planning midway through using the Telegram bot, their associated database entry will be deleted.

After they have completed using the bot to plan their funerals, a personalised link to their e-funeral is generated using the user's Telegram handle and sent to the user.

The e-funeral is a web app built using Flutter's Dart. The appearance of the funeral parlour is customised according to the users' preferences on style, flower arrangements, casket, etc. Interactive features are included, such as the pop-up menu button that allows users to view their preferred menu choice at their funerals, as well as the mouse-over enlargement of users' photos, and the 'Pay Respects' button that will play users' song of choice when pressed.

Lastly, the user is inactive on Telegram within 7 consecutive days, an invitation will be sent to a chosen list of loved ones whose Telegram handles the user must provide beforehand. Those invited must have used the bot before as well, in order to receive the invitation. Since the bot has yet to be deployed, we have currently set the invitation to be sent out 30 seconds after its creation.

4 Installing and Running Code

Our program requires certain APIs and SDKs to run. Please download the dependencies through inputting the following commands into your terminal.

* pip install python-telegram-bot
* pip install --upgrade firebase-admin
* pip install pyrebase4
* flutter pub add go_router
* dart pub global activate flutterfire_cli
* npm install -g firebase-tools
* flutter pub add firebase_core
* flutterfire configure
* flutter pub add cloud_firestore

5 Tech Stack

For our front-end implementation, we used Flutter's Dart as our programming language. It is a flexible language that would allow us to expand our appliation outside of a web app towards mobile application development in the future.

For our back-end implementation, we used NoSQL in Firebase as our programming langauge. This hcoice would allow us to store massive amounts of data and easy modification of our data model if we chose to add more features to our e-funeral planner.