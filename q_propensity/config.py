class Configuration:
    """
    Configuration file for Telco Customer Churn
    """
    def __init__(self):
        self.color = '#00A8E0'
        self.image_path = './propensity.png'
        self.shap_image_path = './Original_Shapley_Naive.png'
        self.pdp_image_path = './Partial_dependence_plot.png'
        self.pipe_image_path = './pipeline_overview.png'
        self.pipe2_image_path = './pipeline_detail.png'


        self.dai_instance = 'http://18.140.223.189:12345'
        self.dai_un = 'h2oai'
        self.dai_pw = 'h2oai'

        self.training_path = './datasets/better_than_rfm.csv'
        self.training_key = 'e4fd52f2-4a37-11eb-b4f9-0242ac110003'
        self.testing_path = './datasets/rfm_train.csv'
        self.testing_key = '3f37f308-4a38-11eb-b4f9-0242ac110003'
        self.experiment_id = 'f3cabe8c-4a37-11eb-b4f9-0242ac110003'

        self.y_col = 'Response'
        self.x_cols = ['Tenure', 'Recency', 'Y_Frequency', 'Mean_Value']

        self.id_column = "DonorId"

        self.title = 'Fundraising Propensity Score'
        self.subtitle = 'Propensity Modeling with Driverless AI & Wave'
        self.icon = 'Money'

        self.model_loaded = False
        self.working_data = self.training_path

    def load_model(self, predictions_file_path):
        self.model_loaded = True
        self.working_data = predictions_file_path

    def get_column_type(self):
        if self.model_loaded:
            return "Propensity Prediction"
        else:
            return "Propensity"

    def get_analysis_type(self):
        if self.model_loaded:
            return "Model Predictions"
        else:
            return "Historical Data"
