# CLAUDE.md - AI Assistant Guide

This document provides comprehensive guidance for AI assistants working with this repository.

## Project Overview

This is a **Streamlit Example Application** that demonstrates interactive data visualization using Python. The application creates a parametric spiral visualization using Altair charts, showcasing Streamlit's capabilities for building interactive web applications with minimal code.

**Purpose**: Serve as a starting template and example for Streamlit applications.

## Repository Structure

```
streamlit-example/
├── .devcontainer/
│   └── devcontainer.json       # DevContainer configuration for Codespaces/VS Code
├── streamlit_app.py            # Main application entry point
├── requirements.txt            # Python dependencies
└── README.md                   # User-facing documentation
```

### Key Files

- **streamlit_app.py** (39 lines): Main application file containing the spiral visualization demo
  - Uses `st.echo()` to display code alongside output
  - Implements interactive sliders for controlling spiral parameters
  - Generates parametric spiral using mathematical calculations
  - Renders visualization with Altair charts

- **requirements.txt**: Minimal dependencies
  - `altair` - Declarative statistical visualization library
  - `pandas` - Data manipulation and analysis
  - `streamlit` - Web app framework

- **.devcontainer/devcontainer.json**: Development environment configuration
  - Base image: Python 3.11 (Debian Bullseye)
  - Auto-installs dependencies on container creation
  - Auto-starts Streamlit server on port 8501
  - Includes Python and Pylance extensions for VS Code

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: Streamlit (interactive web apps)
- **Visualization**: Altair (declarative charts)
- **Data Processing**: Pandas
- **Development Environment**: DevContainer (Docker-based)

## Development Environment

### Running the Application

The application is designed to run in a DevContainer (GitHub Codespaces or VS Code):

1. **Automatic Setup**: DevContainer automatically:
   - Installs dependencies from `requirements.txt`
   - Starts Streamlit server with CORS and XSRF protection disabled
   - Forwards port 8501 for web access

2. **Manual Start** (if needed):
   ```bash
   streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
   ```

3. **Access**: Application opens at `http://localhost:8501`

### Local Development (without DevContainer)

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Git Workflow

### Branching Strategy

- **master**: Main branch with stable code
- **claude/[feature-name]-[id]**: AI assistant feature branches
  - Example: `claude/add-claude-documentation-xlchJ`
  - Pattern: Must start with `claude/` and include session ID suffix

### Commit Conventions

Based on repository history:
- Use clear, descriptive commit messages
- Examples from history:
  - "First commit"
  - "Fix typo!"
  - "Update README"
  - "support packages.txt on devcontainer setup"
  - "add codespaces devcontainer spec"

### Remote Operations

- Repository uses a local proxy for git operations
- Standard git commands apply: `git push -u origin <branch-name>`

## Code Conventions

### Python Style

The codebase follows these patterns:

1. **Imports**: Group by standard library, third-party, and local (if any)
   ```python
   from collections import namedtuple
   import altair as alt
   import math
   import pandas as pd
   import streamlit as st
   ```

2. **Documentation**: Uses Streamlit's markdown strings for user-facing docs
   ```python
   """
   # Welcome to Streamlit!

   Edit `/streamlit_app.py` to customize this app...
   """
   ```

3. **Code Display**: Uses `st.echo()` to show code alongside its output
   ```python
   with st.echo(code_location='below'):
       # Code here is displayed in the UI
   ```

4. **Interactive Controls**: Use Streamlit widgets for user input
   ```python
   total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
   ```

5. **Data Structures**: Use named tuples for simple data containers
   ```python
   Point = namedtuple('Point', 'x y')
   ```

## AI Assistant Guidelines

### When Making Changes

1. **Read Before Edit**: Always read `streamlit_app.py` before making modifications

2. **Test Interactively**: Changes to the Streamlit app should be tested by running the server
   - The app auto-reloads on file changes
   - Verify sliders, visualizations, and interactions work correctly

3. **Preserve Simplicity**: This is an example/template repository
   - Keep code minimal and educational
   - Avoid over-engineering
   - Maintain the demonstrative nature of the code

4. **Dependencies**: When adding new features
   - Update `requirements.txt` if new packages are needed
   - Keep dependencies minimal
   - Prefer well-maintained, popular packages

5. **Documentation**:
   - Update README.md for user-facing changes
   - Update this CLAUDE.md for structural or workflow changes
   - Use Streamlit's markdown strings for in-app documentation

### Common Tasks

#### Adding a New Visualization

1. Import necessary libraries in the appropriate section
2. Use `st.echo()` if the code should be displayed to users
3. Add interactive controls with Streamlit widgets (`st.slider`, `st.selectbox`, etc.)
4. Create DataFrame with pandas if needed
5. Render with Altair chart or Streamlit native components

#### Modifying the Spiral Demo

- Parameters are controlled by sliders at lines 20-21
- Spiral calculation logic is at lines 28-34
- Chart rendering is at lines 36-38
- Consider maintaining the mathematical clarity of the implementation

#### Adding New Dependencies

1. Add to `requirements.txt` (one package per line)
2. Test installation in DevContainer
3. The `updateContentCommand` in devcontainer.json auto-installs on rebuild

### Testing Checklist

Before committing changes:

- [ ] Streamlit server starts without errors
- [ ] All interactive widgets function correctly
- [ ] Visualizations render properly
- [ ] No console errors or warnings
- [ ] Code is displayed correctly if using `st.echo()`
- [ ] README.md is updated if user-facing changes were made

### What NOT to Do

- Don't add complex build systems (this is a simple example)
- Don't add testing frameworks unless specifically requested (keep it simple)
- Don't add linting/formatting configs unless requested
- Don't over-document the code (it's meant to be self-explanatory)
- Don't add error handling that obscures the educational nature
- Don't add authentication, databases, or production features (this is a demo)

## DevContainer Details

The project is optimized for cloud development environments:

- **Image**: `mcr.microsoft.com/devcontainers/python:1-3.11-bullseye`
- **Auto-opened files**: README.md, streamlit_app.py
- **Port 8501**: Auto-forwarded with preview
- **Extensions**: Python, Pylance (VS Code)
- **Package management**: Supports optional `packages.txt` for apt packages

### Rebuilding the Container

If dependencies change:
```bash
# In VS Code: Cmd/Ctrl+Shift+P -> "Rebuild Container"
# Or manually:
pip install -r requirements.txt
```

## Streamlit-Specific Patterns

### State Management

Current app doesn't use session state, but if needed:
```python
if 'key' not in st.session_state:
    st.session_state.key = value
```

### Layout

- Uses default single-column layout
- Consider `st.columns()`, `st.sidebar`, `st.expander()` for complex layouts

### Performance

- Current app recalculates spiral on every slider change
- Use `@st.cache_data` for expensive computations if needed

## Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forums](https://discuss.streamlit.io)
- [Altair Documentation](https://altair-viz.github.io)

## File Change Log

When modifying this project, maintain awareness of:
- **High-impact files**: `streamlit_app.py` (main app logic)
- **Configuration files**: `.devcontainer/devcontainer.json`, `requirements.txt`
- **Documentation files**: `README.md`, this file

---

**Last Updated**: 2026-02-06
**Repository**: tilakkasturi/streamlit-example
**Branch**: claude/add-claude-documentation-xlchJ
