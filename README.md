<div align="center">
  <img src="assets/image.png" alt="Keeping Up with the Internets" width="600"/>
  <h3>AI-Powered Internet Culture Podcasts</h3>
  <p>Transforming Reddit's most intriguing discussions into engaging audio content</p>
</div>

______________________________________________________________________

## 🌟 Overview

Ever felt overwhelmed trying to keep up with internet culture? We transform r/OutOfTheLoop's most engaging discussions into natural, conversational podcasts – making it easy to stay informed while on the go.

### ✨ Key Features

- 🎯 **Smart Content Curation** - Automatically selects the most meaningful discussions
- 🎭 **Multi-Persona Dialogue** - Natural conversations between different personas
- 🔍 **Deep Context Integration** - Synthesizes information from posts, comments, and related links
- 🎙️ **Professional Audio** - Converts discussions into podcast-ready content
- 🚀 **Weekly Updates** - Fresh episodes covering the latest internet phenomena

## 🛠️ Architecture

The project uses LangGraph for orchestrating the podcast generation workflow:

### Core Components

#### 1. Content Collection & Processing

- **RedditPostFetcher**: Retrieves trending discussions from r/OutOfTheLoop
- **RedditPostProcessor**: Processes posts, comments, and related URLs

#### 2. Script Planning & Generation

- **ScriptPlanner**: Evaluates and structures content using 4 core patterns:
  - Mystery Unfolding: Reveals information progressively
  - Debate/Controversy: Explores multiple perspectives
  - Cultural Phenomenon: Analyzes trending topics
  - Complex Situation: Breaks down intricate issues
- **Multi-Persona Design**: Orchestrates natural dialogue flow

#### 3. Dialogue Generation

- **DialogueGenerator**: Creates dynamic conversations
- **Context Integration**: Weaves in URLs, comments, and background
- **Parallel Processing**: Generates reddit post specific dialogues concurrently

#### 4. Script Enhancement

- **ScriptEnhancer**: Improves flow and reduces redundancy
- **Format Standardization**: Ensures consistent dialogue structure
- **Quality Control**: Maintains speaker authenticity

#### 5. Podcast Generation

- **Audio Synthesis**: Converts enhanced scripts to natural speech
- **Voice Differentiation**: Distinct voices for Host, Learner, and Expert
- **Quality Assurance**: Ensures proper pacing and pronunciation
