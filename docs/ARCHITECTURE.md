# System Architecture
**AutoFalloutShelter - Automated Gameplay System**

**Version:** 1.0  
**Last Updated:** February 15, 2026

---

## 1. Overview

AutoFalloutShelter is a multi-layered system that uses computer vision to understand game state, strategic algorithms to make decisions, and input automation to execute actions.

### 1.1 Design Principles

1. **Separation of Concerns**: Each module has a single, well-defined responsibility
2. **Modularity**: Components can be developed, tested, and deployed independently
3. **Loose Coupling**: Modules interact through well-defined interfaces
4. **Fail-Safe**: System degrades gracefully under errors
5. **Observable**: Comprehensive logging and monitoring
6. **Configurable**: Behavior customizable without code changes

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Control Loop                      │
│                    (main.py / Orchestrator)                 │
└───────────┬──────────────────────────────────────┬──────────┘
            │                                      │
            │ Game State                           │ Actions
            ↓                                      ↑
┌───────────────────────┐           ┌────────────────────────┐
│   Vision Module       │           │  Automation Module     │
│  (Screen Analysis)    │           │  (Input Control)       │
├───────────────────────┤           ├────────────────────────┤
│ • ScreenCapture       │           │ • InputController      │
│ • ImageRecognition    │           │ • GameActions          │
│ • TemplateMatching    │           │ • ActionQueue          │
│ • OCR Engine          │           │ • Coordinate Mapper    │
└─────────┬─────────────┘           └────────────────────────┘
          │                                     ↑
          │ GameState Object                    │ Action List
          ↓                                     │
┌──────────────────────────────────────────────┴──────────────┐
│               Strategy Module                                │
│            (Decision Making Engine)                          │
├─────────────────────────────────────────────────────────────┤
│ • ResourceManager    • IncidentHandler                       │
│ • DwellerManager     • RoomManager                          │
│ • TrainingManager    • PriorityScheduler                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ↓
        ┌──────────────────────────────────┐
        │      Data Models & State         │
        ├──────────────────────────────────┤
        │ • GameState    • Room            │
        │ • Dweller      • SPECIAL         │
        │ • Resource     • Incident        │
        └──────────────────────────────────┘

        ┌──────────────────────────────────┐
        │    Cross-Cutting Concerns        │
        ├──────────────────────────────────┤
        │ • Logging (utils)                │
        │ • Configuration                  │
        │ • Error Handling                 │
        │ • Performance Monitoring         │
        └──────────────────────────────────┘
```

### 2.2 Data Flow

```
User Starts Bot
      │
      ↓
┌──────────────────┐
│ Initialize       │ ← Load config, templates, setup logging
└────────┬─────────┘
         │
         ↓
┌────────────────────────────────────────────────────────┐
│              Main Automation Loop                      │
│  ┌──────────────────────────────────────────────┐     │
│  │ 1. CAPTURE: Screenshot game window           │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 2. ANALYZE: Extract game state via CV        │     │
│  │    • Detect resources, dwellers, rooms,      │     │
│  │      incidents using template matching + OCR │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 3. DECIDE: Evaluate situation & strategy     │     │
│  │    • Check for incidents (priority)          │     │
│  │    • Check resource levels                   │     │
│  │    • Optimize dweller assignments            │     │
│  │    • Plan room actions                       │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 4. ACT: Execute top-priority action          │     │
│  │    • Map action to screen coordinates        │     │
│  │    • Execute mouse/keyboard input            │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 5. VERIFY: Confirm action success            │     │
│  │    • Re-capture screen                       │     │
│  │    • Validate expected state change          │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 6. LOG: Record decision and outcome          │     │
│  └──────────────────┬───────────────────────────┘     │
│                     ↓                                  │
│  ┌──────────────────────────────────────────────┐     │
│  │ 7. WAIT: Sleep until next cycle              │     │
│  └──────────────────┬───────────────────────────┘     │
│                     │                                  │
│                     └──────────────────┐               │
│                                        ↓               │
│                     ┌─ No ─ Stop Signal? ─ Yes ─┐     │
│                     │                            ↓     │
│                     └─────────────────→  Shutdown      │
└────────────────────────────────────────────────────────┘
```

---

## 3. Module Specifications

### 3.1 Vision Module (`src/vision/`)

**Responsibility:** Capture and analyze game screen to extract structured game state.

#### Components:

##### 3.1.1 ScreenCapture
```python
class ScreenCapture:
    """Captures screenshots of the game window"""
    
    def __init__(self):
        self.game_window: WindowHandle
        self.capture_region: Rect
    
    def find_game_window() -> WindowHandle:
        """Detect Fallout Shelter window"""
    
    def capture() -> np.ndarray:
        """Capture current game screen as image array"""
    
    def is_game_active() -> bool:
        """Check if game window is visible and active"""
