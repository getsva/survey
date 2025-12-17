from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from .models import Question, QuestionOption, SurveyResponse, SurveyAnswer


class QuestionResource(resources.ModelResource):
    """Resource for exporting Questions with their options"""
    
    class Meta:
        model = Question
        fields = ('id', 'category', 'prompt', 'target_audience', 'note', 'is_active', 'created_at', 'updated_at')
        export_order = ('id', 'category', 'prompt', 'target_audience', 'note', 'is_active', 'created_at', 'updated_at')


class SurveyResponseResource(resources.ModelResource):
    """Resource for exporting Survey Responses with basic information"""
    
    respondent_name = fields.Field(attribute='respondent_name', column_name='Respondent Name')
    respondent_email = fields.Field(attribute='respondent_email', column_name='Respondent Email')
    respondent_role = fields.Field(attribute='get_respondent_role_display', column_name='Respondent Role')
    created_at = fields.Field(attribute='created_at', column_name='Response Date')
    updated_at = fields.Field(attribute='updated_at', column_name='Last Updated')
    
    class Meta:
        model = SurveyResponse
        fields = ('id', 'respondent_name', 'respondent_email', 'respondent_role', 'created_at', 'updated_at')
        export_order = ('id', 'respondent_name', 'respondent_email', 'respondent_role', 'created_at', 'updated_at')


class SurveyAnswerResource(resources.ModelResource):
    """Resource for exporting individual Survey Answers"""
    
    response_id = fields.Field(attribute='response_id', column_name='Response ID')
    respondent_name = fields.Field(attribute='response__respondent_name', column_name='Respondent Name')
    respondent_email = fields.Field(attribute='response__respondent_email', column_name='Respondent Email')
    question_id = fields.Field(attribute='question_id', column_name='Question ID')
    question_category = fields.Field(attribute='question__category', column_name='Question Category')
    question_prompt = fields.Field(attribute='question__prompt', column_name='Question')
    answer_text = fields.Field(attribute='answer_text', column_name='Answer')
    created_at = fields.Field(attribute='created_at', column_name='Answered At')
    
    class Meta:
        model = SurveyAnswer
        fields = ('response_id', 'respondent_name', 'respondent_email', 'question_id', 
                 'question_category', 'question_prompt', 'answer_text', 'created_at')
        export_order = ('response_id', 'respondent_name', 'respondent_email', 'question_id', 
                       'question_category', 'question_prompt', 'answer_text', 'created_at')


class SurveyResponseDetailedResource(resources.ModelResource):
    """
    Resource for exporting Survey Responses in a wide format where each question becomes a column.
    This creates a flattened view where each row is a response and columns are questions.
    """
    
    respondent_name = fields.Field(column_name='Respondent Name')
    respondent_email = fields.Field(column_name='Respondent Email')
    respondent_role = fields.Field(column_name='Respondent Role')
    response_date = fields.Field(column_name='Response Date')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically add question fields
        questions = Question.objects.filter(is_active=True).order_by('id')
        for question in questions:
            field_name = f'q{question.id}'
            # Truncate long prompts for column headers
            prompt_short = question.prompt[:60] + '...' if len(question.prompt) > 60 else question.prompt
            column_name = f'Q{question.id}: {prompt_short}'
            setattr(self, field_name, fields.Field(column_name=column_name, readonly=True))
    
    def dehydrate_respondent_name(self, response):
        return response.respondent_name or 'Anonymous'
    
    def dehydrate_respondent_email(self, response):
        return response.respondent_email or ''
    
    def dehydrate_respondent_role(self, response):
        return response.get_respondent_role_display()
    
    def dehydrate_response_date(self, response):
        return response.created_at.strftime('%Y-%m-%d %H:%M:%S') if response.created_at else ''
    
    def get_queryset(self):
        """Prefetch related answers for efficiency"""
        return super().get_queryset().prefetch_related('answers__question')
    
    def get_export_headers(self):
        """Get headers for export, including dynamic question columns"""
        headers = ['ID', 'Respondent Name', 'Respondent Email', 'Respondent Role', 'Response Date']
        questions = Question.objects.filter(is_active=True).order_by('id')
        for question in questions:
            prompt_short = question.prompt[:60] + '...' if len(question.prompt) > 60 else question.prompt
            column_name = f'Q{question.id}: {prompt_short}'
            headers.append(column_name)
        return headers
    
    def export(self, queryset=None, *args, **kwargs):
        """Override export to populate question columns dynamically"""
        if queryset is None:
            queryset = self.get_queryset()
        
        # Get all active questions ordered by ID
        questions = list(Question.objects.filter(is_active=True).order_by('id'))
        question_ids = [q.id for q in questions]
        
        # Prefetch answers for efficiency
        queryset = queryset.prefetch_related('answers__question')
        
        # Build the dataset manually
        rows = []
        headers = ['ID', 'Respondent Name', 'Respondent Email', 'Respondent Role', 'Response Date']
        
        # Add question headers
        for question in questions:
            prompt_short = question.prompt[:60] + '...' if len(question.prompt) > 60 else question.prompt
            headers.append(f'Q{question.id}: {prompt_short}')
        
        # Build rows
        for response in queryset:
            row = [
                response.id,
                response.respondent_name or 'Anonymous',
                response.respondent_email or '',
                response.get_respondent_role_display(),
                response.created_at.strftime('%Y-%m-%d %H:%M:%S') if response.created_at else '',
            ]
            
            # Create a dictionary of question_id -> answer_text for quick lookup
            answers_dict = {answer.question_id: answer.answer_text for answer in response.answers.all()}
            
            # Add answer for each question
            for qid in question_ids:
                row.append(answers_dict.get(qid, ''))
            
            rows.append(row)
        
        # Return as tablib Dataset
        try:
            import tablib
            data = tablib.Dataset(*rows, headers=headers)
        except ImportError:
            # Fallback: django-import-export should have tablib as dependency
            from import_export import tablib
            data = tablib.Dataset(*rows, headers=headers)
        
        return data
    
    class Meta:
        model = SurveyResponse
        fields = ('id', 'respondent_name', 'respondent_email', 'respondent_role', 'created_at')
        export_order = ('id', 'respondent_name', 'respondent_email', 'respondent_role', 'created_at')

