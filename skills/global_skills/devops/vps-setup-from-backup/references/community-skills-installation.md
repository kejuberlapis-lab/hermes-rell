# Community Skills Installation from GitHub

## When to use
User asks to install skills from GitHub repos (awesome-hermes, specific repos, etc.)
The `hermes skills install` command often fails for GitHub repos — use manual clone + copy instead.

## Method: Clone + Copy SKILL.md

```bash
# 1. Clone repos to /tmp
cd /tmp
git clone --depth 1 https://github.com/OWNER/REPO.git repo-name

# 2. Find all SKILL.md files and copy to hermes skills dir
find repo-name -name "SKILL.md" -type f | while read skill; do
  skill_dir=$(dirname $skill)
  skill_name=$(basename $skill_dir)
  dest=~/.hermes/skills/community/$skill_name
  if [ ! -d "$dest" ]; then
    cp -r "$skill_dir" "$dest" && echo "Installed: $skill_name"
  fi
done
```

## Batch install from multiple repos

```bash
cd /tmp
for repo in owner/repo1 owner/repo2 owner/repo3; do
  name=$(echo $repo | cut -d/ -f2)
  git clone --depth 1 https://github.com/$repo.git $name 2>&1 | tail -1
done

mkdir -p ~/.hermes/skills/community
for dir in repo1 repo2 repo3; do
  find $dir -name "SKILL.md" -type f | while read skill; do
    skill_dir=$(dirname $skill)
    skill_name=$(basename $skill_dir)
    dest=~/.hermes/skills/community/$skill_name
    [ ! -d "$dest" ] && cp -r "$skill_dir" "$dest" && echo "Installed: $skill_name"
  done
done
```

## Popular repos with skills

| Repo | Skills | Description |
|------|--------|-------------|
| wondelai/skills | 60+ | Business, design, coding |
| nexu-io/open-design | 300+ | UI/UX, slides, web design |
| witt3rd/oh-my-hermes | 8 | Multi-agent orchestration |
| Lethe044/hermes-incident-commander | 1 | SRE auto-healing |
| JimmyHuang2002/hermes-backup-recovery | 1 | Backup & restore |
| 0xNyk/awesome-hermes-agent | dir | Directory of all community skills |

## Important notes
- `hermes skills tap add` + `hermes skills install` often fails for GitHub repos
- Manual clone + copy is more reliable
- Skills go to `~/.hermes/skills/community/` to avoid conflict with official skills
- Some repos (like hermes-godmode) are config packs, not skills — check for SKILL.md first
- After installing, restart gateway or `/reload-skills` to pick up new skills
