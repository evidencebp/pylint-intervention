from django.db import models
from django.db import connection
from django.db import connections
from django.utils import timezone

def prefetch_id(db, seq_name):
    """ Fetch the next value in a django id oracle sequence """
    cursor = connections[db].cursor()
    new_id = -1
    try:
        query = "SELECT %s.nextval FROM dual" % seq_name
        cursor.execute(query)
        rows = cursor.fetchall()
        new_id = rows[0][0]
    finally:
        if cursor:
            cursor.close()
    return new_id


class TRequest(models.Model):
    PHYS_GROUPS=[(x,x) for x in ['physics','Top','StandartModel','Exotrics','SUSY','Higgs','JetEtmiss','Tau','FlavourTag',
                                'Egamma','BPhys','TrackingPerf','HeavyIons','Muon']]
    REQUEST_TYPE = [(x,x) for x in ['MC','GROUP','REPROCESING','ANALYSIS']]
    reqid = models.DecimalField(decimal_places=0, max_digits=12, db_column='PR_ID', primary_key=True)
    manager = models.CharField(max_length=32, db_column='MANAGER', null=False, blank=True)
    description = models.CharField(max_length=256, db_column='DESCRIPTION', null=True, blank=True)
    ref_link = models.CharField(max_length=256, db_column='REFERENCE_LINK', null=True, blank=True)
    cstatus = models.CharField(max_length=32, db_column='STATUS', null=False, blank=True)
    provenance = models.CharField(max_length=32, db_column='PROVENANCE', null=False, blank=True)
    request_type = models.CharField(max_length=32, db_column='REQUEST_TYPE',choices=REQUEST_TYPE, null=False, blank=True)
    campaign = models.CharField(max_length=32, db_column='CAMPAIGN', null=False, blank=True)
    subcampaign = models.CharField(max_length=32, db_column='SUB_CAMPAIGN', null=False, blank=True)
    phys_group = models.CharField(max_length=20, db_column='PHYS_GROUP', null=False, choices=PHYS_GROUPS, blank=True)
    energy_gev = models.DecimalField(decimal_places=0, max_digits=8, db_column='ENERGY_GEV', null=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.reqid:
            self.reqid = prefetch_id('deft',u'ATLAS_DEFT.T_PRODMANAGER_REQUEST_ID_SEQ')

        super(TRequest, self).save(*args, **kwargs)

    class Meta:
        #db_table = u'T_PRODMANAGER_REQUEST'
        db_table = u'"ATLAS_DEFT"."T_PRODMANAGER_REQUEST"'


class RequestStatus(models.Model):
    STATUS_TYPES = (
                    ('Created', 'Created'),
                    ('Pending', 'Pending'),
                    ('Unknown', 'Unknown'),
                    ('Approved', 'Approved'),
                    )
    id =  models.DecimalField(decimal_places=0, max_digits=12, db_column='REQ_S_ID', primary_key=True)
    request = models.ForeignKey(TRequest, db_column='PR_ID')
    comment = models.CharField(max_length=256, db_column='COMMENT', null=True)
    owner = models.CharField(max_length=32, db_column='OWNER', null=False)
    status = models.CharField(max_length=32, db_column='STATUS', choices=STATUS_TYPES, null=False)
    timestamp = models.DateTimeField(db_column='TIMESTAMP', null=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_PRODMANAGER_REQ_STAT_ID_SEQ')

        super(TRequest, self).save(*args, **kwargs)

    class Meta:
        #db_table = u'T_PRODMANAGER_REQUEST_STATUS'
        db_table = u'"ATLAS_DEFT"."T_PRODMANAGER_REQUEST_STATUS"'

class StepTemplate(models.Model):
    id =  models.DecimalField(decimal_places=0, max_digits=12,  db_column='STEP_T_ID', primary_key=True)
    step = models.CharField(max_length=12, db_column='STEP_NAME', null=False)
    def_time = models.DateTimeField(db_column='DEF_TIME', null=False)
    status = models.CharField(max_length=12, db_column='STATUS', null=False)
    ctag = models.CharField(max_length=12, db_column='CTAG', null=False)
    priority = models.DecimalField(decimal_places=0, max_digits=5, db_column='PRIORITY', null=False)
    cpu_per_event = models.DecimalField(decimal_places=0, max_digits=7, db_column='CPU_PER_EVENT', null=True)
    output_formats = models.CharField(max_length=80, db_column='OUTPUT_FORMATS', null=True)
    memory = models.DecimalField(decimal_places=0, max_digits=5, db_column='MEMORY', null=True)
    trf_name = models.CharField(max_length=128, db_column='TRF_NAME', null=True)
    lparams = models.CharField(max_length=2000, db_column='LPARAMS', null=True)
    vparams = models.CharField(max_length=4000, db_column='VPARAMS', null=True)
    swrelease = models.CharField(max_length=80, db_column='SWRELEASE', null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_STEP_TEMPLATE_ID_SEQ')
        super(StepTemplate, self).save(*args, **kwargs)

    class Meta:
        #db_table = u'T_STEP_TEMPLATE'
        db_table = u'"ATLAS_DEFT"."T_STEP_TEMPLATE"'

class Ttrfconfig(models.Model):
    tag = models.CharField(max_length=1, db_column='TAG', default='-')
    cid = models.DecimalField(decimal_places=0, max_digits=5, db_column='CID', primary_key=True, default=0)
    trf = models.CharField(max_length=80, db_column='TRF', null=True, default='transformation')
    lparams = models.CharField(max_length=1024, db_column='LPARAMS', null=True, default='parameter list')
    vparams = models.CharField(max_length=4000, db_column='VPARAMS', null=True, default='')
    trfv = models.CharField(max_length=40, db_column='TRFV', null=True)
    status = models.CharField(max_length=12, db_column='STATUS', null=True)
    ami_flag = models.DecimalField(decimal_places=0, max_digits=10, db_column='AMI_FLAG', null=True)
    createdby = models.CharField(max_length=60, db_column='CREATEDBY', null=True)
    input = models.CharField(max_length=20, db_column='INPUT', null=True)
    step = models.CharField(max_length=12, db_column='STEP', null=True)
    formats = models.CharField(max_length=256, db_column='FORMATS', null=True)
    cache = models.CharField(max_length=32, db_column='CACHE', null=True)
    cpu_per_event = models.DecimalField(decimal_places=0, max_digits=5, db_column='CPU_PER_EVENT', null=True, default=1)
    memory = models.DecimalField(decimal_places=0, max_digits=5, db_column='MEMORY', default=1000)
    priority = models.DecimalField(decimal_places=0, max_digits=5, db_column='PRIORITY', default=100)
    events_per_job = models.DecimalField(decimal_places=0, max_digits=10, db_column='EVENTS_PER_JOB', default=1000)


    class Meta:
        app_label = 'panda'
        db_table = u'T_TRF_CONFIG'


class ProductionDataset(models.Model):
    name = models.CharField(max_length=150, db_column='NAME', primary_key=True)
    #task = models.ForeignKey(ProducitonTask,db_column='TASK_ID')
    task_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='TASKID', null=True)
    #parent_task = models.ForeignKey(ProducitonTask,db_column='TASK_ID')
    parent_task_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='PARENT_TID', null=True)
    rid = models.DecimalField(decimal_places=0, max_digits=12, db_column='PR_ID', null=True)
    phys_group = models.CharField(max_length=20, db_column='PHYS_GROUP', null=True)
    events = models.DecimalField(decimal_places=0, max_digits=7, db_column='EVENTS', null=True)
    files = models.DecimalField(decimal_places=0, max_digits=7, db_column='FILES', null=False)
    status = models.CharField(max_length=12, db_column='STATUS', null=True)
    timestamp = models.DateTimeField(db_column='TIMESTAMP', null=False)



    class Meta:
        #db_table = u'T_PRODUCTION_DATASET'
        db_table = u'"ATLAS_DEFT"."T_PRODUCTION_DATASET"'

class InputRequestList(models.Model):
    id = models.DecimalField(decimal_places=0, max_digits=12, db_column='IND_ID', primary_key=True)
    dataset = models.ForeignKey(ProductionDataset, db_column='INPUTDATASET',null=True)
    request = models.ForeignKey(TRequest, db_column='PR_ID')
    slice = models.DecimalField(decimal_places=0, max_digits=12, db_column='SLICE', null=False)
    brief = models.CharField(max_length=150, db_column='BRIEF')
    phys_comment = models.CharField(max_length=256, db_column='PHYSCOMMENT')
    comment = models.CharField(max_length=256, db_column='SLICECOMMENT')
    input_data = models.CharField(max_length=150, db_column='INPUTDATA')
    project_mode = models.CharField(max_length=256, db_column='PROJECT_MODE')
    priority = models.DecimalField(decimal_places=0, max_digits=12, db_column='PRIORITY')
    input_events = models.DecimalField(decimal_places=0, max_digits=12, db_column='INPUT_EVENTS')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_INPUT_DATASET_ID_SEQ')
        super(InputRequestList, self).save(*args, **kwargs)

    class Meta:
        #db_table = u'T_INPUT_DATASET'
        db_table = u'"ATLAS_DEFT"."T_INPUT_DATASET"'

class StepExecution(models.Model):
    STEPS = ['Evgen',
             'Simul',
             'Merge',
             'Digi',
             'Reco',
             'Rec Merge',
             'Rec TAG',
             'Atlfast',
             'Atlf Merge',
             'Atlf TAG']
    STEPS_STATUS = ['NotChecked','NotCheckedSkipped','Skipped','Approved']
    id =  models.DecimalField(decimal_places=0, max_digits=12, db_column='STEP_ID', primary_key=True)
    request = models.ForeignKey(TRequest, db_column='PR_ID')
    step_template = models.ForeignKey(StepTemplate, db_column='STEP_T_ID')
    status = models.CharField(max_length=12, db_column='STATUS', null=False)
    slice = models.ForeignKey(InputRequestList, db_column='IND_ID', null=False)
    priority = models.DecimalField(decimal_places=0, max_digits=5, db_column='PRIORITY', null=False)
    step_def_time = models.DateTimeField(db_column='STEP_DEF_TIME', null=False)
    step_appr_time = models.DateTimeField(db_column='STEP_APPR_TIME', null=True)
    step_exe_time = models.DateTimeField(db_column='STEP_EXE_TIME', null=True)
    step_done_time = models.DateTimeField(db_column='STEP_DONE_TIME', null=True)
    input_events = models.DecimalField(decimal_places=0, max_digits=8, db_column='INPUT_EVENTS', null=True)

    def save_with_current_time(self, *args, **kwargs):
        if not self.step_def_time:
            self.step_def_time = timezone.now()
        self.save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_PRODUCTION_STEP_ID_SEQ')
        super(StepExecution, self).save(*args, **kwargs)

    class Meta:
        #db_table = u'T_PRODUCTION_STEP'
        db_table = u'"ATLAS_DEFT"."T_PRODUCTION_STEP"'

class ProductionTask(models.Model):
    id = models.DecimalField(decimal_places=0, max_digits=12, db_column='TASKID', primary_key=True)
    step = models.ForeignKey(StepExecution, db_column='STEP_ID')
    request = models.ForeignKey(TRequest, db_column='PR_ID')
    parent_id = models.DecimalField(decimal_places=0, max_digits=12, db_column='PARENT_TID', null=False)
    chain_tid = models.DecimalField(decimal_places=0, max_digits=12, db_column='CHAIN_TID', null=False)
    name = models.CharField(max_length=130, db_column='TASKNAME', null=True)
    project = models.CharField(max_length=60, db_column='PROJECT', null=True)
    username = models.CharField(max_length=128, db_column='USERNAME', null=True)
    dsn = models.CharField(max_length=12, db_column='DSN', null=True)
    phys_short = models.CharField(max_length=80, db_column='PHYS_SHORT', null=True)
    simulation_type = models.CharField(max_length=20, db_column='SIMULATION_TYPE', null=True)
    phys_group = models.CharField(max_length=20, db_column='PHYS_GROUP', null=True)
    provenance = models.CharField(max_length=12, db_column='PROVENANCE', null=True)
    status = models.CharField(max_length=12, db_column='STATUS', null=True)
    total_events = models.DecimalField(decimal_places=0, max_digits=10, db_column='TOTAL_EVENTS', null=True)
    total_req_jobs = models.DecimalField(decimal_places=0, max_digits=10, db_column='TOTAL_REQ_JOBS', null=True)
    total_done_jobs = models.DecimalField(decimal_places=0, max_digits=10, db_column='TOTAL_DONE_JOBS', null=True)
    submit_time = models.DateTimeField(db_column='SUBMIT_TIME', null=False)
    start_time = models.DateTimeField(db_column='START_TIME', null=True)
    timestamp = models.DateTimeField(db_column='TIMESTAMP', null=True)
    bug_report = models.DecimalField(decimal_places=0, max_digits=12, db_column='BUG_REPORT', null=False)
    pptimestamp = models.DateTimeField(db_column='PPTIMESTAMP', null=True)
    postproduction = models.CharField(max_length=128, db_column='POSTPRODUCTION', null=True)
    priority = models.DecimalField(decimal_places=0, max_digits=5, db_column='PRIORITY', null=True)
    update_time = models.DateTimeField(db_column='UPDATE_TIME', null=True)
    update_owner = models.CharField(max_length=24, db_column='UPDATE_OWNER', null=True)
    comments = models.CharField(max_length=256, db_column='COMMENTS', null=True)
    inputdataset = models.CharField(max_length=150, db_column='INPUTDATASET', null=True)
    physics_tag = models.CharField(max_length=20, db_column='PHYSICS_TAG', null=True)

    def save(self):
        if self.id == None:
            self.id = self.getId()
        super(ProductionTask, self).save()

    def getId(self):
        cursor = connection.cursor()
        try:
            query = "SELECT %s.nextval FROM dual" % 'ATLAS_DEFT.T_PRODUCTION_TASK_ID_SEQ'
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows[0][0]
        finally:
            if cursor:
                cursor.close()

    class Meta:
        #db_table = u'T_PRODUCTION_STEP'
        db_table = u'"ATLAS_DEFT"."T_PRODUCTION_TASK"'


class MCPattern(models.Model):
    STEPS = ['Evgen',
             'Simul',
             'Merge',
             'Digi',
             'Reco',
             'Rec Merge',
             'Rec TAG',
             'Atlfast',
             'Atlf Merge',
             'Atlf TAG']
    STATUS = [(x,x) for x in ['IN USE','Obsolete']]
    id =  models.DecimalField(decimal_places=0, max_digits=12, db_column='MCP_ID', primary_key=True)
    pattern_name =  models.CharField(max_length=150, db_column='PATTERN_NAME', unique=True)
    pattern_dict = models.CharField(max_length=2000, db_column='PATTERN_DICT')
    pattern_status = models.CharField(max_length=20, db_column='PATTERN_STATUS', choices=STATUS)

    def save_with_current_time(self, *args, **kwargs):
        if not self.step_def_time:
            self.step_def_time = timezone.now()
        self.save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_PRODUCTION_MCP_ID_SEQ')
        super(MCPattern, self).save(*args, **kwargs)

    class Meta:
        db_table = u'"ATLAS_DEFT"."T_PRODUCTION_MC_PATTERN"'


class MCPriority(models.Model):
    STEPS = MCPattern.STEPS;
    id = models.DecimalField(decimal_places=0, max_digits=12, db_column='MCPRIOR_ID', primary_key=True)
    priority_key = models.DecimalField(decimal_places=0, max_digits=12, db_column='PRIORITY_KEY', unique=True)
    priority_dict = models.CharField(max_length=2000, db_column='PRIORITY_DICT')

    def save_with_current_time(self, *args, **kwargs):
        if not self.step_def_time:
            self.step_def_time = timezone.now()
        self.save(*args, **kwargs)



    def save(self, *args, **kwargs):
        if not self.id:
            self.id = prefetch_id('deft',u'ATLAS_DEFT.T_PRODUCTION_MCPRIOR_ID_SEQ')
        super(MCPriority, self).save(*args, **kwargs)

    class Meta:
        db_table = u'"ATLAS_DEFT"."T_PRODUCTION_MC_PRIORITY"'