import sublime
import sublime_plugin


class BookmarksShowAllCommand(sublime_plugin.TextCommand):
    def on_done(self, index):
        if index == -1:  # no selection made
            self.view.set_viewport_position(self.startpos)  # restore scroll position
        else:
            s = self.view.sel()
            s.clear()
            s.add(self.linenums[index])  # replace all cursors with highlight of bookmarked region

    def on_highlight(self, index):
        self.view.show(self.linenums[index])  # scroll bookmarked region into view

    def run(self, edit):
        self.startpos = self.view.viewport_position()

        self.linenums = []
        l = []
        for region in self.view.get_regions("bookmarks"):
            self.linenums.append(region)   # only the selection used to toggle the bookmark
            line = self.view.line(region)  # gets the whole line
            l.append(
                str(self.view.rowcol(line.begin())[0]+1) + ': ' + self.view.substr(line)[:100]
            )

        self.view.window().show_quick_panel(l, self.on_done, on_highlight=self.on_highlight)
