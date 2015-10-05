# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import Signal, receiver

from .models.student import Student
from .models.group import Group
from .models.exam import Exam

@receiver(post_save,sender=Student)
def log_student_updated_added_event(sender,**kwargs):
    # print sender
    """writes info about newly added or updated student
    into log file    """
    logger = logging.getLogger(__name__)
    # logger = logging.getLogger('students.signals')
    # logger = logging.getLogger('django.request')

    student = kwargs['instance']
    if kwargs['created']:
        logger.info("Student added: %s %s (ID: %d)",
            student.first_name, student.last_name, student.id )
    else:
        logger.info("Student updated: %s %s (ID: %d)",
            student.first_name, student.last_name, student.id)

@receiver(post_delete,sender=Student)
def log_student_deleted_event(sender,**kwargs):
    # print sender
    """writes info about newly deleted student
    into log file    """
    logger = logging.getLogger(__name__)

    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)",
            student.first_name, student.last_name, student.id )
 
 # Add events for groups
@receiver(post_save,sender=Group)
def log_group_updated_added_event(sender,**kwargs):
    """writes info about newly added or updated Group
    into log file    """
    # logger = logging.getLogger(__name__)
    logger = logging.getLogger('students.best')

    group = kwargs['instance']
    if kwargs['created']:
        logger.info("Group added: %s (ID: %d)",
            group.title, group.id )
    else:
        logger.info("Group updated: %s %s (ID: %d)",
            group.title, group.starosta, group.id )

@receiver(post_delete,sender=Group)
def log_group_deleted_event(sender,**kwargs):
    """writes info about newly deleted Group
    into log file    """
    logger = logging.getLogger(__name__)

    group = kwargs['instance']
    logger.info("Group deleted: %s (ID: %d)",
        group.title, group.id )

# Add events for Exams
@receiver(post_save,sender=Exam)
def log_exam_updated_added_event(sender,**kwargs):
    """writes info about newly added or updated Exam
    into log file    """
    logger = logging.getLogger(__name__)

    Exam = kwargs['instance']
    if kwargs['created']:
        logger.info("Exam added: %s %s (ID: %d)",
            Exam.nazva, Exam.exam_day, Exam.id )
    else:
        logger.info("Exam updated: %s %s %s (ID: %d)",
            Exam.nazva, Exam.exam_day, Exam.prepod, Exam.id )

@receiver(post_delete,sender=Exam)
def log_exam_deleted_event(sender,**kwargs):
    """writes info about newly deleted Exam
    into log file    """
    logger = logging.getLogger(__name__)

    Exam = kwargs['instance']
    logger.info("Exam deleted: %s %s (ID: %d)",
        Exam.nazva, Exam.prepod, Exam.id )



# Signal after sending mail to admin 526
# Create signal.
email_was_send = Signal(providing_args=['subject','email'])

# These function is receiver. It will receive 
# the signal (message) sent (published) by the sender (publisher).
def simple_receiver(**kwargs):
    subject, email = kwargs['subject'], kwargs['email']
    print 'Receiver # 1'
    print '\tsubject: %s, email: %s\n' % (subject, email)

email_was_send.connect(simple_receiver)

def send_signal_email_for_admin(subject,email):
    email_was_send.send(sender='send_signal_email_for_admin', subject=subject, email=email)

# send_signal_email_for_admin()
# email_for_admin_was_send.send(sender, subject=subject, email=email)

# from django.db.models.signals import pre_save






