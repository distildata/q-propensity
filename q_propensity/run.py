from h2o_wave import Q, ui, app, main, site
import driverlessai

import pandas as pd
import numpy as np
import time

from .utils import ui_table_from_df, python_code_content, dai_content
from .config import Configuration

config = Configuration()

uploaded_files_dict = dict()

def download_model_predictions(experiment_id):

    dai = driverlessai.Client(address=config.dai_instance, username=config.dai_un, password=config.dai_pw,
                              verify=False)

    experiment = dai.experiments.get(experiment_id)

    test_data = dai.datasets.get(config.testing_key)

    pred_path = experiment.predict(test_data, include_columns=config.x_cols).download('./datasets/')

    df = pd.read_csv(pred_path)

    df.to_csv(pred_path, index=False)

    return pred_path


def home_content(header_png):
    df = pd.read_csv(config.training_path).head()

    # header_png, = site.upload([config.image_path])

    items = [
        ui.text_xl('Fundraising Propensity Application'),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text('''This application allows fundraisers to upload their data in the format below and get back AI 
        generated propensity to give scores. Use this for your next fun-run, direct ask for international development etc... direct your energy to those supporters likely to donate, do good it the world.'''),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text(f'![runners]({header_png})'),

        ### workflow explanation here 1) UPLOAD DATA 2_DOWNLOAD SCORES

    ]

    return items


def explain_content(training_file_url,shap_png,pdp_png,pipe_png,pipe2_png):

    df = pd.read_csv(config.training_path).head()
   
    items = [

        ui.text_xl('AI Explained'),
        ui.frame(content=' ', height="20px"),  # whitespace 

        ui.text('''AI is complicated, but we have done the hard work for you. We built an AI model using [H2O Driverless AI](https://www.h2o.ai/products/h2o-driverless-ai/), that you can now use to understand the likelihood to donate of your supporters. We built the model using the data below'''),
        ui.frame(content=' ', height="20px"),  # whitespace

# wINFERENCING VS BUILDING AND FLOW

        ui.separator("Data"),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text('''This is currently synthetic data, real data would be great! We have a dataset of previous donors (and non-donors):

            - their tenure with the non-for-Profit
            - the recency of their last donation
            - the frequency per year for donations 
            - and the average value at the point of the campaign.

        This is the data we have used to train an AI model from which Non-for-Profits can score their data and the likelihood of supporters to donate to your next campaign.'''),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui_table_from_df(df, 5, "Training Data"),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.separator("What Inputs are Important for the Model? Global Feature Shapley Value"),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text('''Shapley values tell us the contribution of each feature to the model, in this case for the model overall (ie Global) rather than for each supporter (Local). More details here. How recently a supporter made a donation is the most useful information to predict whether a supporter will donate'''),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text(f'![global naive shap]({shap_png})'),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.separator("How is Recency Important?"),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text('''We know recency is important, but here we can see how it is important, ie the more recent the donation the higher the likelihood to donate'''),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text(f'![partial dep plot]({pdp_png})'),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.separator("How Does the Model Work?"),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text('''This is not a simple if/else style approach. Driverless AI went optimised the features to use for the model, their transformations, the model and parameters that work best to predict the likelihood for a supporter to donate. More information on how Driverless AI works is [here].(http://docs.h2o.ai/driverless-ai/latest-stable/docs/userguide/index.html) We can see the combination of models and transformations Driverless AI chose for the final model below. This final model utakes the average predictions across 10 different models, think of this like wisedom of the crowd'''),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text(f'![partial dep plot]({pipe_png})'),
        ui.frame(content=' ', height="20px"),  # whitespace

        ui.text(f'![partial dep plot]({pipe2_png})'),

    ]

    return items

# CHANGE SO SCORED DATA IS UPLOADED DATA!

async def upload_dataset(q: Q):

    q.page['main'] = ui.form_card(box='3 2 -1 -1', items=[ui.text_xl('Import Data'),
                                                       ui.file_upload(name='uploaded_file',
                                                                      label='Upload File',
                                                                      multiple=True),
                                                       ])

def select_table():
    
    choices = [ui.choice(file, file) for file in uploaded_files_dict]
  
    items = [
        ui.text_xl(f'Select data'),
        ui.dropdown(name='score_data', label='Pick one', required=True, choices=choices),
        ui.button(name='selected_file', label='Submit', primary=True)
    ]
    return items    


async def initialize_page(q: Q):

    content = []

    if not q.client.app_initialized:
        q.app.header_png, = await q.site.upload([config.image_path])
        q.app.training_file_url, = await q.site.upload([config.working_data])
        q.app.shap_png, = await q.site.upload([config.shap_image_path])
        q.app.pdp_png, = await q.site.upload([config.pdp_image_path])
        q.app.pipe_png, = await q.site.upload([config.pipe_image_path])
        q.app.pipe2_png, = await q.site.upload([config.pipe2_image_path])
        q.client.app_initialized = True

    q.page.drop()

    q.page['title'] = ui.header_card(
        box='1 1 -1 1',
        title=config.title,
        subtitle=config.subtitle,
        icon=config.icon,
        icon_color=config.color,
    )

    q.page['side_bar'] = ui.nav_card(
        box='1 2 2 -1',
        items=[
            ui.nav_group('Menu', items=[
                ui.nav_item(name='#home', label='Home'),
                ui.nav_item(name='#explain', label='AI Explained'),
                ui.nav_item(name='#upload', label='Upload Data'),
                ui.nav_item(name='#model', label='Propensity Scores'),
                ui.nav_item(name='#code', label='Application Code'),
            ])
        ],
    )
    q.page['content'] = ui.form_card(
        box='3 2 -1 -1',
        items=content
    )

    await q.page.save()


@app('/')
async def serve(q: Q):

    await initialize_page(q)
    await initialize_page(q)
    content = q.page["content"]

    if q.args.selected_file:
        content.items = [ui.progress(label="Making Predictions using H2O Driverless AI")]
        await q.page.save()

        config.load_model(download_model_predictions(config.experiment_id))

        predictions_file_url, = await q.site.upload([config.working_data])

        df = pd.read_csv(config.working_data)

        content.items = [
            ui.text_xl(f"{config.y_col} Predictions have been Made on New Data"),
            ui.frame(content=' ', height="20px"),  # whitespace
            ui.text(
                f"[Download the model predictions]({predictions_file_url})."),
        # data viz here would be great
        ]

    else:
        hash = q.args['#']

        if hash == 'home':
            content.items = home_content(q.app.header_png)

        elif hash == 'explain':
            content.items = explain_content(q.app.training_file_url,q.app.shap_png,q.app.pdp_png,q.app.pipe_png,q.app.pipe2_png)

        elif hash == 'upload':
            ## message here for format of the data
            await upload_dataset(q)

        elif hash == 'model':
            content.items = select_table()

        elif hash == 'code':
            content.items = python_code_content('run.py')

        # User uploads a file
        elif q.args.uploaded_file:
            uploaded_file_path = q.args.uploaded_file
            for file in uploaded_file_path:
                filename = file.split('/')[-1]
                uploaded_files_dict[filename] = uploaded_file_path
            time.sleep(1)
            q.page['main'] = ui.form_card(box='3 2 -1 -1', items=[ui.message_bar('success', 'File Imported! Please now score your data'),
                                                               ui.buttons([ui.button(name='#model', label='Propensity Score', primary=True),])])
            await q.page.save()

    await q.page.save()
