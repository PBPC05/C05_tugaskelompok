# Development Workflow

branch:

- `main` → Production-ready branch  
- `dev` → Integration branch  
- `feature/<name>` → For individual features  

## Steps
1. Update local dev branch
git checkout dev
git pull origin dev

2. Create feature branch
git checkout -b feature/<short-name>

3. Make changes
git add .
git commit -m "Add: feature <short-name>"
git push origin feature/<short-name>

4. Open Pull Request into dev
5. PR must be reviewed before merging
6. After tests pass, dev can be merged into main