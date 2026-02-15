# Phased Development Plan
**AutoFalloutShelter - Specification-Driven Development Roadmap**

**Version:** 1.0  
**Date:** February 15, 2026  
**Approach:** Specification-first with automated asset acquisition as critical prerequisite

---

## Overview

Development is organized into **6 major phases**, with **Phase 0 (Asset Acquisition)** being the critical foundation that every subsequent phase depends on. Each phase includes:
- Specific requirements to implement
- Implementation tasks
- Testing strategy
- Acceptance criteria
- Dependencies on prior phases

---

## Phase 0: Automated Asset Acquisition System (WEEKS 1-4)

**Purpose:** Build the infrastructure for capturing, validating, and managing OpenCV template images and OCR training data.

**Why It's First:** No computer vision can work without template images. This phase builds an automated system that continuously supplies the rest of the application.

### Requirements to Implement
- **ASSETS-1**: Asset Capture & Storage
- **ASSETS-2**: Dynamic Asset Discovery & Monitoring
- **ASSETS-3**: Asset Validation & Quality Control
- **ASSETS-4**: Asset Update Management
- **ASSETS-5**: Asset Training Data (OCR)
- **ASSETS-6**: Asset Inventory & Reporting

### Key Components to Build

#### Week 1: Foundation & Capture System
1. **Asset Repository Structure**
   - Create folder hierarchy: `assets/templates/ui/`, `assets/templates/rooms/`, etc.
   - Define metadata schema (JSON for asset descriptions)
   - Implement version control for assets

2. **Screenshot Capture Module** (`src/assets/capture.py`)
   - Implement `ScreenCapture.screenshot()` at configurable resolution
   - Support multiple resolutions (720p, 1080p, 1440p, 4K)
   - Platform-specific capture (Windows, macOS, Linux)
   - Timestamp and tag all captures

3. **Asset Organization**
   - Implement asset naming conventions
   - Create folder structure generator
   - Build metadata writer

#### Week 2: Discovery & Quality Control
1. **UI Element Detection** (`src/assets/discovery.py`)
   - Implement screen region analyzer (detect layout changes)
   - Build pixel-level change detector (compare frame-to-frame)
   - Create element classifier (identify UI buttons, text, icons)

2. **Quality Validation** (`src/assets/validation.py`)
   - Image quality checker (brightness, contrast, clarity)
   - Dimension verification
   - Template matching validation (test against other templates)
   - OCR sample quality assessment

3. **Flagging System**
   - Mark low-quality assets for manual review
   - Generate quality reports
   - Support manual re-capture workflow

#### Week 3: Update Management & OCR Data
1. **Asset Update Detector** (`src/assets/updates.py`)
   - Compare new captures with historical versions
   - Classify changes (minor vs. significant)
   - Version history maintenance

2. **OCR Training Data Collection** (`src/assets/ocr_training.py`)
   - Capture text samples (metric names, numbers)
   - Organize by category (5 numeric values, 3 metric names, etc.)
   - Validate training data diversity

3. **Dependency Management**
   - Notify dependent modules of asset updates
   - Support gradual rollout (A/B testing old vs. new)

#### Week 4: Inventory & Automation
1. **Asset Registry** (`src/assets/registry.py`)
   - Build searchable asset database
   - Implement metadata queries
   - Generate asset coverage reports

2. **End-to-End Automation**
   - Implement automated discovery cycle
   - Background monitoring task
   - Alert system for unexpected elements
   - Human review workflow integration

3. **Documentation**
   - Asset catalog and usage guide
   - Metadata schema documentation
   - Troubleshooting guide

### Testing Strategy

```python
# Unit Tests
tests/unit/test_asset_capture.py       # Screenshot capture accuracy
tests/unit/test_asset_discovery.py     # UI element detection
tests/unit/test_asset_validation.py    # Quality assurance
tests/unit/test_asset_registry.py      # Metadata management

# Integration Tests
tests/integration/test_asset_cycle.py  # Full capture-validate-store cycle
tests/integration/test_ocr_collection.py # OCR training data collection

# System Tests
tests/system/test_continuous_discovery.py # 24h+ monitoring
```

### Success Criteria for Phase 0

- ✅ All 20+ asset types captured (UI buttons, text, icons, etc.)
- ✅ Assets organized in proper folder structure
- ✅ Quality validation passing on all captures (≥90% quality score)
- ✅ OCR training data collected (50+ samples minimum)
- ✅ Discovery system detects new UI changes within 5 minutes
- ✅ Version history maintained with rollback capability
- ✅ Automated cycle runs successfully for 24+ hours
- ✅ Documentation complete and tested

### Deliverables

