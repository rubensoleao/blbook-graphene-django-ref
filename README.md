# Social Media Timeline with Django and Graphene

This project demonstrates how to build a social media timeline by integrating GraphQL with Python, utilizing the Graphene library and Django framework. It's designed as a practical example and reference.

## Installation

First, clone the repository to your local machine:

```bash
git clone <repo_url>
cd <repo_directory>
```

### Setting Up the Environment

Ensure you have Python 3.9 installed. We recommend using a virtual environment for better project isolation. To set up a virtual environment and install the required dependencies, follow these steps:

```bash
python3 -m venv venv                              # Create a virtual environment with Python 3.9
source venv/bin/activate                          # Activate the virtual environment on Unix/Linux
venv\Scripts\activate                             # Activate the virtual environment on Windows
pip install -r requirements/development.txt       # Install the project dependencies
```

## Execution

To run the project locally and interact with the GraphQL API, follow these steps:

1. Start the Django development server:
    ```bash
    python manage.py runserver
    ```

2. Access the GraphQL interface at: `http://localhost:8000/graphql`

You can now execute GraphQL queries and mutations through this interface.

## TODO

- Refactor queries from the main schema to specific apps for better organization.
- Address the issue where the admin portal's cache authentication overrides JWT token authentication.
- Expand the test suite to cover more functionalities.
- Standardize error handling across GraphQL queries.

## Contributing

Contributions to the project are welcome!
