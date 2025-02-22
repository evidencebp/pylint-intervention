# Upload changed_alerts.csv to BigQuery

# Extract relevant commits to improve running time later

create table
general.changed_alerts_commits
as
select
distinct ec.*
from
 general.changed_alerts as ca
 join
general.commits_files as cf
on
ca.repo_name = cf.repo_name
and
ca.path = cf.file
join
general.enhanced_commits as ec
on
cf.repo_name = ec.repo_name
and
cf.commit = ec.commit
;

# Extract commit files (for files without the alert but in the commit)

create table
general.changed_alerts_commit_files
as
select
distinct cf.*
from
 general.changed_alerts_commits as cac
 join
general.commits_files as cf
on
cac.repo_name = cf.repo_name
and
cac.commit = cf.commit
;

# NOTE - Set anchor_date to proper value
DECLARE anchor_date DATE DEFAULT PARSE_DATE('%d/%m/%Y',  '1/8/2022');
DECLARE period_date DATE DEFAULT DATE_ADD(anchor_date, INTERVAL 3 month) ;

SELECT anchor_date, period_date;


drop table if exists general.file_properties_after_change;


create table
general.file_properties_after_change
as
select
cf.repo_name as repo_name
, file
, min(cf.commit_timestamp) as min_commit_time
, max(cf.commit_timestamp) as max_commit_time
, min(cf.commit) as min_commit
, max(extension) as extension
, max(code_extension) as code_extension
, max(is_test) as is_test
, count(distinct cf.commit) as commits
, count(distinct if(parents = 1, cf.commit, null)) as non_merge_commits
, count(distinct case when cf.is_corrective  then cf.commit else null end) as corrective_commits
, 1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit) as corrective_rate
, general.bq_ccp_mle(1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit)) as ccp
, general.bq_refactor_mle(1.0*count(distinct case when cf.is_refactor  then cf.commit else null end)/count(distinct cf.commit))
        as refactor_mle
, avg(if(not cf.is_corrective, non_test_files, null)) as avg_coupling_size
, avg(if(not cf.is_corrective, code_non_test_files, null)) as avg_coupling_code_size
, avg(if(not cf.is_corrective, if(non_test_files > 103 , 103 , non_test_files), null)) as avg_coupling_size_capped
, avg(if(not cf.is_corrective, if(code_non_test_files> 103 , 103 ,code_non_test_files), null)) as avg_coupling_code_size_capped
, avg(if(not cf.is_corrective, if(non_test_files > 103 , null , non_test_files), null)) as avg_coupling_size_cut
, avg(if(not cf.is_corrective, if(code_non_test_files> 10 , null ,code_non_test_files), null)) as avg_coupling_code_size_cut

, if(sum(if(files <= 103, files, null)) > 0
    , sum(if(files <= 103, files - non_test_files, null))/ sum(if(files <= 103, files, null))
    , null) as test_file_ratio_cut
, if(sum(if(code_files <= 103, code_files, null)) > 0
    , sum(if(code_files <= 103, code_files - code_non_test_files, null))/ sum(if(code_files <= 103, code_files, null))
    , null) as test_code_file_ratio_cut


, count(distinct cf.Author_email) as authors
, max(cf.Author_email) as Author_email # Meaningful only when authors=1
, min(ec.commit_month) as commit_month
, avg(if(same_date_as_prev, duration, null)) as same_day_duration_avg

, 0.0 as prev_touch_ago
, 0.0 as bug_prev_touch_ago

# Abstraction
, if (sum(if(ec.is_corrective, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_corrective, 1,0 ))/sum(if(ec.is_corrective, 1,0 ))
, null)
as one_file_fix_rate
, if (sum(if(ec.is_refactor, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
, null)
as one_file_refactor_rate

, if(sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 )) > 0
    , 1.0*sum(if(code_files=1, 1,0 ))/sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 ))
    , null)
as test_usage_rate

