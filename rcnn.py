import tensorflow as tf


def get_CRNN_layers(x_in):
    
    #timestamps = 32
    #freq_dim = 256
    
    x = BatchNormalization()(x_in)
    x =  Reshape((timesteps, freq_dim,1))(x)
    
    
    
    x = Conv2D(64,(5,7),padding='same')(x) #was 32
    x = batch_relu(x)

    x = Conv2D(64,(3,3),padding='same')(x)
    x = batch_relu(x)

    
    x = MaxPooling2D((1,3))(x)
    
    x = Conv2D(64,(3,3),padding='same')(x)
    x = batch_relu(x)
    x = Conv2D(64,(3,3),padding='same')(x)
    x = batch_relu(x)

    
    
    x = MaxPooling2D((2,3))(x)
    

    x = Conv2D(128,(3,3),padding='same')(x)
    x = batch_relu(x)
    x = Conv2D(128,(3,3),padding='same')(x)
    x = batch_relu(x)

    x = MaxPooling2D((2,3))(x)
    
    
    x = Conv2D(128,(3,3),padding='same')(x)
    x = batch_relu(x)
    x = Conv2D(128,(3,3),padding='same')(x)
    x = batch_relu(x)
    
    # flattening 2nd and 3rd dimensions
    x = Reshape((16,int(x.shape[-1]) * int(x.shape[-2])))(x)
    
    x = Bidirectional(CuDNNLSTM(128,return_sequences=False))(x)

    
    return x