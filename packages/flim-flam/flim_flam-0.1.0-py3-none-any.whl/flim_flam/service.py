from functools import lru_cache as cache
from json import loads
from boto3 import client
from enum import Enum, auto


class ServiceRegistrationStatus(Enum):
    registered = auto()
    unregistered = auto()
    deregistering = auto()


class DeployResult(Enum):
    failure_deregistering = auto()
    success_updated = auto()
    success_registered = auto()


@cache
def get_ecs_client():
    return client("ecs")


@cache
def get_secrets_manager_client():
    return client("secretsmanager")


class Service:
    def __init__(
        self,
        name,
        *,
        cluster_name,
        desired_count=1,
        subnet_ids,
        security_group_ids,
        task_role_arn,
        execution_role_arn,
        log_group_name,
        log_region,
        image_uri,
        cpu,
        memory,
        entry=None,
        target_group_arn=None,
        secret_arn=None,
        port=None,
    ):
        self._name = name
        self._cluster_name = cluster_name
        self._desired_count = desired_count
        self._subnet_ids = subnet_ids
        self._security_group_ids = security_group_ids
        self._task_role_arn = task_role_arn
        self._execution_role_arn = execution_role_arn
        self._log_group_name = log_group_name
        self._log_region = log_region
        self._image_uri = image_uri
        self._cpu = cpu
        self._memory = memory
        self._entry = entry
        self._target_group_arn = target_group_arn
        self._secret_arn = secret_arn
        self._port = port

    def get_task_definition_name(self):
        return f"{self._cluster_name}-{self._name}"

    def get_entry(self):
        if self._entry is None:
            return None
        return ["/bin/bash", "-c", self._entry]

    def get_registration_status(self):
        client = get_ecs_client()
        services = client.describe_services(
            cluster=self._cluster_name, services=[self._name]
        )["services"]
        if len(services) == 0 or services[0]["status"] == "INACTIVE":
            return ServiceRegistrationStatus.unregistered
        if services[0]["status"] == "DRAINING":
            return ServiceRegistrationStatus.deregistering
        return ServiceRegistrationStatus.registered

    def get_port_mappings(self):
        if self._port is None:
            return []
        return [dict(containerPort=self._port, hostPort=self._port)]

    @cache
    def get_secrets(self):
        client = get_secrets_manager_client()
        if self._secret_arn is None:
            return []
        data = loads(client.get_secret_value(SecretId=self._secret_arn)["SecretString"])
        return [dict(name=x, valueFrom=f"{self._secret_arn}:{x}") for x in data.keys()]

    @cache
    def get_load_balancers(self):
        if self.port is None:
            return []
        if self._target_group_arn is None:
            raise RuntimeError("Cannot specify a port without a target group")
        return [
            dict(
                targetGroupArn=self._target_group_arn,
                containerName=self._name,
                containerPort=self._port,
            )
        ]

    @cache
    def get_task_definition_arn(self):
        client = get_ecs_client()
        return client.register_task_definition(
            family=self.get_task_definition_name(),
            taskRoleArn=self._task_role_arn,
            executionRoleArn=self._execution_role_arn,
            networkMode="awsvpc",
            requiresCompatibilities=["FARGATE"],
            cpu=str(self._cpu),
            memory=str(self._memory),
            containerDefinitions=[
                dict(
                    name=self.get_task_definition_name(),
                    entryPoint=self.get_entry(),
                    logConfiguration=dict(
                        logDriver="awslogs",
                        options={
                            "awslogs-group": self._log_group_name,
                            "awslogs-region": self._log_region,
                            "awslogs-stream-prefix": self.get_task_definition_name(),
                        },
                    ),
                    image=self._image_uri,
                    portMappings=self.get_port_mappings(),
                    secrets=self.get_secrets(),
                )
            ],
        )["taskDefinition"]["taskDefinitionArn"]

    def deploy(self):
        client = get_ecs_client()
        status = self.get_registration_status()
        if status == ServiceRegistrationStatus.deregistering:
            return False, DeployResult.failure_deregistering

        if status == ServiceRegistrationStatus.registered:
            client.update_service(
                cluster=self._cluster_name,
                service=self._name,
                desiredCount=self._desired_count,
                taskDefinition=self.get_task_definition_arn(),
                forceNewDeployment=True,
            )
            return True, DeployResult.success_updated

        client.create_service(
            cluster=self._cluster_name,
            serviceName=self._name,
            launchType="FARGATE",
            taskDefinition=self.get_task_definition_arn(),
            loadBalancers=self.get_load_balancers(),
            desiredCount=self._desired_count,
            networkConfiguration=dict(
                awsvpcConfiguration=dict(
                    subnets=self._subnet_ids,
                    securityGroups=self._security_group_ids,
                    assignPublicIp="ENABLED",
                )
            ),
        )
        return True, DeployResult.success_registered
