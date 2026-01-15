# Task Manager Application Design

## 1. Use Case Diagram (Draw.io Instructions)

**To create this diagram in draw.io:**

1. Open draw.io and create a new blank diagram
2. Add a "Stick Figure" shape for the User actor
3. Add a rounded rectangle for "Task Manager App" system boundary
4. Add ellipses for each use case:
   - Create Task
   - View Task List
   - Update Task
   - Delete Task
   - Mark Complete
   - Filter Tasks
5. Connect User to each use case with solid lines
6. Add "includes" relationships between related use cases
7. Use the "System Boundary" shape to group the use cases

**Diagram Structure:**
- **Actor**: User (stick figure)
- **System Boundary**: Task Manager App (rounded rectangle)
- **Use Cases**: 6 ellipses connected to the actor
- **Relationships**: Solid lines from actor to use cases

**Use Cases:**
- **Create Task**: User can add new tasks with title, description, priority, and due date
- **View Task List**: User can view all tasks, sorted by priority/due date
- **Update Task**: User can modify task details, status, or priority
- **Delete Task**: User can remove tasks they no longer need
- **Mark Complete**: User can mark tasks as completed
- **Filter Tasks**: User can filter tasks by status (pending/completed), priority, or due date

## 2. Sequence Diagram (File-Based Storage) - Draw.io Instructions

**To create this sequence diagram in draw.io:**

1. Select "Sequence Diagram" template or create blank diagram
2. Add vertical lifelines for each participant:
   - User
   - UI Controller
   - Task Controller
   - Task Model
   - File Handler
   - File System
3. Use the sequence diagram shapes from the toolbar
4. Add horizontal arrows between lifelines for messages
5. Include activation boxes on lifelines where processing occurs
6. Add return messages with dashed arrows
7. Group related interactions (create task flow vs. view tasks flow)

**Key Elements:**
- **Lifelines**: 6 vertical lines representing system components
- **Messages**: Solid arrows for requests, dashed for responses
- **Activations**: Rectangles on lifelines showing processing time
- **Notes**: Optional annotations for complex interactions

**Key Components:**
- **File Handler**: Manages JSON file operations (read/write)
- **Task Model**: Business logic and data validation
- **Task Controller**: Handles user requests and coordinates between model and view
- **UI Controller**: Manages user interface updates

## 3. MVC Component Responsibilities

### Models
**Responsibilities:**
- Represent task entities with attributes (id, title, description, priority, due_date, status, created_date)
- Implement business logic for task validation and state management
- Handle data persistence through file operations
- Provide methods for CRUD operations on task data
- Ensure data integrity and consistency

**Concerns:**
- Data validation (required fields, date formats, priority levels)
- File I/O operations (reading/writing JSON data)
- Task state transitions (pending → completed)
- Data serialization/deserialization

### Views
**Responsibilities:**
- Render task list interface with sorting/filtering options
- Display individual task details and edit forms
- Handle user input collection (forms, buttons, selections)
- Provide visual feedback for user actions (success/error messages)
- Implement responsive design for different screen sizes

**Concerns:**
- UI/UX design and user interaction
- Form validation and input sanitization
- Visual state management (loading states, empty states)
- Accessibility compliance
- Cross-browser compatibility

### Controllers
**Responsibilities:**
- Receive and process user requests from views
- Coordinate between models and views
- Implement application logic and workflow
- Handle errors and exceptions
- Manage application state and navigation

**Concerns:**
- Request routing and response handling
- Business rule enforcement
- Error handling and user feedback
- Session/state management
- Security validation

## 4. Class Diagram - Draw.io Instructions

**To create this class diagram in draw.io:**

1. Select "Class Diagram" template or use UML shapes
2. Create three class rectangles using the "Class" shape from UML section
3. For each class:
   - Top compartment: Class name
   - Middle compartment: Attributes (prefixed with visibility: - private, + public)
   - Bottom compartment: Methods
4. Add relationships:
   - Aggregation: From TaskManager to Task (diamond on TaskManager side)
   - Dependency: From TaskManager to FileHandler (dashed arrow)
5. Use appropriate connectors from the UML shapes library

**Class Details:**
- **Task Class**: Attributes (id, title, description, priority, due_date, status, created_date) and methods
- **TaskManager Class**: Manages task collection and file operations
- **FileHandler Class**: Handles JSON file I/O operations
- **Relationships**: TaskManager contains multiple Tasks, uses FileHandler

**Relationships:**
- TaskManager has many Tasks (composition)
- TaskManager uses FileHandler (dependency)
- Task has methods for data conversion and validation

## 5. CRUD Matrix

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| Task   | ✓      | ✓    | ✓      | ✓      |

### Task Entity Operations:

**Create (C):**
- Add new task with title, description, priority, due date
- Validate required fields and data formats
- Assign unique ID and creation timestamp
- Save to persistent storage

**Read (R):**
- Retrieve all tasks with optional filtering
- Get individual task by ID
- Support sorting by priority, due date, creation date
- Include task statistics (total, completed, overdue)

**Update (U):**
- Modify task attributes (title, description, priority, due date)
- Change task status (pending/completed)
- Validate data integrity during updates
- Update modification timestamp

**Delete (D):**
- Remove task by ID
- Confirm deletion to prevent accidental removal
- Clean up related data if any
- Update task list display

### Additional Operations:
- **Filter**: By status, priority, due date range
- **Search**: By title or description keywords
- **Sort**: By multiple criteria
- **Export**: Save tasks to external formats
- **Import**: Load tasks from external sources