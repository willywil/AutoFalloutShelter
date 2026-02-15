# Development Workflow
**AutoFalloutShelter Project**

**Version:** 1.0  
**Last Updated:** February 15, 2026

---

## 1. Getting Started

### 1.1 Prerequisites

- **Python:** 3.8 or higher (3.10+ recommended)
- **Git:** For version control
- **Tesseract OCR:** For text recognition
- **Operating System:** Windows 10/11 (primary), macOS/Linux (experimental)
- **Hardware:** Minimum 2GB RAM, dual-core CPU

### 1.2 Initial Setup

```bash
# 1. Clone the repository
git clone https://github.com/willywil/AutoFalloutShelter.git
cd AutoFalloutShelter

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install development dependencies
pip install pytest pytest-cov black flake8 mypy

# 5. Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# macOS: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# 6. Verify installation
python -m pytest tests/ -v
```

---

## 2. Project Structure

```
AutoFalloutShelter/
├── main.py                     # Application entry point
├── config.json                 # Runtime configuration
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
│
├── src/                        # Source code
│   ├── __init__.py
│   ├── vision/                 # Computer vision module
│   │   ├── __init__.py
│   │   ├── capture.py          # Screen capture
│   │   ├── recognition.py      # Image recognition
│   │   └── parser.py           # GameState parser
│   ├── automation/             # Input automation module
│   │   ├── __init__.py
│   │   ├── controller.py       # Input controller
│   │   ├── actions.py          # Game actions
│   │   ├── mapper.py           # Coordinate mapper
│   │   └── queue.py            # Action queue
│   ├── strategy/               # Strategy module
│   │   ├── __init__.py
│   │   ├── scheduler.py        # Priority scheduler
│   │   ├── resources.py        # Resource manager
│   │   ├── dwellers.py         # Dweller manager
│   │   ├── incidents.py        # Incident handler
│   │   └── rooms.py            # Room manager
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── game_state.py       # GameState, etc.
│   │   ├── dweller.py          # Dweller, SPECIAL
│   │   ├── room.py             # Room
│   │   └── action.py           # Action
│   └── utils/                  # Utilities
│       ├── __init__.py
│       ├── logging.py          # Logging setup
│       ├── config.py           # Configuration
│       ├── monitor.py          # Performance monitoring
│       └── errors.py           # Error handling
│
├── assets/                     # Static assets
│   └── templates/              # Template images for CV
│       ├── rooms/              # Room templates
│       ├── ui/                 # UI element templates
│       └── icons/              # Icon templates
│
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   │   ├── test_vision.py
│   │   ├── test_automation.py
│   │   ├── test_strategy.py
│   │   └── test_models.py
│   ├── integration/            # Integration tests
│   │   ├── test_main_loop.py
│   │   └── test_end_to_end.py
│   └── fixtures/               # Test data
│       ├── screenshots/        # Sample screenshots
│       └── game_states/        # Sample game states
│
├── docs/                       # Documentation
│   ├── REQUIREMENTS.md         # Requirements specification
│   ├── ARCHITECTURE.md         # System architecture
│   ├── WORKFLOW.md            # This file
│   ├── API.md                  # API documentation
│   ├── USER_GUIDE.md          # User guide
│   └── CONTRIBUTING.md         # Contribution guidelines
│
└── logs/                       # Runtime logs (gitignored)
    └── .gitkeep
```

---

## 3. Development Workflow

### 3.1 Branch Strategy

We follow **GitHub Flow** - a simplified branching model:

```
main (production-ready code)
  ↓
  ├─ feature/cv-resource-detection    # New feature
  ├─ fix/coordinate-mapping-bug       # Bug fix
  ├─ docs/update-architecture         # Documentation
  └─ refactor/split-strategy-module   # Refactoring
```

**Branch Naming Convention:**
- `feature/<description>` - New features
- `fix/<description>` - Bug fixes
- `docs/<description>` - Documentation changes
- `refactor/<description>` - Code refactoring
- `test/<description>` - Test additions/changes

### 3.2 Feature Development Workflow

```bash
# 1. Ensure main is up to date
git checkout main
git pull origin main

# 2. Create feature branch
git checkout -b feature/dweller-assignment-algorithm

# 3. Develop with frequent commits
git add <files>
git commit -m "feat(strategy): implement SPECIAL-based assignment"

# 4. Write/update tests
pytest tests/unit/test_strategy.py -v

# 5. Ensure code quality
black src/
flake8 src/
mypy src/

# 6. Push branch
git push origin feature/dweller-assignment-algorithm

# 7. Create Pull Request on GitHub
# - Fill out PR template
# - Link related issues
# - Request review

# 8. Address review feedback
# - Make changes
# - Push updates
# - Re-request review

# 9. Merge when approved
# - Squash and merge via GitHub UI
# - Delete branch after merge
```

### 3.3 Commit Message Convention

Follow **Conventional Commits** specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, build, etc.)
- `perf`: Performance improvements

**Examples:**
```
feat(vision): add template matching for room detection

Implement multi-scale template matching to detect room types
from screenshots. Supports 720p to 4K resolutions.

Closes #12
```

