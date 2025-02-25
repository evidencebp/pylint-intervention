"""
The following file abstracts a sources code repository.
Currently the repository is git.
However, when extended to support more repositories, the interface
should be moved to an abstract repository class, common to all repositories.
All the repository specific details should be hidden in the specific classes.
"""
from datetime import datetime
from pandas import DataFrame
import subprocess
import re

SHORT_HASH_REGEX = '(?P<hash>[0-9a-f]{8}).*\n'

class GitWrapper(object):
    """ Encapsulation of the git repository
    """
    def __init__(self, working_directory):
        """ Working directory is the local directory of the repository.
        """
        self.working_directory = working_directory
        subprocess.check_output(self._into_working_cmd(), shell=True)

    def _into_working_cmd(self):
        """ A private utility moving to the working directory.
        """
        return "cd %s" % self.working_directory

    def exec_git_command(self, cmd):
        """ An OS abstraction to perform repository commands
        """
        command = self._into_working_cmd() + ' ; ' + cmd
        return subprocess.check_output(command, shell=True)

    def get_commit_files(self, commit):
        """ Gets the files the were modified in a commit.
        """
        files_regex = '\\n?([\/a-zA-Z\.0-9\_\-]*)'
        command = "git show --pretty='format:' --name-only %s" % commit
        files = str(self.exec_git_command(command), 'utf-8')

        return [i for i in re.findall(files_regex, files) if i != '']

    def get_ticket_commits(self, ticket):
        """ Get the commits related to a working ticket.
            The responsibility to the commit is external (e.g., comming from Jira)
            The method treat the ticket like a string the should be part of the
            commit message.
        """
        ticket_commits = []
        try:
            commit_regex = 'commit (?P<hash>[0-9a-f]{5,40})'
            command = "git log --all --full-history --grep '%s' | grep '^commit '" % ticket
            commits = str(self.exec_git_command(command), 'utf-8')
            ticket_commits = re.findall(commit_regex, commits)
        except:
            print("Error processing ticket ", ticket)

        return ticket_commits

    def get_tickets_commits(self, tickets_list):
        """ Gets all commits related to a list of tickets.
            The commits are assigned per ticket.
            See get_ticket_commits remark for assignment logic.
        """
        ticket_commits = []
        for i in tickets_list:
            commits = self.get_ticket_commits(i)
            for j in commits:
                ticket_commits.append((i, j))

        return DataFrame(ticket_commits, columns=['ticket', 'commit'])

    def get_ticket_files(self, ticket):
        commits = self.get_ticket_commits(ticket)
        files = []
        for i in commits:
            files = files + self.get_commit_files(i)

        return files

    def get_all_commits(self
                        , git_format="'format: %H %aE %cD'"
                        , format_regex='(?P<hash>[0-9a-f]{5,40}) (?P<email>[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+) (?P<time>.{25})'
                        , columns=['commit', 'email', 'commit_time']
                        , since=None
                        , until=None
                        , target=None):
        """ Returns all the commits in a given period of time.
            The parameters git_format, format_regex and columns are given to
            allow flexibility.
            git format should provided the information that will be parsed
            using format_regex and stored in the data frame columns
        """
        # Date format is '1 Nov 2016'
        command = "git log --format=%s" % git_format
        command = command + (" --since='%s' " % since) if since else command
        command = command + (" --until='%s' " % until) if until else command
        command = command + (" " + target) if target else command

        commits = self.exec_git_command(command)
        matches = re.findall(format_regex, commits)
        return DataFrame(matches, columns=columns)

    def get_all_commits_titles(self, since=None, until=None):
        """ Gets the titles of all the commits in a period.
        """
        return self.get_all_commits(git_format='oneline'
                                    , format_regex='(?P<hash>[0-9a-f]{5,40}) (?P<title>.*)'
                                    , columns=['commit', 'title']
                                    , since=since
                                    , until=until)

    def get_commits_files(self, commits_df):
        """ Return a dataframe that relates to each commit the files changed in it.
        """
        files_of_commit = []
        for _, row in commits_df.iterrows():
            files = self.get_commit_files(row.commit)
            for file_name in files:
                files_of_commit.append((row.commit, file_name))

        return DataFrame(files_of_commit, columns=['commit', 'file'])


    def get_all_commits_files(self):
        """ File relation to all the commits.
        """
        commits = self.get_all_commits()
        return self.get_commits_files(commits)


    def get_commit_changes(self, commit):
        """ Returns the locations changed in a commit.
        """
        FILE_DIFF_REGEX = 'diff --git a'
        snippets = {}
        file_pos = []

        command = "git show %s --unified=0" % commit
        diff = self.exec_git_command(command)

        for file_start in  re.finditer(FILE_DIFF_REGEX, diff):
            file_pos.append(file_start.span()[0])
        file_pos.append(len(diff))

        for start, end in zip(file_pos, file_pos[1:]):
                file_name, file_snippets = self.process_file_diff(
                                    diff[start:end])
                snippets[file_name] = file_snippets
        return snippets

    def process_file_diff(self, file_diff):
        """ A utility for parsing a change in a file (in a commit).
        """
        # TODO verify that there are change or deleted rows in the snippet
        SNIPPET_REGEX = '@@ -(?P<offset1>\d+)(,(?P<len1>\d+))?\s\+(?P<name2>\d+)(,(?P<len2>\d+))?\s@@'
        file_name = re.search('diff --git a/(?P<file_name>[\w\/\.]*)', file_diff).group('file_name')

        snippets_matches = re.findall(SNIPPET_REGEX, file_diff)
        snippets = [(int(m[0]), int(m[2] or 0)) for m in snippets_matches]


        snippets = sorted(snippets, key=lambda x: x[0])

        return file_name, snippets


    def get_file_prev_commit(self, commit, file_name):
        """ Find the commit in which a file was changed, prior to the current commit.
        """
        # TODO - handle merges
        command = "git log --format='format: %H' --all --full-history -- " + file_name
        commits = self.exec_git_command(command)
        prev_commit_regex = commit + '\n (?P<hash>[0-9a-f]{40})'
        match = re.search(prev_commit_regex, commits)

        return match.group('hash') if match else None

    def show_file_content(self, file_name, commit=None):
        """ Show file in a given commit version.
        """
        if commit:
            command = 'git show %s:%s' % (commit, file_name)
        else:
            command = 'git show HEAD:%s' % file_name
        return self.exec_git_command(command)

    def get_commit_date(self, commit):
        """ Find the date of a commit.
        """
        DATE_REGEX = '^(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
        command = "git show --date=short --format='%cd' " + commit
        commit_content = self.exec_git_command(command)

        match = re.search(DATE_REGEX, commit_content)

        return datetime(int(match.groups()[0])
                        , int(match.groups()[1])
                        , int(match.groups()[2])).date()

    def get_blame(self, file_name, commit=None):
        """ git blame, enable a blame of a previous version too.
        """
        if commit:
            command = "git blame %s -- %s " % (commit, file_name)
        else:
            command = "git blame %s" % file_name
        return self.exec_git_command(command)

    def get_blame_commits(self, file_name, commit=None):
        """ The commits of the file in a given blame
        """
        blame_content = self.get_blame(file_name, commit)

        return re.findall(SHORT_HASH_REGEX, blame_content)

    def find_function_first_author(self
                                    , function_definition_regex
                                    , file_name):
        """ Find the first author that wrote a function in a given file.
        """
        command = "git log -G '%s' --source --all --reverse -- %s " % (function_definition_regex
                                                                         , file_name)
        log_output = self.exec_git_command(command)
        match = re.search('Author: (?P<name>[\w ]+) .*\nDate', log_output)
        author = match.group('name') if match else None

        return author


