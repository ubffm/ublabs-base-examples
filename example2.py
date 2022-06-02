#!/usr/bin/env python3
import re
import base_api

REPO_PATTERN = re.compile(r"(l[ia]ng[uv]|sprach)", re.IGNORECASE)


def has_relevant_title(repo):
    return bool(
        re.findall(REPO_PATTERN, repo["name"])
        or re.findall(REPO_PATTERN, repo["name_en"])
    )


def is_oa(repo):
    oa_ratio = repo["num_oa_records"] / repo["num_records"]
    if oa_ratio >= 0.8 and repo["num_records"] > 100:
        return True
    return False


def main():
    repos = list(base_api.iter_list_repositories(coll="de"))
    print("Repos total:", len(repos))
    profiles = [
        base_api.list_profile(repo.get("internal_name"), wait=1)
        for repo in repos
        if has_relevant_title(repo)
    ]
    print("Relevant:", len(profiles))
    print("Result:")
    for profile in profiles:
        if is_oa(profile):
            print(profile["internal_name"])


if __name__ == "__main__":
    main()
