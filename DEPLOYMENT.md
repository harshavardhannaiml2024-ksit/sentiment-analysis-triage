# 🚀 Deployment Guide

Complete guide for deploying the Sentiment Analysis Dashboard to various platforms.

## Table of Contents

1. [Streamlit Cloud (Easiest)](#streamlit-cloud)
2. [Docker Deployment](#docker-deployment)
3. [AWS Deployment](#aws-deployment)
4. [Azure Deployment](#azure-deployment)
5. [Google Cloud Platform](#google-cloud-platform)
6. [Heroku Deployment](#heroku-deployment)
7. [Self-Hosted Server](#self-hosted-server)

---

## 🌥️ Streamlit Cloud

**Best for**: Quick deployment, free tier available, no infrastructure management

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Push to GitHub**
   ```bash
   cd sentiment-analysis-triage
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/sentiment-analysis-triage.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository: `yourusername/sentiment-analysis-triage`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Configure Secrets** (Optional)
   - In Streamlit Cloud dashboard, go to app settings
   - Click "Secrets"
   - Copy contents from `.streamlit/secrets.toml.example`
   - Paste and update with your actual credentials

4. **Access Your App**
   - URL will be: `https://yourusername-sentiment-analysis-triage.streamlit.app`

### Resource Limits (Free Tier)
- 1 GB RAM
- 1 CPU core
- 1 GB storage
- Sleeps after 7 days of inactivity

### Tips
- Use VADER instead of BERT for better performance on free tier
- Reduce batch size to 10-20 for memory efficiency
- App will sleep after inactivity; first load may be slow

---

## 🐳 Docker Deployment

**Best for**: Consistent environments, easy scaling, local development

### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

### Option 1: Docker Compose (Recommended)

**Basic Deployment (App Only)**
```bash
cd sentiment-analysis-triage
docker-compose up -d
```

**With PostgreSQL Database**
```bash
docker-compose --profile with-db up -d
```

**Access the app**: http://localhost:8501

**View logs**
```bash
docker-compose logs -f sentiment-analysis
```

**Stop the app**
```bash
docker-compose down
```

### Option 2: Docker Build & Run

**Build the image**
```bash
docker build -t sentiment-analysis:latest .
```

**Run the container**
```bash
docker run -d \
  --name sentiment-analysis \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config.yaml:/app/config.yaml \
  sentiment-analysis:latest
```

**Access the app**: http://localhost:8501

### Docker Configuration

**Environment Variables**
```bash
docker run -d \
  -p 8501:8501 \
  -e PYTHONUNBUFFERED=1 \
  -e MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english \
  sentiment-analysis:latest
```

**Custom Port**
```bash
docker run -d -p 8080:8501 sentiment-analysis:latest
```

### Production Considerations

1. **Use Docker Secrets** for sensitive data
2. **Set resource limits**:
   ```bash
   docker run -d \
     --memory="4g" \
     --cpus="2" \
     -p 8501:8501 \
     sentiment-analysis:latest
   ```

3. **Enable health checks** (already configured in Dockerfile)

4. **Use reverse proxy** (Nginx/Traefik) for HTTPS

---

## ☁️ AWS Deployment

**Best for**: Enterprise deployments, scalability, AWS ecosystem integration

### Option 1: AWS ECS (Elastic Container Service)

1. **Push Docker image to ECR**
   ```bash
   # Create ECR repository
   aws ecr create-repository --repository-name sentiment-analysis
   
   # Login to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   
   # Tag and push image
   docker tag sentiment-analysis:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/sentiment-analysis:latest
   docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/sentiment-analysis:latest
   ```

2. **Create ECS Task Definition**
   - Go to AWS ECS Console
   - Create new task definition (Fargate)
   - Container: Use your ECR image
   - Memory: 4GB, CPU: 2 vCPU
   - Port mapping: 8501

3. **Create ECS Service**
   - Create cluster (if needed)
   - Create service using task definition
   - Configure load balancer (ALB)
   - Set desired tasks: 1 (or more for HA)

4. **Configure Load Balancer**
   - Create Application Load Balancer
   - Target group: ECS service
   - Health check: `/_stcore/health`
   - Configure HTTPS with ACM certificate

**Estimated Cost**: ~$50-100/month (Fargate + ALB)

### Option 2: AWS EC2

1. **Launch EC2 Instance**
   - AMI: Ubuntu 22.04 LTS
   - Instance type: t3.medium (2 vCPU, 4GB RAM)
   - Security group: Allow ports 22, 80, 443, 8501

2. **Install Docker**
   ```bash
   ssh ubuntu@your-ec2-ip
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker ubuntu
   ```

3. **Deploy Application**
   ```bash
   git clone https://github.com/yourusername/sentiment-analysis-triage.git
   cd sentiment-analysis-triage
   docker-compose up -d
   ```

4. **Configure Nginx (Optional)**
   ```bash
   sudo apt install nginx -y
   sudo nano /etc/nginx/sites-available/sentiment-analysis
   ```
   
   Add configuration:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

**Estimated Cost**: ~$30-50/month (t3.medium + storage)

### Option 3: AWS Elastic Beanstalk

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize and Deploy**
   ```bash
   cd sentiment-analysis-triage
   eb init -p docker sentiment-analysis
   eb create sentiment-analysis-env
   eb open
   ```

**Estimated Cost**: ~$40-60/month

---

## 🔷 Azure Deployment

**Best for**: Microsoft ecosystem, enterprise deployments

### Option 1: Azure Container Instances (ACI)

1. **Login to Azure**
   ```bash
   az login
   ```

2. **Create Resource Group**
   ```bash
   az group create --name sentiment-analysis-rg --location eastus
   ```

3. **Create Container Registry**
   ```bash
   az acr create --resource-group sentiment-analysis-rg \
     --name sentimentanalysisacr --sku Basic
   ```

4. **Push Docker Image**
   ```bash
   az acr login --name sentimentanalysisacr
   docker tag sentiment-analysis:latest sentimentanalysisacr.azurecr.io/sentiment-analysis:latest
   docker push sentimentanalysisacr.azurecr.io/sentiment-analysis:latest
   ```

5. **Deploy Container**
   ```bash
   az container create \
     --resource-group sentiment-analysis-rg \
     --name sentiment-analysis-app \
     --image sentimentanalysisacr.azurecr.io/sentiment-analysis:latest \
     --cpu 2 --memory 4 \
     --dns-name-label sentiment-analysis-unique \
     --ports 8501
   ```

6. **Access**: http://sentiment-analysis-unique.eastus.azurecontainer.io:8501

**Estimated Cost**: ~$50-70/month

### Option 2: Azure App Service

1. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name sentiment-analysis-plan \
     --resource-group sentiment-analysis-rg \
     --sku B2 --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create \
     --resource-group sentiment-analysis-rg \
     --plan sentiment-analysis-plan \
     --name sentiment-analysis-app \
     --deployment-container-image-name sentimentanalysisacr.azurecr.io/sentiment-analysis:latest
   ```

3. **Configure Port**
   ```bash
   az webapp config appsettings set \
     --resource-group sentiment-analysis-rg \
     --name sentiment-analysis-app \
     --settings WEBSITES_PORT=8501
   ```

**Estimated Cost**: ~$60-80/month

---

## 🌐 Google Cloud Platform

**Best for**: Google ecosystem, ML workloads

### Option 1: Cloud Run (Recommended)

1. **Enable APIs**
   ```bash
   gcloud services enable run.googleapis.com containerregistry.googleapis.com
   ```

2. **Build and Push**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/sentiment-analysis
   ```

3. **Deploy**
   ```bash
   gcloud run deploy sentiment-analysis \
     --image gcr.io/YOUR_PROJECT_ID/sentiment-analysis \
     --platform managed \
     --region us-central1 \
     --memory 4Gi \
     --cpu 2 \
     --allow-unauthenticated
   ```

4. **Access**: URL provided in output

**Estimated Cost**: ~$30-50/month (pay per use)

### Option 2: Google Kubernetes Engine (GKE)

1. **Create Cluster**
   ```bash
   gcloud container clusters create sentiment-analysis-cluster \
     --num-nodes=2 \
     --machine-type=n1-standard-2
   ```

2. **Deploy Application**
   ```bash
   kubectl create deployment sentiment-analysis \
     --image=gcr.io/YOUR_PROJECT_ID/sentiment-analysis
   
   kubectl expose deployment sentiment-analysis \
     --type=LoadBalancer \
     --port=80 \
     --target-port=8501
   ```

**Estimated Cost**: ~$150-200/month

---

## 🟣 Heroku Deployment

**Best for**: Simple deployments, hobby projects

### Prerequisites
- Heroku account
- Heroku CLI installed

### Steps

1. **Create Heroku App**
   ```bash
   heroku login
   heroku create sentiment-analysis-app
   ```

2. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Create Procfile**
   ```bash
   echo "web: streamlit run app.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **Scale**
   ```bash
   heroku ps:scale web=1
   ```

6. **Open App**
   ```bash
   heroku open
   ```

**Estimated Cost**: 
- Free tier: Limited hours/month
- Hobby: $7/month
- Standard: $25-50/month

---

## 🖥️ Self-Hosted Server

**Best for**: Full control, on-premises deployment

### Prerequisites
- Linux server (Ubuntu 22.04 recommended)
- Root/sudo access
- Domain name (optional)

### Steps

1. **Update System**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Install Dependencies**
   ```bash
   sudo apt install python3.11 python3-pip python3-venv nginx certbot python3-certbot-nginx -y
   ```

3. **Clone Repository**
   ```bash
   cd /opt
   sudo git clone https://github.com/yourusername/sentiment-analysis-triage.git
   cd sentiment-analysis-triage
   ```

4. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python -c "import nltk; nltk.download('vader_lexicon')"
   ```

5. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/sentiment-analysis.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Sentiment Analysis Dashboard
   After=network.target
   
   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/opt/sentiment-analysis-triage
   Environment="PATH=/opt/sentiment-analysis-triage/venv/bin"
   ExecStart=/opt/sentiment-analysis-triage/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

6. **Start Service**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable sentiment-analysis
   sudo systemctl start sentiment-analysis
   ```

7. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/sentiment-analysis
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

8. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/sentiment-analysis /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

9. **Setup HTTPS (Optional)**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

---

## 🔒 Security Best Practices

### All Deployments

1. **Use Environment Variables** for secrets
2. **Enable HTTPS** with valid SSL certificate
3. **Implement Authentication** if needed
4. **Regular Updates**: Keep dependencies updated
5. **Backup Data**: Regular backups of uploaded data
6. **Monitor Logs**: Set up logging and monitoring
7. **Rate Limiting**: Prevent abuse
8. **Firewall Rules**: Restrict unnecessary ports

### Secrets Management

**Streamlit Cloud**: Use built-in secrets management
**Docker**: Use Docker secrets or environment files
**AWS**: Use AWS Secrets Manager or Parameter Store
**Azure**: Use Azure Key Vault
**GCP**: Use Secret Manager

---

## 📊 Performance Optimization

### For Production Deployments

1. **Use VADER for Large Datasets**
   - Faster than BERT
   - Lower memory usage
   - Toggle in sidebar

2. **Optimize Batch Size**
   - 4GB RAM: batch_size = 16
   - 8GB RAM: batch_size = 32
   - 16GB RAM: batch_size = 64

3. **Enable Caching**
   - Already implemented with `@st.cache_resource`
   - Models loaded once per session

4. **Use CDN** for static assets

5. **Database Connection Pooling**
   - Already configured in SQL connector
   - Adjust pool size based on load

---

## 🔍 Monitoring & Logging

### Recommended Tools

- **Application Monitoring**: New Relic, Datadog, AppDynamics
- **Log Management**: ELK Stack, Splunk, CloudWatch
- **Uptime Monitoring**: UptimeRobot, Pingdom
- **Error Tracking**: Sentry, Rollbar

### Health Check Endpoint

Built-in Streamlit health check: `http://your-app/_stcore/health`

---

## 💰 Cost Comparison

| Platform | Monthly Cost | Best For |
|----------|-------------|----------|
| Streamlit Cloud (Free) | $0 | Testing, demos |
| Streamlit Cloud (Pro) | $20 | Small teams |
| Heroku Hobby | $7 | Personal projects |
| AWS ECS Fargate | $50-100 | Production |
| Azure ACI | $50-70 | Medium workloads |
| GCP Cloud Run | $30-50 | Pay-per-use |
| Self-Hosted VPS | $10-50 | Full control |

---

## 🆘 Troubleshooting

### Common Issues

**Out of Memory**
- Reduce batch size
- Use VADER instead of BERT
- Increase container memory

**Slow Performance**
- Enable caching
- Use GPU if available
- Optimize batch processing

**Connection Timeouts**
- Increase timeout settings
- Check network connectivity
- Verify firewall rules

**Model Download Fails**
- Check internet connectivity
- Increase timeout
- Pre-download models in Dockerfile

---

## 📞 Support

For deployment issues:
1. Check platform-specific documentation
2. Review application logs
3. Verify configuration files
4. Test locally with Docker first

---

**Last Updated**: 2026-05-17