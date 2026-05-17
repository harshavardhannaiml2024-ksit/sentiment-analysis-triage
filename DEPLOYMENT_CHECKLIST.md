# 🚀 Deployment Checklist

Use this checklist to ensure a smooth deployment of the Sentiment Analysis Dashboard.

## Pre-Deployment Checklist

### ✅ Code Preparation

- [ ] All code is committed to version control (Git)
- [ ] `.gitignore` is properly configured
- [ ] No sensitive data (API keys, passwords) in code
- [ ] All dependencies listed in `requirements.txt`
- [ ] Sample data is included for testing
- [ ] Documentation is up to date (README.md, QUICKSTART.md)

### ✅ Configuration

- [ ] `config.yaml` is properly configured
- [ ] `.env.example` is created with all required variables
- [ ] Streamlit config files are in `.streamlit/` directory
- [ ] Database connection strings are prepared (if using databases)
- [ ] API credentials are ready (if using external APIs)

### ✅ Testing

- [ ] Application runs locally without errors
- [ ] Sample data analysis works correctly
- [ ] All visualizations render properly
- [ ] Export functionality works
- [ ] File upload works with CSV/Excel files
- [ ] Memory usage is acceptable for target environment

---

## Deployment Options

Choose your deployment platform and follow the corresponding checklist:

### 🌥️ Option 1: Streamlit Cloud (Easiest)

**Best for**: Quick deployment, demos, small teams

#### Prerequisites
- [ ] GitHub account created
- [ ] Streamlit Cloud account created (free at share.streamlit.io)
- [ ] Repository is public or Streamlit Cloud has access

#### Steps
- [ ] Push code to GitHub repository
- [ ] Go to share.streamlit.io
- [ ] Click "New app"
- [ ] Select repository and branch
- [ ] Set main file path: `app.py`
- [ ] Configure secrets (if needed) in Streamlit Cloud dashboard
- [ ] Click "Deploy"
- [ ] Wait for deployment (5-10 minutes)
- [ ] Test the deployed application
- [ ] Share the URL with your team

#### Post-Deployment
- [ ] Verify app is accessible
- [ ] Test with sample data
- [ ] Monitor resource usage
- [ ] Set up custom domain (optional)

**Estimated Time**: 15-30 minutes  
**Cost**: Free (with limitations) or $20/month (Pro)

---

### 🐳 Option 2: Docker Deployment

**Best for**: Consistent environments, local development, self-hosting

#### Prerequisites
- [ ] Docker installed on target machine
- [ ] Docker Compose installed (optional but recommended)
- [ ] Sufficient resources (4GB RAM, 2 CPU cores minimum)

