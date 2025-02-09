# project-companion-backend

Project Companion - is like a club for girls who love working on tech projects together. Imagine you want to build a cool software but need a friend to help. You can find other girls who also want to build the same project and ask them to join you. If you and your team get stuck, you can ask a mentor for help. Some mentors help for free, and some might ask for a small fee. Everyone has a profile that shows what they like and what they’re good at, so it’s easy to find the right people to work with.

Project Companion aims to empower women in tech by enabling them to find project partners, join existing project groups, and seek mentorship from experienced professionals. It is a community-driven, open-source project that provides numerous opportunities for growth, collaboration, and mentorship.

Key Features:

Project Collaboration:

Women interested in collaborating on projects can express their interest by specifying the project name and domain.
They can send collaboration requests to listed female techies. Upon acceptance, they can work together on the project.

Group Joining:
Users can view existing project groups and express interest in joining based on the project's tech stack.
Group members can accept the requests, adding the new member to their project.

Hiring Mentors:
If a project group encounters challenges they can't resolve, they can hire a mentor for guidance.
Mentors should have substantial experience and typically be team leads or senior developers.

Mentor Types:
Mentors are categorized as Free or Paid.
Paid mentors can set their payment terms (hourly, monthly, or task-based).

Mentor Profiles:
Include work experience, type of mentorship offered, domain expertise, LinkedIn profile, GitHub link, etc.

Companion Profiles:
Display the user’s tech stack, domain expertise, and topics of interest.


Installation Steps
------------------

1. Clone the repository
2. Activate virtual environment, venv
3. Install requirements.txt, pip install -r requirements.txt

**Postgres Database Configuration**

- sudo su postgres
- createdb project_companion
- createuser -P project_companion
- password for role - project_companion@123
- psql
- grant all privileges on database project_companion to project_companion;
- \q
- exit

**Migrations**

- python manage.py makemigrations
- python manage.py migrate
- python manage.py loaddata states countries
- python manage.py runserver

**Create user groups and permissions:**

- python manage.py create_groups_and_permissions

**Create a superuser:**

- python manage.py createsuperuser

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


**Create a branch**

- git checkout -b your_name
- git pull origin main
- git merge origin/main
- do the coding
- git merge origin/main  , to get the latest codes from the main branch
- git add .
- git commit -a -m "commit your changes"
- git push origin your_name
- git pull origin main

Before creating a pull request, make sure your branch (your_name) is up to date with the latest changes from the main branch to avoid conflicts.

- git checkout your_name
- git pull origin main

- 1) Navigate to Your Repository on GitHub:

Open your web browser and go to your repository on GitHub.

- 2) Create a New Pull Request:

On the repository's main page, click the "Pull requests" tab.
Click the "New pull request" button.

- 3) Select Branches for Comparison:

In the "base:" dropdown, select the branch you want to merge into (main).
In the "compare:" dropdown, select the branch you want to merge from (amina).

- 4) Review and Create the Pull Request:

Review the changes that will be merged. GitHub will show you the differences between the branches.
Add a title and description for your pull request. This is your opportunity to explain the purpose of the PR, any important details, and any relevant context.
Click the "Create pull request" button

- 5) Address Any Feedback:

After creating the pull request, reviewers may leave comments or request changes. Address any feedback by making additional commits to your branch (amina) and pushing them to the remote repository.
The pull request will automatically update with the new commits.


**To untrack migrations files**

- git ls-files */migrations/*.py | xargs git rm --cached
- git commit -m "Stop tracking migration files"
- git push

 **to remove or alter sensitive data, large files, or any other unwanted changes that have been committed in the past.**

- git filter-branch --force --index-filter \
"git rm --cached --ignore-unmatch migration.py" \
--prune-empty --tag-name-filter cat -- --all


**To drop & recreate database**

Delete all the files under migrations folder in each app except __init__.py
or 
- find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
- find . -path "*/migrations/*.pyc" -delete
- find . -name "__pycache__" -type d -exec rm -r {} +

- rm db.sqlite3 (if db is sqlite)

- sudo su postgres
- psql
- DROP DATABASE project_companion;
- \q

- createdb project_companion
- psql
- grant all privileges on database project_companion to project_companion;
- \q
- exit


celery worker command

celery -A project_companion_backend worker --loglevel=INFO

celery -A project_companion_backend worker --loglevel=INFO -E

export PYTHONPATH="$PYTHONPATH:~/Documents/Project Companion/project-companion-backend"

celery -A project_companion_backend worker --loglevel=DEBUG -E
