# Security and Cost Decisions

## Authentication: GitHub OIDC

GitHub Actions assumes an AWS IAM role through OIDC. This avoids storing long-lived AWS access keys in repository secrets.

Security practices:
- Keep `id-token: write` limited to workflows that need AWS federation.
- Restrict the IAM trust policy to the intended repository and permitted branch/workflow context.
- Scope ECR permissions to the lab repository wherever possible.
- Do not commit credentials, tokens, or local `.env` files.
- Review workflow changes before merging because CI workflows can access repository and cloud permissions.

## ECR image immutability

The ECR repository uses immutable tags. The workflow uses the Git commit SHA as the tag and checks for an existing tag before attempting a push. This prevents accidental overwrite of a published tag.

The existence check must fail closed: errors other than a confirmed missing image should fail the workflow rather than being interpreted as permission to push.

## Image scanning

Trivy scans the built image and is configured to fail the job for HIGH and CRITICAL findings (with unfixed vulnerabilities ignored). A passing scan means no findings matching that configured policy were detected; it is not a guarantee that an image is vulnerability-free.

## Cost-conscious execution

- Docker build and runtime checks use GitHub-hosted runners.
- No persistent EC2/ECS/EKS environment is required for the lab's current scope.
- ECR storage and image transfer can incur AWS charges. A lifecycle policy is configured to retain a limited number of recent images; periodically review stored images and AWS billing.
- Remove cloud resources that are no longer needed, and verify the active AWS region/account before making changes.

## Known boundaries

This is a learning lab, not a complete enterprise security program. Production systems may additionally require signed images, SBOM generation and retention, provenance/attestation, policy enforcement, centralized secrets management, audit integration, and a formal vulnerability exception process.
