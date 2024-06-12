BRANCH="main"

echo "Synchronizing repository..."

#cd Heatcharts-visualization || { echo "Failed to navigate to repository directory"; exit 1; }

git pull origin $BRANCH

echo "Repository synchronized successfully!"

python ./gui.py