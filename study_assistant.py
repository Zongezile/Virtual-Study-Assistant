with open('.env', 'r') as fp:
    HF_API_KEY = fp.read().strip()

import math
from huggingface_hub import InferenceClient
subjects = {}
subject = "example"

while True:
    subject = input("Enter subject name: ")
    if subject == ' ' or subject == '':
        break

    time = None
    while type(time) != int or time < 0:
        try:
            time = int(input("Enter time allocated for " + subject + ": "))
        except ValueError:
            pass

    subjects[subject] = time

if subjects:
    total_time_m = 0
    print('Your study plan:')
    for key, value in subjects.items():
        total_time_m += value
        print(key+': '+str(value)+' minutes')
    print(f'Total study time: {total_time_m} minutes')
    total_time_with_breaks = math.ceil(total_time_m/60)*15 + total_time_m
    print(f'Total time including breaks: {total_time_with_breaks} minutes')

    real_study_time = None
    while type(real_study_time) != int or real_study_time < 0:
        try:
            real_study_time = int(input("Enter time spent studying: "))
        except ValueError:
            pass

    percent = real_study_time / total_time_m * 100
    if percent > 100: percent = 100
    print(f'You have completed {percent:.2f}% of your planned study time.')

    client = InferenceClient(token=HF_API_KEY)
    subjects = ', '.join(subjects.keys())
    prompt = f"I have to prepare for my {subjects} exams. I've completed {percent:.2f}% of my curriculum. My motivation should be "

    response = client.text_generation(
        prompt=prompt,
        model="gpt2",
        temperature=2,
        max_new_tokens=50,
        seed=42,
        return_full_text=True,
    )
    print(response)

if __name__ == '__main__':
    pass