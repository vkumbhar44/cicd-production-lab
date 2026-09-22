# Lessons Learned and Next Steps

## Key lessons

- CI/CD is more than a successful image build: test, scan, publish, and validate the artifact.
- Runtime configuration should be explicit and tested rather than assumed.
- GitHub OIDC can provide short-lived AWS access without static IAM keys.
- Immutable tags prevent published image references from being overwritten.
- A workflow should handle reruns safely; idempotency is part of operational reliability.
- An image validated before publication is not the same as validating the artifact actually retrieved from the registry.
- Artifact promotion and application deployment are different concerns.
- Ephemeral GitHub-hosted runners are useful for validation but do not provide persistent deployment environments.

## Current scope

This repository focuses on CI/CD, ECR publishing, and artifact validation. The promotion workflow demonstrates progression/gates but does not deploy the app to persistent environments.

## Recommended follow-on project

Use a separate Kubernetes/Platform Engineering project for actual deployment strategy implementation:

1. Deploy the application to a Kubernetes cluster using Helm.
2. Implement rolling updates and readiness/liveness probes.
3. Demonstrate rollback to a previous image digest.
4. Implement blue-green deployment with a real service/traffic switch.
5. Implement canary rollout with measurable rollout checks.
6. Add GitOps reconciliation with Argo CD.
7. Document operational trade-offs, rollback conditions, and cost controls.

Keep this repository as the focused CI/CD and image supply-chain lab; avoid adding a simulated deployment just to claim a production rollout.
