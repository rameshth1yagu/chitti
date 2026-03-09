# Chitti Robot Context
- **Hardware:** NVIDIA Jetson Orin Nano, Waveshare UGV.
- **Goal:** Principal Robotics pivot. Use JAX for all AI logic.
- **Safety:** Never move if voltage < 11.5V.
- **Available Tools:** Use the `chitti_mcp` server for hardware access.
## Workspace Mapping
- **Host Path:** `~/chitti/jetson_container`
- **Container Path:** `/workspace`
- **Note:** All `.whl` and infrastructure files are in `/workspace/mcp_deps`.