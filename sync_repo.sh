BRANCH="main"

echo "Synchronizing repository..."

#cd Heatcharts-visualization || { echo "Failed to navigate to repository directory"; exit 1; }
#git -c http.proxy="" -c https.proxy="" clone https://wrgitlab.ext.net.nokia.com/pawwozni/Heatcharts-visualization.git

git -c http.proxy="" -c https.proxy="" pull origin $BRANCH

echo "Repository synchronized successfully!"

python ./gui.py