```

##### 3.1.2 ImageRecognition
```python
class ImageRecognition:
    """Analyzes screenshots to extract game state"""
    
    def __init__(self):
        self.templates: Dict[str, np.ndarray]
        self.ocr_engine: TesseractOCR
    
    def load_templates(template_dir: str):
        """Load reference images for matching"""
    
    def detect_resources(image: np.ndarray) -> ResourceLevels:
        """Extract power/food/water/caps from UI"""
    
    def detect_dwellers(image: np.ndarray) -> List[DwellerState]:
        """Find all visible dwellers and their states"""
    
    def detect_rooms(image: np.ndarray) -> List[RoomState]:
        """Identify rooms, types, and production states"""
    
    def detect_incidents(image: np.ndarray) -> List[Incident]:
        """Find active fires, attacks, etc."""
    
    def read_text(region: Rect) -> str:
        """OCR text from specified screen region"""
```

##### 3.1.3 GameStateParser
```python
class GameStateParser:
    """Combines CV results into structured GameState"""
    
    def parse(image: np.ndarray) -> GameState:
        """Convert screenshot to GameState object"""
    
    def validate_state(state: GameState) -> bool:
        """Sanity check extracted game state"""
```

**Outputs:** `GameState` object containing:
- Resource levels (power, food, water, caps)
- Dweller list with positions, stats, health
- Room list with types, production states, assignments
- Active incidents with locations and types
- UI element positions (for coordinate mapping)

---

### 3.2 Strategy Module (`src/strategy/`)

**Responsibility:** Analyze game state and decide optimal actions.

#### Components:

##### 3.2.1 PriorityScheduler
```python
class PriorityScheduler:
    """Determines what to do next based on game state"""
    
    def evaluate(game_state: GameState) -> Action:
        """Return highest-priority action to take"""
        
    # Priority order:
    # 1. CRITICAL: Handle incidents (fires, attacks)
    # 2. URGENT: Address resource emergencies
    # 3. HIGH: Collect ready resources
    # 4. MEDIUM: Optimize dweller assignments
    # 5. LOW: Training, building, upgrades
```

##### 3.2.2 ResourceManager
```python
class ResourceManager:
    """Manages resource collection and production"""
    
    def __init__(self):
        self.thresholds: ResourceThresholds
    
    def needs_urgent_action(game_state: GameState) -> Optional[Action]:
        """Check if resources critically low"""
    
    def should_collect(room: Room) -> bool:
        """Determine if room is ready to collect"""
    
    def prioritize_production() -> ResourceType:
        """Which resource needs production priority"""
```

##### 3.2.3 DwellerManager
```python
class DwellerManager:
    """Optimizes dweller job assignments"""
    
    def optimal_assignment(dweller: Dweller, rooms: List[Room]) -> Room:
        """Find best room for dweller based on SPECIAL"""
    
    def needs_reassignment(dweller: Dweller) -> bool:
        """Check if dweller should be moved"""
    
    def balance_assignments(game_state: GameState) -> List[Action]:
        """Generate actions to optimize all assignments"""