, if(sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 )) > 0
    , 1.0*sum(if(ec.is_refactor and code_files=1, 1,0 ))
        /sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 ))
    , null)
as test_usage_in_refactor_rate

, if(sum(if(ec.is_refactor, 1,0 )) > 0
    , 1.0*sum(if( code_non_test_files = code_files and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
    , null )
as no_test_refactor_rate
, sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0)) as textual_abstraction_commits
, 1.0*sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0))/count(*) as textual_abstraction_commits_rate

, avg(cast(ec.is_typo as int64)) as typo_rate

, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) > 1,1,0))/count(distinct ec.commit) as tangling_rate
, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) = 3,1,0))/count(distinct ec.commit) as bingo_rate


, -1.0 as testing_involved_prob
, -1.0 as corrective_testing_involved_prob
, -1.0 as refactor_testing_involved_prob
, null as abs_content_ratio # We have data only in head, not per year

, count(distinct if(is_performance, ec.commit, null))/count(distinct ec.commit) as performance_rate
, count(distinct if(is_security, ec.commit, null))/count(distinct ec.commit) as security_rate

from
general.changed_alerts_commit_files as cf
join
general.changed_alerts_commits as ec
on
cf.commit = ec.commit and cf.repo_name = ec.repo_name
where
date(ec.commit_timestamp) > anchor_date
#and date(ec.commit_timestamp) <= period_date
group by
repo_name
, file
;

DECLARE anchor_date DATE DEFAULT PARSE_DATE('%d/%m/%Y',  '1/8/2022');
DECLARE period_date DATE DEFAULT DATE_ADD(anchor_date, INTERVAL 3 month) ;

SELECT anchor_date, period_date;


drop table if exists general.file_properties_after_change_3m;


create table
general.file_properties_after_change_3m
as
select
cf.repo_name as repo_name
, file
, min(cf.commit_timestamp) as min_commit_time
, max(cf.commit_timestamp) as max_commit_time
, min(cf.commit) as min_commit
, max(extension) as extension
, max(code_extension) as code_extension
, max(is_test) as is_test
, count(distinct cf.commit) as commits
, count(distinct if(parents = 1, cf.commit, null)) as non_merge_commits
, count(distinct case when cf.is_corrective  then cf.commit else null end) as corrective_commits
, 1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit) as corrective_rate
, general.bq_ccp_mle(1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit)) as ccp
, general.bq_refactor_mle(1.0*count(distinct case when cf.is_refactor  then cf.commit else null end)/count(distinct cf.commit))
        as refactor_mle
, avg(if(not cf.is_corrective, non_test_files, null)) as avg_coupling_size
, avg(if(not cf.is_corrective, code_non_test_files, null)) as avg_coupling_code_size
, avg(if(not cf.is_corrective, if(non_test_files > 103 , 103 , non_test_files), null)) as avg_coupling_size_capped
, avg(if(not cf.is_corrective, if(code_non_test_files> 103 , 103 ,code_non_test_files), null)) as avg_coupling_code_size_capped
, avg(if(not cf.is_corrective, if(non_test_files > 103 , null , non_test_files), null)) as avg_coupling_size_cut
, avg(if(not cf.is_corrective, if(code_non_test_files> 10 , null ,code_non_test_files), null)) as avg_coupling_code_size_cut

, if(sum(if(files <= 103, files, null)) > 0
    , sum(if(files <= 103, files - non_test_files, null))/ sum(if(files <= 103, files, null))
    , null) as test_file_ratio_cut
, if(sum(if(code_files <= 103, code_files, null)) > 0
    , sum(if(code_files <= 103, code_files - code_non_test_files, null))/ sum(if(code_files <= 103, code_files, null))
    , null) as test_code_file_ratio_cut


, count(distinct cf.Author_email) as authors
, max(cf.Author_email) as Author_email # Meaningful only when authors=1
, min(ec.commit_month) as commit_month
, avg(if(same_date_as_prev, duration, null)) as same_day_duration_avg

