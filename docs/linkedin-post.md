## LinkedIn post

🚀 **Built a CI/CD + Container Image Supply-Chain Lab with GitHub Actions and AWS ECR**

Over the past few weeks, I’ve been building a hands-on CI/CD lab to understand what happens beyond simply building a Docker image.

Here’s what I implemented:

🔹 Automated Docker image build with GitHub Actions  
🔹 Development and production container checks  
🔹 Trivy image scanning for HIGH and CRITICAL vulnerabilities  
🔹 GitHub Actions → AWS authentication using OIDC (no long-lived AWS access keys)  
🔹 SHA-tagged image publishing to Amazon ECR  
🔹 Immutable-tag handling to make publishing reruns safe  
🔹 Runtime validation by pulling the published image from ECR and checking its endpoints  
🔹 Environment-promotion workflow logic using GitHub Environments  

One important lesson: **artifact promotion is not the same as deployment.** This lab validates and promotes image references, but it does not claim to perform live blue-green or canary deployments. I’m keeping this repository focused and plan to implement real Kubernetes deployment strategies in a separate Platform Engineering project.

This project helped me connect CI/CD concepts with practical workflow design, cloud authentication, image immutability, validation, and failure handling.

🔗 GitHub: https://github.com/vkumbhar44/cicd-production-lab

I’m continuing to learn by building, documenting, and sharing the implementation—not just the theory.

#DevOps #CICD #AWS #GitHubActions #Docker #AmazonECR #Trivy #PlatformEngineering #LearningInPublic
