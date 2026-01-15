# Task Manager Application

## Overview
This project is a Task Manager application built using TypeScript and Express. It allows users to create, view, update, and delete tasks, providing a simple interface for task management.

## Features
- Create new tasks with title, description, priority, and due date.
- View a list of all tasks, sorted by priority or due date.
- Update existing tasks and mark them as complete.
- Delete tasks that are no longer needed.
- Filter tasks by status, priority, or due date.

## Project Structure
```
task-manager
├── src
│   ├── app.ts                # Entry point of the application
│   ├── routes
│   │   └── index.ts          # Route definitions
│   ├── controllers
│   │   └── taskController.ts  # Task-related request handlers
│   ├── models
│   │   └── task.ts           # Task entity definition
│   ├── services
│   │   └── fileHandler.ts     # File operations for task data
│   ├── views
│   │   ├── index.html         # Main HTML file
│   │   ├── taskList.html      # Task list view
│   │   └── taskForm.html      # Task creation/updating form
│   ├── utils
│   │   └── validators.ts       # Data validation utilities
│   └── types
│       └── index.ts           # TypeScript interfaces and types
├── tests
│   └── taskManager.test.ts    # Unit tests for the application
├── .gitignore                 # Files to ignore in Git
├── package.json               # npm configuration file
├── tsconfig.json              # TypeScript configuration file
└── README.md                  # Project documentation
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd task-manager
   ```
3. Install the dependencies:
   ```
   npm install
   ```

## Usage
To start the application, run:
```
npm start
```
The application will be available at `http://localhost:3000`.

## Testing
To run the tests, use:
```
npm test
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License.