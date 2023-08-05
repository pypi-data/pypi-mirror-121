# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2018-2021 Andrew Rechnitzer
# Copyright (C) 2020-2021 Colin B. Macdonald
# Copyright (C) 2021 Nicholas J H Lai

from datetime import datetime
import logging

from peewee import fn
import peewee as pw

from plom.rules import censorStudentNumber as censorID
from plom.rules import censorStudentName as censorName
from plom.db.tables import (
    Annotation,
    Bundle,
    DNMGroup,
    Group,
    IDGroup,
    QGroup,
    Rubric,
    Test,
    TPage,
    User,
)
from plom.db.tables import plomdb

log = logging.getLogger("DB")


########## Bundle creation ##########


def createReplacementBundle(self):
    try:
        bref = Bundle.create(name="replacements")
    except pw.IntegrityError as e:
        log.error("Create replacement page bundle = {}.{} error - {}".format(e))
        return False
    return True


def doesBundleExist(self, bundle_name, md5):
    """Checks if bundle with certain name and md5sum exists.

    Args:
        bundle_name (str)
        md5 (str)

    Returns:
        2-tuple: there are 4 possibilities:
            * neither match: no matching bundle, return `(False, None)`
            * name but not md5: return `(True, "name")` - user is trying
              to upload different bundles with same name.
            * md5 but not name: return `(True, "md5sum")` - user is trying
              to upload same bundle with different name.
            * both match: return `(True, "both")` - user could be retrying
              after network failure (for example) or uploading unknown or
              colliding pages.  That is, they previously uploaded some
              from the bundle but now are uploading more (Issue #1008).
    """
    bref = Bundle.get_or_none(name=bundle_name)
    if bref is not None:
        if bref.md5sum == md5:
            return (True, "both")
        else:
            return (True, "name")
    # name not known, so just check md5sum
    if Bundle.get_or_none(md5sum=md5) is not None:
        return (True, "md5sum")
    return (False, None)


def createNewBundle(self, bundle_name, md5):
    """Checks to see if bundle exists.

    Args:
        bundle_name (str)
        md5 (str)

    Returns:
        2-tuple: If bundle exists that matches by name *xor* by md5sum
            then return `(False, "name")` or `(False, "md5sum")`.
            If bundle matches both 'name' *and* 'md5sum' then return
            `(True, skip_list)` where `skip_list` is a list of the
            page-orders from that bundle that are already in the
            system.  The scan scripts will then skip those uploads.
            If no such bundle return `(True, [])`: we have created
            the bundle and return an empty skip-list.
    """
    exists, reason = self.doesBundleExist(bundle_name, md5)
    if not exists:
        Bundle.create(name=bundle_name, md5sum=md5)
        return (True, [])
    elif reason == "both":
        bref = Bundle.get_or_none(name=bundle_name, md5sum=md5)
        skip_list = []
        for iref in bref.images:
            skip_list.append(iref.bundle_order)
        return (True, skip_list)
    else:
        return (False, reason)


########## Test creation stuff ##############
def areAnyPapersProduced(self):
    """True if any papers have been created in the DB."""
    return len(Test.select()) > 0


def nextqueue_position(self):
    lastPos = Group.select(fn.MAX(Group.queue_position)).scalar()
    if lastPos is None:
        return 0
    return lastPos + 1


def createTest(self, t):
    with plomdb.atomic():
        try:
            tref = Test.create(test_number=t)  # must be unique
        except pw.IntegrityError as e:
            log.error("Create test {} error - {}".format(t, e))
            return False
    return True


def addTPages(self, tref, gref, t, pages, v):
    """
    For initial construction of test-pages for a test. We use these so we know what structured pages we should have.
    """
    flag = True
    with plomdb.atomic():
        for p in pages:
            try:
                TPage.create(
                    test=tref,
                    group=gref,
                    page_number=p,
                    version=v,
                    scanned=False,
                )
            except pw.IntegrityError as e:
                log.error("Adding page {} for test {} error - {}".format(p, t, e))
                flag = False
    return flag


def createIDGroup(self, t, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create IDGroup - No test with number {}".format(t))
        return False
    with plomdb.atomic():
        # make the Group
        gid = "i{}".format(str(t).zfill(4))
        try:
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="i",
                queue_position=self.nextqueue_position(),
            )  # must be unique
        except pw.IntegrityError as e:
            log.error(
                "Create ID for gid={} test={}: cannot create Group - {}".format(
                    gid, t, e
                )
            )
            return False
        # make the IDGroup
        try:
            iref = IDGroup.create(test=tref, group=gref)
        except pw.IntegrityError as e:
            log.error(
                "Create ID for gid={} test={} Group={}: cannot create IDGroup - {}.".format(
                    gid, t, gref, e
                )
            )
            return False
        return self.addTPages(tref, gref, t, pages, 1)  # always version 1.


