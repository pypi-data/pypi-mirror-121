import subprocess
import logging
import os

from django.conf import settings

from .models import Submission

logger = logging.getLogger(__name__)

CATEGORY_SPAM = 'spam'
CATEGORY_HAM = 'not-spam'


def learn(directory, spam):
    classifier_data_dir = os.path.join(settings.BASE_DIR, 'classifier_data')
    category = CATEGORY_SPAM if spam else CATEGORY_HAM
    command = ['dbacl', '-l', category, directory]
    if not os.path.exists(classifier_data_dir):
        os.makedirs(classifier_data_dir)
    process = subprocess.run(
        command,
        cwd=classifier_data_dir,
        stdout=subprocess.PIPE,
        # capture_output=True, # Python > 3.6 only
    )
    process.stdout.decode('utf-8')


class ClassificationError(RuntimeError):
    pass


def classify(text):
    command = ['dbacl', '-c', CATEGORY_SPAM, '-c', CATEGORY_HAM, '-U']
    process = subprocess.run(
        command,
        cwd=os.path.join(settings.BASE_DIR, 'classifier_data'),
        input=text.encode('utf-8'),
        stdout=subprocess.PIPE,
        # capture_output=True, # Python > 3.6 only
    )
    output = process.stdout.decode('utf-8')
    if output:
        cls, _, pc = output.strip('\n%').split(' ')
        return (cls, int(pc))
    else:
        raise ClassificationError('No classification output.')


def is_spam(text):
    classifier_settings = getattr(settings, 'CLASSIFIER', {})
    silently_discard_confidence = classifier_settings.get('SILENTLY_DISCARD_CONFIDENCE', 80)
    record_and_discard_confidence = classifier_settings.get('RECORD_AND_DISCARD_CONFIDENCE', 60)

    try:
        category, confidence = classify(text)
    except ClassificationError as e:
        logger.warning(f'Classification error; marking as non-spam {e}.')
        category, confidence = CATEGORY_HAM, 0
    submission = Submission(
        content=text,
        spam_auto=(category == 'spam'),
        confidence=confidence,
    )
    if category == 'spam' and confidence >= silently_discard_confidence:
        # Don't record spam we're super-confident of.
        pass
    else:
        submission.save()

    if category == 'spam' and confidence >= record_and_discard_confidence:
        logger.info(f'Ignore contact form message spam with confidence {confidence} beginning: {submission.content[:50]}.')
        return True, submission
    else:
        logger.info(f'Accepted contact form message with category "{category}" and confidence {confidence} beginning: {submission.content[:50]}.')
        return False, submission


def spam_footer(submission, site):
    return """

--
Spam score: {category} ({confidence}% confidence)
Train as spam: https://{site.domain}/classifier/{id}/spam/
Train as not spam: https://{site.domain}/classifier/{id}/not-spam/
""".format(site=site, category=('spam' if submission.spam_auto else 'not-spam'), confidence=submission.confidence, id=submission.id)