```
fix(automation): correct coordinate mapping for ultrawide displays

The coordinate mapper was using incorrect aspect ratio calculations
for 21:9 displays, causing clicks to miss targets by 50-100 pixels.

Fixes #45
```

```
docs(architecture): update data flow diagram

Added verification step to main loop diagram and clarified
error handling flow.
```

---

## 4. Code Quality Standards

### 4.1 Code Style

**Python Style Guide:** PEP 8 with following specifics:

- **Line Length:** 88 characters (Black default)
- **Indentation:** 4 spaces
- **Quotes:** Double quotes preferred
- **Imports:** Organized (stdlib, third-party, local)
- **Type Hints:** Required for public functions

**Automated Formatting:**
```bash
# Format all code
black src/ tests/

# Check formatting (no changes)
black --check src/ tests/
```

**Linting:**
```bash
# Run flake8
flake8 src/ --max-line-length=88 --extend-ignore=E203

# Run mypy for type checking
mypy src/ --ignore-missing-imports
```

### 4.2 Documentation Standards

**Docstrings:** Required for all public classes, methods, and functions.

```python
def detect_resources(image: np.ndarray) -> ResourceLevels:
    """
    Extract resource levels from game UI screenshot.

    Analyzes the resource bars in the top portion of the game UI
    to determine current power, food, and water levels as percentages.

    Args:
        image: Screenshot as numpy array (BGR format from OpenCV)

    Returns:
        ResourceLevels object containing power, food, water percentages
        (0.0 to 1.0) and counts for caps, stimpaks, and radaway.

    Raises:
        ValueError: If image dimensions are invalid (<720p)
        CVError: If UI elements cannot be located

    Example:
        >>> screenshot = capture_screen()
        >>> resources = detect_resources(screenshot)
        >>> print(f"Power: {resources.power:.1%}")
        Power: 87.5%
    """
```

**Inline Comments:** Use sparingly, explain "why" not "what".

```python
# Good: Explains reasoning
# Use multi-scale matching because room size varies by merge level
templates = self._get_templates_at_scales([0.8, 1.0, 1.2])

# Bad: Restates code
# Loop through templates
for template in templates:
    ...
```

### 4.3 Testing Standards

**Test Coverage Target:** ≥70% overall, ≥90% for critical paths

**Test Organization:**
```python
# tests/unit/test_dweller_manager.py

import pytest
from src.strategy.dwellers import DwellerManager
from src.models import Dweller, Room, SPECIAL

class TestDwellerManager:
    """Test suite for DwellerManager class"""
    
    @pytest.fixture
    def manager(self):
        """Fixture: Create DwellerManager instance"""
        return DwellerManager()
    
    @pytest.fixture
    def sample_dweller(self):
        """Fixture: Create sample dweller with high strength"""
        return Dweller(
            id="dweller_1",
            name="Test Dweller",
            level=10,
            health=100,
            happiness=75,
            special=SPECIAL(strength=10, perception=3, endurance=5,
                          charisma=2, intelligence=4, agility=3, luck=6)
        )
    
    def test_optimal_assignment_strength_to_power(self, manager, sample_dweller):
        """Test that high-strength dweller assigned to power room"""
        power_room = Room(id="room_1", room_type=RoomType.POWER_GENERATOR, ...)
        water_room = Room(id="room_2", room_type=RoomType.WATER_TREATMENT, ...)
        
        result = manager.optimal_assignment(sample_dweller, [power_room, water_room])
        
        assert result == power_room
    
    def test_optimal_assignment_no_rooms_raises_error(self, manager, sample_dweller):
        """Test that empty room list raises ValueError"""
        with pytest.raises(ValueError, match="No rooms available"):
            manager.optimal_assignment(sample_dweller, [])
```

**Running Tests:**
```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_dweller_manager.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run only fast tests (skip integration)
pytest tests/unit/ -v

# Run tests matching pattern
pytest tests/ -k "dweller" -v
```

---

## 5. Development Guidelines

### 5.1 Specification-Driven Development

**Before writing code:**

1. **Check Requirements:** Refer to `docs/REQUIREMENTS.md`
2. **Check Architecture:** Refer to `docs/ARCHITECTURE.md`
3. **Create Issue:** If not exists, create GitHub issue describing work
4. **Write Tests First (TDD):** Define expected behavior via tests
5. **Implement:** Write minimal code to pass tests
6. **Refactor:** Improve code quality while keeping tests passing

### 5.2 Issue-Driven Development

All work should be tied to a GitHub issue:

1. **Issue describes WHAT:** What needs to be done and why
2. **Comments describe HOW:** How it will be implemented
3. **PR closes issue:** PR description references issue with "Closes #N"

**Issue Template Example:**
```markdown
## Description
[Clear description of the feature/bug]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Tests written and passing
- [ ] Documentation updated

## Technical Approach
[Brief outline of implementation]

## Priority
[Critical / High / Medium / Low]
```

### 5.3 Pull Request Guidelines

**PR Title:** Should match commit convention
```
feat(vision): implement room state detection
fix(automation): correct dweller drag coordinates
docs(readme): add installation instructions
```