, 0.0 as prev_touch_ago
, 0.0 as bug_prev_touch_ago

# Abstraction
, if (sum(if(ec.is_corrective, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_corrective, 1,0 ))/sum(if(ec.is_corrective, 1,0 ))
, null)
as one_file_fix_rate
, if (sum(if(ec.is_refactor, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
, null)
as one_file_refactor_rate

, if(sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 )) > 0
    , 1.0*sum(if(code_files=1, 1,0 ))/sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 ))
    , null)
as test_usage_rate

, if(sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 )) > 0
    , 1.0*sum(if(ec.is_refactor and code_files=1, 1,0 ))
        /sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 ))
    , null)
as test_usage_in_refactor_rate

, if(sum(if(ec.is_refactor, 1,0 )) > 0
    , 1.0*sum(if( code_non_test_files = code_files and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
    , null )
as no_test_refactor_rate
, sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0)) as textual_abstraction_commits
, 1.0*sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0))/count(*) as textual_abstraction_commits_rate

, avg(cast(ec.is_typo as int64)) as typo_rate

, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) > 1,1,0))/count(distinct ec.commit) as tangling_rate
, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) = 3,1,0))/count(distinct ec.commit) as bingo_rate


, -1.0 as testing_involved_prob
, -1.0 as corrective_testing_involved_prob
, -1.0 as refactor_testing_involved_prob
, null as abs_content_ratio # We have data only in head, not per year

, count(distinct if(is_performance, ec.commit, null))/count(distinct ec.commit) as performance_rate
, count(distinct if(is_security, ec.commit, null))/count(distinct ec.commit) as security_rate

from
general.changed_alerts_commit_files as cf
join
general.changed_alerts_commits as ec
on
cf.commit = ec.commit and cf.repo_name = ec.repo_name
where
date(ec.commit_timestamp) > anchor_date
and date(ec.commit_timestamp) <= period_date
group by
repo_name
, file
;



# NOTE - Set anchor_date to proper value
DECLARE anchor_date DATE DEFAULT PARSE_DATE('%d/%m/%Y',  '1/2/2022');
DECLARE period_date DATE DEFAULT DATE_ADD(anchor_date, INTERVAL 3 month) ;

SELECT anchor_date, period_date;


drop table if exists general.file_properties_before_change;


create table
general.file_properties_before_change
as
select
cf.repo_name as repo_name
, file
, min(cf.commit_timestamp) as min_commit_time
, max(cf.commit_timestamp) as max_commit_time
, min(cf.commit) as min_commit
, max(extension) as extension
, max(code_extension) as code_extension
, max(is_test) as is_test
, count(distinct cf.commit) as commits
, count(distinct if(parents = 1, cf.commit, null)) as non_merge_commits
, count(distinct case when cf.is_corrective  then cf.commit else null end) as corrective_commits
, 1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit) as corrective_rate
, general.bq_ccp_mle(1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit)) as ccp
, general.bq_refactor_mle(1.0*count(distinct case when cf.is_refactor  then cf.commit else null end)/count(distinct cf.commit))
        as refactor_mle
, avg(if(not cf.is_corrective, non_test_files, null)) as avg_coupling_size
, avg(if(not cf.is_corrective, code_non_test_files, null)) as avg_coupling_code_size
, avg(if(not cf.is_corrective, if(non_test_files > 103 , 103 , non_test_files), null)) as avg_coupling_size_capped
, avg(if(not cf.is_corrective, if(code_non_test_files> 103 , 103 ,code_non_test_files), null)) as avg_coupling_code_size_capped
, avg(if(not cf.is_corrective, if(non_test_files > 103 , null , non_test_files), null)) as avg_coupling_size_cut
, avg(if(not cf.is_corrective, if(code_non_test_files> 10 , null ,code_non_test_files), null)) as avg_coupling_code_size_cut