```

##### 3.2.4 IncidentHandler
```python
class IncidentHandler:
    """Responds to incidents"""
    
    def create_response_plan(incident: Incident, 
                            dwellers: List[Dweller]) -> List[Action]:
        """Generate actions to handle incident"""
    
    def select_responders(incident: Incident,
                         available: List[Dweller]) -> List[Dweller]:
        """Choose best dwellers to send"""
```

##### 3.2.5 RoomManager
```python
class RoomManager:
    """Manages room building and upgrades"""
    
    def should_build_room(game_state: GameState) -> Optional[RoomType]:
        """Decide if new room needed"""
    
    def should_upgrade_room(room: Room) -> bool:
        """Decide if room should be upgraded"""
    
    def calculate_rush_risk(room: Room) -> float:
        """Estimate rush failure probability"""
```

**Outputs:** `Action` objects representing decisions:
```python
@dataclass
class Action:
    type: ActionType  # CLICK, DRAG, COLLECT, ASSIGN, etc.
    priority: int
    target: ActionTarget  # What to interact with
    parameters: Dict[str, Any]  # Action-specific params
    expected_outcome: GameState  # For verification
```

---

### 3.3 Automation Module (`src/automation/`)

**Responsibility:** Execute actions by controlling mouse and keyboard.

#### Components:

##### 3.3.1 InputController
```python
class InputController:
    """Low-level input control"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def click(x: int, y: int):
        """Single click at coordinates"""
    
    def drag(x1: int, y1: int, x2: int, y2: int, duration: float):
        """Drag from point A to point B"""
    
    def hold_click(x: int, y: int, duration: float):
        """Click and hold (for rushing)"""
    
    def validate_coordinates(x: int, y: int) -> bool:
        """Check coordinates are within game window"""
```

##### 3.3.2 CoordinateMapper
```python
class CoordinateMapper:
    """Maps game elements to screen coordinates"""
    
    def __init__(self):
        self.game_bounds: Rect
        self.resolution: Tuple[int, int]
    
    def map_room_to_coords(room_position: Tuple[int, int]) -> Tuple[int, int]:
        """Convert logical room position to screen coords"""
    
    def map_dweller_to_coords(dweller_position: Tuple[int, int]) -> Tuple[int, int]:
        """Convert dweller position to screen coords"""
    
    def map_ui_element(element: UIElement) -> Tuple[int, int]:
        """Get coordinates for UI button/element"""
```

##### 3.3.3 GameActions
```python
class GameActions:
    """High-level game actions"""
    
    def __init__(self, input_controller: InputController):
        self.input = input_controller
        self.mapper = CoordinateMapper()
    
    def collect_resource(room: Room):
        """Click room to collect resources"""
    
    def assign_dweller(dweller: Dweller, room: Room):
        """Drag dweller to room"""
    
    def rush_room(room: Room):
        """Click and hold to rush production"""
    
    def send_to_incident(dweller: Dweller, incident: Incident):
        """Send dweller to handle incident"""
```

##### 3.3.4 ActionQueue
```python
class ActionQueue:
    """Manages queued actions"""
    
    def __init__(self):
        self.queue: PriorityQueue[Action]
    
    def enqueue(action: Action):
        """Add action to queue"""
    
    def dequeue() -> Action:
        """Get next action by priority"""
    
    def clear():
        """Remove all queued actions"""
    
    def execute_next() -> ActionResult:
        """Execute next action from queue"""
```

**Inputs:** `Action` objects from Strategy module  
**Outputs:** `ActionResult` objects (success/failure with details)

---

### 3.4 Models Module (`src/models/`)

**Responsibility:** Define data structures shared across modules.

#### Core Data Models:

```python
@dataclass
class GameState:
    """Complete game state at a point in time"""
    timestamp: float
    resources: ResourceLevels
    dwellers: List[Dweller]
    rooms: List[Room]
    incidents: List[Incident]
    ui_elements: Dict[str, UIElement]

@dataclass
class ResourceLevels:
    power: float  # 0.0 to 1.0
    food: float
    water: float
    caps: int
    stimpaks: int
    radaway: int

@dataclass
class SPECIAL:
    strength: int
    perception: int
    endurance: int
    charisma: int
    intelligence: int
    agility: int
    luck: int

@dataclass
class Dweller:
    id: str
    name: str
    level: int
    health: int
    happiness: int
    special: SPECIAL
    current_room_id: Optional[str]
    position: Tuple[int, int]
    is_training: bool
    is_exploring: bool
    is_pregnant: bool
    is_armed: bool

@dataclass
class Room:
    id: str
    room_type: RoomType
    level: int
    merge_size: int  # 1, 2, or 3
    position: Tuple[int, int]
    assigned_dwellers: List[str]
    production_state: ProductionState
    production_progress: float
    is_upgrading: bool

@dataclass
class Incident:
    type: IncidentType
    location: Tuple[int, int]
    room_id: str
    severity: int
    detected_at: float

@dataclass
class Action:
    type: ActionType
    priority: int
    target: ActionTarget
    parameters: Dict[str, Any]
    expected_outcome: Optional[GameState]
```

---

### 3.5 Utils Module (`src/utils/`)

**Responsibility:** Cross-cutting utilities and helpers.

#### Components:

```python
# Logging
def setup_logging(level: str, log_file: str):
    """Configure application logging"""

# Configuration
class Config:
    """Load and access configuration"""
    def __init__(self, config_file: str):
        self.settings: Dict[str, Any]
    
    def get(key: str, default: Any = None) -> Any:
        """Get configuration value"""

# Performance Monitoring
class PerformanceMonitor:
    """Track timing and performance metrics"""
    def start_timer(name: str):
        """Start timing operation"""
    
    def stop_timer(name: str) -> float:
        """Stop timer and return duration"""
    
    def get_metrics() -> Dict[str, float]:
        """Get all performance metrics"""

# Error Handling
class ErrorHandler:
    """Centralized error handling"""
    def handle_error(error: Exception, context: str):
        """Log error and determine recovery action"""
    
    def should_retry(error: Exception) -> bool:
        """Determine if error is transient"""
```

---

## 4. Integration and Control Flow

### 4.1 Main Loop (main.py)

```python
def main():
    # Initialize
    config = Config('config.json')
    setup_logging(config.get('log_level'))
    
    # Create modules
    screen_capture = ScreenCapture()
    image_recognition = ImageRecognition()
    game_state_parser = GameStateParser(image_recognition)
    
    strategy = PriorityScheduler(
        ResourceManager(config),
        DwellerManager(config),
        IncidentHandler(config),
        RoomManager(config)
    )
    
    automation = GameActions(
        InputController(),
        CoordinateMapper()
    )
    
    monitor = PerformanceMonitor()
    error_handler = ErrorHandler()
    
    # Main loop
    logger.info("Starting automation loop")
    
    while not stop_signal:
        try:
            cycle_start = time.time()
            
            # 1. Capture
            monitor.start_timer('capture')
            screenshot = screen_capture.capture()
            monitor.stop_timer('capture')
            
            # 2. Analyze
            monitor.start_timer('analyze')
            game_state = game_state_parser.parse(screenshot)
            monitor.stop_timer('analyze')
            
            # 3. Decide
            monitor.start_timer('decide')
            action = strategy.evaluate(game_state)
            monitor.stop_timer('decide')
            
            # 4. Act
            if action:
                monitor.start_timer('act')
                result = automation.execute(action)
                monitor.stop_timer('act')
                
                # 5. Verify
                if action.priority >= PRIORITY_HIGH:
                    verify_action_result(action, result)
                
                # 6. Log
                logger.info(f"Executed: {action.type} - {result.status}")
            
            # 7. Wait
            cycle_duration = time.time() - cycle_start
            sleep_time = max(0, config.get('cycle_time') - cycle_duration)
            time.sleep(sleep_time)
            
        except Exception as e:
            error_handler.handle_error(e, 'main_loop')
            if not error_handler.should_retry(e):
                break
    
    logger.info("Automation stopped")
```

### 4.2 Error Handling Strategy

```
Error Occurs
    │
    ↓
Classify Error Type
    │
    ├─→ Transient (e.g., CV detection failure)
    │       ↓
    │   Log warning
    │       ↓
    │   Retry (max 3x)
    │       ↓
    │   Continue with next cycle
    │
    ├─→ Recoverable (e.g., action failed)
    │       ↓
    │   Log error
    │       ↓
    │   Skip action
    │       ↓
    │   Continue with next cycle
    │
    └─→ Critical (e.g., game window lost)
            ↓
        Log critical error
            ↓
        Attempt recovery
            ↓
        If recovery fails → Graceful shutdown
```

---

## 5. Performance Considerations

### 5.1 Optimization Strategies

1. **Screen Capture:**
   - Capture only game window region, not full screen
   - Use efficient capture method (e.g., mss library)
   - Cache window position between captures

2. **Image Analysis:**
   - Use template matching only for regions of interest
   - Cache templates after loading
   - Use multi-scale matching only when needed
   - Optimize OCR regions (small, well-defined areas)

3. **Decision Making:**
   - Short-circuit evaluation (check critical conditions first)
   - Cache calculation results within cycle
   - Use heuristics to avoid expensive computations

4. **Action Execution:**
   - Batch related actions when possible
   - Use minimal delays while ensuring reliability

### 5.2 Resource Usage Targets

- **CPU:** <25% average, <50% peak
- **Memory:** <512MB
- **Disk I/O:** Log rotation to prevent disk filling
- **Cycle Time:** 1-5 seconds configurable

---

## 6. Scalability and Extensibility

### 6.1 Adding New Features

To add a new capability:

1. **New Game Element Detection:**
   - Add template images to `assets/`
   - Extend `ImageRecognition` with detection method
   - Update `GameState` model if needed

2. **New Strategy:**
   - Create new manager in `src/strategy/`
   - Integrate with `PriorityScheduler`
   - Add configuration options

3. **New Action Type:**
   - Define action in `ActionType` enum
   - Implement in `GameActions`
   - Add verification logic

### 6.2 Configuration Override

All behavior configurable via `config.json`:

```json
{
  "cycle_time": 2.0,
  "resource_thresholds": {
    "power": 0.7,
    "food": 0.6,
    "water": 0.6
  },
  "strategy_profile": "balanced",
  "features": {
    "auto_collect": true,
    "auto_assign": true,
    "auto_rush": false,
    "incident_response": true
  },
  "performance": {
    "capture_fps": 2,
    "use_ocr": true,
    "cache_templates": true
  }
}
```

---

## 7. Testing Strategy

### 7.1 Unit Tests
- Each module tested independently
- Mock dependencies (e.g., mock screenshots for CV tests)
- Test edge cases and error conditions

### 7.2 Integration Tests
- Test module interactions
- Use recorded game sessions for regression testing
- Validate full cycle execution

### 7.3 System Tests
- Run with actual game
- Monitor for extended periods (24h+ runs)
- Performance profiling under load

---

## 8. Deployment Architecture

```
AutoFalloutShelter/
├── main.py                 # Entry point
├── config.json             # User configuration
├── requirements.txt        # Dependencies
├── src/
│   ├── __init__.py
│   ├── vision/
│   ├── automation/
│   ├── strategy/
│   ├── models/
│   └── utils/
├── assets/
│   └── templates/          # Reference images
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/           # Test screenshots
├── docs/
│   ├── REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   └── USER_GUIDE.md
└── logs/                   # Runtime logs
```

---

## 9. Security and Safety

### 9.1 Safety Mechanisms

1. **Failsafe:** PyAutoGUI corner failsafe enabled
2. **Validation:** All coordinates validated before clicking
3. **Isolation:** Only interact with game window
4. **Monitoring:** Log all actions for auditability

### 9.2 Security Considerations

- No network communication
- No sensitive data collection
- Read/write only to project directory
- No system-level modifications

---

## 10. Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-15 | Initial | Initial architecture specification |

---

**Document Status:** Draft - Ready for Review
