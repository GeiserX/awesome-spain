# Security Policy

## Reporting Security Issues

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please use GitHub's private vulnerability reporting:

1. Go to the **Security** tab of this repository
2. Click **"Report a vulnerability"**
3. Fill out the form with details

I will respond within **48 hours** and work with you to understand and address the issue.

### What to Include

- Type of issue (e.g., XSS, SQL injection, authentication bypass)
- Full paths of affected source files
- Step-by-step instructions to reproduce
- Proof-of-concept or exploit code (if possible)
- Impact assessment and potential attack scenarios

## Supported Versions

Only the latest version receives security updates. Please always use the most recent release.

## Security Best Practices for Contributors

1. **Never commit secrets** — use environment variables
2. **Validate all input** — especially from external sources
3. **Keep dependencies updated** — Dependabot is enabled on this repo
4. **Follow the principle of least privilege** in all code

## Contact

For security questions that aren't vulnerabilities, open a regular issue or reach out via the repository's Discussions tab.
