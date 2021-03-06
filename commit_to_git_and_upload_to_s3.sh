if [ -n "$(git status --porcelain)" ]; then 
  echo "*** Files have been updated. ***";
  git add *
  git commit -m "latest voter info updates"
  git push origin master
  aws s3 cp /home/shane_d/voters_info/votersedge-voting-info/json s3://votersedge-voting-info-static/json --grants read=uri=http://acs.amazonaws.com/groups/global/AllUsers --recursive --include "*.*"
else 
  echo "*** Files have not changed. Nothing to commit and upload. ***";
fi