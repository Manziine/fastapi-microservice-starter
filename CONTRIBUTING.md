# Contributing to FastAPI Microservice Starter

Thank you for your interest in contributing! This document outlines the process for contributing to this project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Convention](#commit-convention)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md). Be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/fastapi-microservice-starter.git
   cd fastapi-microservice-starter
   ```
3. Add the upstream remote:
   ```bash
   git remote add upstream https://github.com/Manziine/fastapi-microservice-starter.git
   ```

## Development Setup

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your local settings

# Run database migrations
alembic upgrade head

# Start the development server
uvicorn app.main:app --reload
```

## Branching Strategy

We use GitFlow:

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feat/*` | New features |
| `fix/*` | Bug fixes |
| `test/*` | Test additions |
| `docs/*` | Documentation updates |
| `refactor/*` | Code refactoring |

Always branch from `main` and target `main` in your PR.

## Commit Convention

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation change
- `test`: Adding tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `ci`: CI/CD changes
- `chore`: Build process or tooling

### Examples
```
feat(auth): add refresh token rotation
fix(users): handle null email in profile update
test(health): add readiness probe tests
docs: update API endpoint documentation
```

## Pull Request Process

1. **Create a branch** from `main` using the naming conventions above
2. **Write tests** for your changes
3. **Run the test suite** locally: `pytest tests/ -v`
4. **Update documentation** if needed
5. **Open a PR** with:
   - Clear title following commit convention
   - Description of what changed and why
   - Link to related issues (if any)
   - Screenshots for UI changes
6. **Address review feedback** promptly
7. PRs require at least **1 approval** before merge

## Testing Guidelines

- Maintain **>80% code coverage**
- Write **unit tests** for business logic
- Write **integration tests** for API endpoints
- Use **pytest fixtures** for test setup
- Mock external dependencies

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py -v
```

## Questions?

Open a [GitHub Discussion](https://github.com/Manziine/fastapi-microservice-starter/discussions) or reach out via the issue tracker.