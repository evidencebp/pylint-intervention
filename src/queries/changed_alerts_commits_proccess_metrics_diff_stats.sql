# anchor_commits_metrics_diff_stats.csv
select
alert as msg
, state as change
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, stddev(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff_sd
, avg(after.ccp - before.ccp) as ccp_diff
, stddev(after.ccp - before.ccp) as ccp_diff_sd
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, stddev(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff_sd
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, stddev(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff_sd
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
, stddev(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff_sd
from
general.alert_change_commits_anchors as ca
join
general.file_properties_before_anchor as before
on
ca.repo_name = before.repo_name
and
ca.file_name = before.file
join
general.file_properties_after_anchor as after
on
ca.repo_name = after.repo_name
and
ca.file_name = after.file
group by
change
, msg
order by msg, change
;

# anchor_commits_metrics_diff_stats_5_commits.csv
select
alert as msg
, state as change
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, stddev(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff_sd
, avg(after.ccp - before.ccp) as ccp_diff
, stddev(after.ccp - before.ccp) as ccp_diff_sd
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, stddev(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff_sd
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, stddev(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff_sd
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
, stddev(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff_sd
from
general.alert_change_commits_anchors as ca
join
general.file_properties_before_anchor as before
on
ca.repo_name = before.repo_name
and
ca.file_name = before.file
join
general.file_properties_after_anchor as after
on
ca.repo_name = after.repo_name
and
ca.file_name = after.file
where
before.commits >= 5
and
after.commits >= 5
group by
change
, msg
order by msg, change
;


# anchor_commits_metrics_diff_stats_5_commits_3m.csv
select
alert as msg
, state as change
, count(*) as cases
, avg(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff
, stddev(after.same_day_duration_avg - before.same_day_duration_avg) as same_day_duration_avg_diff_sd
, avg(after.ccp - before.ccp) as ccp_diff
, stddev(after.ccp - before.ccp) as ccp_diff_sd
, avg(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff
, stddev(after.avg_coupling_code_size_cut - before.avg_coupling_code_size_cut) as avg_coupling_code_size_cut_diff_sd
, avg(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff
, stddev(after.one_file_fix_rate - before.one_file_fix_rate) as one_file_fix_rate_diff_sd
, avg(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff
, stddev(after.test_usage_rate - before.test_usage_rate) as test_usage_rate_diff_sd
from
general.alert_change_commits_anchors as ca
join
general.file_properties_before_anchor_3m as before
on
ca.repo_name = before.repo_name
and
ca.file_name = before.file
join
general.file_properties_after_anchor_3m as after
on
ca.repo_name = after.repo_name
and
ca.file_name = after.file
where
before.commits >= 5
and
after.commits >= 5
group by
change
, msg
order by msg, change
;