def createDNMGroup(self, t, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create DNM - No test with number {}".format(t))
        return False

    gid = "d{}".format(str(t).zfill(4))
    with plomdb.atomic():
        # make the dnmgroup
        try:
            # A DNM group may have 0 pages, in that case mark it as scanned and set status = "complete"
            sc = True if len(pages) == 0 else False
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="d",
                scanned=sc,
                queue_position=self.nextqueue_position(),
            )
        except pw.IntegrityError as e:
            log.error(
                "Create DNM - cannot make Group {} of Test {} error - {}".format(
                    gid, t, e
                )
            )
            return False
        try:
            dref = DNMGroup.create(test=tref, group=gref)
        except pw.IntegrityError as e:
            log.error(
                "Create DNM - cannot create DNMGroup {} of group {} error - {}.".format(
                    dref, gref, e
                )
            )
            return False
        return self.addTPages(tref, gref, t, pages, 1)


# def createQGroup(self, t, q, v, pages, mark):
def createQGroup(self, t, q, v, pages):
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        log.warning("Create Q - No test with number {}".format(t))
        return False

    gid = "q{}g{}".format(str(t).zfill(4), q)

    with plomdb.atomic():
        # make the qgroup
        try:
            gref = Group.create(
                test=tref,
                gid=gid,
                group_type="q",
                version=v,
                queue_position=self.nextqueue_position(),
            )
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create group {} of Test {} error - {}".format(
                    gid, t, e
                )
            )
            return False
        try:
            # qref = QGroup.create(
            #     test=tref, group=gref, question=q, version=v, fullmark=mark
            # )
            qref = QGroup.create(test=tref, group=gref, question=q, version=v)
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create QGroup of question {} error - {}.".format(
                    gid, e
                )
            )
            return False
        ## create annotation 0 owned by HAL
        try:
            uref = User.get(name="HAL")
            aref = Annotation.create(qgroup=qref, edition=0, user=uref)
        except pw.IntegrityError as e:
            log.error(
                "Create Q - cannot create Annotation  of question {} error - {}.".format(
                    gid, e
                )
            )
            return False

        return self.addTPages(tref, gref, t, pages, v)


def getPageVersions(self, t):
    """Get the mapping between page numbers and version for a test.

    Args:
        t (int): a paper number.

    Returns:
        dict: keys are page numbers (int) and value is the page
            version (int), or empty dict if there was no such paper.
    """
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        return {}
    return {p.page_number: p.version for p in tref.tpages}


def getQuestionVersions(self, t):
    """Get the mapping between question numbers and versions for a test.

    Args:
        t (int): a paper number.

    Returns:
        dict: keys are question numbers (int) and value is the question
            version (int), or empty dict if there was no such paper.
    """
    tref = Test.get_or_none(test_number=t)
    if tref is None:
        return {}
    return {q.question: q.version for q in tref.qgroups}


def id_paper(self, paper_num, user_name, sid, sname):
    """Associate student name and id with a paper in the database.

    See also :func:`plom.db.db_identify.ID_id_paper` which is similar.

    Args:
        paper_num (int)
        user_name (str): User who did the IDing.
        sid (str): student id.
        sname (str): student name.

    Returns:
        tuple: `(True, None, None)` if successful, `(False, 409, msg)`
            means `sid` is in use elsewhere, a serious problem for
            the caller to deal with.  `(False, int, msg)` covers all
            other errors.  `msg` gives details about errors.  Some
            of these should not occur, and indicate possible bugs.
            `int` gives a hint of suggested HTTP status code,
            currently it can be 404 or 409.

    TODO: perhaps several sorts of exceptions would be better.
    """
    uref = User.get(name=user_name)  # TODO: or hardcode HAL like before
    # since user authenticated, this will always return legit ref.

    logbase = 'User "{}" tried to ID paper {}'.format(user_name, paper_num)
    with plomdb.atomic():
        tref = Test.get_or_none(Test.test_number == paper_num)
        if tref is None:
            msg = "denied b/c paper not found"
            log.error("{}: {}".format(logbase, msg))
            return False, 404, msg
        iref = tref.idgroups[0]
        iref.user = uref
        iref.status = "done"
        iref.student_id = sid
        iref.student_name = sname
        iref.identified = True
        iref.time = datetime.now()
        try:
            iref.save()
        except pw.IntegrityError:
            msg = "student id {} already entered elsewhere".format(censorID(sid))
            log.error("{} but {}".format(logbase, msg))
            return False, 409, msg
        tref.identified = True
        tref.save()
        log.info(
            'Paper {} ID\'d by "{}" as "{}" "{}"'.format(
                paper_num, user_name, censorID(sid), censorName(sname)
            )
        )
    return True, None, None


### Create some default rubrics
def createNoAnswerRubric(self, questionNumber, maxMark):
    """Create rubrics for when no answer given for question

    Each question needs one such rubric

    Args:
        questionNumber (int)
        maxMark: the max mark for that question

    Returns:
        Bool: True if successful, False if rubric already exists.
    """
    rID = 1000 + questionNumber
    uref = User.get(name="HAL")

    if Rubric.get_or_none(rID) is None:
        Rubric.create(
            key=rID,
            delta="0",
            text="No answer given",
            kind="absolute",
            question=questionNumber,
            user=uref,
            creationTime=datetime.now(),
            modificationTime=datetime.now(),
        )
        log.info("Created no-answer-rubric for question {}".format(questionNumber))
    else:
        log.info(
            "No-answer-rubric (up) for question {} already exists".format(
                questionNumber
            )
        )
        return False

    return True
