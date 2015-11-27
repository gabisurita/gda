import web

def POSTParse(RawPost):
    """Parse POST Filds into dict."""
    FieldList = [Field.split("=") for Field in RawPost.split("&")]

    try:
        FieldMap = {Q[0]: urllib.unquote(Q[1].replace("+", " ")).
                    decode('utf8') for Q in FieldList}

        return FieldMap
    except:
        return {}

def IsLogged(Redirect=True):
    """ Define secure (logged in only) area"""
    try:
        if Session.user_id:
            return True
        else:
            if Redirect:
                raise web.seeother('/login')
            else:
                return False

    except AttributeError:
        if Redirect:
            raise web.seeother('/login')
        else:
            return False

def CommitComment(Inst, Response):
    """Submit a comment to an instance"""
    if "trigger" in Response:
        if Response["trigger"] == "comment":
            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()

            Me = LocS.query(User).filter(User.id == Session.user_id).one()

            if "anonymous" not in Response:
                Response["anonymous"] = False

            if Inst.__class__ == Teacher:
                LocTeacher = LocS.query(Teacher).filter(
                    Teacher.id == Inst.id).one()

                NewComment = TeacherComment(
                    text=Response["text"],
                    teacher=LocTeacher,
                    user=Me,
                    anonymous=bool(Response["anonymous"]))

            if Inst.__class__ == Subject:
                LocSubject = LocS.query(Subject).filter(
                    Subject.id == Inst.id).one()

                NewComment = SubjectComment(
                    text=Response["text"],
                    subject=LocSubject,
                    user=Me,
                    anonymous=bool(Response["anonymous"]))

            if Inst.__class__ == Offering:
                LocOffering = LocS.query(Offering).filter(
                    Offering.id == Inst.id).one()

                NewComment = OfferingComment(
                    text=Response["text"],
                    offering=LocOffering,
                    user=Me,
                    anonymous=bool(Response["anonymous"]))

            try:
                LocS.add(NewComment)
                LocS.commit()
                return False

            except:
                LocS.rollback()
                return True
