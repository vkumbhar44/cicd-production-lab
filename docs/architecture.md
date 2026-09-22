# Architecture and Delivery Design

## Scope

This repository is a CI/CD and container-image supply-chain lab. GitHub Actions provides the ephemeral execution environment. Amazon ECR stores versioned container images. No long-running application infrastructure is deployed.

## Logical architecture

```text
GitHub repository
  |
  | push to main / manual dispatch
  v
GitHub Actions: ECR publisher
  1. Checkout
  2. Build image
  3. Run development and production containers
  4. Verify configuration and health
  5. Scan image with Trivy
  6. Assume AWS role through OIDC
  7. Login to ECR
  8. Check immutable Git SHA tag
  9. Push only when tag is absent
  |
  v
Amazon ECR
  |
  | successful publisher completion
  v
GitHub Actions: ECR runtime validation
  1. Assume AWS role through OIDC
  2. Pull SHA-tagged image
  3. Run production container
  4. Check /health and /info
  5. Print logs
  6. Remove test container
```

## Artifact identity

The Git commit SHA is used as the image tag. This provides a traceable association between source revision and the published image.

The ECR repository is configured for immutable tags. An existing SHA tag must not be overwritten. The publisher checks whether the tag exists and skips the push when it does.

A future hardening improvement is to record and promote the ECR **image digest** (`sha256:...`) as the canonical artifact identity. A Git SHA tag identifies the intended source revision, while a digest identifies the exact image content.

## Runtime configuration

The application supports `APP_ENV` and `LOG_LEVEL`. Workflows exercise development and production configurations, and the ECR runtime-validation workflow checks the image after retrieving it from ECR.

## Ephemeral validation, not deployment

The GitHub-hosted runner is temporary. It starts the image, runs checks, captures logs, and removes the test container. It does not provide a persistent endpoint or an environment that receives user traffic.

Consequently, this lab does not claim to implement live rolling, blue-green, or canary deployment. Those require a deployment target plus rollout/traffic-management and rollback mechanisms.
