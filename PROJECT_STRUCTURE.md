# Project Structure

```
mlops/
├── .github/
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline
│
├── services/                         # Microservices
│   ├── api-gateway/                  # API Gateway service
│   │   ├── src/app/
│   │   │   ├── main.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── ml-service/                   # ML Service
│   │   ├── src/app/
│   │   │   ├── main.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── user-service/                  # User Service
│   │   ├── src/app/
│   │   │   ├── main.py
│   │   │   ├── logger.py
│   │   │   └── metrics.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── notification-service/         # Notification Service
│       ├── src/app/
│       │   ├── main.py
│       │   ├── logger.py
│       │   └── metrics.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── training/                          # ML Training
│   ├── train.py                      # Training script
│   └── requirements.txt              # Training dependencies
│
├── tests/                             # Tests
│   ├── test_api.py
│   └── test_train.py
│
├── terraform/                         # Infrastructure as Code
│   ├── main.tf                        # GCP Cloud Run
│   ├── variables.tf
│   ├── outputs.tf
│   ├── versions.tf
│   ├── terraform.tfvars.example
│   ├── README.md
│   │
│   ├── aws/                           # AWS ECS
│   │   ├── main.tf
│   │   └── variables.tf
│   │
│   └── vm/                            # GCP VMs
│       ├── main.tf
│       └── variables.tf
│
├── docs/                              # Documentation
│   ├── DEPLOYMENT.md
│   ├── MICROSERVICES_ARCHITECTURE.md
│   ├── IMPLEMENTATION_SUMMARY.md
│   └── COMPLETE_STATUS.md
│
├── artifacts/                         # Model artifacts
│   └── model.pkl
│
├── docker-compose.yml                 # Local development
├── prometheus.yml                     # Prometheus config
├── pytest.ini                         # Pytest config
├── requirements.txt                   # Root dependencies (for training)
├── README.md                          # Main README
└── .gitignore
```

## Directory Descriptions

### `services/`
Contains all microservices. Each service is self-contained with its own:
- Source code (`src/app/`)
- Dockerfile
- Requirements file

### `training/`
ML model training scripts and dependencies.

### `terraform/`
Infrastructure as Code configurations:
- `main.tf` - GCP Cloud Run (default)
- `aws/` - AWS ECS deployment
- `vm/` - GCP VM deployment

### `docs/`
All documentation files.

### `tests/`
Test files for the project.

### `artifacts/`
Generated model files (committed to repo for demo purposes).

