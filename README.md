# Job and Resource Tracking Application
### Overview
This project is a Flask-based web application, designed for internal use at [JOT Finishing in Rochester, NY](https://www.mapquest.com/us/new-york/jot-finishing-413254536). While the data from JOT Finishing will remain private, this repository may serve as guide for similar projects or it may be used by other manufacturing companies as is.  
The application consists of user authentication, data collection for company jobs, and analytic dashboards showing job trends and resourse usage. Additionally, I implemented a tool allowing admin-level users to estimate the amount of time and resources a given job will take (**coming soon**). Future versions of the estimation and analytic features could integrate more sophisticated ML forecasting techniques, however JOT finishing does not currently have enough data for such approaches to be appropriate.

### Features
- **User Authentication:** Admin can add new users to the system with verying levels of access. All users may log in, log out, and reset their password with a one-time reset link sent via email. 
- **Role Management:** Roles in the system include admin level and general users. Admin has access to more detailed data dashboards and the estimation feature, along with the authority to view all users in the system, register new users, add parts, and update roles.
- **Parts Management:** JOT specifically works with metal parts, as specified by their customers. Admin may add new parts to the system as needed; the resulting parts list is referenced in the job data collection form.
- **Job Data Collection:** Users complete a form to record part they are working with and the task they are completing; the task is then timed in batches (specified by the user) and these times are recorded in a database table along with the form inputs. **Resource data collection will be added in later versions**
- **Time/Resource Estimation:** **Coming soon.** Admin will have access to a tool that pulls from existing job data to estimate how long a given task will take and the amount of resources (e.g. paint) required.
- **Data Visualization Dashboards:** **Coming soon.** Currently admins may view tables containing data related to users, completed, jobs and parts.

### Tech Stack
- **Backend:** Python, Flask, SQLAlchemy Object Relational Mapper
- **Frontend:** HTML, JavaScript, CSS (**Coming soon**), Jinja2 templates
- **Database:** SQLite (The JOT database is not included. The app creates a new database automatically in a folder called instance, if one doesn't already exist.)
- **Email Handling:** Flask-Mailman (configured for SMTP)


### Set Up
1. Clone this repository:
   ```git clone https://github.com/kendallc23/job_tracker.git```
2. Create and activate a Python environment (I usually use Anaconda).
3. Install dependencies:
   ``` pip install -r requirements.txt ```
4. Configure environment variables by filling out the .env.example file.
5. Run the application:
   ```flask run```

### File Structure
- app.py — Main application setup
- models.py — Database models (User, Part, Job)
- forms.py — WTForms classes
- routes.py — Application routes and logic
- extensions.py — Flask extensions (db, bcrypt, login manager)
- config.py — Configuration settings
- templates — HTML templates organized by feature (/auth contains pages related to log in, registration, and password reset; /dash contains user and admin dashboards; /data contains the pages for job data collection, estimation, adding new parts and data overview; /errors contains error notification pages).
- static — Static files (CSS, JS)

### License
This project is licensed under the [MIT License](LICENSE).

