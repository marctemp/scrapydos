import re
import pandas as pd
import numpy as np
from json import dump
from datetime import datetime
from fuzzywuzzy import fuzz, process


DATA_DIR = """/Users/marcte/Documents/_Development/Procurement/data/"""

# dates must be saved in format yyyy-mm-dd
SPECIALISTS_EXT = """opportunities-specialists"""
RESEARCH_EXT = """opportunities-research"""
DIGITAL_EXT = """opportunities-digital"""

SPECIALISTS_LOC = f'{DATA_DIR}{SPECIALISTS_EXT}'
RESEARCH_LOC = f'{DATA_DIR}{RESEARCH_EXT}'
DIGITAL_LOC = f'{DATA_DIR}{DIGITAL_EXT}'

NORM_REGEX = re.compile(r'([^\s\w])+')


def split_fields(df, heavy_text_fields):
    recs = []

    def split_field(df, field):
        text = []
        for rec in df[field]:
            try:
                text.append(rec.split("}}"))
            except AttributeError:
                text.append([rec])
        return text
    for field in heavy_text_fields:
        recs.append(split_field(df, field))
    return recs


# for c in heavy_text_fields:
# df[c] = split_field(df, c)


def normalise_texts(texts, regex):
    txts = []

    def normalise_text(text, regex):
        try:
            return regex.sub('', text).lower().strip()
        except AttributeError:
            return text
        except TypeError:
            return '' if isinstance(text, float) else text
    for text in texts:
        try:
            ts = [normalise_text(t, regex) for t in text]
            txts.append(' '.join(ts).strip())
        except TypeError:
            if isinstance(ts[0], int):
                txts.append(ts[0])
            elif isinstance(ts[0], datetime):
                txts.append(f'{ts[0].strftime("%Y-%m-%d")}')
            elif np.isnan(ts[0]):
                txts.append(ts[0])
            else:
                txts.append(ts[0])
    return txts


def lower_text(v):
    try:
        return v.lower()
    except:
        return v


def dig():
    df = pd.read_excel(f'{DIGITAL_LOC}.xlsx', index_col=0)

    # df = pd.read_json(f'{DIGITAL_LOC}.json', orient='index',
    #                   convert_dates=['PublishedDate', 'DeadlineForAskingQuestions', 'DeadlineForApplications', 'LatestStartDate', 'ContractStartDate'])

    heavy_text_fields = ['SummaryOfTheWork', 'ContractLength', 'BudgetRange', 'WhyTheWorkIsBeingDone', 'ProblemToBeSolved', 'WhoTheUsersAreAndWhatTheyNeedToDo', 'EarlyMarketEngagement', 'AnyWorkThatHasAlreadyBeenDone',
                         'ExistingTeam', 'WorkingArrangements', 'SecurityClearance', 'AdditionalTermsAndConditions', 'EssentialSkillsAndExperience', 'NiceToHaveSkillsAndExperience', 'ProposalCriteria', 'CulturalFitCriteria', 'PaymentApproach', 'AssessmentMethods', 'EvaluationWeighting']

    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s = split_fields(
        df, heavy_text_fields)

    df['SummaryOfTheWork'] = a
    df['ContractLength'] = b
    df['BudgetRange'] = c
    df['WhyTheWorkIsBeingDone'] = d
    df['ProblemToBeSolved'] = e
    df['WhoTheUsersAreAndWhatTheyNeedToDo'] = f
    df['EarlyMarketEngagement'] = g
    df['AnyWorkThatHasAlreadyBeenDone'] = h
    df['ExistingTeam'] = i
    df['WorkingArrangements'] = j
    df['SecurityClearance'] = k
    df['AdditionalTermsAndConditions'] = l
    df['EssentialSkillsAndExperience'] = m
    df['NiceToHaveSkillsAndExperience'] = n
    df['ProposalCriteria'] = o
    df['CulturalFitCriteria'] = p
    df['PaymentApproach'] = q
    df['AssessmentMethods'] = r
    df['EvaluationWeighting'] = s

    for c in heavy_text_fields:
        df[c] = normalise_texts(df[c].tolist(), f'{NORM_REGEX}')

    df = df.applymap(lower_text)

    # df.to_csv(f'{DIGITAL_LOC}.csv', index=True)

    # df.to_json(f'{DIGITAL_LOC}.json', orient='index',
    #            date_format='iso', date_unit='s')

    spendage_df = pd.read_csv(f'{DATA_DIR}spendage-dos.csv')

    cust_list = [cust.lower() for cust in set(spendage_df['CustomerName'])]
    org_list = df['Organisation'].tolist()

    # p = [process.extractOne(cust, cust_list.remove(cust))
    #      for cust in cust_list]

    # removes customers with acros (rcwa)
    cust_opts_th, cust_opts = {}, {}
    THRESHOLD = 90

    tmp = cust_list

    for i, cust in enumerate(tmp):
        tmp.remove(cust)
        cl_match = process.extractOne(cust, tmp)
        cust_opts[f'{cust}'] = cl_match
        cust_opts_th[f'{cust}'] = cl_match if cl_match[1] >= THRESHOLD else (
            '', cl_match[1])

    d = pd.DataFrame.from_dict(cust_opts, orient='index', columns=[
                               'AlternativeName', 'SimilarityScore'])

    d.to_csv(f'./customer_names_lenient.csv')

    d = pd.DataFrame.from_dict(cust_opts_th, orient='index', columns=[
                               'AlternativeName', 'SimilarityScore'])

    d.to_csv(f'./customer_names_threshold_{THRESHOLD}.csv')

    print('h')

    # opts = {org: process.extractBests(org,cust_list) for org in org_list}
    # best = [process.extractOne(org,cust_list) for org in org_list]

    df['OrganisationFiltered'] = best


