from openai import OpenAI
import os

os.environ["http_proxy"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"

mdl = 'gpt-3.5-turbo'
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

completion = client.chat.completions.create(
        model=mdl,
        messages=[
            #{'role': 'system', 'content': 'You are a helpful assistant. I will give some descriptions of experiments, please summmerise experiment conditions from the descriptions, and translate them to concept names in gene ontology'},
            {'role': 'user', 'content': '''Please summmerise conditions of the experiment from the following descriptions, and translate it to concept names in gene ontology (https://purl.obolibrary.org/obo/go.owl) and tell me their gene ontology ID:

            Characteristics 	strain: MR-1(pBBR-glk-galP)
            treatment: grown under a fumarate-respiring condition
            Treatment protocol 	The cell suspension was centrifuged at 13,000 rpm for 1 min to precipitate the cells.
            Growth protocol 	MR-1(pBBR-glk-galP) was grown in GMM supplemented with fumarate (40 mM) as an electron acceptor, and cells were harvested at the logarithmic growth phase (OD600 0.2–0.3). These cells were incubated for 3 h in the presence (the fumarate-respiring condition) or absence (the fermentative condition) of fumarate.'''},
        ]
)

print(completion.choices[0].message.content, '\n')

completion = client.chat.completions.create(
        model=mdl,
        messages=[
            {'role': 'user', 'content': 'Please answer 2+2.'}
        ]
)
print(completion.choices[0].message.content)