, if(sum(if(files <= 103, files, null)) > 0
    , sum(if(files <= 103, files - non_test_files, null))/ sum(if(files <= 103, files, null))
    , null) as test_file_ratio_cut
, if(sum(if(code_files <= 103, code_files, null)) > 0
    , sum(if(code_files <= 103, code_files - code_non_test_files, null))/ sum(if(code_files <= 103, code_files, null))
    , null) as test_code_file_ratio_cut


, count(distinct cf.Author_email) as authors
, max(cf.Author_email) as Author_email # Meaningful only when authors=1
, min(ec.commit_month) as commit_month
, avg(if(same_date_as_prev, duration, null)) as same_day_duration_avg

, 0.0 as prev_touch_ago
, 0.0 as bug_prev_touch_ago

# Abstraction
, if (sum(if(ec.is_corrective, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_corrective, 1,0 ))/sum(if(ec.is_corrective, 1,0 ))
, null)
as one_file_fix_rate
, if (sum(if(ec.is_refactor, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
, null)
as one_file_refactor_rate

, if(sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 )) > 0
    , 1.0*sum(if(code_files=1, 1,0 ))/sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 ))
    , null)
as test_usage_rate

, if(sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 )) > 0
    , 1.0*sum(if(ec.is_refactor and code_files=1, 1,0 ))
        /sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 ))
    , null)
as test_usage_in_refactor_rate

, if(sum(if(ec.is_refactor, 1,0 )) > 0
    , 1.0*sum(if( code_non_test_files = code_files and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
    , null )
as no_test_refactor_rate
, sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0)) as textual_abstraction_commits
, 1.0*sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0))/count(*) as textual_abstraction_commits_rate

, avg(cast(ec.is_typo as int64)) as typo_rate

, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) > 1,1,0))/count(distinct ec.commit) as tangling_rate
, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) = 3,1,0))/count(distinct ec.commit) as bingo_rate


, -1.0 as testing_involved_prob
, -1.0 as corrective_testing_involved_prob
, -1.0 as refactor_testing_involved_prob
, null as abs_content_ratio # We have data only in head, not per year

, count(distinct if(is_performance, ec.commit, null))/count(distinct ec.commit) as performance_rate
, count(distinct if(is_security, ec.commit, null))/count(distinct ec.commit) as security_rate

from
general.changed_alerts_commit_files as cf
join
general.changed_alerts_commits as ec
on
cf.commit = ec.commit and cf.repo_name = ec.repo_name
where
date(ec.commit_timestamp) < anchor_date
#and date(ec.commit_timestamp) => period_date
group by
repo_name
, file
;



# NOTE - Set anchor_date to proper value
DECLARE anchor_date DATE DEFAULT PARSE_DATE('%d/%m/%Y',  '1/2/2022');
DECLARE period_date DATE DEFAULT DATE_SUB(anchor_date, INTERVAL 3 month) ;

SELECT anchor_date, period_date;


drop table if exists general.file_properties_before_change_3m;


create table
general.file_properties_before_change_3m
as
select
cf.repo_name as repo_name
, file
, min(cf.commit_timestamp) as min_commit_time
, max(cf.commit_timestamp) as max_commit_time
, min(cf.commit) as min_commit
, max(extension) as extension
, max(code_extension) as code_extension
, max(is_test) as is_test
, count(distinct cf.commit) as commits
, count(distinct if(parents = 1, cf.commit, null)) as non_merge_commits
, count(distinct case when cf.is_corrective  then cf.commit else null end) as corrective_commits
, 1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit) as corrective_rate
, general.bq_ccp_mle(1.0*count(distinct if(cf.is_corrective, cf.commit, null))/count(distinct cf.commit)) as ccp
, general.bq_refactor_mle(1.0*count(distinct case when cf.is_refactor  then cf.commit else null end)/count(distinct cf.commit))
        as refactor_mle
