# Harness vs Framework vs Platform

In the rapidly evolving landscape of generative AI, the terminology used to describe the infrastructure stack is often overloaded. To understand the purpose of the Agent Harness Cookbook, we must strictly define the boundaries between a **Framework**, a **Platform**, and a **Harness**.

## The Agent Framework (e.g., LangGraph, AutoGen, CrewAI)
An agent framework is the orchestration layer. It provides the abstractions needed to build agentic workflows: state graphs, memory checkpointers, prompt templating, and tool-binding utilities. 
- **Purpose:** To make the LLM "do things" efficiently (looping, reasoning, calling tools).
- **The Problem:** Frameworks are optimized for flexibility and capability, not enterprise security. They will happily execute a malicious SQL query if the LLM decides it's the right next step.

## The AI Platform (e.g., AWS Bedrock, Vertex AI, Azure OpenAI)
An AI Platform provides the hosted runtime environment, model endpoints, and foundational infrastructure. They often include built-in vector databases, model routing, and basic data governance (like opting out of training data).
- **Purpose:** To provide scalable, reliable compute and model inference.
- **The Problem:** Platforms operate at the infrastructure layer. They do not understand the specific business logic, actor chains, or fine-grained tool privileges of your specific application.

## The Agent Harness (This Cookbook)
An agent harness is the deterministic **security and design layer** that sits *around* the framework and *on top* of the platform. It can be implemented across any framework or internal runtime.

- **Purpose:** To make capability explicit, bounded, and auditable.
- **How it works:** If LangGraph is the engine that drives the car, the Harness is the steering wheel, the brakes, and the seatbelts. 

The harness does not care *how* the framework loops or *which* platform is serving the model. Its only job is to intercept the data flowing into the framework (Input Guards, Memory Isolation) and the decisions flowing out of the framework (Tool Privilege Brokers, Sandboxing) to enforce deterministic enterprise policy.

By decoupling the Harness from the Framework, you ensure that even if you migrate from Semantic Kernel to LangGraph next year, your security boundaries, audit trails, and approval gates remain intact.

## What Else Is Needed

The harness is one layer. Production agent systems also need API gateways,
identity federation (OAuth 2.0, OIDC), principal propagation through tool calls,
secret management, network security, and compliance framework integration. See
[What This Cookbook Does Not Cover](what-this-cookbook-does-not-cover.md) for the
full list.
