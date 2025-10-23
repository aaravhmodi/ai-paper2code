# 🧬 AI Paper-to-Code Generator

> **Retrieve, analyze, and reconstruct AI research into working code prototypes.**  
> Built with **PyTorch, LangChain, ChromaDB, and an MCP Server**.

---

## 🚀 Overview

**AI Paper-to-Code** is an intelligent Retrieval-Augmented Generation (RAG) system that reads research papers from **arXiv** and automatically generates **code skeletons**, summaries, and algorithm prototypes.

It bridges the gap between academic research and implementation by embedding papers into a **vector database (ChromaDB)**, retrieving contextually relevant content, and using language models to convert theory into executable code.

---

## 🧠 System Architecture

```text
┌──────────────────────────┐
│    Document Sources      │
│  (arXiv / PDFs / Docs)   │
└────────────┬─────────────┘
             │
        [Ingestion & Embedding]
             │
┌──────────────────────────────┐
│         ChromaDB             │
│  (Stores text + vectors)     │
└────────────┬────────────────┘
             │
        [Retriever Layer]
             │
┌──────────────────────────────┐
│     PyLang RAG Pipeline      │
│ (Retrieve + Generate chain)  │
└────────────┬────────────────┘
             │
        [MCP Server API]
             │
┌──────────────────────────────┐
│   Frontend / Agent System    │
│  (Chat UI / LangGraph / VS)  │
└──────────────────────────────┘
