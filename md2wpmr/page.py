import os
import mkdocs
import md2wpmr.tools

from bs4 import BeautifulSoup

class Page(mkdocs.structure.pages.Page):
    
    def __init__(self, export, md_page):
        self.export = export
        self.md_page = md_page
        self.is_root_page = not self.md_page.parent # not in a section
        self.set_absolute_dirname()
        self.set_absolute_destination_path()
        self.prepare_content()
        
    def prepare_content_img(self):
        # set absolute path to internal img (all src ??)
        for img in self.html_soup.find_all('img'):
            if not img['src'].startswith('http'):
                img['src'] = os.path.realpath(self.absolute_dirname + img['src'])
    
    def prepare_content_id_and_link(self):
        # id
        for tag in self.html_soup.find_all(attrs={"id":True}):
            if not tag['id'].startswith('fc-pdf-'): # reserved
                tag['id'] = self.absolute_destination_path + '@' + tag['id']
                tag['id'] = md2wpmr.tools.hash_to_md5(tag['id'])
            # toc
            header_levels = []
            for level in range (1, self.export.toc_page_level_depth + 1):
                header_levels.append(f'h{level}')
            if tag.name in header_levels:
                self.export.html_toc += f'<tr class="level-{tag.name[-1]} {self.pdf_section_type}"><td> <a class="level-{tag.name[-1]}" href="#{tag["id"]}">{tag.text}</a></td></tr>'

        for link in self.html_soup.find_all('a'):
             # TODO add class external / internal
            href = link['href']
            if not md2wpmr.tools.is_external_link(href):
                if md2wpmr.tools.is_anchor_link(href):
                    # anchor 
                    href = self.absolute_destination_path + href.replace('#','@')
                    href = md2wpmr.tools.hash_to_md5(href)
                    link['href'] = '#' + href
                elif md2wpmr.tools.is_markdown_link(href):
                    # markdown
                    href = os.path.realpath(self.absolute_dirname + href)
                    href = href.replace('#','@')
                    href = md2wpmr.tools.hash_to_md5(href)
                    link['href'] = '#' + href
                else:
                    # TODO use the logger
                    print('WARNING - HTML Internal Link: ' + href)
                    # https://codereview.stackexchange.com/questions/31523/adding-a-new-class-to-html-tag-and-writing-it-back-with-beautiful-soup
                    link['class'] = link.get('class', []) + ['fc-pdf-error']
           
    def prepare_content(self):
        if self.is_root_page:
            self.pdf_section_type = 'introductory'
        else:
            self.pdf_section_type = 'chaptered'
        self.html_soup = BeautifulSoup(self.md_page.content, 'html.parser')
        self.md_page.content = None
        self.prepare_content_img()
        self.prepare_content_id_and_link()
        # print(self.html_soup)
        id = md2wpmr.tools.hash_to_md5(self.absolute_destination_path)
        self.content = f'<div class="fc-pdf-section {self.pdf_section_type}" id="{id}">' + str(self.html_soup) +  '</div>'

    def add_content(self):
        self.export.html_pages +=self.content

    def set_absolute_destination_path(self):
        join = os.path.join(self.export.md_docs_dir, self.md_page.file.dest_path)
        self.absolute_destination_path = os.path.realpath(join)
        print(self.absolute_destination_path)

    def set_absolute_dirname(self):
        join = os.path.join(self.export.md_docs_dir, self.md_page.file.src_path)
        real = os.path.realpath(join)
        self.absolute_dirname = os.path.dirname(real) + os.sep
        # print(self.md_page.file)
   