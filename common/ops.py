import tensorflow as tf

INITIALIZER = tf.contrib.layers.xavier_initializer()
PADDING = 'SAME'

def conv2d(x, filter_size, stride, feature_map_dim, name):
    with tf.variable_scope(name, initializer=INITIALIZER):
        # create weight variable and convolve
        filter_dims = [filter_size, filter_size, x.get_shape()[-1], feature_map_dim]
        stride_dims = [1, stride, stride, 1]
        W = tf.get_variable('weights', filter_dims)
        conv = tf.nn.conv2d(x, W, stride_dims, padding=PADDING, name='conv')

        # add bias and relu activation
        b = tf.get_variable('bias', [feature_map_dim])
        h = tf.nn.relu(tf.add(conv, b, name='add'), name='relu')

    return h

def pool(x, ksize, stride, name):
    with tf.variable_scope(name):
        # max pooling
        window_dims = [1, ksize, ksize, 1]
        stride_dims = [1, stride, stride, 1]
        pool = tf.nn.max_pool(x, window_dims, stride_dims, padding=PADDING, name='pool')

    return pool

def fc(x, output_dim, name, activation=True):
    with tf.variable_scope(name, initializer=INITIALIZER):
        # create weight variable and matrix multiply
        weight_shape = [x.get_shape()[-1], output_dim]
        W = tf.get_variable('weights', weight_shape)
        mm = tf.matmul(x, W, name='matmul')

        # add bias and relu activation (if true)
        b = tf.get_variable('bias', [output_dim])
        add_op = tf.add(mm, b, name='add')
        h = tf.nn.relu(add_op, name='relu') if activation else add_op

    return h

def dropout(x, keep_prob, name):
    with tf.variable_scope(name):
        drop = tf.nn.dropout(x, keep_prob, name='dropout')

    return drop

def softmax(x, output_dim, name):
    with tf.variable_scope(name, initializer=INITIALIZER):
        # create weight variable and matrix multiply
        weight_shape = [x.get_shape()[-1], output_dim]
        W = tf.get_variable('weights', weight_shape)
        mm = tf.matmul(x, W, name='matmul')

        # add bias and relu activation (if true)
        b = tf.get_variable('bias', [output_dim])
        h = tf.nn.softmax(tf.add(mm, b, name='add'), name='softmax')

    return h
