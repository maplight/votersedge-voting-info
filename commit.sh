- if [ -n "$(git status --porcelain)" ]; then
      echo "*** Files have been updated. ***";
      git add *;
      git commit -m "latest voter info updates";
      git push origin master;
      echo "*** Files committed to git. ***";
  else
      echo "*** Files have not changed. Nothing to commit and upload. ***";
  fi