# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_delete, post_save, post_migrate
from django.dispatch import Signal, receiver

from .models.student import Student
from .models.group import Group
from .models.exam import Exam


@receiver(post_save)
def log_instance_updated_added_event(sender, **kwargs):
    """Writes info about newly added or updated instance
    into log file    """
    logger = logging.getLogger(__name__)

    # attribs = kwargs.items()
    instance = kwargs['instance']

    if instance.__class__ is Student:
        if kwargs['created']:
            logger.info("Student added: %s %s (ID: %d)",
                        instance.first_name, instance.last_name, instance.id)
        else:
            logger.info("Student updated: %s %s (ID: %d)",  # " %s",
                        instance.first_name, instance.last_name, instance.id)  # ,attribs)

    elif instance.__class__ is Group:
        if kwargs['created']:
            logger.info("Group added: %s (ID: %d)",
                        instance.title, instance.id)
        else:
            logger.info("Group updated: %s %s (ID: %d)",
                        instance.title, instance.starosta, instance.id)

    elif instance.__class__ is Exam:
        if kwargs['created']:
            logger.info("Exam added: %s %s (ID: %d)",
                        instance.nazva, instance.exam_day, instance.id)
        else:
            logger.info("Exam updated: %s %s %s (ID: %d)",
                        instance.nazva, instance.exam_day, instance.prepod, instance.id)


@receiver(post_delete)
def log_instance_deleted_event(sender, **kwargs):
    """Writes info about newly deleted instance
    into log file    """
    logger = logging.getLogger(__name__)

    instance = kwargs['instance']

    if instance.__class__ is Student:
        logger.info("Student deleted: %s %s (ID: %d)",
                    instance.first_name, instance.last_name, instance.id)

    elif instance.__class__ is Group:
        logger.info("Group deleted: %s (ID: %d)",
                    instance.title, instance.id)

    elif instance.__class__ is Exam:
        logger.info("Exam deleted: %s %s (ID: %d)",
                    instance.nazva, instance.prepod, instance.id)


# Add counter for request
counter = 0

from django.core.signals import request_started


@receiver(request_started)
def log_count_request(**kwargs):
    """Counts every request  """
    logger = logging.getLogger('students.request')
    global counter
    counter += 1
    environ = kwargs['environ']
    path_info = environ['PATH_INFO']
    # referrer = environ['HTTP_REFERER'][21:]
    logger.info("Jump from %s . Requests summary: %s", path_info, counter)


# Custom signal handler for post_migrate
from django.db.models.signals import post_migrate


@receiver(post_migrate, dispatch_uid='Migrate for current database')
def log_migrate_command_event(**kwargs):
    """Writes info message every run post_migrate  """
    logger = logging.getLogger(__name__)

    base = kwargs['using']
    logger.info("For migrate was using current database: %s", base)
