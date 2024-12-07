
from utils import run_powershell_cmd
def get_raw_metrics(file: str)-> dict:

    metrics_dict = {}
    cmd = f'radon raw {file}'

    result = str(run_powershell_cmd(cmd).stdout)

    for i in ['LOC', 'LLOC', 'SLOC', 'Comments', 'Single comments', 'Multi', 'Blank']:
        i_pos = result.find(i)
        metrics_dict[i] = int(result[i_pos
                                     + len(i)
                                     +2 # for ': '
                                     : result.find('\\r\\n', i_pos)])
    return metrics_dict

print(get_raw_metrics("C:/src/alex-bot/alexBot/cogs/voiceCommands.py"))