```
Phase 0 Completion:
├── assets/templates/          (20+ template images organized)
├── assets/training/           (OCR training datasets)
├── src/assets/                (4 modules: capture, discovery, validation, registry)
├── data/asset_registry.json   (complete asset inventory)
├── docs/ASSET_ACQUISITION_GUIDE.md
└── tests/                     (comprehensive test suite)
```

---

## Phase 1: Human Interface & System Monitoring (WEEKS 5-6)

**Purpose:** Build operator dashboard and system health monitoring before implementing AI logic.

**Dependencies:** Phase 0 must be complete (assets functioning)

### Requirements to Implement
- **HUI-1**: Operator Dashboard
- **HUI-2**: Human Control Detection
- **HUI-3**: Operator Notifications
- **SYS-1**: Memory Management & Leak Detection
- **SYS-2**: Comprehensive Logging
- **SYS-3**: Process Monitoring
- **SYS-4**: Performance Profiling

### Key Components to Build

#### Week 5: Dashboard & Monitoring
1. **Operator Dashboard** (`src/ui/dashboard.py`)
   - Real-time game state display
   - AI control status indicator
   - Latest actions log viewer
   - Performance metrics panel
   - CLI version of dashboard

2. **Logging System** (`src/system/logging.py`)
   - Structured JSON logging
   - Multiple log levels
   - Log rotation and archiving
   - Real-time log queries

3. **Memory Monitoring** (`src/system/memory.py`)
   - Per-module memory tracking
   - Memory usage trends
   - Leak detection algorithm
   - Automatic alerts and recovery

#### Week 6: Control Detection & Performance
1. **Human Input Detection** (`src/ui/control_detector.py`)
   - Mouse/keyboard monitoring
   - Game state change detection
   - Human vs. AI action discrimination

2. **Notification System** (`src/ui/notifications.py`)
   - Alert generation and delivery
   - Priority levels
   - History and acknowledgment

3. **Performance Profiler** (`src/system/profiler.py`)
   - Component-level timing
   - Bottleneck identification
   - Trend tracking

### Testing Strategy

```python
tests/unit/test_dashboard.py
tests/unit/test_logging.py
tests/unit/test_memory_monitoring.py
tests/unit/test_control_detection.py
tests/integration/test_dashboard_integration.py
tests/system/test_24h_monitoring.py
```

### Success Criteria for Phase 1

- ✅ Dashboard displays game state accurately
- ✅ Human input detected within 100ms
- ✅ Memory leaks detected automatically
- ✅ All actions logged with timestamps
- ✅ Performance bottlenecks identified
- ✅ System runs stable for 24+ hours under monitoring

---

## Phase 2: Core Computer Vision (WEEKS 7-10)

**Purpose:** Implement vision modules using captured assets, starting with detection before complex analytics.

**Dependencies:** Phase 0 (assets), Phase 1 (logging & monitoring)

### Requirements to Implement
- **CV-1**: Screen Capture (using Phase 0 assets)
- **CV-2**: Resource Detection (fuel, power, food, water)
- **CV-3**: Dweller Detection (location, status)
- **CV-4**: Room Detection (type, occupancy)
- **CV-5**: Incident Detection (fires, attacks, etc.)

### Development Approach

**Week 7-8: Basic Detection**
- Template matching for UI elements
- Resource level reading (using OCR)
- Dweller position tracking

**Week 9-10: Advanced Recognition**
- Incident pattern detection
- State change tracking
- Confidence scoring

### Deliverables
```
src/models/        (GameState, Dweller, Room, etc.)
src/vision/        (detection modules)
tests/vision/      (vision tests)
```

---

## Phase 3: Control & State Management (WEEKS 11-12)

**Purpose:** Implement automation input control and AI/human state management.

**Dependencies:** Phase 0, 1, 2

### Requirements to Implement
- **AUTO-1**: Input Controller
- **AUTO-2**: Action Queue
- **AUTO-3**: Action Verification
- **CTL-1**: AI vs. Human Awareness
- **CTL-2**: Action Conflict Resolution

### Deliverables
```
src/automation/    (input control modules)
src/control/       (state management)
```

---

## Phase 4: Strategy & Decision Making (WEEKS 13-16)

**Purpose:** Implement core AI logic for resource and dweller management.

**Dependencies:** Phase 0, 1, 2, 3

### Requirements to Implement
- **STRAT-1**: Resource Management
- **STRAT-2**: Dweller Assignment
- **STRAT-3**: Incident Response
- **STRAT-4**: Training Management
- **STRAT-5**: Room Building

### Deliverables
```
src/strategy/      (decision making modules)
```

---

## Phase 5: Analytics & Learning (WEEKS 17-24)

**Purpose:** Implement data collection and generational learning system.

**Dependencies:** Phase 0, 1, 2, 3, 4

