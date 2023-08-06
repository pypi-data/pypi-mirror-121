"""
This module is needed to save the library objects from lab_orchestrator_lib.model.model into a django database. It
provides `Model` classes for all resources that needs to be saved in a database.
"""
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

from lab_orchestrator_lib.model.model import check_dns_subdomain_name, check_dns_name


def not_empty(value):
    if isinstance(value, str) and len(value) <= 0:
        raise ValidationError(
            '%(value)s is to empty.',
            params={'value': value},
        )


def validate_dns_label(value):
    if not check_dns_name(value):
        raise ValidationError(
            '%(value)s is not a valid dns label.',
            params={'value': value},
        )


def validate_dns_subdomain(value):
    if not check_dns_subdomain_name(value):
        raise ValidationError(
            '%(value)s is not a valid dns subdomain.',
            params={'value': value},
        )


class DockerImageModel(models.Model):
    """Database representation of the DockerImage class from lab_orchestrator_lib.model.model.

    This class is used in the adapter to store the DockerImage data in a django database. This is also useful
    for django view sets serialization.
    """
    name = models.CharField(max_length=32, validators=[not_empty], unique=True, null=False)
    description = models.CharField(max_length=128, validators=[not_empty], null=False)
    url = models.CharField(max_length=256, validators=[not_empty], null=False)

    def __str__(self):
        return f"{self.name}: {self.url} ({self.pk})"


class LabModel(models.Model):
    """Database representation of the Lab class from lab_orchestrator_lib.model.model.

    This class is used in the adapter to store the Lab data in a django database. This is also useful
    for django view sets serialization.
    """
    name = models.CharField(max_length=32, validators=[not_empty], unique=True, null=False)
    namespace_prefix = models.CharField(
        max_length=32,
        validators=[validate_dns_label, not_empty],
        unique=True, null=False)
    description = models.CharField(max_length=128, validators=[not_empty], null=False)

    def __str__(self):
        return f"{self.name} ({self.pk})"


class LabDockerImageModel(models.Model):
    """Database representation of the LabDockerImage class from lab_orchestrator_lib.model.model.

    This class is used in the adapter to store the LabDockerImage data in a django database. This is also useful
    for django view sets serialization.
    """
    lab = models.ForeignKey(LabModel, on_delete=models.DO_NOTHING, null=False, related_name="lab_docker_images")
    docker_image = models.ForeignKey(
        DockerImageModel, on_delete=models.DO_NOTHING,
        null=False, related_name="lab_docker_images")
    docker_image_name = models.CharField(
        max_length=32,
        validators=[validate_dns_subdomain, not_empty],
        null=False)

    def __str__(self):
        return f"{self.lab.name} - {self.docker_image.name} ({self.docker_image_name})"


class LabInstanceModel(models.Model):
    """Database representation of the LabInstance class from lab_orchestrator_lib.model.model.

    This class is used in the adapter to store the LabInstance data in a django database. This is also useful
    for django view sets serialization.
    """
    lab = models.ForeignKey(LabModel, on_delete=models.CASCADE, null=False, related_name="lab_instances")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name="lab_instances")

    def __str__(self):
        return f"{self.lab.name} - {self.user.pk} ({self.pk})"
