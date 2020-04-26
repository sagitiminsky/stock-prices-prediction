from keras.layers import Dense, Flatten
import apps.config

def many_2_x(prediction_type,model,split):
    stocks_num=len(apps.config.stock_names)

    if prediction_type==apps.config.MANY2ONE:
        model.add(Dense(int(split * 0.3), name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model

    else: #prediction_type == MANY2MANY
        model.add(Flatten(input_shape=(int(split * 0.7)*stocks_num, 1)))
        model.add(Dense(int(split * 0.3)*stocks_num, name="output"))
        model.compile(loss='mse', optimizer='adam')
        return model