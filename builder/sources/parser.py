import re

class AseParser:
    answer_pattern = re.compile(r'####\s*(?:<a name="[\w-]+"></a>)*\s*' + \
                                r'(\d+)\.\s*([^\r\n]+)\s*(?:\[.*\]\(.*\))?' + \
                                r'\s*(.*)\s*',
                                re.MULTILINE | re.DOTALL)
    answer_title_pattern = re.compile(r'(\d+)\.\s*(.*)') # UTF-BOM protection
    definitions_pattern = re.compile(r'^\s*((?:<a name="[\w-]+"></a>\s*)+)(.*?)(?=(?:\r?\n\<a|\#|\Z))',
                                     re.MULTILINE | re.DOTALL)
    definitions_tags_pattern = re.compile(r'(?<=\<a name=")([\w-]+)(?="></a>)')
    def parse_answer(self, answer_text):
        match = self.answer_pattern.match(answer_text)
        if match is not None:
            groups = match.groups()
            return {
                'title':groups[1].strip(),
                'number':int(groups[0]),
                'text':groups[2].strip()
            }

    def parse_question_section(self, section_text):
        """hax hax"""
        section = {'questions':{}}
        lines = section_text.split('\n')
        i = 0
        while i < len(lines) and len(lines[i]) > 0 and \
                not lines[i][0].isspace() and lines[i][0] not in ('-', '='):
            i = i + 1
        section['title'] = '\n'.join(lines[:i]).lstrip('# ')
        for match in self.answer_title_pattern.finditer(section_text):
            groups = match.groups()
            section['questions'][int(groups[0])] = {'title':groups[1]}
        return section
    
    def parse_definitions(self, text):
        definitions = []
        for match in self.definitions_pattern.finditer(text):
            groups = match.groups()
            tags = self.definitions_tags_pattern.findall(groups[0])
            if not tags:
                print "Parse error for following text: " + match.group(0)
            else:
                definitions.append({'tags':tags, 'text':match.group(2).strip()})
        return definitions
