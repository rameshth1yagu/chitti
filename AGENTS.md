# Chitti AI Agent Context

## 🤖 System Identity
- **Name:** Chitti
- **Role:** Autonomous UGV (Unmanned Ground Vehicle)
- **Architecture:** NVIDIA Jetson Orin Nano (JetPack 6.1) -> Waveshare UGV Board

## 🛠️ Current Hardware Context
- **Motor Controller:** Serial (/dev/ttyACM0) @ 1000000 baud
- **MCP Server:** Running in JAX Docker container (jetson_container_20260308_221107)
- **Primary Libraries:** JAX, FastMCP, PySerial

## 📏 Operational Constraints
- **Battery Safety:** Do not move if voltage < 11.0V.
- **Motor Limit:** Max power 0.3 (30%) for indoor testing.

## ✅ Completed Milestones
- **Phase 1:** MCP Bridge Established. Natural language motor control active.
