# CI/CD Production Lab

A hands-on CI/CD learning repository focused on building, testing, scanning, publishing, and validating a containerized application with GitHub Actions and Amazon ECR.

**Repository:** [vkumbhar44/cicd-production-lab](https://github.com/vkumbhar44/cicd-production-lab)

## Project goals

This lab demonstrates how to build a repeatable container delivery workflow while applying practical CI/CD and supply-chain concepts:

- Validate application changes with automated tests.
- Build a Docker image once per workflow run and test it with development and production runtime configuration.
- Scan the image for HIGH and CRITICAL vulnerabilities with Trivy.
- Authenticate GitHub Actions to AWS through OIDC instead of long-lived AWS access keys.
- Publish SHA-tagged images to Amazon ECR.
- Preserve ECR tag immutability and make publishing reruns safe.
- Pull an image from ECR and validate its runtime behavior on a GitHub-hosted runner.
- Practice environment promotion logic without claiming that simulated promotion is a real deployment.

## Delivery flow

```text
Code change / manual workflow dispatch
                 |
                 v
      Build container image
                 |
                 v
      Run dev + prod checks
                 |
                 v
          Trivy image scan
                 |
                 v
       GitHub OIDC -> AWS role
                 |
                 v
       Login to Amazon ECR
                 |
                 v
    Check immutable Git-SHA tag
          /              \
       Exists            Missing
         |                  |
     Skip push           Push image
          \                /
           v              v
             Publish job
                 |
                 v
    ECR Runtime Validation
    (pull + run + endpoint checks)
```

The runtime-validation workflow is configured to support both manual dispatch and automatic invocation after the ECR publisher completes successfully. Confirm the latest run in GitHub Actions before treating the end-to-end trigger as verified.

## Workflows

| Workflow | Purpose |
|---|---|
| `ecr-publish.yml` | Build, test, scan, authenticate to AWS with OIDC, and publish a SHA-tagged image to ECR. |
| `runtime-config-test.yml` | Validate development and production runtime configuration using `APP_ENV` and `LOG_LEVEL`. |
| `ecr-runtime-validation.yml` | Pull an existing SHA-tagged image from ECR, run it, validate endpoints, print logs, and clean up. |
| `image-promotion.yml` | Verify an existing ECR image and demonstrate sequential development → staging → production promotion gates. This is promotion logic, not a deployment to persistent environments. |

Workflow filenames and behavior should be kept in sync with the actual files in `.github/workflows/`.

## Application endpoints

The Flask application exposes:

| Endpoint | Purpose |
|---|---|
| `/` | Application route |
| `/health` | Basic health response used by validation |
| `/info` | Runtime/application information |
| `/version` | Version information |

Runtime configuration:

- `APP_ENV` — defaults to `development`
- `LOG_LEVEL` — defaults to `INFO`

Example production configuration: `APP_ENV=production`, `LOG_LEVEL=WARNING`.

## AWS and GitHub configuration

The ECR workflow expects these GitHub Actions repository variables:

| Variable | Purpose |
|---|---|
| `AWS_ROLE_ARN` | IAM role assumed by GitHub Actions using OIDC |
| `AWS_REGION` | AWS region containing the ECR repository |
| `ECR_REPOSITORY` | ECR repository name |

The AWS role requires narrowly scoped permissions for the operations performed by the workflows, including ECR image inspection, upload, and download as applicable. Keep the role trust policy restricted to the intended GitHub organization/repository and branch or workflow context.

**Never commit AWS access keys, tokens, or other credentials.** This lab uses GitHub OIDC for AWS authentication.

## Run locally

Prerequisites: Python, the project's dependencies, and Docker if you want to build/run the container locally.

```powershell
cd E:\cicd-production-lab
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```

Docker build and runtime checks are performed on GitHub-hosted runners in this lab, so local Docker is not required to execute those GitHub Actions workflows.

## What this project does—and does not—demonstrate

**Implemented lab capabilities**
- CI validation and container build/test workflow
- Trivy image scanning
- OIDC-based AWS authentication
- ECR image publishing with immutable SHA tags
- ECR image runtime validation on an ephemeral GitHub-hosted runner
- Environment promotion workflow logic

**Not a live deployment**
- No persistent EC2, ECS, or EKS deployment target is provisioned by this lab.
- Environment promotion is not equivalent to deploying separate running environments.
- Blue-green and canary traffic shifting are not implemented here.
- The GitHub-hosted runner is temporary; it validates the image and then cleans up.

These are intentional scope boundaries to keep this lab focused and cost-conscious. A separate Kubernetes/Platform Engineering project can implement actual rolling, blue-green, or canary deployments.

## Documentation

- [Architecture](docs/architecture.md)
- [Workflow guide](docs/workflows.md)
- [Security and cost decisions](docs/security-and-cost.md)
- [Lessons learned and next steps](docs/lessons-learned.md)
- [LinkedIn project post](docs/linkedin-post.md)

## Learning outcomes

This project helped practice CI/CD pipeline design, container validation, image vulnerability scanning, immutable artifact versioning, GitHub Actions workflow orchestration, AWS OIDC federation, and the distinction between artifact promotion and real application deployment.
