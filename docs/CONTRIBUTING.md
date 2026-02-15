# Contributing to AutoFalloutShelter

Thank you for your interest in contributing to AutoFalloutShelter! This document provides guidelines for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Specification-Driven Development](#specification-driven-development)
- [Pull Request Process](#pull-request-process)
- [Code Standards](#code-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation](#documentation)

---

## Code of Conduct

This project follows a standard code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Assume good intentions

Unacceptable behavior will not be tolerated and may result in being banned from the project.

---

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/AutoFalloutShelter.git
cd AutoFalloutShelter
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov black flake8 mypy pre-commit

# Install pre-commit hooks
pre-commit install

# Verify setup
pytest tests/ -v
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

---

## Development Process

### Workflow Overview

1. **Find or Create an Issue**
   - Check existing issues for tasks to work on
   - Create new issue if needed, describing the problem/feature
   - Comment on issue to claim it

2. **Read Specifications**
   - Review `docs/REQUIREMENTS.md` for functional requirements
   - Review `docs/ARCHITECTURE.md` for technical design
   - Understand acceptance criteria from issue

3. **Develop Using TDD**
   - Write tests first (define expected behavior)
   - Implement minimal code to pass tests
   - Refactor while keeping tests green

4. **Ensure Quality**
   - Run tests: `pytest tests/ -v`
   - Format code: `black src/ tests/`
   - Lint code: `flake8 src/`
   - Type check: `mypy src/`

5. **Commit and Push**
   - Use conventional commit messages
   - Push to your fork
   - Create Pull Request

6. **Code Review**
   - Address reviewer feedback
   - Update PR as needed
   - Merge when approved

---

## Specification-Driven Development

**This project follows a specification-first approach.**

### Before Writing Code

1. **Check if requirement exists in `docs/REQUIREMENTS.md`**
   - If yes: Implement according to spec
   - If no: Add requirement first, then implement

2. **Check if architecture covers your change in `docs/ARCHITECTURE.md`**
   - If yes: Follow architecture design
   - If no: Propose architecture change in issue

3. **Write tests that encode acceptance criteria**
   - Tests are executable specifications
   - Tests must fail before implementation
   - Tests must pass after implementation

### Example: Adding Resource Detection

```python
# Step 1: Check REQUIREMENTS.md
# CV-2: Resource Detection
# - CV-2.1: Shall detect power level (0-100%)
# - Accepts: Resource detection accuracy ≥95%

# Step 2: Write test first (TDD)
def test_detect_power_level():
    """Test CV-2.1: Shall detect power level"""
    screenshot = load_fixture('screenshots/power_75percent.png')
    recognition = ImageRecognition()
    
    resources = recognition.detect_resources(screenshot)
    
    # Acceptance: ±5% accuracy (CV-2.6)
    assert 0.70 <= resources.power <= 0.80

# Step 3: Run test (it fails)
pytest tests/unit/test_vision.py::test_detect_power_level -v
# FAILED - NotImplementedError

# Step 4: Implement
class ImageRecognition:
    def detect_resources(self, image: np.ndarray) -> ResourceLevels:
        # Implementation here
        power_region = image[10:30, 100:200]
        power_level = self._analyze_bar(power_region)
        return ResourceLevels(power=power_level, ...)

# Step 5: Run test (it passes)
pytest tests/unit/test_vision.py::test_detect_power_level -v
# PASSED
```

---

## Pull Request Process

### PR Title Convention

Use conventional commit format:

```
feat(module): add brief description
fix(module): fix brief description
docs(module): update brief description
test(module): add brief description
refactor(module): improve brief description
```

### PR Description Template

```markdown
## Description
[Brief description of changes]

## Related Issues
Closes #123
Relates to #124

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Requirements Implemented
- [ ] CV-2.1: Power level detection
- [ ] CV-2.2: Food level detection

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Test coverage maintained/improved

## Quality Checks
- [ ] Code formatted with Black
- [ ] No linting errors (flake8)
- [ ] Type hints added (mypy clean)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated

## Screenshots (if applicable)
[Add screenshots for visual changes]
```

### Review Criteria

PRs will be reviewed for:

- ✅ **Specification Compliance**: Does it implement requirements correctly?
- ✅ **Test Coverage**: Are there tests? Do they pass?
- ✅ **Code Quality**: Is code clean, readable, maintainable?
- ✅ **Documentation**: Are docstrings and docs updated?
- ✅ **No Breaking Changes**: Unless intentional and documented

---

## Code Standards

### Python Style

- **Style Guide**: PEP 8
- **Line Length**: 88 characters (Black default)
- **Formatter**: Black (mandatory)
- **Linter**: Flake8
- **Type Hints**: Required for public APIs

```python
# Good example
def detect_dwellers(
    self, 
    image: np.ndarray, 
    confidence_threshold: float = 0.85
) -> List[Dweller]:
    """
    Detect all visible dwellers in the screenshot.

    Args:
        image: Screenshot as BGR numpy array
        confidence_threshold: Minimum confidence for detection (0.0-1.0)

    Returns:
        List of detected Dweller objects with positions and states

    Raises:
        ValueError: If image dimensions are invalid
    """
    if image.shape[0] < 720:
        raise ValueError(f"Image height too small: {image.shape[0]}")
    
    dwellers = []
    # Implementation...
    return dwellers
```

### Commit Message Format

Follow **Conventional Commits**:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Refactoring
- `style`: Formatting
- `chore`: Maintenance

**Examples:**
```
feat(vision): implement dweller health detection

Add health bar analysis to determine dweller health percentage.
Uses color thresholding to detect red health bar pixels.

Implements CV-3.2, closes #15
```

```
fix(automation): correct coordinate scaling for 4K displays

Previous implementation used hardcoded scale factor of 1.0,
causing clicks to be off by 2x on 4K displays. Now correctly
calculates scale based on actual vs reference resolution.

Fixes #42
```

---

## Testing Requirements

### Test Coverage

- **Minimum Coverage**: 70% overall
- **Critical Paths**: 90%+ coverage
- **New Code**: Must include tests

```bash
# Run with coverage
pytest tests/ --cov=src --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Test Organization

```python
# tests/unit/test_dweller_manager.py

import pytest
from src.strategy.dwellers import DwellerManager
from src.models import Dweller, SPECIAL

class TestDwellerManager:
    """Test suite for DwellerManager"""
    
    @pytest.fixture
    def manager(self):
        """Create manager instance"""
        return DwellerManager()
    
    def test_optimal_assignment_matches_highest_special(self, manager):
        """Test STRAT-2.1: Assign based on highest SPECIAL stat"""
        # Arrange
        dweller = create_dweller(special=SPECIAL(strength=10, ...))
        power_room = create_room(room_type=RoomType.POWER_GENERATOR)
        diner = create_room(room_type=RoomType.DINER)
        
        # Act
        result = manager.optimal_assignment(dweller, [power_room, diner])
        
        # Assert
        assert result == power_room, "High strength should assign to power"
```

### Test Types

1. **Unit Tests** (`tests/unit/`):
   - Test individual functions/methods
   - Mock dependencies
   - Fast execution (<1s total)

2. **Integration Tests** (`tests/integration/`):
   - Test module interactions
   - Use real dependencies (no mocks)
   - Slower execution acceptable

3. **Fixtures** (`tests/fixtures/`):
   - Sample screenshots
   - Game state JSON files
   - Template images

---

## Documentation

### Required Documentation

All contributions must include appropriate documentation:

1. **Docstrings**: All public classes, methods, functions
2. **Inline Comments**: For complex logic (explain "why", not "what")
3. **README Updates**: If changing user-facing behavior
4. **CHANGELOG**: Add entry under `[Unreleased]`
5. **Specification Updates**: If adding/changing requirements

### Docstring Format

```python
def complex_function(
    param1: Type1,
    param2: Type2,
    param3: Optional[Type3] = None
) -> ReturnType:
    """
    One-line summary of function purpose.

    More detailed description if needed. Explain what the function
    does, its purpose in the system, and any important behavior.

    Args:
        param1: Description of param1
        param2: Description of param2
        param3: Optional description. Defaults to None which means...

    Returns:
        Description of return value and its structure

    Raises:
        ValueError: When and why this is raised
        CustomError: When and why this is raised

    Example:
        >>> result = complex_function(arg1, arg2)
        >>> print(result.attribute)
        expected_output
    
    Note:
        Any important notes, caveats, or implementation details
    """
```

### CHANGELOG Format

```markdown
## [Unreleased]
### Added
- Computer vision: Room state detection (#12)
- Strategy: Enhanced dweller assignment algorithm (#15)

### Changed
- Automation: Improved coordinate mapping precision (#18)

### Fixed
- Vision: OCR errors on 720p displays (#20)

### Deprecated
- Old assignment algorithm (will be removed in v0.3.0)
```

---

## Issue Guidelines

### Creating Issues

Use appropriate issue templates:

**Feature Request:**
```markdown
## Feature Description
[Clear description of the feature]

## Requirements Reference
[Reference to REQUIREMENTS.md section, if applicable]

## Use Case
[Why is this needed? What problem does it solve?]

## Proposed Implementation
[High-level approach]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests written
- [ ] Documentation updated
```

**Bug Report:**
```markdown
## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- OS: Windows 11
- Python Version: 3.10.5
- Game Resolution: 1920x1080
- AutoFalloutShelter Version: 0.1.0

## Logs/Screenshots
[Attach relevant logs or screenshots]
```

---

## Questions?

- **Documentation**: Check `docs/` folder first
- **Discussions**: Use GitHub Discussions for questions
- **Issues**: Create issue if you found a bug or have feature request
- **Contact**: Mention @willywil in discussions

---

## Attribution

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to AutoFalloutShelter! 🎮🤖**