def spe():
    df = pd.read_excel(f'{SPECIALISTS_LOC}.xlsx', index_col=0)

    # df = pd.read_json(f'{SPECIALISTS_LOC}.json', orient='index',
    #                   convert_dates=['PublishedDate', 'DeadlineForAskingQuestions', 'DeadlineForApplications', 'LatestStartDate', 'ContractStartDate'])

    heavy_text_fields = ['SummaryOfTheWork', 'ContractLength', 'MaximumDayRate', 'EarlyMarketEngagement', 'WhoTheSpecialistWillWorkWith', 'WhatTheSpecialistWillWorkOn', 'AddressWhereTheWorkWillTakePlace', 'WorkingArrangements',
                         'SecurityClearance', 'AdditionalTermsAndConditions', 'EssentialSkillsAndExperience', 'NiceToHaveSkillsAndExperience', 'CulturalFitCriteria', 'AssessmentMethods', 'EvaluationWeighting']

    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o = split_fields(
        df, heavy_text_fields)

    df['SummaryOfTheWork'] = a
    df['ContractLength'] = b
    df['MaximumDayRate'] = c
    df['EarlyMarketEngagement'] = d
    df['WhoTheSpecialistWillWorkWith'] = e
    df['WhatTheSpecialistWillWorkOn'] = f
    df['AddressWhereTheWorkWillTakePlace'] = g
    df['WorkingArrangements'] = h
    df['SecurityClearance'] = i
    df['AdditionalTermsAndConditions'] = j
    df['EssentialSkillsAndExperience'] = k
    df['NiceToHaveSkillsAndExperience'] = l
    df['CulturalFitCriteria'] = m
    df['AssessmentMethods'] = n

    for c in heavy_text_fields:
        df[c] = normalise_texts(df[c].tolist(), NORM_REGEX)

    df = df.applymap(lower_text)

    df.to_csv(f'{SPECIALISTS_LOC}.csv', index=True)

    df.to_json(f'{SPECIALISTS_LOC}.json', orient='index',
               date_format='iso', date_unit='s')


def res():
    df = pd.read_excel(f'{RESEARCH_LOC}.xlsx', index_col=0)

    # df = pd.read_json(f'{RESEARCH_LOC}.json', orient='index',
    #                   convert_dates=['PublishedDate', 'DeadlineForAskingQuestions', 'DeadlineForApplications'])

    heavy_text_fields = ['SummaryOfTheWork', 'ResearchDates', 'EarlyMarketEngagement', 'DescriptionOfYourParticipants', 'AssistedDigitalAndAccessibilityRequirements', 'ResearchPlan',
                         'ResearchLocation', 'AccessRestrictionsAtLocation', 'NumberOfResearchRounds', 'NumberOfParticipantsPerRound', 'HowOftenResearchWillHappen', 'EveningOrWeekendResearch',
                         'AdditionalTermsAndConditions', 'EssentialSkillsAndExperience', 'NiceToHaveSkillsAndExperience', 'ProposalCriteria', 'AssessmentMethods', 'EvaluationWeighting']

    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r = split_fields(
        df, heavy_text_fields)

    df['SummaryOfTheWork'] = a
    df['ResearchDates'] = b
    df['EarlyMarketEngagement'] = c
    df['DescriptionOfYourParticipants'] = d
    df['AssistedDigitalAndAccessibilityRequirements'] = e
    df['ResearchPlan'] = f
    df['ResearchLocation'] = g
    df['AccessRestrictionsAtLocation'] = h
    df['NumberOfResearchRounds'] = i
    df['NumberOfParticipantsPerRound'] = j
    df['HowOftenResearchWillHappen'] = k
    df['EveningOrWeekendResearch'] = l
    df['AdditionalTermsAndConditions'] = m
    df['EssentialSkillsAndExperience'] = n
    df['NiceToHaveSkillsAndExperience'] = o
    df['ProposalCriteria'] = p
    df['AssessmentMethods'] = q
    df['EvaluationWeighting'] = r

    for c in heavy_text_fields:
        df[c] = normalise_texts(df[c].tolist(), NORM_REGEX)

    df = df.applymap(lower_text)

    df.to_csv(f'{RESEARCH_LOC}.csv', index=True)

    df.to_json(f'{RESEARCH_LOC}.json', orient='index',
               date_format='iso', date_unit='s')


dig()
# spe()
# res()
