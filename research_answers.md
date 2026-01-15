# Research Answers

## How HTTP Keeps Track of User Information

HTTP is a system where each time you ask for something from a website, it's like starting fresh - the website doesn't remember what you did before. To fix this and keep track of things like who you are when you log in, websites use special tools:

- **Cookies**: Small pieces of information saved in your web browser. Every time you visit the site, your browser sends these cookies back, so the site knows it's you.

- **Sessions**: The website saves your information on its own computer, and gives you a special code (stored in a cookie) to prove who you are.

- **Tokens**: Special codes given to you when you log in. You send this code with every request to show you're allowed to access certain things.

This helps websites remember if you're logged in, keep items in your shopping cart, and show content just for you.

## Moving Django Data to MariaDB

To move a Django website's data to a MariaDB database (a type of database that stores information in tables), follow these steps:

1. **Set up the database connection**: In Django's settings file, tell it to use MariaDB instead of the default database. Add the database name, username, password, and where the database is located.

2. **Install the needed software**: Make sure you have the right Python tool installed to connect to MariaDB.

3. **Create migration files**: Run a Django command to make files that describe how to change the database structure.

4. **Apply the changes**: Run another Django command to actually update the MariaDB database with your changes.

For real websites, be careful with these steps to avoid losing data or causing problems.