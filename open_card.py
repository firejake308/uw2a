import aqt

def openBrowseLink(search, highlight=None):
    browser = aqt.dialogs.open("Browser", aqt.mw)
    query = '''{}'''.format(search)
    browser.form.searchEdit.lineEdit().setText(query)
    browser.onSearchActivated()
    if not highlight or not browser.editor:
        return
    # this might not highlight anymore
    browser.editor.web.findText(highlight)