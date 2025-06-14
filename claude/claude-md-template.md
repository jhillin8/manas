# Project Context for Claude Code

## Project Overview
- **Project Type**: [Web App | Mobile App | API | Desktop App | CLI Tool | Library | etc.]
- **Primary Language**: [JavaScript/TypeScript | Python | Java | C# | Rust | Go | etc.]
- **Framework/Stack**: [React/Next.js | Vue/Nuxt | Django/Flask | Spring Boot | .NET | etc.]
- **Architecture**: [Monolith | Microservices | JAMstack | Serverless | etc.]

## Development Environment
- **Package Manager**: [npm | yarn | pnpm | pip | cargo | maven | etc.]
- **Node Version**: [18+ | 20+ | Latest LTS]
- **Python Version**: [3.9+ | 3.11+ | Latest]
- **Database**: [PostgreSQL | MySQL | MongoDB | SQLite | Redis | etc.]
- **Cloud Provider**: [AWS | GCP | Azure | Vercel | Netlify | etc.]

## Project Structure
```
├── src/             # Source code
├── tests/           # Test files
├── docs/            # Documentation
├── config/          # Configuration files
├── scripts/         # Build/deployment scripts
└── README.md        # Project documentation
```

## Code Standards & Conventions
- **Code Style**: [Prettier + ESLint | Black + Flake8 | Rustfmt | Gofmt | etc.]
- **Naming Convention**: 
  - Files: [camelCase | kebab-case | snake_case]
  - Functions: [camelCase | snake_case]
  - Constants: [UPPER_SNAKE_CASE | SCREAMING_SNAKE_CASE]
- **Import Organization**: [Absolute paths preferred | Relative paths | Barrel exports]
- **Comment Style**: Use JSDoc/docstrings for public APIs, inline comments for complex logic

## Testing Strategy
- **Unit Tests**: [Jest | Pytest | XUnit | Cargo test]
- **Integration Tests**: [Supertest | TestContainers | Postman]
- **E2E Tests**: [Playwright | Cypress | Selenium]
- **Test Command**: `[npm test | pytest | cargo test | dotnet test]`
- **Coverage Target**: 80%+ for critical paths

## Build & Deployment
- **Build Command**: `[npm run build | python setup.py | cargo build --release]`
- **Dev Server**: `[npm run dev | python manage.py runserver | cargo run]`
- **Environment Variables**: Check `.env.example` for required vars
- **CI/CD**: [GitHub Actions | GitLab CI | Jenkins | CircleCI]

## Git Workflow
- **Branch Naming**: `[feature/description | bugfix/issue-number | hotfix/description]`
- **Commit Convention**: [Conventional Commits | Semantic | Custom format]
- **PR Requirements**: Tests pass, code review, no merge conflicts
- **Protected Branches**: main/master requires PR approval

## Dependencies & Libraries
- **Core Dependencies**: [List key libraries and their purposes]
- **Dev Dependencies**: [List development tools]
- **Peer Dependencies**: [If applicable]
- **Version Pinning**: [Exact versions | Semantic versioning | Range allowed]

## Common Patterns & Best Practices
- **Error Handling**: [Try/catch blocks | Result types | Error boundaries]
- **State Management**: [Redux | Zustand | Context API | Vuex | etc.]
- **API Communication**: [Fetch | Axios | SWR | React Query | etc.]
- **Authentication**: [JWT | OAuth | Session-based | etc.]
- **Logging**: [Console | Winston | Serilog | structured logging]

## Performance Considerations
- **Bundle Size**: Monitor and optimize for web projects
- **Database**: Use indexes, avoid N+1 queries, connection pooling
- **Caching**: [Redis | In-memory | CDN | Browser cache]
- **Optimization**: Lazy loading, code splitting, image optimization

## Security Guidelines
- **Input Validation**: Sanitize all user inputs
- **Authentication**: Implement proper auth flows
- **CORS**: Configure appropriately for API endpoints
- **Environment Variables**: Never commit secrets to version control
- **Dependencies**: Regular security audits and updates

## Known Issues & Gotchas
- **Platform-Specific**: [Browser compatibility | OS differences | Mobile quirks]
- **Performance Bottlenecks**: [Known slow operations | Memory leaks to avoid]
- **Third-Party Limitations**: [API rate limits | Service downtimes | etc.]
- **Development Quirks**: [Hot reload issues | Build cache problems | etc.]

## Documentation & Resources
- **API Docs**: [Swagger/OpenAPI | Postman collection | etc.]
- **Architecture Docs**: [System design | Database schema | etc.]
- **Runbooks**: [Deployment procedures | Troubleshooting guides]
- **External Resources**: [Official docs | Community resources | etc.]

## Team Preferences
- **Code Review**: [Focus areas | Required approvals | Style preferences]
- **Communication**: [Slack channels | Issue tracking | Meeting cadence]
- **Tools**: [IDE preferences | Browser dev tools | Debugging tools]
- **Deployment Windows**: [Preferred deployment times | Freeze periods]

---

## Claude Code Specific Instructions
- **File Editing**: Prefer surgical edits over full file rewrites
- **Testing**: Always run tests after significant changes
- **Documentation**: Update relevant docs when changing APIs
- **Dependencies**: Confirm before adding new dependencies
- **Permissions**: Ask before modifying config files or build scripts

## Quick Commands
```bash
# Start development
[npm run dev | python manage.py runserver | cargo run]

# Run tests
[npm test | pytest | cargo test]

# Build for production
[npm run build | python setup.py build | cargo build --release]

# Check code quality
[npm run lint | flake8 . | cargo clippy]
```