#### Steps
- [ ] Clone repository to target machine
- [ ] Create `.env` file from `.env.example`
- [ ] Update configuration in `config.yaml`
- [ ] Build Docker image: `docker build -t sentiment-analysis .`
- [ ] Test locally: `docker run -p 8501:8501 sentiment-analysis`
- [ ] Or use Docker Compose: `docker-compose up -d`
- [ ] Verify application is running: http://localhost:8501
- [ ] Test with sample data
- [ ] Configure reverse proxy (Nginx/Traefik) for production
- [ ] Set up SSL certificate (Let's Encrypt)

#### Post-Deployment
- [ ] Set up automatic restarts
- [ ] Configure log rotation
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Create backup strategy
- [ ] Document deployment process

**Estimated Time**: 1-2 hours  
**Cost**: Infrastructure costs only

---

### ☁️ Option 3: AWS Deployment

**Best for**: Enterprise deployments, scalability, AWS ecosystem

#### Prerequisites
- [ ] AWS account created
- [ ] AWS CLI installed and configured
- [ ] IAM user with appropriate permissions
- [ ] Docker image built and tested

#### Option 3A: AWS ECS (Fargate)

- [ ] Create ECR repository
- [ ] Push Docker image to ECR
- [ ] Create ECS cluster
- [ ] Create task definition (4GB memory, 2 vCPU)
- [ ] Create ECS service
- [ ] Configure Application Load Balancer
- [ ] Set up target group with health checks
- [ ] Configure security groups (allow 80, 443)
- [ ] Set up Route 53 for DNS (optional)
- [ ] Configure ACM certificate for HTTPS
- [ ] Test deployment
- [ ] Set up CloudWatch logging
- [ ] Configure auto-scaling (optional)

**Estimated Time**: 2-4 hours  
**Cost**: ~$50-100/month

#### Option 3B: AWS EC2

- [ ] Launch EC2 instance (t3.medium or larger)
- [ ] Configure security group (SSH, HTTP, HTTPS)
- [ ] SSH into instance
- [ ] Install Docker and Docker Compose
- [ ] Clone repository
- [ ] Deploy with Docker Compose
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL with Certbot
- [ ] Configure automatic backups
- [ ] Set up CloudWatch monitoring

**Estimated Time**: 2-3 hours  
**Cost**: ~$30-50/month

---

### 🔷 Option 4: Azure Deployment

**Best for**: Microsoft ecosystem, enterprise deployments

#### Prerequisites
- [ ] Azure account created
- [ ] Azure CLI installed
- [ ] Resource group created

#### Option 4A: Azure Container Instances

- [ ] Create Azure Container Registry
- [ ] Push Docker image to ACR
- [ ] Create container instance
- [ ] Configure DNS label
- [ ] Set resource limits (2 CPU, 4GB memory)
- [ ] Configure environment variables
- [ ] Test deployment
- [ ] Set up Azure Monitor

**Estimated Time**: 1-2 hours  
**Cost**: ~$50-70/month

#### Option 4B: Azure App Service

- [ ] Create App Service Plan (B2 or higher)
- [ ] Create Web App
- [ ] Configure container settings
- [ ] Set application settings
- [ ] Configure custom domain (optional)
- [ ] Enable HTTPS
- [ ] Set up Application Insights
- [ ] Configure auto-scaling

**Estimated Time**: 2-3 hours  
**Cost**: ~$60-80/month

---

### 🌐 Option 5: Google Cloud Platform

**Best for**: Google ecosystem, ML workloads

#### Prerequisites
- [ ] GCP account created
- [ ] gcloud CLI installed
- [ ] Project created

#### Option 5A: Cloud Run (Recommended)

- [ ] Enable Cloud Run API
- [ ] Build and push image to GCR
- [ ] Deploy to Cloud Run
- [ ] Configure memory (4GB) and CPU (2)
- [ ] Set up custom domain (optional)
- [ ] Configure environment variables
- [ ] Enable Cloud Logging
- [ ] Test deployment

**Estimated Time**: 1-2 hours  
**Cost**: ~$30-50/month (pay-per-use)

#### Option 5B: Google Kubernetes Engine

- [ ] Create GKE cluster
- [ ] Configure kubectl
- [ ] Apply Kubernetes manifests
- [ ] Set up Ingress controller
- [ ] Configure SSL certificate
- [ ] Set up monitoring
- [ ] Configure auto-scaling

**Estimated Time**: 3-4 hours  
**Cost**: ~$150-200/month

---

### 🟣 Option 6: Heroku

**Best for**: Simple deployments, hobby projects

#### Prerequisites
- [ ] Heroku account created
- [ ] Heroku CLI installed

#### Steps
- [ ] Create Heroku app
- [ ] Add Python buildpack
- [ ] Create Procfile
- [ ] Push to Heroku
- [ ] Scale web dyno
- [ ] Configure environment variables
- [ ] Test deployment
- [ ] Set up custom domain (optional)

**Estimated Time**: 30 minutes - 1 hour  
**Cost**: $7-50/month

---

### 🖥️ Option 7: Self-Hosted Server

**Best for**: Full control, on-premises deployment

#### Prerequisites
- [ ] Linux server (Ubuntu 22.04 recommended)
- [ ] Root/sudo access
- [ ] Domain name (optional)

#### Steps
- [ ] Update system packages
- [ ] Install Python 3.11+
- [ ] Install Nginx
- [ ] Clone repository
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Create systemd service
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL with Certbot
- [ ] Configure firewall
- [ ] Set up log rotation
- [ ] Configure automatic backups

**Estimated Time**: 2-4 hours  
**Cost**: Server costs only

---

## Post-Deployment Checklist

### ✅ Verification

- [ ] Application is accessible via URL
- [ ] Sample data analysis works
- [ ] All visualizations render correctly
- [ ] File upload functionality works
- [ ] Export functionality works
- [ ] No console errors in browser
- [ ] Health check endpoint responds: `/_stcore/health`

### ✅ Security

- [ ] HTTPS is enabled (SSL certificate)
- [ ] Secrets are stored securely (not in code)
- [ ] Firewall rules are configured
- [ ] Only necessary ports are open
- [ ] Authentication is enabled (if required)
- [ ] Rate limiting is configured (if needed)
- [ ] CORS is properly configured
- [ ] Security headers are set

### ✅ Performance

- [ ] Application loads in reasonable time (<5 seconds)
- [ ] Analysis completes without timeout
- [ ] Memory usage is within limits
- [ ] CPU usage is acceptable
- [ ] Database connections are pooled (if applicable)
- [ ] Caching is working properly

### ✅ Monitoring

- [ ] Application logs are accessible
- [ ] Error tracking is set up (Sentry, Rollbar)
- [ ] Uptime monitoring is configured (UptimeRobot, Pingdom)
- [ ] Resource monitoring is enabled (CPU, memory, disk)
- [ ] Alerts are configured for critical issues
- [ ] Backup strategy is in place

### ✅ Documentation

- [ ] Deployment process is documented
- [ ] Access credentials are stored securely
- [ ] Team members have access to documentation
- [ ] Troubleshooting guide is available
- [ ] Rollback procedure is documented

---

## Troubleshooting Common Issues

### Issue: Out of Memory

**Symptoms**: Application crashes, slow performance
**Solutions**:
- [ ] Increase container/instance memory
- [ ] Reduce batch size in configuration
- [ ] Use VADER instead of BERT
- [ ] Enable swap space (for VMs)

### Issue: Slow Performance

**Symptoms**: Long analysis times, timeouts
**Solutions**:
- [ ] Increase CPU allocation
- [ ] Enable GPU (if available)
- [ ] Optimize batch size
- [ ] Use caching effectively
- [ ] Consider using VADER for large datasets

### Issue: Connection Timeouts

**Symptoms**: Database/API connection failures
**Solutions**:
- [ ] Increase timeout settings
- [ ] Check network connectivity
- [ ] Verify firewall rules
- [ ] Check security group settings
- [ ] Verify credentials

### Issue: SSL Certificate Errors

**Symptoms**: HTTPS not working, certificate warnings
**Solutions**:
- [ ] Verify certificate is valid
- [ ] Check certificate expiration
- [ ] Ensure domain matches certificate
- [ ] Renew certificate if expired
- [ ] Check reverse proxy configuration

### Issue: Model Download Fails

**Symptoms**: First-time startup fails
**Solutions**:
- [ ] Check internet connectivity
- [ ] Increase timeout settings
- [ ] Pre-download models in Dockerfile
- [ ] Use alternative model mirror
- [ ] Check disk space

---

## Rollback Procedure

If deployment fails or issues arise:

1. **Immediate Actions**
   - [ ] Stop new deployments
   - [ ] Assess impact and severity
   - [ ] Notify team members

2. **Rollback Steps**
   - [ ] Revert to previous version/image
   - [ ] Restart services
   - [ ] Verify rollback successful
   - [ ] Test critical functionality

3. **Post-Rollback**
   - [ ] Document what went wrong
   - [ ] Fix issues in development
   - [ ] Test thoroughly before redeploying
   - [ ] Update deployment checklist

---

## Maintenance Schedule

### Daily
- [ ] Check application logs for errors
- [ ] Monitor resource usage
- [ ] Verify uptime

### Weekly
- [ ] Review performance metrics
- [ ] Check for security updates
- [ ] Verify backups are working

### Monthly
- [ ] Update dependencies
- [ ] Review and optimize costs
- [ ] Test disaster recovery
- [ ] Update documentation

### Quarterly
- [ ] Security audit
- [ ] Performance optimization
- [ ] Capacity planning
- [ ] Team training on updates

---

## Support Contacts

**Technical Issues**:
- Documentation: README.md, DEPLOYMENT.md
- GitHub Issues: [Your Repository URL]

**Platform-Specific Support**:
- Streamlit Cloud: https://docs.streamlit.io
- AWS: https://aws.amazon.com/support/
- Azure: https://azure.microsoft.com/support/
- GCP: https://cloud.google.com/support/

---

## Success Criteria

Deployment is considered successful when:

- ✅ Application is accessible via public URL
- ✅ All features work as expected
- ✅ Performance meets requirements
- ✅ Security measures are in place
- ✅ Monitoring is configured
- ✅ Team can access and use the application
- ✅ Documentation is complete

---

**Last Updated**: 2026-05-17

**Deployment Status**: [ ] Not Started | [ ] In Progress | [ ] Complete

**Deployed By**: _______________

**Deployment Date**: _______________

**Deployment URL**: _______________