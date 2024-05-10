import subprocess


def pytest_sessionstart(session):
    """在测试会话开始时执行的代码"""
    print("Starting Docker containers...")
    # docker compose -f ../test_services/compose-kafka.yml up -d
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "../test_services/compose-kafka.yml",
            "up",
            "-d",
        ],
        check=True,
    )


def pytest_sessionfinish(session, exitstatus):
    """在测试会话结束时执行的代码"""
    print("Stopping Docker containers...")
    # subprocess.run(["docker-compose", "down"], check=True)
    subprocess.run(
        [
            "docker",
            "compose",
            "-f",
            "../test_services/compose-kafka.yml",
            "down",
        ],
        check=True,
    )