, avg(if(not cf.is_corrective, non_test_files, null)) as avg_coupling_size
, avg(if(not cf.is_corrective, code_non_test_files, null)) as avg_coupling_code_size
, avg(if(not cf.is_corrective, if(non_test_files > 103 , 103 , non_test_files), null)) as avg_coupling_size_capped
, avg(if(not cf.is_corrective, if(code_non_test_files> 103 , 103 ,code_non_test_files), null)) as avg_coupling_code_size_capped
, avg(if(not cf.is_corrective, if(non_test_files > 103 , null , non_test_files), null)) as avg_coupling_size_cut
, avg(if(not cf.is_corrective, if(code_non_test_files> 10 , null ,code_non_test_files), null)) as avg_coupling_code_size_cut

, if(sum(if(files <= 103, files, null)) > 0
    , sum(if(files <= 103, files - non_test_files, null))/ sum(if(files <= 103, files, null))
    , null) as test_file_ratio_cut
, if(sum(if(code_files <= 103, code_files, null)) > 0
    , sum(if(code_files <= 103, code_files - code_non_test_files, null))/ sum(if(code_files <= 103, code_files, null))
    , null) as test_code_file_ratio_cut


, count(distinct cf.Author_email) as authors
, max(cf.Author_email) as Author_email # Meaningful only when authors=1
, min(ec.commit_month) as commit_month
, avg(if(same_date_as_prev, duration, null)) as same_day_duration_avg

, 0.0 as prev_touch_ago
, 0.0 as bug_prev_touch_ago

# Abstraction
, if (sum(if(ec.is_corrective, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_corrective, 1,0 ))/sum(if(ec.is_corrective, 1,0 ))
, null)
as one_file_fix_rate
, if (sum(if(ec.is_refactor, 1,0 )) > 0
, 1.0*sum(if( code_non_test_files = 1 and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
, null)
as one_file_refactor_rate

, if(sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 )) > 0
    , 1.0*sum(if(code_files=1, 1,0 ))/sum(if((code_non_test_files = 1 and code_files = 2 ) or code_files=1, 1,0 ))
    , null)
as test_usage_rate

, if(sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 )) > 0
    , 1.0*sum(if(ec.is_refactor and code_files=1, 1,0 ))
        /sum(if(ec.is_refactor and ((code_non_test_files = 1 and code_files = 2 ) or code_files=1), 1,0 ))
    , null)
as test_usage_in_refactor_rate

, if(sum(if(ec.is_refactor, 1,0 )) > 0
    , 1.0*sum(if( code_non_test_files = code_files and ec.is_refactor, 1,0 ))/sum(if(ec.is_refactor, 1,0 ))
    , null )
as no_test_refactor_rate
, sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0)) as textual_abstraction_commits
, 1.0*sum(if(general.bq_abstraction(lower(message)) > 0, 1, 0))/count(*) as textual_abstraction_commits_rate

, avg(cast(ec.is_typo as int64)) as typo_rate

, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) > 1,1,0))/count(distinct ec.commit) as tangling_rate
, sum(if(cast(ec.is_corrective as int64) + cast(ec.is_adaptive as int64) + cast(ec.is_refactor as int64) = 3,1,0))/count(distinct ec.commit) as bingo_rate


, -1.0 as testing_involved_prob
, -1.0 as corrective_testing_involved_prob
, -1.0 as refactor_testing_involved_prob
, null as abs_content_ratio # We have data only in head, not per year

, count(distinct if(is_performance, ec.commit, null))/count(distinct ec.commit) as performance_rate
, count(distinct if(is_security, ec.commit, null))/count(distinct ec.commit) as security_rate

from
general.changed_alerts_commit_files as cf
join
general.changed_alerts_commits as ec
on
cf.commit = ec.commit and cf.repo_name = ec.repo_name
where
date(ec.commit_timestamp) < anchor_date
and date(ec.commit_timestamp) >= period_date
group by
repo_name
, file
;
