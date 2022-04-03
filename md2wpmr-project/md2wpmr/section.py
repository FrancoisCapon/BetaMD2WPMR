import mkdocs
import md2wpmr.tools

from md2wpmr.page import Page

class Section(mkdocs.structure.nav.Section):
    def __init__(self, export, md_section):
        self.md_section = md_section
        self.export = export
    
    def add_content(self):
        id = "fc-pdf-chapter-" + str(self.export.number_chapter)
        id = md2wpmr.tools.hash_to_md5(id)
        self.export.number_chapter += 1
        self.export.html_pages += '<div class="fc-pdf-chapter">'
        self.export.html_pages += f'<h1 id="{id}">' + self.md_section.title + '</h1>'
        self.export.html_toc += f'<tr class="level-0"><td><a class="level-0" href="#{id}">{self.md_section.title}</a></td></tr>'
        for md_nav_object in self.md_section.children:
            if md_nav_object.is_page:
               Page(self.export, md_nav_object).add_content()
        self.export.html_pages += '</div>'
