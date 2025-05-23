import json
import logging
import re
import textwrap
import dateutil.parser
from dojo.models import Finding

logger = logging.getLogger(__name__)

CWE_REGEX = r'cwe-\d+'


class SarifParser(object):
    """OASIS Static Analysis Results Interchange Format (SARIF) for version 2.1.0 only.

    https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=sarif
    """

    def get_scan_types(self):
        return ["SARIF"]

    def get_label_for_scan_types(self, scan_type):
        return scan_type  # no custom label for now

    def get_description_for_scan_types(self, scan_type):
        return "SARIF report file can be imported in SARIF format."

    def get_findings(self, filehandle, test):
        tree = json.load(filehandle)
        return self.get_items(tree, test)

    def get_items(self, tree, test):
        items = list()
        # for each runs
        for run in tree.get('runs', list()):
            # load rules
            rules = get_rules(run)
            artifacts = get_artifacts(run)
            # get the timestamp of the run if possible
            run_date = self._get_last_invocation_date(run)
            for result in run.get('results', list()):
                item = get_item(result, rules, artifacts, run_date)
                items.append(item)
        return items

    def _get_last_invocation_date(self, data):
        invocations = data.get('invocations', [])
        if len(invocations) == 0:
            return None
        # try to get the last 'endTimeUtc'
        raw_date = invocations[-1].get('endTimeUtc')
        if raw_date is None:
            return None
        # if the data is here we try to convert it to datetime
        return dateutil.parser.isoparse(raw_date)


def get_rules(run):
    rules = {}
    for item in run['tool']['driver'].get('rules', []):
        rules[item['id']] = item
    return rules


def get_rule_tags(rule):
    if 'properties' not in rule:
        return []
    if 'tags' not in rule['properties']:
        return []
    else:
        return rule['properties']['tags']


def search_cwe(value, cwes):
    matches = re.search(CWE_REGEX, value, re.IGNORECASE)
    if matches:
        cwes.append(int(matches[0].split("-")[1]))


def get_rule_cwes(rule):
    cwes = []
    # data of the specification
    if 'relationships' in rule and type(rule['relationships']) == list:
        for relationship in rule['relationships']:
            value = relationship['target']['id']
            search_cwe(value, cwes)
        return cwes

    for tag in get_rule_tags(rule):
        search_cwe(tag, cwes)
    return cwes


def get_result_cwes_properties(result):
    """Some tools like njsscan store the CWE in the properties of the result"""
    cwes = []
    if 'properties' in result and 'cwe' in result['properties']:
        value = result['properties']['cwe']
        search_cwe(value, cwes)
    return cwes


def get_artifacts(run):
    artifacts = {}
    custom_index = 0  # hack because some tool doesn't generate this attribute
    for tree_artifact in run.get('artifacts', []):
        artifacts[tree_artifact.get('index', custom_index)] = tree_artifact
        custom_index += 1
    return artifacts


def get_severity(data):
    """Convert level value to severity
    """
    if 'warning' == data:
        return 'Medium'
    elif 'error' == data:
        return 'Critical'
    else:
        return 'Info'


def get_message_from_multiformatMessageString(data, rule):
    """Get a message from multimessage struct

    See here for the specification: https://docs.oasis-open.org/sarif/sarif/v2.1.0/os/sarif-v2.1.0-os.html#_Toc34317468
    """
    if rule is not None and 'id' in data:
        text = rule['messageStrings'][data['id']].get('text')
        arguments = data.get('arguments', [])
        # argument substitution
        for i in range(6):  # the specification limit to 6
            substitution_str = "{" + str(i) + "}"
            if substitution_str in text:
                text = text.replace(substitution_str, arguments[i])
            else:
                return text
    else:
        # TODO manage markdown
        return data.get('text')


def cve_try(val):
    # Match only the first CVE!
    cveSearch = re.search("(CVE-[0-9]+-[0-9]+)", val, re.IGNORECASE)
    if cveSearch:
        return cveSearch.group(1).upper()
    else:
        return None


def get_item(result, rules, artifacts, run_date):
    # if there is a location get it
    file_path = None
    line = -1
    if "locations" in result:
        location = result['locations'][0]
        if 'physicalLocation' in location:
            file_path = location['physicalLocation']['artifactLocation']['uri']
            # 'region' attribute is optionnal
            if 'region' in location['physicalLocation']:
                line = location['physicalLocation']['region']['startLine']

    # test rule link
    rule = rules.get(result.get('ruleId'))
    title = result.get('ruleId')
    description = ''
    if 'message' in result:
        description = get_message_from_multiformatMessageString(
            result['message'], rule)
        if len(description) < 150:
            title = description
    severity = get_severity(result.get('level', 'warning'))
    if rule is not None:
        # get the severity from the rule
        if 'defaultConfiguration' in rule:
            severity = get_severity(
                rule['defaultConfiguration'].get('level', 'warning'))

        if 'shortDescription' in rule:
            description = get_message_from_multiformatMessageString(
                rule['shortDescription'], rule)
        elif 'fullDescription' in rule:
            description = get_message_from_multiformatMessageString(
                rule['fullDescription'], rule)
        elif 'name' in rule:
            description = rule['name']
        else:
            description = rule['id']

    finding = Finding(
        title=textwrap.shorten(title, 150),
        severity=severity,
        description=description,
        static_finding=True,  # by definition
        dynamic_finding=False,  # by definition
        file_path=file_path,
        line=line,
    )

    if 'ruleId' in result:
        finding.vuln_id_from_tool = result['ruleId']
        # for now we only support when the id of the rule is a CVE
        finding.cve = cve_try(result['ruleId'])
    # some time the rule id is here but the tool doesn't define it
    if rule is not None:
        cwes_extracted = get_rule_cwes(rule)
        if len(cwes_extracted) > 0:
            finding.cwe = cwes_extracted[-1]

    # manage the case that some tools produce CWE as properties of the result
    cwes_properties_extracted = get_result_cwes_properties(result)
    if len(cwes_properties_extracted) > 0:
        finding.cwe = cwes_properties_extracted[-1]

    # manage fixes provided in the report
    if "fixes" in result:
        finding.mitigation = "\n".join([fix.get('description', {}).get("text") for fix in result["fixes"]])

    if run_date:
        finding.date = run_date

    return finding
