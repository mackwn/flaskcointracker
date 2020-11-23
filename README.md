Toy app which tracks cryptocurrency prices using Coinbase API and sends email price notifications based on user create notifications. Uses the Flask framework with Celery and SendGrid to update prices in a background task and send the email notifications. 

<h2>App structure</h2>
<hr>
<ul>
<li>flaskcointracker - main application module</li>
    <ul>
    <li>__init__ - create app and load config</li>
    <li>emails.py</li>
    <li>forms.py</li>
    <li>helpers.py - application logic, primarily handling tasks related to coin price APIs, updating prices, and sending notifications</li>
    <li>models.py</li>
    <li>views.py</li>
    <li>migrations</li>
    <li>tests - testing suite focused on integration of the user and notification system</li>
    </ul>
<li>manage.py - cli tasks especially to seed database with cryptocurrency types</li>
<li>requirements.txt</li>
<li>run.py - command for running application in development </li>
</ul>

<h2>Requirements</h2>
<hr>
App developed with Python version 3.8.6. 

Production version requires Redis and Postgres to be installed. Email notifications require a SendGrid account with a verified domain. 

<h2>Environment Configuration</h2>
<hr>

<h3>Local development</h3>
<ul>
<li>Create .env and populate with the following key value pairs</li>
    <ul>
    <li>SENDGRID_API_KEY - obtain from sengrid account</li>
    <li>SECRET_KEY - set to a secure value</li>
    <li>MAIL_DEFAULT_SENDER - should be set to an verified domain on your sendgrid account</li>
    <li>NOREPLY - no reply email address for notifications - should be verified sendgrid domain</li>
    <li>ADMIN_EMAIL - email to send feedback to</li>
    <li>FLASK_APP=flaskcointracker</li>
    </ul>
<ul>

<h3>Docker development</h3>
<ul>
<li>Create development.env and populate with the following key value pairs</li>
  <ul>
    <li>SENDGRID_API_KEY - obtain from sengrid account</li>
    <li>SECRET_KEY - set to a secure value</li>
    <li>MAIL_DEFAULT_SENDER - should be set to an verified domain on your sendgrid account</li>
    <li>NOREPLY - no reply email address for notifications - should be verified sendgrid domain</li>
    <li>ADMIN_EMAIL - email to send feedback to</li>
    <li>FLASK_APP=flaskcointracker</li>
    <li>FLASK_ENV=dvelopment</li>
    <li>REDIS_URL='redis://redis:6379/0'</li>
    <li>DATABASE_URL='postgresql://cointrackerdb:cointrackerdb@db:5432/cointrackerdb_prod'</li>
    <li>POSTGRES_USER=cointrackerdb</li>
    <li>POSTGRES_PASSWORD=cointrackerdb</li>
    <li>POSTGRES_DB=cointrackerdb_prod</li>
    </ul>ul>

<h3>Docker production</h3>
<ul>
<li>Create production.env and populate with the following key value pairs</li>
    <ul>
    <li>SENDGRID_API_KEY - obtain from sengrid account</li>
    <li>SECRET_KEY - set to a secure value</li>
    <li>MAIL_DEFAULT_SENDER - should be set to an verified domain on your sendgrid account</li>
    <li>NOREPLY - no reply email address for notifications - should be verified sendgrid domain</li>
    <li>ADMIN_EMAIL - email to send feedback to</li>
    <li>FLASK_APP=flaskcointracker</li>
    <li>FLASK_ENV=production</li>
    <li>REDIS_URL='redis://redis:6379/0'</li>
    <li>DATABASE_URL - format should be postgresql://[user]:[password]@db:5432/[db]</li>
    <li>POSTGRES_USER - set to a secure value</li>
    <li>POSTGRES_PASSWORD - set to a secure value</li>
    <li>POSTGRES_DB - set to a secure value</li>
    </ul>
<ul>

<h2>Running Application<h2>
<hr>
<h3>Locally</h3>

<ul>
<li>Ensure environment variables are set up in .env</li>
<li>Run the following commands</li>
<ul>
<li>flask db upgrade - create database with most recent migration</li>
<li>python manage.py seed_db - load database with crpytocurrencies</li>
<li>redis-server - run redis in another terminal</li>
<li>celery worker -A flaskcointracker.celery - start celery worker in another terminal</li>
<li>celery beat -A flaskcointracker.celery - start celery periodic task in another terminal</li>
</ul>
<li>App should now be available on :5000</li>
</ul>

<h3>Docker - production</h3>

<ul>
<li>Ensure environment variables are set up in production.env and postgres.env</li>
<li>Run the following commands:<li>
<ul>
<li>docker-compose -f docker-compose.prod.yml up -d </li>
<li>docker-compose -f docker-compose.prod.yml exec web flask db upgrade</li>
<li>docker-compose -f docker-compose.prod.yml exec web python manage.py seed_db</li>
</ul>
<li>App should now be available on :5000</li>

</ul>




