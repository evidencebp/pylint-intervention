
def generate_intro(interventions_file):
    template = """I'd like to conduct a software engineering experiment regarding the benefit of [Pylint](https://pypi.org/project/pylint/)  alerts removal.
The experiment is described [here](https://github.com/evidencebp/pylint-intervention/).
In the experiments, Pylint is used with some specific alerts, files are selected for intervention and control.
After the interventions are done, one can wait and examine the results.

I'm asking for your approval for conducting an intervention in your repository.

See examples of interventions in [stanford-oval/storm](https://github.com/stanford-oval/storm/pull/181), [gabfl/vault](https://github.com/gabfl/vault/pull/82), and [coreruleset/coreruleset](https://github.com/coreruleset/coreruleset/pull/3837).

You can see the [planed interventions](https://github.com/evidencebp/pylint-intervention/tree/main/interventions/candidates/{interventions_file})

May I do the interventions?"""

    print("Pylint alerts corrections as part of an intervention experiment")
    print("#"*50)
    print(template.format(interventions_file=interventions_file))

if __name__ == "__main__":
    generate_intro("aaugustin_websockets_interventions_October_05_2024.csv")