# Development Workflow

branch:

- `master` → Production-ready branch  
- `dev` → Integration branch  
- `feat/<name>` → For individual features  

## Steps
1. Update local dev branch
git checkout dev
git pull origin dev

2. Create feature branch
git checkout -b feat/<short-name>
<short-name> -> feature name

3. Make changes
git add .
git commit -m "Add: feat <short-name>"
git push origin feat/<short-name>

4. Open Pull Request into dev
5. If there is no issues, dev can be merged into main