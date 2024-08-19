import docker


def parse_container_status(container_name) -> str:
    """解析容器状态"""

    client = docker.from_env()

    # 获取容器对象
    container = client.containers.get(container_name)

    container_info = container.attrs  # 获取容器的详细信息

    # 获取容器的健康检查状态
    health_status = (
        container_info.get("State", {})
        .get("Health", {})
        .get("Status", "No health check")
    )
    return health_status
