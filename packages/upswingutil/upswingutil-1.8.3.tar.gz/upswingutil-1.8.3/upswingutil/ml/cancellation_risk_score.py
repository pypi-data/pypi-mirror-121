import pandas as pd
import numpy as np
from upswingutil.db import Mongodb
from loguru import logger
import tensorflow as tf
# from sklearn.model_selection import train_test_split
# from sklearn.utils import resample
from upswingutil.resource import get_model_from_cloud_storage, upload_model_to_cloud_storage


class CancellationRiskScore:
    __file_name__ = 'cancellation_risk_score_{}.pkl'

    def __init__(self, orgId: str, hotelId: str):
        self.orgId = orgId
        self.hotelId = hotelId

    def get_data(self) -> list:
        """
        retrieve data from mongodb for the model to train
        """
        __pipeline__ = [
            {
                '$match': {
                    'status': {
                        '$nin': [
                            'Quote', 'Unconfirmed', 'OwnerOccupied', 'Maintenance'
                        ]
                    }
                }
            },
            {
                '$addFields': {
                    'cancellation_lead_in': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': '$arrivalDate'
                                        }, {
                                            '$toDate': '$cancelledDate'
                                        }
                                    ]
                                }, 60 * 60 * 24 * 1000
                            ]
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'durationOfStay': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': '$departureDate'
                                        }, {
                                            '$toDate': '$arrivalDate'
                                        }
                                    ]
                                }, 60 * 60 * 24 * 1000
                            ]
                        }
                    }
                }
            },
            {
                '$addFields': {
                    'Leadin': {
                        '$floor': {
                            '$divide': [
                                {
                                    '$subtract': [
                                        {
                                            '$toDate': '$arrivalDate'
                                        }, {
                                            '$toDate': '$createdDate'
                                        }
                                    ]
                                }, 60 * 60 * 24 * 1000
                            ]
                        }
                    }
                }
            },
            {
                '$project': {
                    '_id': 1,
                    'cancellation_lead_in': 1,
                    'durationOfStay': 1,
                    'Leadin': 1,
                    'geustCount': 1,
                    'clientId': 1,
                    'Class': 1,
                    'adults': 1,
                    'bookingSourceId': 1,
                    'booking_level': 1,
                    'categoryId': 1,
                    'children': 1,
                    "cancellationPolicyId": 1,
                    'cancellation_time_indays': '7',
                    'guest_type': 1,
                    'paymentModeId': 1,
                    'status': 1,
                    'travelAgentId': 1,
                    'ArrivalMonth': {
                        '$month': {
                            '$toDate': '$arrivalDate'

                        }
                    },
                    'dayoftheweek': {
                        '$dayOfWeek': {
                            '$toDate': '$arrivalDate'  # (according to dataset-- sunday is1 , sat is 7)
                        }
                    }

                }

            }
        ]
        mongo = Mongodb(self.orgId)
        result = mongo.execute_pipeline(mongo.RESERVATION_COLLECTION, __pipeline__)
        mongo.close_connection()
        return result

    def preprocess(self):
        """
        preprocess data extracted from mongodb and return data for training and testing of model
        """
        df = pd.DataFrame(self.get_data())
        logger.info(f'DataFrame Created from the Data Pipeline !!')

        df.dropna(axis=0, inplace=True)
        df['status'] = df['status'].apply(lambda x: 'Not Cancelled' if x in ['Departed', 'Arrived'] else 'Cancelled')

        # splitting the data----
        x = df.loc[:,
            ['_id', 'adults', 'bookingSourceId', 'booking_level', 'cancellationPolicyId', 'categoryId',
             'children', 'clientId', 'paymentModeId', 'travelAgentId', 'Class', 'guest_type',
             'cancellation_lead_in', 'durationOfStay', 'Leadin', 'cancellation_time_indays', 'ArrivalMonth',
             'dayoftheweek']]
        y = df.loc[:, ['status']]

        # Encoding----
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y = le.fit_transform(y)

        # Encoding----
        from sklearn.compose import ColumnTransformer
        from sklearn.preprocessing import OneHotEncoder
        ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), [3, 10, 11])],
                               remainder="passthrough")
        x = ct.fit_transform(x)

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

        return x_train, x_test, y_train, y_test

    def train(self):
        file_name = CancellationRiskScore.__file_name__.format(self.hotelId)
        """ Create model using preprocessed data and store the model in google cloud storage """
        x_train, x_test, y_train, y_test = self.preprocess()
        x_train = np.asarray(x_train).astype(
            int)  # as this error was coming (valueerror-failed-to-convert-a-numpy-array-to-a-     tensor-unsupported-object-type)
        y_train = np.asarray(y_train).astype(int)
        x_test = np.asarray(x_test).astype(int)

        # Initializing the ANN
        ann = tf.keras.models.Sequential()

        # Adding the input layer and the first hidden layer
        ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

        # Adding the second hidden layer
        ann.add(tf.keras.layers.Dense(units=6, activation='relu'))

        # Adding the output layer
        ann.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

        # Part 3 - Training the ANN

        # Compiling the ANN
        ann.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # Training the ANN on the Training set
        model = ann.fit(x_train, y_train, batch_size=32, epochs=100)
        upload_model_to_cloud_storage(model, self.orgId,
                                      file_name)  # storing the generated model as a pickle file in cloud storage
        logger.info(f"New Model created, File saved: {file_name}")
        logger.info(f"Completed Cancellation Risk Score model for {self.hotelId}")

    def predict(self, var1, var2, var3, var4):
        """ predict result for the new data from the model created while training and stored in cloud storage """
        file_name = CancellationRiskScore.__file_name__.format(self.hotelId)
        model = get_model_from_cloud_storage(self.orgId, file_name)
        result = model.predict(var1, var2, var3, var4)
        return result
