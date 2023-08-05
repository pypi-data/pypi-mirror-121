# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2020 Andrew Rechnitzer
# Copyright (C) 2020-2021 Colin B. Macdonald
# Copyright (C) 2021 Jed Yeo

from plom.misc_utils import format_int_list_with_runs
from plom.messenger import ScanMessenger
from plom.plom_exceptions import PlomExistingLoginException


def get_number_of_questions(server=None, pwd=None):
    """Contact server for number of questions."""
    if server and ":" in server:
        s, p = server.split(":")
        msgr = ScanMessenger(s, port=p)
    else:
        msgr = ScanMessenger(server)
    msgr.start()

    try:
        msgr.requestAndSaveToken("scanner", pwd)
    except PlomExistingLoginException:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            'In order to force-logout the existing authorisation run "plom-scan clear"'
        )
        raise

    try:
        spec = msgr.get_spec()
    finally:
        msgr.closeUser()
        msgr.stop()
    return spec["numberOfQuestions"]


def check_and_print_scan_status(server=None, pwd=None):
    """Prints summary of test/hw uploads.

    More precisely. Prints lists
    * which tests have been used (ie at least one uploaded page)
    * which tests completely scanned (both tpages and hwpage)
    * incomplete tests (missing one tpage or one hw-question)
    """
    if server and ":" in server:
        s, p = server.split(":")
        msgr = ScanMessenger(s, port=p)
    else:
        msgr = ScanMessenger(server)
    msgr.start()

    try:
        msgr.requestAndSaveToken("scanner", pwd)
    except PlomExistingLoginException as e:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            'In order to force-logout the existing authorisation run "plom-scan clear"'
        )
        raise

    try:
        spec = msgr.get_spec()
        # returns pairs of [page,version] - only display pages
        ST = msgr.getScannedTests()
        UT = msgr.getUnusedTests()
        IT = msgr.getIncompleteTests()
    finally:
        msgr.closeUser()
        msgr.stop()

    print("Test papers unused: [{}]".format(format_int_list_with_runs(UT)))

    print("Scanned tests in the system:")
    for t in ST:
        scannedTPages = []
        scannedHWPages = []
        for x in ST[t]:
            if x[0][0] == "t":  # is a test page = "t.p"
                p = int(x[0].split(".")[1])
                scannedTPages.append(p)
            elif x[0][0] == "h":  # is a hw page = "h.q.o"
                q = int(x[0].split(".")[1])
                if q not in scannedHWPages:
                    scannedHWPages.append(q)

        print(
            "\t{}: testPages [{}] hwPages [{}]".format(
                t,
                format_int_list_with_runs(scannedTPages),
                format_int_list_with_runs(scannedHWPages),
            )
        )
    print("Number of scanned tests in the system: {}".format(len(ST)))
    print("Incomplete scans - listed with their missing pages: ")
    for t in IT:
        missingPagesT = []
        missingPagesH = []
        for x in IT[t]:  # each entry is [page, version, scanned?]
            if x[0][0] == "t":  # is a test page
                p = int(x[0].split(".")[1])
                if x[2] is False:
                    missingPagesT.append(p)
            elif x[0][0] == "h":  # is a w page
                q = int(x[0].split(".")[1])
                if x[2] is False:
                    missingPagesH.append(q)
        print(
            "\t{}: t[{}] h[{}]".format(
                t,
                format_int_list_with_runs(missingPagesT),
                format_int_list_with_runs(missingPagesH),
            )
        )


def checkMissingHWQ(server=None, pwd=None):
    if server and ":" in server:
        s, p = server.split(":")
        msgr = ScanMessenger(s, port=p)
    else:
        msgr = ScanMessenger(server)
    msgr.start()

    try:
        msgr.requestAndSaveToken("scanner", pwd)
    except PlomExistingLoginException as e:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            'In order to force-logout the existing authorisation run "plom-scan clear"'
        )
        raise

    try:
        missingHWQ = msgr.getMissingHW()
    finally:
        msgr.closeUser()
        msgr.stop()
    return missingHWQ


def replaceMissingHWQ(server, pwd, student_id, question):
    if server and ":" in server:
        s, p = server.split(":")
        msgr = ScanMessenger(s, port=p)
    else:
        msgr = ScanMessenger(server)
    msgr.start()

    try:
        msgr.requestAndSaveToken("scanner", pwd)
    except PlomExistingLoginException as e:
        print(
            "You appear to be already logged in!\n\n"
            "  * Perhaps a previous session crashed?\n"
            "  * Do you have another scanner-script running,\n"
            "    e.g., on another computer?\n\n"
            'In order to force-logout the existing authorisation run "plom-scan clear"'
        )
        raise

    try:
        rval = msgr.replaceMissingHWQuestion(
            student_id=student_id, test=None, question=question
        )  # can replace by SID or by test-number
        msgr.triggerUpdateAfterHWUpload()
    finally:
        msgr.closeUser()
        msgr.stop()
    return rval
