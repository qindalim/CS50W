# Crypto Portfolio

## Project Introduction

Crypto Portfolio is an app to track your cryptocurrency portfolio. In this project, we will refer to cryptocurrency as "coins". This project is done solely for simulation and educational purposes. Please do your due diligence and happy investing!

## Distinctiveness and Complexity

Distinctiveness <br>

Since I invest and trade frequently, I often want to have an app to simulate my "what-if" investments easily by fetching live data and calculating hypothetical profits if I were to invest in certain coins. Even though a similar live tracking function is widely available on many exchanges, they would usually involve the real trading of cryptocurrency and calculation of real profits - and that is not ideal because I do not want to invest in coins that I am not confident enough in. Also, simulation websites that are currently available do not pull live prices from the exchanges immediately. Hence, to allow for a personal simulation that does not involve real trading, I have decided to create this app to help me in my investment decision making. 

Complexity <br>

In summary, this app allows users to maintain a portfolio of coins by adding and deleting coins easily. To allow for accurate data to be fetched from the "ccxt" - the CryptoCurrency eXchange Trading Library, user input especially the ticker will be verified first before being posted. Each coin also has a unique ID tagged to it to allow the correct prices and profits to be inputted into the correct rows of coins. Since the main purpose of this app is to increase the convenience for the user, most of the process is being automated in the backend, from the storing of coins to the automated fetching of live prices and calculation of profits and total profits. Once a coin is being inputted, the page refreshes to fetch all the live prices and calculate the live profits after a short delay given to resolve the promise. Everytime the user refreshes the page, as long as the exchange is open, live prices and profits will be updated accordingly. If the user chooses to remove the coin from his portfolio, a simple click on the delete button would remove the coin completely from the app after confirmation. If the user wants to view just his profits comprehensively in a single page, going to the profits page would render such a view for the user to examine his portfolio extensively. The final touch to this project is that the profit fields will turn green whenever there is positive profit, and red when there is a loss. <br>

When the user switches account or another user registers for a new account, it will be a brand new portfolio with no coins. The user can then start adding coins again and build his portfolio from scratch. <br>

Lastly, a superuser is also created to handle the admin page. This user is mainly used for backend maintenance to monitor for bugs and changes in the Django model, and will not interfere with any actions done on the user side. Since this app is only made for simulation and educational purposes, user data would not be leaked since it does not involve real life trading and profits. 

## Project Setup

In your terminal, cd into the capstone directory and run the following code to make migrations for the crypto app and apply the migrations to your database. The last line of code would then start up the Django web server. From there, visit the website in your browser and start using its functions!

```
python manage.py makemigrations crypto
python manage.py migrate
python manage.py runserver
```

## File Description
In the code is a Django project called capstone that contains a single app called crypto. 

Open up crypto/urls.py, where the URL configuration for this app is defined. This includes a default index route, a /login route, a /logout route, a /register route and several other routes that lead to the other secondary pages contained within this app for completion. 

Open up network/views.py to see the views associated with each of these routes. The index view returns an index.html page that contains the main functionalites of this app, including the addition and deletion of coins, fetching of live data and profit calculation. The add_coin and delete_coin views receive requests and make changes to the Django model through the addition or deletion of an entry respectively. The login_view view renders a login form when a user tries to GET the page. When a user submits the form using the POST request method, the user is authenticated, logged in, and redirected to the index page. The logout_view view logs the user out and redirects them to the index page. Finally, the register route displays a registration form to the user, and creates a new user when the form is submitted. 

Open up network/models.py to see the models associated with this project. This project utilises the User model for authentication purposes, and 1 other Portfolio model which stores all the essential information of the coins bought by the user, such as the buying price and quantity, coin name, as well as the ticker.

Open up the templates folder. This folder contains all the html files to the respective webpages, and also the main layout.html file that all the webpages inherit their layouts from. Since this app allows for tracking and storing of personal investments, all the functions would only be made available if the user is logged in. The index.html file renders a webpage that allows a user to add new coins to his portfolio, which will be stored in the Portfolio model in the backend. This data will be stored permanently in the model, unless the user chooses to delete the coin from his portfolio. In the process of adding coins, there will be a correctness check, where all fields have to be filled and a valid ticker has to be used before the coin is added. Otherwise, the user would have to fill the form again. This is to faciliate the fetching of live prices. In the same page, the user would be able to view all his coins in a consolidated table below, which would fetch all the live prices of the respective coins from "ccxt" automatially and calculate their profits at that point in time. In this table, the user can also choose to delete his coin to remove it from his portfolio, and the corresponding entry will be removed from the Django model in the backend after confirmation. The folder also contains the about.html, profile.html and profit.html files, that render webpages to show the about page, profile page and profit pages respectively. The about page gives an introduction of the application, the profile page shows the user name, ID and email, while the profit page is a simplified version of the index.html page that only shows the current portfolio and profits. Lastly, the folder also contains the login.html and register.html pages that render the login and register pages for user authentication.
