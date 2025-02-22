# metrics_diff_stats
select
change
, msg
, msg_id
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, avg(after.ccp - before.ccp) as ccp_diff
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
from
general.changed_alerts as ca
join
general.file_properties_before_change as before
on
ca.repo_name = before.repo_name
and
ca.path = before.file
join
general.file_properties_after_change as after
on
ca.repo_name = after.repo_name
and
ca.path = after.file
group by
change
, msg
, msg_id
order by change, msg
;

# metrics_diff_stats_5_commits
select
change
, msg
, msg_id
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, avg(after.ccp - before.ccp) as ccp_diff
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
from
general.changed_alerts as ca
join
general.file_properties_before_change as before
on
ca.repo_name = before.repo_name
and
ca.path = before.file
join
general.file_properties_after_change as after
on
ca.repo_name = after.repo_name
and
ca.path = after.file
where
before.commits >= 5
and
after.commits >= 5
group by
change
, msg
, msg_id
order by change, msg
;


# metrics_diff_stats_3m
select
change
, msg
, msg_id
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, avg(after.ccp - before.ccp) as ccp_diff
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
from
general.changed_alerts as ca
join
general.file_properties_before_change_3m as before
on
ca.repo_name = before.repo_name
and
ca.path = before.file
join
general.file_properties_after_change_3m as after
on
ca.repo_name = after.repo_name
and
ca.path = after.file
group by
change
, msg
, msg_id
order by change, msg
;

# metrics_diff_stats_5_commits_3m
select
change
, msg
, msg_id
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, avg(after.ccp - before.ccp) as ccp_diff
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
from
general.changed_alerts as ca
join
general.file_properties_before_change_3m as before
on
ca.repo_name = before.repo_name
and
ca.path = before.file
join
general.file_properties_after_change_3m as after
on
ca.repo_name = after.repo_name
and
ca.path = after.file
where
before.commits >= 5
and
after.commits >= 5
group by
change
, msg
, msg_id
order by change, msg
;

