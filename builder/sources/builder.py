# coding=utf-8

import codecs
from os import path, makedirs, listdir
from markdown import markdown
from log import AseLog
from parser import AseParser
from assetizer import AseAssetizer
from renderer import AseRenderer
from dictionary import AseDictionary

class AseBuilder:
    def __init__(self, config):
        self.config = config
        self.logger = AseLog(config['mute'])
        self.assetizer = AseAssetizer(config['assets_dir'], config['assets'])
        self.parser = AseParser()
        self.dict = AseDictionary()
        self.renderer = AseRenderer(config['template_dir'], '.tpl', self.dict)

    def _get_sections(self):
        self.dict['sections'] = {}
        questions_dir = self.config['questions_dir']
        for filename in listdir(questions_dir):
            with open(path.join(questions_dir, filename), 'r') as f:
                section = self.parser.parse_question_section(f.read())
                self.dict['sections'][filename.replace('.md', '')] = section

    def _create_missing_answers(self):
        for name, section in self.dict['sections'].iteritems():
            answers_dir = path.join(self.config['answers_dir'], name)
            if not path.exists(answers_dir):
                makedirs(answers_dir) # if anything goes wrong, this will throw an exception
            for number, question in section['questions'].iteritems():
                answer_filename = 'a%d.md' % number
                answer_file = path.join(answers_dir, answer_filename)
                if not path.exists(answer_file):
                    self.logger.put('missing_answer', answer_file)
                    with open(answer_file, 'w') as f:
                        data = {
                            'answer_number':number,
                            'answer_title':question['title'],
                            'answer_text':'Здесь ничего нет, вообще ничего', #todo
                            'questions_path':'../../questions/%s.md' % name #todo
                        }
                        answer = self.renderer.render('empty_answer.md', data)
                        f.write(answer)
                with open(answer_file, 'r') as f: #todo double file access
                    answer = self.parser.parse_answer(f.read())
                    if answer is not None:
                        question['answer'] = answer['text']
                    else:
                        print self.logger.log('faulty_answer', answer_file)

    def _prepare(self):
        self._get_sections()
        self._create_missing_answers()
        self.assetizer.install_assets()
        with open(self.config['definitions_file'], 'r') as f:
            self.dict['definitions'] = self.parser.parse_definitions(f.read())

    def _merge_answers(self):
        for name, section in self.dict['sections'].iteritems():
            answers = []
            for number, question in section['questions'].iteritems():
                text = markdown(codecs.decode(question['answer'], 'utf-8'))
                answers.append(self.renderer.render('answer.html', {
                    'answer_number':number,
                    'answer_title':question['title'],
                    'answer_content':text
                }))
            filename = path.join(self.config['html_dir'], name + '.html')
            compiled = self.renderer.render('composite.html', {
                'answers':codecs.encode('\n'.join(answers), 'utf-8')
            })
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(compiled)

    def build(self):
        self._prepare()
        sections = self._merge_answers()
        #for name, answers in sections.iteritems():
        #    filename = name + '.md'