**PR Description Template:**
```markdown
## Changes
[Summary of what changed]

## Related Issues
Closes #123
Relates to #124

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
[Before/after screenshots for UI changes]

## Checklist
- [ ] Code follows style guide
- [ ] Documentation updated
- [ ] Tests passing
- [ ] No linting errors
```

**Review Process:**
1. At least one approval required
2. All CI checks must pass
3. No merge conflicts
4. Squash and merge to keep history clean

---

## 6. Continuous Integration

### 6.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov black flake8 mypy
    
    - name: Check formatting
      run: black --check src/ tests/
    
    - name: Lint
      run: flake8 src/ --max-line-length=88
    
    - name: Type check
      run: mypy src/ --ignore-missing-imports
    
    - name: Run tests
      run: pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

### 6.2 Pre-commit Hooks

Install pre-commit hooks to catch issues early:

```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**`.pre-commit-config.yaml`:**
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
        args: [--max-line-length=88]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.0
    hooks:
      - id: mypy
        args: [--ignore-missing-imports]
```

---

## 7. Release Process

### 7.1 Versioning

Follow **Semantic Versioning (SemVer):** `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes (e.g., API changes)
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes (backward compatible)

**Examples:**
- `0.1.0` - Initial MVP release
- `0.2.0` - Added exploration management
- `0.2.1` - Fixed coordinate mapping bug
- `1.0.0` - First stable release

### 7.2 Release Checklist

```markdown
## Release Checklist for v0.1.0

- [ ] All planned features implemented
- [ ] All tests passing
- [ ] Documentation updated
- [ ] CHANGELOG updated
- [ ] Version bumped in `src/__init__.py`
- [ ] Git tag created: `git tag v0.1.0`
- [ ] Tag pushed: `git push origin v0.1.0`
- [ ] GitHub Release created with notes
- [ ] Known issues documented
```

### 7.3 Changelog Maintenance

Keep `CHANGELOG.md` updated with every significant change:

```markdown
# Changelog

## [Unreleased]
### Added
- Exploration management module

### Changed
- Improved dweller assignment algorithm

### Fixed
- Coordinate mapping for ultrawide displays

## [0.1.0] - 2026-03-01
### Added
- Initial computer vision system
- Basic resource management
- Incident detection and response
- Automated dweller assignment

### Known Issues
- OCR accuracy low on 720p displays
- Rush probability calculation needs tuning
```

---

## 8. Agent-First Development

### 8.1 Autonomous Development Principles

To enable AI agents to work autonomously:

1. **Requirements are single source of truth:** All behavior defined in specs
2. **Tests validate requirements:** Tests encode acceptance criteria
3. **Architecture guides implementation:** Clear module boundaries and contracts
4. **Issues define work:** Each task has clear deliverables
5. **Documentation is code-adjacent:** Easy to reference during development

### 8.2 Agent Workflow

```
Agent receives task
     ↓
1. Read REQUIREMENTS.md for functional requirements
     ↓
2. Read ARCHITECTURE.md for technical approach
     ↓
3. Read relevant code in src/ for context
     ↓
4. Read existing tests for behavior expectations
     ↓
5. Implement feature following specs
     ↓
6. Write/update tests to validate
     ↓
7. Run quality checks (tests, linting, formatting)
     ↓
8. Commit with conventional commit message
     ↓
9. Create PR linking to issue
```

### 8.3 Specification Updates

When requirements change:

1. Update `docs/REQUIREMENTS.md` first
2. Update `docs/ARCHITECTURE.md` if design changes
3. Create issue describing implementation
4. Implement changes
5. Update tests to match new requirements

---

## 9. Troubleshooting

### 9.1 Common Issues

**Issue: Tesseract not found**
```bash
# Windows: Add Tesseract to PATH
setx PATH "%PATH%;C:\Program Files\Tesseract-OCR"

# Or set in code
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

**Issue: Import errors**
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Issue: Tests failing**
```bash
# Clear pytest cache
pytest --cache-clear

# Verbose output for debugging
pytest tests/ -vv --tb=long
```

### 9.2 Getting Help

- **Check Documentation:** `docs/` folder
- **Search Issues:** Existing GitHub issues
- **Create Issue:** Describe problem with reproduction steps
- **Discussions:** Use GitHub Discussions for questions

---

## 10. Resources

### 10.1 Documentation

- **Requirements:** `docs/REQUIREMENTS.md`
- **Architecture:** `docs/ARCHITECTURE.md`
- **API Reference:** `docs/API.md`
- **User Guide:** `docs/USER_GUIDE.md`

### 10.2 External Resources

- **Python Style Guide:** [PEP 8](https://pep8.org/)
- **Conventional Commits:** [conventionalcommits.org](https://www.conventionalcommits.org/)
- **Semantic Versioning:** [semver.org](https://semver.org/)
- **GitHub Flow:** [guides.github.com/introduction/flow](https://guides.github.com/introduction/flow/)

---

## 11. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Initial | Initial workflow documentation |

---

**This is a living document. Update as processes evolve.**
