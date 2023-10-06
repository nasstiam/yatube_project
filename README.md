# yatube_project

### Description:

Yatube - social network for publishing posts. authenticated users can publish posts, leave comments 
and follow other authors. Users can see all posts of the social network and only posts of followed authors, 
as well as author's Profile page or only posts of a specific group.
Designed by MVT architecture. Uses post pagination and caching. Registration is implemented with data verification, 
password change and recovery via mail. Tests are written that check the operation of the service.

### Installation instructions:

Clone the repository and go to the command line:

```git clone https://github.com/nasstiam/yatube_project```

```cd yatube_project```

Create and activate a virtual environment:

```python3 -m venv venv```

* If you have Linux/mac OS

    ```source venv/bin/activate```

* If you have windows

    ```source venv/scripts/activate```
    ```python -m pip install --upgrade pip```

Install the dependencies from the file requirements.txt:

```pip install -r requirements.txt```

Perform migrations:

```python manage.py migrate```

Launch the project:

```python manage.py runserver```