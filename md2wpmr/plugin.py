import mkdocs
import sys
import os
import shutil

from md2wpmr.page import Page
from md2wpmr.section import Section

# from bs4 import BeautifulSoup

class Export(mkdocs.plugins.BasePlugin):

    # https://www.mkdocs.org/dev-guide/plugins/#config_scheme
    config_scheme = (
        ('number_column', mkdocs.config.config_options.Type(int)),
        ('number_row_pages', mkdocs.config.config_options.Type(int)),
        ('number_row_toc', mkdocs.config.config_options.Type(int))
    )

    # https://www.mkdocs.org/dev-guide/plugins/#on_config
    def on_config(self, config):
        if (sys.argv[1] == 'build'):
            self.export = True
            # https://www.mkdocs.org/user-guide/configuration/#use_directory_urls
            # relative image path = relative .md
            config['use_directory_urls'] = False 
            self.md_config = config
            self.md_docs_dir = self.md_config['docs_dir'] + os.sep
            self.path_mkdocs = os.path.abspath(self.md_docs_dir + '..' + os.sep) + os.sep
            self.path_matrix_mkdocs_column = self.path_mkdocs + 'matrix' + os.sep + str(self.config['number_column']) + "-mkdocs" + os.sep
            self.path_matrix_mkdocs_cell_toc = self.path_matrix_mkdocs_column + str(self.config['number_row_toc']) + "-mkdocs-toc" + os.sep
            self.path_matrix_mkdocs_cell_pages = self.path_matrix_mkdocs_column + str(self.config['number_row_pages']) + "-mkdocs-pages" + os.sep
            shutil.rmtree(self.path_matrix_mkdocs_column, ignore_errors = True)
            os.mkdir(self.path_matrix_mkdocs_column)
            os.mkdir(self.path_matrix_mkdocs_cell_toc)
            os.mkdir(self.path_matrix_mkdocs_cell_pages)
        else:
            self.export = False
        # print(self.config)
        # print(self.path_cell_pages)

    # https://www.mkdocs.org/dev-guide/plugins/#on_nav
    def on_nav(self, nav, config, files):
        if not self.export:
            return
        # print('on_nav')
        # PDF => only files from nav 
        for file in files.documentation_pages():
            files.remove(file)
        for page in nav.pages:
            # don't use navigation title but page title
            page.title = None
            files.append(page.file)
        self.md_nav = nav
        return nav

    # https://www.mkdocs.org/dev-guide/plugins/#on_page_content
    def on_page_content(self, html, page, config, files):
        if not self.export:
            return
        # print('on_page_content')
        # export if last page
        if page == self.md_nav.pages[-1]:
            self.do()
        return

    def do(self):
        self.html_pages = '<div id="fc-pdf-content">'
        self.html_toc = '<div id="fc-pdf-toc"><table><thead><tr><th></th></tr></thead>'
        self.number_chapter = 1
        for md_nav_object in self.md_nav:
            if md_nav_object.is_page:
                Page(self, md_nav_object).add_content()
            elif md_nav_object.is_section:
                Section(self, md_nav_object).add_content()
        self.html_pages += '</div>'
        self.html_toc += '</table></div>'
        with open(f'{self.path_matrix_mkdocs_cell_pages}content.html', 'w',  encoding='utf8') as file:
            file.write(self.html_pages)
        file.close()
        with open(f'{self.path_matrix_mkdocs_cell_toc}content.html', 'w',  encoding='utf8') as file:
            file.write(self.html_toc)
        file.close()
        exit()

