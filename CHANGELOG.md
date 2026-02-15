# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure with modular architecture
- Requirements specification document (REQUIREMENTS.md)
- System architecture documentation (ARCHITECTURE.md)
- Development workflow guide (WORKFLOW.md)
- Contributing guidelines (CONTRIBUTING.md)
- GitHub issues for development tracking (#1-#7)
- Core module scaffolding:
  - Vision module for computer vision
  - Automation module for input control
  - Strategy module for decision making
  - Models module for data structures
  - Utils module for cross-cutting concerns
- Python package dependencies (requirements.txt)
- Git configuration and repository setup

### Repository
- **GitHub**: [willywil/AutoFalloutShelter](https://github.com/willywil/AutoFalloutShelter)
- **License**: MIT

---

## Project Status

🚧 **Current Phase**: Foundation & Planning

The project is in initial planning and architecture phase. Core specifications are complete and ready for implementation.

### Next Milestones

1. **v0.1.0 - MVP (Target: March 2026)**
   - Basic computer vision (resource detection)
   - Simple automation (resource collection)
   - Incident detection and response
   - Dweller assignment

2. **v0.2.0 - Enhanced Automation (Target: April 2026)**
   - Advanced CV (room states, dweller tracking)
   - Optimized assignment algorithms
   - Training management
   - Room building

3. **v1.0.0 - Stable Release (Target: June 2026)**
   - All critical and high-priority features
   - 70%+ test coverage
   - Complete documentation
   - 24h+ unattended operation

---

## Development Notes

- All changes should reference GitHub issues
- Follow [conventional commits](https://www.conventionalcommits.org/) for commit messages
- Update this file under `[Unreleased]` section for all notable changes
- Move changes to versioned section upon release

---

## Template for New Entries

```markdown
## [Version] - YYYY-MM-DD

### Added
- New feature description (#issue)

### Changed
- Modified behavior description (#issue)

### Deprecated
- Soon-to-be removed feature (#issue)

### Removed
- Removed feature (#issue)

### Fixed
- Bug fix description (#issue)

### Security
- Security improvement (#issue)
```
