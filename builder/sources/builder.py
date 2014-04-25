class AseBuilder:
    def __init__(self, config):
        self.config = config
        self._get_sections()
        self.logger = AseLog(config['mute'])

    def _get_sections(self):
        self.sections = {}
        questions_dir = self.config['questions_dir']
        for filename in os.listdir(questions_dir):
            with open(os.path.join(questions_dir, filename), 'r') as f:
                questions = self._parse_questions(f.read())
                self.sections[filename.replace('.md', '')] = questions

    def _parse_questions(self, text):
        lines = text.split('\n')
        questions = {}
        for line in lines:
            match = re.match(r'^\D{0,3}(\d+)\.\s(.*)$', line.strip())
            if (match):
                groups = match.groups()
                questions[int(groups[0])] =  {
                    'title':groups[1].strip()
                }
        return questions

    def _create_missing_answers(self):
        for section, questions in self.sections.iteritems():
            answers_dir = os.path.join(self.config['answers_dir'], \
                                       section)
            if not os.path.exists(answers_dir):
                os.makedirs(answers_dir) # if anything goes wrong, this will throw an exception
            for number, question in questions.iteritems():
                answer_filename = 'a%d.md' % number
                answer_file = os.path.join(answers_dir, answer_filename)
                if not os.path.exists(answer_file):
                    self.logger.put('missing_answer', answer_file)
                    with open(answer_file, 'w') as f:
                        data = {
                            'answer_number':number,
                            'answer_title':question['title']
                        }
                        answer = self.renderer.render('empty_answer', data)
                        f.write(answer)

    def build(self):
        self._create_missing_answers()
        sections = self._merge_answers()
