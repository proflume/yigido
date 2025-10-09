# Contributing to Task Manager

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the community
- Show empathy towards others

## How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, etc.)

### Suggesting Features

1. **Check existing feature requests**
2. **Create a new issue** describing:
   - The problem you're trying to solve
   - Your proposed solution
   - Alternative solutions considered
   - Additional context

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes** following our coding standards

4. **Write/update tests** for your changes

5. **Run tests** to ensure everything passes
   ```bash
   make test-backend
   make test-frontend
   ```

6. **Commit your changes** with clear messages
   ```bash
   git commit -m "feat: add new feature"
   ```

   Follow conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation
   - `style:` Formatting
   - `refactor:` Code refactoring
   - `test:` Tests
   - `chore:` Maintenance

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots if UI changes

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### Frontend

```bash
cd frontend
npm install
```

## Coding Standards

### Python (Backend)

- Follow **PEP 8** style guide
- Use **Black** for formatting
- Use **isort** for import sorting
- Maximum line length: 120 characters
- Add docstrings to functions and classes

```python
def example_function(param1: str, param2: int) -> bool:
    """
    Short description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    pass
```

### TypeScript (Frontend)

- Use **TypeScript** for type safety
- Follow **ESLint** rules
- Use functional components with hooks
- Add JSDoc comments for complex functions

```typescript
/**
 * Fetches tasks from the API
 * @param params - Query parameters
 * @returns Promise with task list
 */
async function fetchTasks(params?: TaskParams): Promise<Task[]> {
  // Implementation
}
```

### Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)

```python
def test_user_registration_success():
    # Arrange
    payload = {...}
    
    # Act
    response = client.post('/api/v1/auth/users/', payload)
    
    # Assert
    assert response.status_code == 201
```

## Documentation

- Update README.md if adding features
- Update API documentation for API changes
- Add comments for complex logic
- Update type definitions

## Review Process

1. Automated tests must pass
2. Code review by maintainers
3. Address review feedback
4. Merge once approved

## Questions?

Feel free to open an issue for questions or reach out to the maintainers.

Thank you for contributing! 🎉
