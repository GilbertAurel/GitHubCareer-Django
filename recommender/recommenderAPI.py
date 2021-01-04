import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel


def recommendation(input_json, input_param):
    # FETCHING DATA FROM API
    counter = 0
    job_recommended = []
    jobs = input_json

    # Getting user input - insert to list
    input_value = [{'title': 'INPUT', 'description': input_param}]
    title = input_value[0].get('title')
    added_jobs = jobs.append(input_value, ignore_index=True, sort=False)

    # Term frequency and inverse document frequency
    tfv = TfidfVectorizer(min_df=0, max_features=None,
                          strip_accents='unicode', analyzer='word',
                          token_pattern=r'\w{1,}',
                          ngram_range=(1, 3),
                          stop_words='english')
    added_jobs['description'] = added_jobs['description'].fillna('')
    tfv_matrix = tfv.fit_transform(added_jobs['description'])

    # Sigmoid kernel for Sigmoid calculationsa
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    indices = pd.Series(added_jobs.index, index=added_jobs['title'])

    # Search for the very peculiar input
    jobs_list_length = len(added_jobs)
    jobs_last = jobs_list_length - 1

    for i in range(jobs_list_length):
        # 0.7615941559557649 is sigmoid value for very peculiar input
        if sig[jobs_last][i] <= 0.7615941559557649:
            counter += 1

    if counter >= jobs_last:
        return None
    else:
        # Getting final result
        id_input = indices[title]
        sig_scores = list(enumerate(sig[id_input]))
        sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
        sig_scores = sig_scores[1:15]
        job_indices = [i[0] for i in sig_scores]

        for job in job_indices:
            job_dic = {
                'title' : added_jobs['title'].iloc[job]
            }
            job_recommended.append(job_dic)

        # # Return all recommended titles
        return job_recommended
        # return added_jobs['title'].iloc[job_indices]
