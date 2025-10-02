# Contributing to TaskFlow

Thank you for your interest in contributing to TaskFlow! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming environment.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Potential implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit with clear messages
7. Push to your fork
8. Open a Pull Request

## Development Setup

See [README.md](README.md) for detailed setup instructions.

### Quick Start

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
python wsgi.py

# Frontend
cd frontend
npm install
npm run dev
```

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
def create_task(title: str, description: str) -> Task:
    """
    Create a new task.
    
    Args:
        title: Task title
        description: Task description
    
    Returns:
        Created task object
    """
    # Implementation
```

### TypeScript (Frontend)

- Use TypeScript strict mode
- Define interfaces for props and data structures
- Use functional components with hooks
- Follow React best practices

```typescript
interface TaskProps {
  task: Task;
  onUpdate: (task: Task) => void;
}

const TaskCard: React.FC<TaskProps> = ({ task, onUpdate }) => {
  // Implementation
};
```

### Commit Messages

Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(auth): add password reset functionality
fix(tasks): resolve duplicate task creation bug
docs(api): update authentication endpoint documentation
```

## Testing

### Backend Tests

```bash
cd backend
pytest
pytest --cov=app tests/
```

All new features must include tests.

### Frontend Tests

```bash
cd frontend
npm test
npm run test:coverage
```

## Documentation

- Update README.md if adding new features
- Update API.md for API changes
- Add inline comments for complex logic
- Update architecture docs for structural changes

## Code Review Process

1. All PRs require review before merging
2. Address reviewer feedback
3. Ensure CI/CD checks pass
4. Squash commits if requested
5. Maintain a clean git history

## Questions?

Feel free to open an issue for any questions or clarifications needed.

Thank you for contributing! 🎉
