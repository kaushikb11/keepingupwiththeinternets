# 🎙️ Keeping Up with the Internets

An AI-powered podcast generator that turns Reddit's r/OutOfTheLoop top weekly discussions into engaging audio content.

## 🌟 Features

- **Automated Content Curation**: Fetches and processes top posts from r/OutOfTheLoop
- **Intelligent Script Generation**: Creates dynamic, multi-persona discussions
- **Natural Dialogue**: Features Host, Learner, and Expert perspectives
- **Audio Generation**: Converts scripts to podcast-ready audio
- **Parallel Processing**: Efficiently handles multiple posts and sections

## 🛠️ Architecture

The project uses LangGraph for orchestrating the podcast generation workflow:

1. **Content Collection**
   - Fetches top posts from r/OutOfTheLoop
   - Processes URLs and related content
   - Generates summaries using AI

2. **Script Planning**
   - Evaluates post relevance and discussion potential
   - Creates structured discussion plans
   - Organizes content into engaging sections

3. **Dialogue Generation**
   - Generates natural conversations between personas
   - Creates smooth transitions between topics
   - Enhances script flow and coherence

4. **Audio Production**
   - Converts final script to audio using Azure Speech Services
   - Handles proper pacing and formatting
