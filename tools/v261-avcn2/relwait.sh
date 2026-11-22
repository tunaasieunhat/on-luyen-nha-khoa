S=$1
for i in $(seq 1 60); do
  st=$(gh api "repos/tunaasieunhat/on-luyen-nha-khoa/actions/runs?head_sha=$S&per_page=5" --jq '.workflow_runs[] | select(.name=="Build APK Android") | .status+":"+(.conclusion//"")+":"+(.id|tostring)' 2>/dev/null)
  case "$st" in completed*) echo "$(date +%H:%M:%S) $st"; break;; esac
  sleep 30
done
gh api repos/tunaasieunhat/on-luyen-nha-khoa/releases --jq '.[0:2][] | .tag_name+" "+.name+" "+([.assets[]|.name+":"+(.size|tostring)]|join(","))'