### Requirements to Implement
- **ANALYTICS-1**: Stats Menu Reading
- **ANALYTICS-2**: Shelter Statistics
- **ANALYTICS-3**: Time-Series Tracking
- **ANALYTICS-4**: Decision Integration
- **ANALYTICS-5**: Performance Analytics
- **ANALYTICS-6**: Data Storage
- **LRN-1**: Strategic Learning
- **LRN-2**: Generational Evolution
- **LRN-3**: Resource Learning
- **LRN-4**: Incident Learning
- **LRN-5**: Feedback Integration

### Development Pattern
1. **Weeks 17-18:** Stats collection, basic analytics
2. **Weeks 19-20:** Time-series database, trend analysis
3. **Weeks 21-22:** Learning framework, decision feedback
4. **Weeks 23-24:** Generational evolution, strategy mutation

### Learning Cycle Details

**Generation Period:** 24 hours of gameplay

**Generational Evolution Process:**
```
Day N Gameplay          Day N+1 Analysis        Day N+2 Implementation
└─ Collect all          ├─ Analyze stats        ├─ Mutate parameters
  decisions            ├─ Identify winners     ├─ Test new strategy
└─ Record outcomes      ├─ Find patterns        ├─ Compare performance
                       └─ Score strategies     └─ Deploy best strategy
```

### Deliverables
```
src/analytics/     (stats collection modules)
src/learning/      (learning framework)
data/*.db          (time-series database)
```

---

## Phase 6: Polish & Optimization (WEEKS 25-26)

**Purpose:** Performance optimization, documentation, and MVP release.

**Dependencies:** All prior phases

### Activities
- Performance bottleneck elimination
- Code cleanup and standards compliance
- Comprehensive documentation
- Extended stability testing (72+ hours)
- User manual and troubleshooting guide

### Deliverables
```
README.md           (updated with full guide)
INSTALLATION.md     (setup instructions)
USER_GUIDE.md       (operation manual)
TROUBLESHOOTING.md
ARCHITECTURE.md     (updated)
```

---

## Overall Timeline

| Phase | Duration | Focus | Dependencies |
|-------|----------|-------|--------------|
| **Phase 0** | Weeks 1-4 | Assets Acquisition | None |
| **Phase 1** | Weeks 5-6 | UI & Monitoring | Ph0 |
| **Phase 2** | Weeks 7-10 | Vision | Ph0, Ph1 |
| **Phase 3** | Weeks 11-12 | Control & State | Ph0-2 |
| **Phase 4** | Weeks 13-16 | Strategy | Ph0-3 |
| **Phase 5** | Weeks 17-24 | Analytics & Learning | Ph0-4 |
| **Phase 6** | Weeks 25-26 | Polish & Release | Ph0-5 |
| **Total** | **26 weeks** | Full MVP System | |

---

## Key Principles

### 1. Specification-Driven
- Requirements drive all implementation
- Code written to satisfy specific requirements
- No scope creep without requirement changes

### 2. Automated Asset Foundation
- Manual work minimized through automation
- Assets continuously refreshed
- System self-healing for visual changes

### 3. Operator Visibility
- Dashboard always showing system state
- Logging comprehensive and queryable
- Performance never "mysterious"

### 4. Incremental Learning
- Each generation builds on previous success
- Operator feedback integrated immediately
- Performance metrics tracked across generations

### 5. Testing First
- Tests written before implementation
- Acceptance criteria determined upfront
- Phase completion verified by tests

---

## Success Metrics by Phase

| Phase | Target Success Rate | Target Performance |
|-------|-------------------|-------------------|
| Ph0 | 100% asset coverage | Zero data loss |
| Ph1 | 100% action logging | <5% overhead |
| Ph2 | ≥95% detection accuracy | <500ms per frame |
| Ph3 | ≥98% action success | <100ms per action |
| Ph4 | ≥90% decision correctness | <200ms per decision |
| Ph5 | ≥85% prediction accuracy | ≥10% improvement/generation |
| Ph6 | 24h+ continuous uptime | Zero critical bugs |

---

## Phase 0 Start: Next Steps

1. **Read Requirements**
   - Study REQUIREMENTS.md sections on ASSETS-1 through ASSETS-6
   - Review STATS_MENU_RESEARCH.md for context on what will be captured

2. **Set Up Project Structure**
   - Create asset folder hierarchy
   - Set up database schema for asset registry
   - Initialize version control for assets

3. **Begin Asset Capture**
   - Launch Fallout Shelter
   - Implement basic screenshot capture
   - Start collecting initial UI templates

4. **Implement Discovery**
   - Build detection system for new UI elements
   - Create quality validation tests
   - Set up continuous monitoring

**Estimated Time to Phase 0 Completion:** 4 weeks with focused development

---

*This plan is living documentation. Phases may be adjusted based on implementation learnings, but the Phase 0-first sequence is non-negotiable as all vision systems depend on available assets.*
