
# CLAUDE.md — Project Chitti (Cognitive Edge Sentry)

## Project Identity

* **Name**: Project Chitti — Cognitive Edge Sentry
* **Repo Root**: `~/chitti/`
* **Purpose**: A persistent, multi-home autonomous AI agent that discovers, maps, and remembers environments using on-device VLM and SLAM.
* **Core Innovation**: Combines volatile visual processing (RAM-only frames) with **Multi-Tenant Semantic Memory** (SSD-based SQLite) to manage multiple houses.

## ⚠️ STRICT DIRECTIVES

* **Directory Lock**: All modifications, creations, logs, and data **MUST** stay within `~/chitti/`.
* **System Safety**: Never modify files in `/etc/`, `/var/`, or `/usr/`.
* **TDD Requirement**: 1. Write Test → 2. Implement → 3. Verify → 4. Refactor.
* **Privacy**: Raw frames must stay in `/dev/shm` and be purged immediately after inference. Only metadata, coordinates, and maps reach the SSD.

## Control & Authorization
* **Confirmation Trigger**: Before pivoting from a planned task or changing a core architectural decision (e.g., changing a ROS 2 message type or shifting I2C addresses), I must ask: "I am proposing a deviation from the plan. Do you approve?"
* **Deletion Safety**: If a refactor requires removing a file, I must first suggest the deletion and wait for your confirmation.

## Hardware Stack

* **Edge Brain**: NVIDIA Jetson Orin Nano SUPER (8GB LPDDR5).
* **Middleware**: JetPack 6.1, ROS 2 Humble, CycloneDDS.
* **Control**: Waveshare UGV Rover via PCA9685 I²C (Bus 1, 0x40).
* **Sensing**: CSI Camera (`/dev/video0`) and RPLidar.

---

## 🛰️ Communication & Memory Architecture

### 1. ROS 2 Topics (Internal Nervous System)

**Use for**: High-frequency telemetry and hardware control.

* **Examples**: `/camera/image_raw`, `/cmd_vel`, `/scan`, `/tf`, `/battery_state`.

### 2. MCP Tools & Resources (Agentic Brain)

**Use for**: High-level reasoning, memory retrieval, and multi-step tasks.

* **Tools**: `capture_and_analyze()`, `initiate_discovery(house_name)`, `move_to_room(name)`, `get_logs(category)`.
* **Resources**: `chitti://telemetry`, `chitti://knowledge_base`, `chitti://map_metadata`.

### 3. Persistent Data Structure (`~/chitti/data/`)

* `maps/`: Stores `.yaml` and `.posegraph` files for persistent floorplans.
* `chitti.db`: SQLite database for houses, room labels, and object coordinates.
* `logs/`: Logical JSON logs (system, vision, safety, motion, discovery).

---

## Detailed Roadmap & Task Specifications

### Phase 0: Investigative Refactor (Mandatory)

* **Logic**: Audit existing codebase for SSD-write leaks, architectural debt, and naming violations.
* **Implementation**: Modularize logic into `core/`, `safety/`, `hri/`, and `config/`. Initialize `data/chitti.db`.
* **Validation**: `pytest tests/test_imports.py` must pass for all modular paths.
* **Complete when**: Repository structure is clean, functions have type hints, and the database schema is initialized.

### Phase 1: Foundation, Safety & Privacy

* **Task 1.1: Environment Hardening**
* **Logic**: Lock hardware into MAXN power mode and pin clocks to prevent thermal-induced latency spikes.
* **Implementation**: Script `setup_maxn.sh` (nvpmodel + jetson_clocks).
* **Validation**: `jtop` confirms 25W mode and max GPU frequency.
* **Complete when**: `verify_jetson_setup.py` confirms the system is locked for high-performance AI.


* **Task 1.2: Volatile Privacy Pipeline**
* **Logic**: Capture CSI frames to RAM (`/dev/shm`) and purge post-inference to ensure zero SSD residue.
* **Implementation**: Use OpenCV GStreamer pipeline with a `tmpfs` target.
* **Validation**: `lsof` check proves no image files exist on the root SSD during capture.
* **Complete when**: 50-cycle audit confirms zero bytes of image data residue on SSD.


* **Task 1.3: Safety Systems**
* **Logic**: Implement a "Dead Man's Switch" via GPIO. Relay Pin 26 must stay HIGH to keep motors powered.
* **Implementation**: `safety/estop.py` daemon flips Pin 26 to LOW if heartbeat fails (>2s).
* **Validation**: Manually kill the process; verify motor power relay clicks OFF within 2s.
* **Complete when**: Hardware failsafe is verified to cut power on crash or high temp (>80°C).



