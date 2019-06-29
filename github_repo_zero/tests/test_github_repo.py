from datadog_checks.github_repo_zero import GithubRepoZeroCheck


def test_check(aggregator, instance):
    check = GithubRepoZeroCheck('github_repo_zero', {}, {})
    check.check(instance)
    
    # In order to print debug logs we need to force the test to fail
    # assert False
