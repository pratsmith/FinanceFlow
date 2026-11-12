# FinanceFlow — End-to-End DevOps & Cloud Project

## Architecture & Tech Stack
- **Application:** Python + Streamlit (`finance_app.py`) with interactive Plotly analytics
- **Cloud Database:** AWS DynamoDB (emulated locally via `amazon/dynamodb-local`)
- **Infrastructure as Code:** Terraform (`terraform/main.tf`)
- **Configuration Management:** Ansible (`local_setup.yml`)
- **Containerization:** Docker (`Dockerfile`)
- **Orchestration:** Kubernetes via Minikube (`k8s/deploy.yaml`, NodePort `30080`)
- **Monitoring:** Prometheus + Grafana deployed via Helm (NodePort `30300`)

## Quick Access URLs
- **FinanceFlow Dashboard:** `http://192.168.49.2:30080`
- **Grafana Monitoring:** `http://192.168.49.2:30300`
