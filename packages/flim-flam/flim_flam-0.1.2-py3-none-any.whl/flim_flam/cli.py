from argparse import ArgumentParser
from functools import lru_cache as cache
from flim_flam.service import Service


@cache
def get_args():
    parser = ArgumentParser()
    parser.add_argument("name", type=str)
    parser.add_argument("--cluster-name", type=str, required=True)
    parser.add_argument("--desired-count", type=int, required=True)
    parser.add_argument("--subnet-id", type=str, action="append")
    parser.add_argument("--security-group-id", type=str, action="append")
    parser.add_argument("--task-role-arn", type=str, required=True)
    parser.add_argument("--execution-role-arn", type=str, required=True)
    parser.add_argument("--log-group-name", type=str, required=True)
    parser.add_argument("--log-region", type=str, required=True)
    parser.add_argument("--image-uri", type=str, required=True)
    parser.add_argument("--cpu", type=int, required=True)
    parser.add_argument("--memory", type=int, required=True)
    parser.add_argument("--entry", type=str, required=True)
    parser.add_argument("--target-group-arn", default=None, type=str)
    parser.add_argument("--secret-arn", default=None, type=str)
    parser.add_argument("--port", default=None, type=int)
    return parser.parse_args()


def run():
    args = get_args()

    if len(args.subnet_id) == 0:
        raise RuntimeError("At least one subnet ID must be specified.")
    if len(args.security_group_id) == 0:
        raise RuntimeError("At least one security group ID must be specified.")

    service = Service(
        args.name,
        cluster_name=args.cluster_name,
        desired_count=args.desired_count,
        subnet_ids=args.subnet_id,
        security_group_ids=args.security_group_id,
        task_role_arn=args.task_role_arn,
        execution_role_arn=args.execution_role_arn,
        log_group_name=args.log_group_name,
        log_region=args.log_region,
        image_uri=args.image_uri,
        cpu=args.cpu,
        memory=args.memory,
        entry=args.entry,
        target_group_arn=args.target_group_arn,
        secret_arn=args.secret_arn,
        port=args.port,
    )

    success, result = service.deploy()
    print(f"Deployment result: {result.name}")
