# 🤝 Contributing to Agentic Design Patterns

Thank you for your interest in contributing to the Agentic Design Patterns repository! This project aims to provide comprehensive, production-ready implementations of AI agent design patterns. We welcome contributions from developers of all skill levels.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Types of Contributions](#types-of-contributions)
- [Development Process](#development-process)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Recognition](#recognition)

## 📜 Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- A Gemini API key (for testing agent functionality)

### Setup
1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/your-username/Agentic-design-patterns-.git
   cd Agentic-design-patterns-
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies** for a specific project:
   ```bash
   cd prompt_chaining/  # or any other pattern directory
   pip install -r requirements.txt
   ```
5. **Set up environment variables**:
   ```bash
   cp .env.example .env  # from the repository root
   # Edit .env and add your GEMINI_API_KEY
   ```

## 🎯 Types of Contributions

### 🐛 Bug Reports
- Use the bug report template when creating issues
- Include detailed steps to reproduce
- Provide environment information and error logs

### ✨ Feature Requests
- Use the feature request template
- Clearly describe the problem and proposed solution
- Consider how it fits with existing patterns

### 📝 Documentation
- Improve existing documentation
- Add examples and tutorials
- Translate documentation to other languages

### 🔧 Code Contributions
- Fix bugs
- Implement new features
- Refactor existing code
- Add tests

## 🔄 Development Process

### 1. Choose an Issue
- Check the [Issues](https://github.com/josephsenior/Agentic-design-patterns-/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-number-description
```

### 3. Make Changes
- Write clear, focused commits
- Test your changes thoroughly
- Follow the coding standards below

### 4. Test Your Changes
- Run existing tests
- Add new tests for new functionality
- Test manually with different scenarios

### 5. Submit a Pull Request
- Push your branch to your fork
- Create a pull request with a clear description
- Reference any related issues

## 🏗️ Project Structure

Each pattern follows this consistent structure:
```
pattern_name/
├── core_implementation.py  # Main implementation
├── example.py              # Usage examples
├── README.md               # Pattern documentation
├── requirements.txt        # Dependencies
└── .env.example           # Environment template
```

## 💻 Coding Standards

### Python Style
- Follow [PEP 8](https://pep8.org/) style guidelines
- Use type hints for function parameters and return values
- Write descriptive variable and function names
- Keep functions focused and under 50 lines when possible

### Code Quality
```python
# ✅ Good: Clear, descriptive names and type hints
def analyze_document(text: str, max_tokens: int = 1000) -> Dict[str, Any]:
    """Analyze document and extract key information."""
    pass

# ❌ Avoid: Unclear names, no type hints
def process(t, mt=1000):
    pass
```

### Error Handling
- Use specific exception types
- Provide meaningful error messages
- Handle edge cases gracefully

### Documentation
- Add docstrings to all public functions and classes
- Include parameter descriptions and return value information
- Provide usage examples in docstrings

## 🧪 Testing

### Running Tests
Each project may have its own testing approach. Generally:
```bash
# Navigate to project directory
cd pattern_name/

# Install test dependencies if needed
pip install pytest

# Run tests
pytest
```

### Writing Tests
- Write tests for new functionality
- Include both positive and negative test cases
- Test edge cases and error conditions
- Aim for good test coverage

## 📚 Documentation

### README Files
Each pattern should have a comprehensive README including:
- Pattern description and use cases
- Installation instructions
- Usage examples
- Architecture diagrams
- API documentation

### Code Comments
- Explain complex logic
- Document assumptions and limitations
- Reference related patterns or concepts

## 🔄 Submitting Changes

### Pull Request Process
1. **Update your branch** with the latest changes from main:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Ensure your code passes all checks**:
   - Tests pass
   - Code style is correct
   - Documentation is updated

3. **Create a pull request**:
   - Use a clear, descriptive title
   - Fill out the pull request template completely
   - Reference any related issues
   - Add screenshots for UI changes

4. **Respond to feedback**:
   - Address review comments promptly
   - Make requested changes
   - Keep the conversation going until approval

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat(prompt_chaining): add support for custom prompt templates
fix(routing): resolve memory leak in router handler
docs(multi_agent): update API documentation
```

## 🏆 Recognition

Contributors will be:
- Listed in the repository contributors
- Mentioned in release notes for significant contributions
- Recognized in the project's acknowledgments

Thank you for contributing to the Agentic Design Patterns project! Your efforts help make AI agent development more accessible and robust. 🚀
