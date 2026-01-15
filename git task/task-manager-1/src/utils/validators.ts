export function validateTaskData(task) {
    const { title, description, priority, dueDate } = task;

    if (!title || typeof title !== 'string') {
        return { valid: false, message: 'Title is required and must be a string.' };
    }

    if (!description || typeof description !== 'string') {
        return { valid: false, message: 'Description is required and must be a string.' };
    }

    const validPriorities = ['low', 'medium', 'high'];
    if (!priority || !validPriorities.includes(priority)) {
        return { valid: false, message: 'Priority is required and must be one of: low, medium, high.' };
    }

    if (!dueDate || isNaN(Date.parse(dueDate))) {
        return { valid: false, message: 'Due date is required and must be a valid date.' };
    }

    return { valid: true, message: 'Task data is valid.' };
}

export function validateTaskUpdateData(task) {
    const { title, description, priority, dueDate } = task;

    if (title && typeof title !== 'string') {
        return { valid: false, message: 'Title must be a string if provided.' };
    }

    if (description && typeof description !== 'string') {
        return { valid: false, message: 'Description must be a string if provided.' };
    }

    const validPriorities = ['low', 'medium', 'high'];
    if (priority && !validPriorities.includes(priority)) {
        return { valid: false, message: 'Priority must be one of: low, medium, high if provided.' };
    }

    if (dueDate && isNaN(Date.parse(dueDate))) {
        return { valid: false, message: 'Due date must be a valid date if provided.' };
    }

    return { valid: true, message: 'Task update data is valid.' };
}