### Phase 2: The Nervous System (ROS 2 & MCP)

* **Task 2.1: ROS 2 Migration**
* **Logic**: Move hardware I/O to ROS 2 Topics using Shared Memory (Iceoryx) for zero-copy efficiency.
* **Implementation**: Create nodes for `camera`, `motor`, and `safety`.
* **Validation**: `ros2 topic delay /camera/image_raw` shows <10ms latency.
* **Complete when**: All hardware interaction is handled via ROS 2 messages.


* **Task 2.2: MCP Server Bridge**
* **Logic**: Wrap ROS 2 Services and SQLite queries into MCP Tools for LLM access.
* **Implementation**: `hri/mcp_server.py`. Map `move_robot` to ROS 2 actions.
* **Validation**: Trigger `capture_and_analyze()` from AI; verify text summary response.
* **Complete when**: Robot reflexes are exposed as high-level "thoughts" for the AI.


* **Task 2.3: UGV Kinematics**
* **Logic**: Translate Twist (v, w) to PCA9685 PWM signals for differential drive.
* **Implementation**: Write `core/kinematics.py` with 400kHz I2C communication.
* **Validation**: Robot moves exactly 1 meter with <5% error.
* **Complete when**: `cmd_vel` inputs produce accurate physical movement.



### Phase 3: Performance & Edge DevOps

* **Task 3.1: TensorRT Acceleration**
* **Logic**: Quantize VLM to FP16 using `trtexec` to utilize the 1024 CUDA cores.
* **Implementation**: Build `.engine` file; update `core/inference.py` to use TensorRT bindings.
* **Validation**: Inference time per frame must be <600ms.
* **Complete when**: TensorRT engine replaces standard CPU/GPU inference.


* **Task 3.2: C++ Bottleneck Port**
* **Logic**: Port high-frequency I/O (encoding/capture) to C++ to free CPU for the AI brain.
* **Implementation**: Create `core/bindings.cpp` using `pybind11` and LibArgus.
* **Validation**: Frame capture-to-encoding latency drops by >50%.
* **Complete when**: Python layer uses C++ backend for performance-critical tasks.


* **Task 3.3: Containerization**
* **Logic**: Build an L4T multi-stage Docker image to isolate all dependencies.
* **Implementation**: Use `nvcr.io/nvidia/l4t-base`; volume mount `~/chitti/data`.
* **Complete when**: `docker-compose up` launches the full stack on any JetPack 6.1 install.



### Phase 4: Persistent Autonomy & Spatial Learning

* **Task 4.1: Persistent SLAM**
* **Logic**: Enable `slam_toolbox` map serialization to save/load house floorplans.
* **Implementation**: Save `.posegraph` files to `data/maps/`.
* **Validation**: Reboot; call `localize`; robot finds pose on saved map in <5s.
* **Complete when**: Chitti can load a specific house blueprint on command.


* **Task 4.2: Semantic Learning**
* **Logic**: Map VLM descriptions to (x, y) coordinates in `chitti.db`.
* **Implementation**: Tool `label_room("Kitchen")` links current pose to "Kitchen" in SQLite.
* **Validation**: "Go to Kitchen" command navigates robot to correct saved coordinates.
* **Complete when**: AI can query the SQLite DB to find and navigate to saved landmarks.



### Phase 5: Discovery & Multi-Home Intelligence

* **Task 5.1: Autonomous Discovery Mode**
* **Logic**: Implement Frontier Exploration to detect "unexplored" boundaries and generate Nav2 goals.
* **Implementation**: MCP Tool `initiate_discovery(house_name)`. Loop: [Scan -> Explore -> Identify].
* **Validation**: Robot explores a 3-room area autonomously and returns to origin.
* **Complete when**: Robot successfully closes a new map and notifies the AI.


* **Task 5.2: Multi-Map Management**
* **Logic**: Associate `house_id` with maps and room registries in SQLite.
* **Implementation**: MCP Tool `switch_house(house_name)`. Triggers relocalization on a new map.
* **Validation**: Chitti identifies its location in House A after being moved from House B.
* **Complete when**: AI can switch environments and resume autonomy in <10 seconds.



---

## Critical Python Standards

* **Naming**: `snake_case` (vars/functions), `PascalCase` (classes), `UPPER_CASE` (constants).
* **Type Hints**: Mandatory for all function signatures.
* **Complexity**: Max 25 lines per function; max 3 levels of nesting. Use guard clauses.
* **Logging**: Split logs into logical files in `~/chitti/logs/`. Expose via `get_logs` MCP Tool.