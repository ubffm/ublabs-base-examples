#!/usr/bin/env python3
import re
import base_api

REPO_PATTERN = re.compile(r"(l[ia]ng[uv]|sprach)", re.IGNORECASE)


def has_relevant_title(repo, pattern=REPO_PATTERN):
    """Check if alle title fields in a repository repo agsinst the prodived pattern"""
    return bool(
        re.findall(pattern, repo["name"])
        or re.findall(pattern, repo["name_en"])
    )


def is_oa(repo, ratio=0.0, minimum=0):
    """Check the open access status of a given repo.

    ratio: minimum ratio of oa titles (float)
    minimum: minimum number of documents total."""
    oa_ratio = repo["num_oa_records"] / repo["num_records"]
    return oa_ratio >= ratio and repo["num_records"] >= minimum


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
        if is_oa(profile, ratio=0.8, minimum=100):
            print(profile["internal_name"])


if __name__ == "__main__":
    main()
