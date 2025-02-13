# Run on schema from https://github.com/evidencebp/general
drop table if exists general.code_python_python_feb_aug_22;

create table
general.code_python_python_feb_aug_22
as
select
base.repo_name
, base.path
, general.bq_repo_split(base.repo_name) as repo_split
, general.bq_file_split(base.repo_name
                         , base.path) as file_split
, base.size as base_size
, next.size as next_size
from
general.contents_1_february_2022 as base
join
general.repos as r
on
base.repo_name = r.repo_name
join
general.contents_1_august_2022 as next
on
base.repo_name = next.repo_name
and
base.path = next.path
and
base.content != next.content
and regexp_replace(base.content, r'\s', '') != regexp_replace(next.content, r'\s', '')
where
base.extension = '.py'
and not regexp_contains(lower(base.path), '(test|setup|__init__|version|__manifest__)')
;


drop table if exists general.code_python_feb_content_aug_22;

create table
general.code_python_feb_content_aug_22
as
select
diff.repo_name
, diff.path
, repo_split
, file_split
, base_size
, content
from
general.code_python_python_feb_aug_22 as diff
join
general.contents_1_february_2022 as cont
on
diff.repo_name = cont.repo_name
and
diff.path = cont.path
;
