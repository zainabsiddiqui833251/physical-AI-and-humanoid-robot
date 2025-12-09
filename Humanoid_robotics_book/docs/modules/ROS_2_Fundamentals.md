---
title: "ROS 2 Fundamentals"
sidebar_position: "2"
---

# Module 2: ROS 2 Fundamentals

## Introduction

Welcome to the ROS 2 Fundamentals module. This module provides a comprehensive introduction to the Robot Operating System 2 (ROS 2), a flexible framework for writing robot software. ROS 2 is an open-source, meta-operating system that helps you build robot applications. It provides libraries and tools to help you build and run complex robot behavior across a wide variety of robotic platforms.

## Key Concepts

ROS 2 is designed to support a wide range of robotic applications, from individual robots to large, multi-robot systems. Key concepts include:

*   **Distributed System:** ROS 2 is inherently a distributed system, allowing different processes (nodes) to run on different machines and communicate seamlessly.
*   **Middleware Abstraction:** ROS 2 utilizes DDS (Data Distribution Service) as its underlying middleware, providing robust, real-time communication capabilities.
*   **Real-time Capabilities:** Designed with real-time control in mind, ROS 2 offers better performance and reliability for time-sensitive robotic tasks.
*   **Multi-platform Support:** ROS 2 supports Linux, macOS, and Windows.
*   **Component-Based Architecture:** Applications are built from small, reusable pieces called nodes.

## Learning Outcomes

Upon completing this module, you will be able to:

*   Understand the fundamental architecture and core concepts of ROS 2.
*   Differentiate and effectively use ROS 2 nodes, topics, services, and actions for inter-process communication.
*   Create, build, and manage ROS 2 packages using Python.
*   Utilize launch files for orchestrating and managing ROS 2 nodes.
*   Implement and manage ROS 2 parameters for dynamic node configuration.
*   Gain practical experience in developing basic ROS 2 robotic applications.

## Examples

Throughout this module, practical examples will be provided to illustrate each concept, including:

*   Creating simple publisher and subscriber nodes.
*   Implementing custom ROS 2 services and actions.
*   Building a basic ROS 2 package with Python nodes.
*   Using launch files to start complex robotic systems.
*   Configuring node behavior using parameters.

## Core Topics

### 1. ROS 2 Architecture and Core Concepts

*   **What is ROS?** Understanding the purpose and history of ROS and ROS 2.
*   **ROS 2 Concepts:**
    *   **Nodes:** Independent processes that perform computations.
    *   **Topics:** Asynchronous message passing for data streams (publish/subscribe).
    *   **Services:** Synchronous request/reply communication (client/server).
    *   **Actions:** Asynchronous, goal-oriented communication for long-running tasks.
    *   **Parameters:** Dynamic configuration values for nodes.
    *   **Messages and Data Types:** Defining and using data structures for communication.
*   **ROS 2 Middleware (DDS):** How DDS enables robust communication.
*   **Build System (ament/colcon):** Understanding how ROS 2 code is built.
*   **ROS 2 Graph:** Visualizing the communication between nodes.

### 2. Nodes, Topics, Services, and Actions

*   **Nodes:** Creating and running ROS 2 nodes.
*   **Topics:**
    *   Publishing and subscribing to messages.
    *   Common message types (e.g., `std_msgs`, `geometry_msgs`).
    *   Quality of Service (QoS) settings for reliable communication.
*   **Services:**
    *   Defining service interfaces (`.srv` files).
    *   Implementing service servers and clients.
*   **Actions:**
    *   Defining action interfaces (`.action` files).
    *   Implementing action servers and clients.
    *   Feedback and goal management.

### 3. Building ROS 2 Packages with Python

*   **Package Structure:** Understanding the `package.xml` and `CMakeLists.txt` (or `setup.py`/`setup.cfg` for Python).
*   **Creating a ROS 2 Package:** Using `ros2 pkg create`.
*   **Writing Python Nodes:**
    *   Basic node structure using `rclpy`.
    *   Node lifecycle management.
    *   Spinning the node.
*   **Building and Sourcing:** Using `colcon build` and `source` commands.
*   **Debugging Python Nodes:** Using `print` statements and ROS 2 logging.

### 4. Launch Files and Parameter Management

*   **Launch Files:**
    *   Understanding Python-based launch files.
    *   Launching multiple nodes simultaneously.
    *   Controlling node behavior with arguments.
*   **Parameter Management:**
    *   Declaring parameters in nodes.
    *   Getting, setting, and updating parameters dynamically.
    *   Using `ros2 param` command-line tool.
    *   Passing parameters via launch files.

## Time Duration

### 3-5 weeks
This module is estimated to take **3 to 5 weeks** to complete, allowing for hands-on practice and understanding of the core ROS 2 concepts.


