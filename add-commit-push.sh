echo -e "\033[0;31mgit status\033[0m"
git status

echo -e "\033[0;31mEnter commit message:\033[0m"
read message

echo -e "\033[0;31mgit add -A\033[0m"
git add -A
echo -e "\033[0;31mgit commit -m \"$message\"\033[0m"
git commit -m "$message"
echo -e "\033[0;31mgit push\033[0m"
git push

echo -e "\033[0;31mPress enter to close...\033[0m"
read