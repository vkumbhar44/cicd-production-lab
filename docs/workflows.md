# Workflow Guide

> Keep this guide aligned with the actual YAML in `.github/workflows/`. Workflow behavior can change as the lab evolves.

## 1. `ecr-publish.yml` — Build, scan, and publish

**Triggers:** push to `main` and manual dispatch.

**Main stages:**
1. Checkout source.
2. Configure Docker Buildx.
3. Build the application image.
4. Run development and production containers with distinct runtime settings.
5. Verify environment variables and health; verify the development startup log.
6. Remove test containers.
7. Scan the image using Trivy for HIGH and CRITICAL vulnerabilities.
8. Assume the AWS publishing role through GitHub OIDC.
9. Log in to ECR and tag the image with the commit SHA.
10. Check ECR for that immutable tag. Skip the push if it already exists; push if it is absent; fail if the lookup fails for another reason.

**Why the existence check matters:** rerunning a workflow for the same commit should not attempt to overwrite an immutable ECR tag. The check makes the publishing step safe to rerun without weakening tag immutability.

## 2. `runtime-config-test.yml` — Configuration validation

Builds/runs the image in GitHub Actions and checks development and production runtime configuration. It validates the intended `APP_ENV` and `LOG_LEVEL` values and performs health checks. This is a test workflow, not a deployment.

## 3. `ecr-runtime-validation.yml` — Validate the published artifact

Supports manual dispatch and automatic invocation after the ECR publisher completes successfully.

The workflow assumes the AWS role through OIDC, pulls the SHA-tagged image from ECR, starts it with production configuration, validates `/health` and `/info`, emits logs, and cleans up.

For an end-to-end test, confirm:
- The workflow exists on the repository's default branch.
- The publisher completed successfully.
- The runtime-validation workflow was automatically triggered.
- The image tag corresponds to the publisher run's source SHA.
- Endpoint checks passed and cleanup ran.

A failed publisher should not be treated as a successful publication. The runtime validation should only proceed for the intended successful publisher event (or an explicit manual run).

## 4. `image-promotion.yml` — Promotion logic

The promotion workflow verifies an existing ECR image and models sequential development → staging → production progression using GitHub Environments.

This is useful for practicing immutable-artifact promotion and environment gates. Unless deployment commands target real infrastructure, it is **not** a deployment to three actual environments.

## Troubleshooting notes

- **Immutable tag already exists:** expected ECR behavior. The publisher should detect the existing tag and skip pushing it.
- **`DescribeImages` denied:** verify the IAM role has `ecr:DescribeImages` scoped to the intended repository.
- **Image pull denied:** verify the role has ECR download permissions such as `ecr:BatchGetImage`, `ecr:BatchCheckLayerAvailability`, and `ecr:GetDownloadUrlForLayer`.
- **OIDC assume-role failure:** verify the GitHub OIDC provider, role trust policy, repository/branch subject constraints, and workflow `id-token: write` permission.
- **Automatic runtime validation did not trigger:** confirm the listener workflow is present on the default branch and inspect the publisher conclusion and `workflow_run` condition.
