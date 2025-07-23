# Spy Cats Backend

Spy Cats Backend is a lightweight FastAPI application for managing covert feline missions. It allows you to create agent profiles (cats), assign them to missions with specific targets, and validate breeds via an external API. The project includes full CRUD functionality for both cats and missions, making it suitable as a backend foundation for more advanced spy-themed apps or demos.

---

## Technologies Used

- Python
- FastAPI
- SQLModel
- Pydantic
- python-dotenv

---

## Features

- Cats (Agents)
  - Create cat agents with name, salary, and breed
  - Breed is validated via a third-party API
  - Update cat salary
  - View all registered cats

- Missions
  - Create missions with a target (cat assignment is optional)
  - Assign or reassign a cat to a mission
  - Update mission status and internal notes
  - View all missions with their assigned agents

- Fully documented interactive API with Swagger UI

---

## Installation

1. Clone the repository:
   `git clone https://github.com/Shushunya/spy-cats.git`
   `cd spy-cats-backend`

2. Set up a virtual environment:
   `python -m venv venv`
   `source venv/bin/activate  # On Windows: venv\Scripts\activate`

3. Install dependencies:
   `pip install -r requirements.txt`

4. Run the development server:
   `uvicorn main:app --reload`

---

## Usage


Once the server is running, go to:

http://localhost:8000/docs

to explore and test all available endpoints using the FastAPI interactive documentation.

You can also use the provided Postman collection to test the API:

Postman Collection: [View in Postman](https://oleksandra-2280674.postman.co/workspace/Oleksandra's-Workspace~9051d974-4419-441a-8225-6d3138fddc85/collection/46344847-53d97601-9b80-4d14-b6fc-ef7d5baf5615?action=share&creator=46344847)


---

## API Overview

### Cats

- POST /cats/ – Create a new cat (breed is validated externally)
- GET /cats/ – Retrieve a list of all cats
- PUT /cats/{cat_id}/salary – Update a cat’s salary

### Missions

- POST /missions/ – Create a mission with a target (optional agent assignment)
- GET /missions/ – List all missions and their assigned cats
- PUT /missions/{mission_id}/assign – Assign or reassign a cat to a mission
- PUT /missions/{mission_id}/update – Update a mission’s state and/or notes

---

## License

This project is licensed under the MIT License.  
You're free to use, modify, and distribute it with attribution. See the LICENSE file for full terms.

---

## Contributing

Contributions are welcome. If you’d like to suggest improvements, report bugs, or add features, feel free to fork the repo and submit a pull request.

---

## Author

Developed by a solo developer as an open-source project.  
Feedback and suggestions are welcome via GitHub Issues.
